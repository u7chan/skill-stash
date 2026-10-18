#!/usr/bin/env bash
#
# video-edit.sh - speed up one interval of a video while keeping the rest at
# 1x speed, burn a bottom-center telop with a background box, and optionally
# normalize the result for iOS playback.
#
# Requires: bash, ffmpeg (with libx264, libfreetype, libfontconfig), ffprobe.
#
set -euo pipefail

FFMPEG=${FFMPEG:-ffmpeg}
FFPROBE=${FFPROBE:-ffprobe}

die() { printf 'video-edit: error: %s\n' "$*" >&2; exit 1; }
warn() { printf 'video-edit: warning: %s\n' "$*" >&2; }

usage() {
  cat <<'EOF'
Usage:
  video-edit.sh -i INPUT -o OUTPUT --start START --end END --speed FACTOR
                [--telop TEXT | --telop-file FILE] [--font FILE]
                [--font-size PX] [--box-opacity 0..1] [--telop-margin PX]
                [--ios] [--fps RATE] [--crf N] [--preset NAME]
                [--audio-bitrate RATE] [-y] [--dry-run]

Speed up only [START, END) and keep the other parts at 1x. START and END accept
seconds (24, 24.5) or clock values (00:00:24, 1:02:03.5). END is exclusive.

Telop:
  --telop '>> x3'       Text burned into the sped-up interval, bottom center,
                        with a translucent black box. Prefer this for short text.
  --telop-file FILE     Read the text from a file (use for quotes, '%', or
                        multi-line text; avoids drawtext escaping problems).
  --font FILE           Font file. Auto-detected with fontconfig when omitted.
  --font-size PX        Default: 5.75% of the source frame height.
  --box-opacity 0..1    Black box opacity. Default: 0.55.
  --telop-margin PX     Distance from the bottom edge. Default: 7.2% of height.

iOS:
  --ios                 H.264 High@4.1, yuv420p, <=30 fps, <=1920x1080
                        (portrait: <=1080x1920), AAC-LC 48 kHz stereo,
                        faststart. Downscales only; keeps the aspect ratio.

Other:
  --fps RATE            Output frame rate (e.g. 30, 30000/1001).
                        Default: source rate; capped at 30 with --ios.
  --crf N               libx264 CRF. Default: 20.
  --preset NAME         libx264 preset. Default: medium.
  --audio-bitrate RATE  AAC bitrate. Default: 192k.
  -y, --overwrite       Overwrite OUTPUT.
  --dry-run             Print the filtergraph and command without encoding.
  -h, --help            Show this help.

Examples:
  video-edit.sh -i in.mp4 -o out.mp4 --start 24 --end 44 --speed 3 --telop '>> x3'
  video-edit.sh -i in.mp4 -o out-ios.mp4 --start 24 --end 44 --speed 3 \
                --telop '>> x3' --ios
EOF
}

INPUT=''
OUTPUT=''
START=''
END=''
SPEED=''
TELOP=''
TELOP_FILE=''
FONT=''
FONT_SIZE=''
BOX_OPACITY='0.55'
TELOP_MARGIN=''
TELOP_COLOR='white'
IOS=0
DRY_RUN=0
OVERWRITE=0
CRF='20'
PRESET='medium'
FPS_OPT=''
AUDIO_BITRATE='192k'

while (($#)); do
  case "$1" in
    -i|--input)        (($# >= 2)) || die "$1 needs a value"; INPUT=$2; shift 2 ;;
    -o|--output)       (($# >= 2)) || die "$1 needs a value"; OUTPUT=$2; shift 2 ;;
    --start)           (($# >= 2)) || die "$1 needs a value"; START=$2; shift 2 ;;
    --end)             (($# >= 2)) || die "$1 needs a value"; END=$2; shift 2 ;;
    --speed)           (($# >= 2)) || die "$1 needs a value"; SPEED=$2; shift 2 ;;
    --telop)           (($# >= 2)) || die "$1 needs a value"; TELOP=$2; shift 2 ;;
    --telop-file)      (($# >= 2)) || die "$1 needs a value"; TELOP_FILE=$2; shift 2 ;;
    --font)            (($# >= 2)) || die "$1 needs a value"; FONT=$2; shift 2 ;;
    --font-size)       (($# >= 2)) || die "$1 needs a value"; FONT_SIZE=$2; shift 2 ;;
    --box-opacity)     (($# >= 2)) || die "$1 needs a value"; BOX_OPACITY=$2; shift 2 ;;
    --telop-margin)    (($# >= 2)) || die "$1 needs a value"; TELOP_MARGIN=$2; shift 2 ;;
    --ios)             IOS=1; shift ;;
    --fps)             (($# >= 2)) || die "$1 needs a value"; FPS_OPT=$2; shift 2 ;;
    --crf)             (($# >= 2)) || die "$1 needs a value"; CRF=$2; shift 2 ;;
    --preset)          (($# >= 2)) || die "$1 needs a value"; PRESET=$2; shift 2 ;;
    --audio-bitrate)   (($# >= 2)) || die "$1 needs a value"; AUDIO_BITRATE=$2; shift 2 ;;
    -y|--overwrite)    OVERWRITE=1; shift ;;
    --dry-run)         DRY_RUN=1; shift ;;
    -h|--help)         usage; exit 0 ;;
    --)                shift; break ;;
    *)                 die "unknown option: $1 (see --help)" ;;
  esac
done

[ -n "$INPUT" ] || die "--input is required"
[ -n "$OUTPUT" ] || die "--output is required"
[ -n "$START" ] || die "--start is required"
[ -n "$END" ] || die "--end is required"
[ -n "$SPEED" ] || die "--speed is required"
[ -f "$INPUT" ] || die "input not found: $INPUT"
[ -d "$(dirname "$OUTPUT")" ] || die "output directory not found: $(dirname "$OUTPUT")"
if [ -n "$TELOP" ] && [ -n "$TELOP_FILE" ]; then
  die "use either --telop or --telop-file, not both"
fi
if [ -n "$TELOP_FILE" ] && [ ! -f "$TELOP_FILE" ]; then
  die "telop file not found: $TELOP_FILE"
fi

command -v "$FFMPEG" >/dev/null 2>&1 || die "ffmpeg not found: $FFMPEG"
command -v "$FFPROBE" >/dev/null 2>&1 || die "ffprobe not found: $FFPROBE"
ENCODERS=$("$FFMPEG" -hide_banner -encoders 2>/dev/null || true)
grep -q ' libx264 ' <<<"$ENCODERS" || die "this ffmpeg has no libx264 encoder"

if [ -e "$OUTPUT" ] && [ "$INPUT" -ef "$OUTPUT" ]; then
  die "input and output are the same file"
fi
if [ -e "$OUTPUT" ] && (( ! OVERWRITE )); then
  die "output already exists: $OUTPUT (use -y to overwrite)"
fi

# --- validate numbers -------------------------------------------------------

[[ $SPEED =~ ^[0-9]+([.][0-9]+)?$ ]] && ! [[ $SPEED =~ ^0+([.]0+)?$ ]] \
  || die "--speed must be a positive number: $SPEED"
[[ $BOX_OPACITY =~ ^[0-9]+([.][0-9]+)?$ ]] \
  || die "--box-opacity must be a number between 0 and 1: $BOX_OPACITY"
awk -v o="$BOX_OPACITY" 'BEGIN { exit !(o >= 0 && o <= 1) }' \
  || die "--box-opacity must be between 0 and 1: $BOX_OPACITY"
[[ $CRF =~ ^[0-9]+$ ]] && (( CRF >= 0 && CRF <= 51 )) \
  || die "--crf must be an integer between 0 and 51: $CRF"

to_seconds() {
  awk -v t="$1" 'BEGIN {
    n = split(t, p, ":")
    if (n < 1 || n > 3) exit 1
    for (i = 1; i <= n; i++) {
      if (p[i] !~ /^[0-9]+([.][0-9]+)?$/) exit 1
    }
    if (n == 1) s = p[1]
    else if (n == 2) s = p[1] * 60 + p[2]
    else s = p[1] * 3600 + p[2] * 60 + p[3]
    printf "%.6f", s
  }'
}

START_S=$(to_seconds "$START") || die "invalid --start: $START"
END_S=$(to_seconds "$END") || die "invalid --end: $END"
SPEED_NUM=$(awk -v s="$SPEED" 'BEGIN { printf "%.6f", s + 0 }')

# --- inspect source ---------------------------------------------------------

DUR_RAW=$("$FFPROBE" -v error -show_entries format=duration -of default=nw=1:nk=1 "$INPUT")
DUR=$(awk -v d="$DUR_RAW" 'BEGIN { if (d + 0 > 0) printf "%.6f", d + 0; else exit 1 }') \
  || die "could not read duration from input: $INPUT"

SIZE=$("$FFPROBE" -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$INPUT")
VW=${SIZE%%x*}
SIZE_REST=${SIZE#*x}
VH=${SIZE_REST%%x*}
[[ $VW =~ ^[0-9]+$ && $VH =~ ^[0-9]+$ ]] && (( VW > 0 && VH > 0 )) \
  || die "could not read video dimensions from input: $INPUT"

# ffmpeg autorotates on transcode, so use the displayed dimensions for telop
# sizing and for the iOS downscale decision.
ROT_RAW=$("$FFPROBE" -v error -select_streams v:0 -show_entries stream_side_data=rotation -of default=nw=1:nk=1 "$INPUT" || true)
ROT=${ROT_RAW%%$'\n'*}
if [[ $ROT =~ ^-?[0-9]+$ ]] && (( ROT % 180 != 0 )); then
  tmp=$VW
  VW=$VH
  VH=$tmp
fi

FPS_STR=$("$FFPROBE" -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=nw=1:nk=1 "$INPUT")
FPS_NUM=$(awk -v f="$FPS_STR" 'BEGIN {
  if (f ~ /^[0-9]+\/[0-9]+$/) {
    split(f, a, "/")
    if (a[2] > 0) { printf "%.6f", a[1] / a[2]; exit }
  } else if (f ~ /^[0-9]+([.][0-9]+)?$/) {
    printf "%.6f", f + 0
    exit
  }
  print "0"
}')
awk -v f="$FPS_NUM" 'BEGIN { exit !(f > 0) }' || { FPS_STR='30/1'; FPS_NUM='30.000000'; }

HAS_AUDIO=0
A_STREAM=$("$FFPROBE" -v error -select_streams a:0 -show_entries stream=index -of csv=p=0 "$INPUT")
if [ -n "$A_STREAM" ]; then HAS_AUDIO=1; fi

if awk -v s="$START_S" -v d="$DUR" 'BEGIN { exit !(s >= d) }'; then
  die "--start ($START) is at or after the end of the video (${DUR}s)"
fi
if awk -v e="$END_S" -v s="$START_S" 'BEGIN { exit !(e <= s) }'; then
  die "--end ($END) must be after --start ($START)"
fi
if awk -v e="$END_S" -v d="$DUR" 'BEGIN { exit !(e > d + 0.001) }'; then
  die "--end ($END) is after the end of the video (${DUR}s)"
fi
if awk -v e="$END_S" -v d="$DUR" 'BEGIN { exit !(e > d) }'; then
  END_S=$DUR
fi

# --- font / telop -----------------------------------------------------------

TMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/video-edit.XXXXXX")
cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

TELOP_PATH=''
FONT_PATH=''
DRAWTEXT=''

if [ -n "$TELOP" ] || [ -n "$TELOP_FILE" ]; then
  TELOP_PATH=$TELOP_FILE
  if [ -n "$TELOP" ]; then
    TELOP_PATH="$TMP_DIR/telop.txt"
    printf '%s' "$TELOP" > "$TELOP_PATH"
  fi

  TELOP_TEXT_DETECT=''
  if [ -n "$TELOP" ]; then
    TELOP_TEXT_DETECT=$TELOP
  else
    TELOP_TEXT_DETECT=$(cat "$TELOP_PATH")
  fi

  NEEDS_CJK=0
  NON_ASCII=$(printf '%s' "$TELOP_TEXT_DETECT" | tr -d '\n\r\t' | LC_ALL=C grep -c '[^ -~]' || true)
  if (( NON_ASCII > 0 )); then
    NEEDS_CJK=1
  fi

  if [ -n "$FONT" ]; then
    [ -f "$FONT" ] || die "font not found: $FONT"
    FONT_PATH=$FONT
  elif command -v fc-match >/dev/null 2>&1; then
    if (( NEEDS_CJK )); then
      FONT_PATH=$(fc-match -f '%{file}\n' 'sans-serif:lang=ja:weight=bold' 2>/dev/null || true)
    else
      FONT_PATH=$(fc-match -f '%{file}\n' 'sans-serif:weight=bold' 2>/dev/null || true)
    fi
  fi

  if [ -z "$FONT_PATH" ] || [ ! -f "$FONT_PATH" ]; then
    for candidate in \
      /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf \
      /usr/share/fonts/TTF/DejaVuSans-Bold.ttf \
      /Library/Fonts/Arial.ttf \
      /System/Library/Fonts/Supplemental/Arial.ttf; do
      if [ -f "$candidate" ]; then FONT_PATH=$candidate; break; fi
    done
  fi
  [ -n "$FONT_PATH" ] && [ -f "$FONT_PATH" ] \
    || die "no usable font found; pass --font /path/to/font.ttf"

  if (( NEEDS_CJK )) && command -v fc-query >/dev/null 2>&1; then
    JA_LANGS=$(fc-query -f '%{lang}\n' "$FONT_PATH" 2>/dev/null | tr '|' '\n' | grep -cx 'ja' || true)
    if (( JA_LANGS == 0 )); then
      warn "font may not cover Japanese: $FONT_PATH (pass --font if the telop is garbled)"
    fi
  fi

  if [ -z "$FONT_SIZE" ]; then
    FONT_SIZE=$(awk -v h="$VH" 'BEGIN { printf "%d", h * 0.0575 + 0.5 }')
    (( FONT_SIZE >= 8 )) || FONT_SIZE=8
  fi
  [[ $FONT_SIZE =~ ^[0-9]+$ ]] && (( FONT_SIZE >= 8 )) \
    || die "--font-size must be an integer >= 8: $FONT_SIZE"
  if [ -z "$TELOP_MARGIN" ]; then
    TELOP_MARGIN=$(awk -v h="$VH" 'BEGIN { printf "%d", h * 0.072 + 0.5 }')
  fi
  [[ $TELOP_MARGIN =~ ^[0-9]+$ ]] \
    || die "--telop-margin must be an integer >= 0: $TELOP_MARGIN"
  BOX_BORDER=$(awk -v f="$FONT_SIZE" 'BEGIN { printf "%d", f / 3 + 0.5 }')
  (( BOX_BORDER >= 4 )) || BOX_BORDER=4
  LINE_SPACING=$(awk -v f="$FONT_SIZE" 'BEGIN { printf "%d", f / 8 + 0.5 }')

  # Escape characters that are significant inside a filtergraph option value.
  filter_escape() {
    local s=$1
    s=${s//\\/\\\\}
    s=${s//\'/\\\'}
    s=${s//:/\\:}
    s=${s//,/\\,}
    printf '%s' "$s"
  }

  DRAWTEXT=",drawtext=fontfile=$(filter_escape "$FONT_PATH")"
  DRAWTEXT+=":textfile=$(filter_escape "$TELOP_PATH")"
  DRAWTEXT+=":expansion=none:fontcolor=${TELOP_COLOR}:fontsize=${FONT_SIZE}"
  DRAWTEXT+=":line_spacing=${LINE_SPACING}:box=1:boxcolor=black@${BOX_OPACITY}"
  DRAWTEXT+=":boxborderw=${BOX_BORDER}:x=(w-text_w)/2:y=h-text_h-${TELOP_MARGIN}"
fi

# --- frame rate -------------------------------------------------------------

FPS_OUT_STR=$FPS_STR
FPS_OUT_NUM=$FPS_NUM
if [ -n "$FPS_OPT" ]; then
  FPS_OUT_STR=$FPS_OPT
  FPS_OUT_NUM=$(awk -v f="$FPS_OPT" 'BEGIN {
    if (f ~ /^[0-9]+\/[0-9]+$/) { split(f, a, "/"); if (a[2] > 0) { printf "%.6f", a[1] / a[2]; exit } }
    else if (f ~ /^[0-9]+([.][0-9]+)?$/) { printf "%.6f", f + 0; exit }
    print "0"
  }')
  awk -v f="$FPS_OUT_NUM" 'BEGIN { exit !(f > 0) }' \
    || die "--fps must be a positive number or fraction: $FPS_OPT"
fi
if (( IOS )) && awk -v f="$FPS_OUT_NUM" 'BEGIN { exit !(f > 30.001) }'; then
  FPS_OUT_STR='30/1'
  FPS_OUT_NUM='30.000000'
  warn "capped the frame rate at 30 fps for iOS"
fi

# --- filtergraph ------------------------------------------------------------

HAS_LEAD=0
HAS_TAIL=0
if awk -v s="$START_S" 'BEGIN { exit !(s > 0.000001) }'; then HAS_LEAD=1; fi
if awk -v e="$END_S" -v d="$DUR" 'BEGIN { exit !(e < d - 0.000001) }'; then HAS_TAIL=1; fi
N=$((1 + HAS_LEAD + HAS_TAIL))

NEED_EVEN=0
if (( VW % 2 != 0 || VH % 2 != 0 )); then NEED_EVEN=1; fi

NEED_SCALE=0
MAXW=0
MAXH=0
if (( IOS )); then
  if (( VW >= VH )); then MAXW=1920; MAXH=1080; else MAXW=1080; MAXH=1920; fi
  if (( VW > MAXW || VH > MAXH )); then NEED_SCALE=1; fi
fi

parts=()
vpre="[0:v]setpts=PTS-STARTPTS"
if (( NEED_EVEN )) && ! (( IOS && NEED_SCALE )); then
  vpre+=",scale=trunc(iw/2)*2:trunc(ih/2)*2"
fi
vpre+=",fps=${FPS_OUT_STR},setsar=1"

if (( N > 1 )); then
  vfeed=''
  afeed=''
  for ((i = 0; i < N; i++)); do
    vfeed+="[vs$i]"
    afeed+="[as$i]"
  done
  parts+=("${vpre},split=${N}${vfeed}")
  if (( HAS_AUDIO )); then
    parts+=("[0:a]asetpts=PTS-STARTPTS,asplit=${N}${afeed}")
  fi
else
  parts+=("${vpre}[vs0]")
  if (( HAS_AUDIO )); then
    parts+=("[0:a]asetpts=PTS-STARTPTS[as0]")
  fi
fi

# atempo only accepts 0.5..2 on older ffmpeg versions; chain stages.
ATEMPO=$(awk -v f="$SPEED_NUM" 'BEGIN {
  n = 0
  while (f > 2.000001) { n++; a[n] = 2; f /= 2 }
  while (f < 0.499999) { n++; a[n] = 0.5; f /= 0.5 }
  n++; a[n] = f
  s = ""
  for (i = 1; i <= n; i++) s = s (i > 1 ? "," : "") sprintf("atempo=%.6f", a[i])
  print s
}')

seg=0
if (( HAS_LEAD )); then
  parts+=("[vs${seg}]trim=start=0:end=${START_S},setpts=PTS-STARTPTS[v${seg}]")
  if (( HAS_AUDIO )); then
    parts+=("[as${seg}]atrim=start=0:end=${START_S},asetpts=PTS-STARTPTS[a${seg}]")
  fi
  seg=$((seg + 1))
fi

parts+=("[vs${seg}]trim=start=${START_S}:end=${END_S},setpts=(PTS-STARTPTS)/${SPEED_NUM},fps=${FPS_OUT_STR}${DRAWTEXT}[v${seg}]")
if (( HAS_AUDIO )); then
  parts+=("[as${seg}]atrim=start=${START_S}:end=${END_S},asetpts=PTS-STARTPTS,${ATEMPO}[a${seg}]")
fi
seg=$((seg + 1))

if (( HAS_TAIL )); then
  parts+=("[vs${seg}]trim=start=${END_S},setpts=PTS-STARTPTS[v${seg}]")
  if (( HAS_AUDIO )); then
    parts+=("[as${seg}]atrim=start=${END_S},asetpts=PTS-STARTPTS[a${seg}]")
  fi
fi

if (( N > 1 )); then
  vconcat=''
  aconcat=''
  for ((i = 0; i < N; i++)); do
    vconcat+="[v$i]"
    aconcat+="[a$i]"
  done
  parts+=("${vconcat}concat=n=${N}:v=1:a=0[vcat]")
  if (( HAS_AUDIO )); then
    parts+=("${aconcat}concat=n=${N}:v=0:a=1[aout]")
  fi
else
  parts+=("[v0]null[vcat]")
  if (( HAS_AUDIO )); then
    parts+=("[a0]anull[aout]")
  fi
fi

if (( IOS && NEED_SCALE )); then
  parts+=("[vcat]scale=${MAXW}:${MAXH}:force_original_aspect_ratio=decrease:force_divisible_by=2,setsar=1[vout]")
else
  parts+=("[vcat]null[vout]")
fi

FILTER=$(IFS=';'; printf '%s' "${parts[*]}")

# --- command ----------------------------------------------------------------

CMD=("$FFMPEG" -hide_banner -nostdin)
if (( OVERWRITE )); then CMD+=(-y); else CMD+=(-n); fi
CMD+=(-i "$INPUT" -filter_complex "$FILTER")
if (( HAS_AUDIO )); then
  CMD+=(-map '[vout]' -map '[aout]')
else
  CMD+=(-map '[vout]' -an)
fi
CMD+=(-c:v libx264 -preset "$PRESET" -crf "$CRF" -pix_fmt yuv420p)
if (( IOS )); then
  CMD+=(-profile:v high -level:v 4.1)
fi
case "$OUTPUT" in
  *.mp4|*.mov|*.MP4|*.MOV)
    CMD+=(-tag:v avc1 -movflags +faststart)
    ;;
esac
if (( HAS_AUDIO )); then
  CMD+=(-c:a aac -b:a "$AUDIO_BITRATE")
  if (( IOS )); then
    CMD+=(-ar 48000 -ac 2)
  fi
fi
CMD+=("$OUTPUT")

EXPECTED=$(awk -v s="$START_S" -v e="$END_S" -v x="$SPEED_NUM" -v d="$DUR" \
  'BEGIN { printf "%.3f", s + (e - s) / x + (d - e) }')

if (( DRY_RUN )); then
  printf 'filtergraph:\n%s\n\n' "$FILTER"
  printf 'command:\n'
  printf '%q ' "${CMD[@]}"
  printf '\n\nexpected duration: %ss\n' "$EXPECTED"
  exit 0
fi

if (( HAS_AUDIO )); then
  printf 'audio: yes\n'
else
  printf 'audio: none (video only)\n'
fi
if [ -n "$TELOP_PATH" ]; then
  printf 'telop font: %s (%spx, bottom margin %spx)\n' "$FONT_PATH" "$FONT_SIZE" "$TELOP_MARGIN"
fi
printf 'expected duration: %ss\n' "$EXPECTED"

"${CMD[@]}"

ACTUAL=$("$FFPROBE" -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUTPUT")
printf 'wrote: %s\n' "$OUTPUT"
printf 'duration: %ss (expected %ss)\n' "$ACTUAL" "$EXPECTED"
