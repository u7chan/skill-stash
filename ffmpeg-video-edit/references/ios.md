# iOS向けエンコード

iPhone・iPadのFiles/Safari/写真で確実に再生させるための最低条件と、`--ios` が何をしているかの説明。

## 安全側の仕様

| 項目 | 値 |
| --- | --- |
| コンテナ | MP4（`.mp4` / `.mov`） |
| 映像 | H.264 High profile、level 4.1、yuv420p |
| 解像度 | 1920x1080以下（縦動画は1080x1920以下） |
| フレームレート | 30fps以下 |
| 音声 | AAC-LC、48kHz、ステレオ以下 |
| 配置 | `moov` を先頭に置く（faststart） |

古い端末を無視してよいならlevel 4.2以上や4Kも選べるが、配布先が不明なときはこの範囲に収める。4Kは再生対応が端末とOSの世代に依存する。

## H.264のレベル

マクロブロック数 `MB = ceil(width / 16) * ceil(height / 16)` が `MaxFS` に収まり、`MB * fps` が `MaxMBPS` に収まる必要がある。

| level | MaxFS (MB) | MaxMBPS | 目安 |
| --- | --- | --- | --- |
| 4.0 | 8192 | 245760 | 1920x1080@30（8160MB / 244800） |
| 4.1 | 8192 | 245760 | 1920x1080@30。ビットレート上限が4.0より高い |
| 4.2 | 8704 | 522240 | 1920x1080@60 |
| 5.0 | 22080 | 589824 | 2090x1252@30（10349MB） |
| 5.1 | 36864 | 983040 | 3840x2160@30（32400MB） |
| 5.2 | 36864 | 2073600 | 3840x2160@60 |

MaxFS / MaxMBPS は仕様上の上限。実際のビットレート上限はプロファイルでも変わる。

### 中途半端な解像度の例

2090x1252は `131 * 79 = 10349MB` で、level 4.1のMaxFS 8192を超える。level 5.0が要求されるため、`--ios` は1920x1080に収まるようダウンスケールする。1080pクラスの上限（1920x1080 / 1080x1920）に収めれば、レベルの計算を意識せずに済む。

## faststart

`-movflags +faststart` を付けると、エンコード後に `moov` がファイル先頭へ移動する。ダウンロードしながら再生できるようになる。

```bash
grep -abo moov out.mp4 | head -1
# 例: 36:moov  （先頭付近 = faststart済み）
```

`moov` がファイル末尾にあると、ダウンロード完了まで再生が始まらないことがある。

## `--ios` の挙動

- 映像: H.264 High@4.1、yuv420p、30fps以下。1920x1080（縦は1080x1920）を超える場合だけアスペクト比を保ってダウンスケールする。黒帯は追加しない。
- 音声: AAC-LC 48kHz ステレオ。5.1chなどはステレオへ落とす。
- 回転メタデータ付きの動画は、ffmpegのautorotate後の表示寸法で上限を判定する。
- 出力拡張子が `.mp4` / `.mov` のときに `-tag:v avc1` と `-movflags +faststart` を付ける。

## 検証

```bash
ffprobe -v error \
  -show_entries stream=codec_name,profile,level,pix_fmt,width,height,r_frame_rate,sample_rate,channels \
  -show_entries format=duration -of default=noprint_wrappers=1 out.mp4
```

- `profile=High`、`level=41`、`pix_fmt=yuv420p`、`r_frame_rate=30/1` 以下を確認する。
- `format=duration` はAACのprimingで数十ms長くなることがある。映像ストリームの尺で確認する。
- 実機のFiles/Safariで再生する。デスクトップのQuickTimeでの再生は実機確認の代わりにならない。
- 4KやHEVCを選ぶ場合は、想定する最も古い端末で先に再生確認する。
