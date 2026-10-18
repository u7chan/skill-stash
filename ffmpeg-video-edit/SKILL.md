---
name: ffmpeg-video-edit
description: 動画の指定区間だけを倍速化し、他の区間は等倍のまま、下部中央に背景付きテロップ（例: >> x3）を焼き込む。必要ならiOSで再生できるH.264/AACのMP4へ正規化する。動画の一部だけ速度を変えたい、操作ログに倍速バッジを入れたい、iPhone向けに変換したいときに使う。
---

# ffmpeg video edit

ffmpegで「指定区間だけ倍速 + 下部中央テロップ + iOS向け正規化」を行う。1区間の指定と結合は `scripts/video-edit.sh` が処理する。複数区間や別位置のテロップは `references/recipes.md` のフィルタを手で組む。

## 前提

- `ffmpeg` と `ffprobe`。libx264・libfreetype・fontconfig が有効であること。
- `ffmpeg -hide_banner -filters | grep drawtext` が通ること。`drawtext` がなければテロップは焼けない。
- 日本語テロップは fontconfig の `:lang=ja` でフォントを自動選択する。見つからない環境では `--font` を指定する。
- 出力は既存ファイルを上書きしない。`-y` を明示したときだけ上書きする。

mise 等でffmpegのバージョンが未設定の場合は、実行パスを明示する。

```bash
FFMPEG=/path/to/ffmpeg FFPROBE=/path/to/ffprobe \
  ./scripts/video-edit.sh ...
```

## 最短手順

1. 入力・区間・倍率・テロップ・iOS要否を確定する。区間は秒（`24`、`24.5`）または `HH:MM:SS(.ms)`。ENDは排他。
2. `--dry-run` でフィルタgraphを確認する。
3. 実行する。
4. 期待尺・フレーム数・テロップを検証し、必要ならiOS実機で再生する。

```bash
# 24s〜44sだけ3倍速、他は等倍。下部中央に >> x3
./scripts/video-edit.sh -i input.mp4 -o out.mp4 \
  --start 24 --end 44 --speed 3 --telop '>> x3'

# 同じ内容をiOS向けに正規化
./scripts/video-edit.sh -i input.mp4 -o out-ios.mp4 \
  --start 24 --end 44 --speed 3 --telop '>> x3' --ios
```

## スクリプトの動作

- 入力を `trim` で前半・対象区間・後半に分ける。対象区間だけ `setpts` と `atempo` で倍速化し、`concat` で戻す。前後は速度を変えず再エンコードする。
- 出力はCFR。対象区間は速度変更後に `fps` で再サンプリングする。これを省略すると、エンコーダ側のフレーム補間で尺が1フレーム伸びることがある。
- 音声は `atempo` を0.5〜2.0の段に分割して適用する（古いffmpegでも動く）。
- テロップは対象区間の全フレームに焼き込む。下部中央、白文字、黒の半透明ボックス。文字列は一時ファイルへ書き `textfile=` で渡すため、`%` や `'` を含んでもエスケープ不要。
- 回転メタデータ付き動画は、ffmpegのautorotate後の表示寸法でテロップサイズとiOS上限を判定する。
- `--ios` は H.264 High@4.1 / yuv420p / 30fps以下 / AAC-LC 48kHz stereo / faststart。1920x1080（縦は1080x1920）を超える場合だけダウンスケールし、黒帯は追加しない。
- 音声がない入力は映像だけを出力する。

## オプション

| オプション | 説明 |
| --- | --- |
| `-i`, `-o` | 入力と出力。出力の親ディレクトリは存在している必要がある |
| `--start`, `--end` | 倍速区間。ENDは排他。動画末尾を超えるENDは微小超過のみ末尾へ丸める |
| `--speed` | 倍率。`0.5` でスロー、`3` で3倍速。0より大きい数 |
| `--telop` | 焼き込む文字列。例 `'>> x3'` |
| `--telop-file` | テロップをファイルから読む。長文・複数行・記号入りに向く |
| `--font` | フォントファイル。省略時は fontconfig で自動選択 |
| `--font-size` | 文字サイズ(px)。既定は元動画の高さの5.75% |
| `--box-opacity` | 背景ボックスの不透明度。既定 `0.55` |
| `--telop-margin` | 下端からの余白(px)。既定は高さの7.2% |
| `--ios` | iOS向けに正規化する |
| `--fps` | 出力フレームレート。既定は入力と同じ。`--ios` では30fpsに制限 |
| `--crf`, `--preset` | libx264の画質設定。既定は CRF 20 / medium |
| `--audio-bitrate` | AACビットレート。既定 `192k` |
| `-y` | 既存の出力を上書きする |
| `--dry-run` | フィルタgraphとコマンドだけ表示する |

## 検証

期待尺は次の式で計算する。

```text
output = start + (end - start) / speed + (duration - end)
```

```bash
ffprobe -v error \
  -show_entries stream=codec_name,profile,level,pix_fmt,width,height,r_frame_rate,sample_rate,channels \
  -show_entries format=duration -of default=noprint_wrappers=1 out.mp4
```

- `format=duration` はAACのprimingで数十ms長くなることがある。映像ストリームのdurationとフレーム数も見る。
- 速度区間の中央、開始直前、終了直後の3点でフレームを抜き、テロップの有無を目視する。

```bash
ffmpeg -ss 23.5 -i out.mp4 -frames:v 1 check_before.png
ffmpeg -ss 26   -i out.mp4 -frames:v 1 check_mid.png
ffmpeg -ss 40   -i out.mp4 -frames:v 1 check_after.png
```

- iOS向けは `profile=High`, `level=41`, `pix_fmt=yuv420p`, `moov` が先頭にあることを確認する。`moov` の位置は `grep -abo moov out.mp4 | head -1` で調べ、先頭付近（数十バイト〜数KiB）ならfaststart済み。
- デスクトップのQuickTimeで再生できても実機確認の代わりにはしない。iPhoneのFiles/Safariで再生する。

## iOS向けの判断

- 1080pクラスに収める。H.264 High@4.1は1920x1080@30まで（マクロブロック上限8192）。1920x1080は8160マクロブロックで、30fpsなら上限内。
- 2090x1252のような中途半端な解像度はlevel 5.0を要求する。iPhoneの世代によっては再生できないため、`--ios` でダウンスケールする。
- 縦動画は1080x1920を上限にする。
- 黒帯は追加しない。アスペクト比を保ち、プレイヤー側のレターボックスに任せる。
- 4Kのまま配信するならH.264はlevel 5.xが必要で、古い端末では再生できない。HEVCも選択肢だが、このスクリプトはHEVCを出力しない。まずH.264 1080pで確認する。
- AAC-LC 48kHz stereo。5.1chなどは `--ios` でステレオへダウンミックスする。

## 注意

- 入力側の `-ss` とフィルタの `trim` を併用すると二重に切れる。スクリプトは入力側シークを使わない。
- `trim` の `end` は排他。境界フレームは重複しない。
- `concat` は全セグメントの解像度・fps・SAR・音声形式が一致している必要がある。スクリプトは分割前に正規化する。
- テロップは焼き込み。後から位置や文言だけを変更することはできない。素材と設定を残す。
- 日本語が豆腐になる場合は `--font` を指定する。`fc-query -f '%{lang}\n' font.ttf | tr '|' '\n' | grep -x ja` で日本語対応を確認できる。
- VFR入力は `fps` でCFR化する。音声のみ・映像なしの入力は対象外。
- 出力が奇数解像度の場合は、エンコード可能なよう2の倍数へ丸める（1px切れる）。

## references

- `references/recipes.md`: 複数区間の倍速、テロップ位置・フェード、手動フィルタの組み方
- `references/ios.md`: iOS互換の仕様、H.264レベル表、faststartと実機確認
