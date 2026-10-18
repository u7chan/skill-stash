# フィルタレシピ

`scripts/video-edit.sh` は「1区間の倍速 + 下部中央テロップ」専用。ここでは手でフィルタを組むときの型を示す。時刻は秒。`trim` の `end` は排他。

## 共通の考え方

1. `setpts=PTS-STARTPTS` で0起点にし、`fps` と `setsar=1` で全セグメントの条件を揃える。
2. `split` でセグメント数に分ける。音声も `asplit` する。フィルタは同じ入力ストリームを2回参照できない。
3. 速度を変えるセグメントだけ `setpts=(PTS-STARTPTS)/倍率` と `atempo` を付ける。速度変更後は `fps` で再サンプリングしてCFRに戻す。
4. `concat` で戻す。解像度・fps・SAR・音声のサンプルレート/チャンネルが一致していないと失敗する。
5. テロップは対象セグメントの `setpts` の後に `drawtext` を付ける。

## 1区間だけ倍速（24s〜44sを3倍、他は等倍）

```bash
ffmpeg -hide_banner -i in.mp4 -filter_complex "\
[0:v]setpts=PTS-STARTPTS,fps=30,setsar=1,split=3[vs0][vs1][vs2];\
[vs0]trim=start=0:end=24,setpts=PTS-STARTPTS[v0];\
[vs1]trim=start=24:end=44,setpts=(PTS-STARTPTS)/3,fps=30[v1];\
[vs2]trim=start=44,setpts=PTS-STARTPTS[v2];\
[v0][v1][v2]concat=n=3:v=1:a=0[v];\
[0:a]asetpts=PTS-STARTPTS,asplit=3[as0][as1][as2];\
[as0]atrim=start=0:end=24,asetpts=PTS-STARTPTS[a0];\
[as1]atrim=start=24:end=44,asetpts=PTS-STARTPTS,atempo=2,atempo=1.5[a1];\
[as2]atrim=start=44,asetpts=PTS-STARTPTS[a2];\
[a0][a1][a2]concat=n=3:v=0:a=1[a]" \
-map '[v]' -map '[a]' -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac out.mp4
```

- 3倍は `atempo=3` でもよいが、`atempo` が0.5〜2.0しか受け付けないffmpegでも動くよう `2` と `1.5` に分ける。
- 先頭や末尾を切らない場合は該当セグメントを削る。前半だけ、後半だけのときは `concat=n=2` や `n=1` になる。
- 先頭から途中まで（前半なし）なら `trim=start=0:end=END`、末尾まで（後半なし）なら `trim=start=START`。

## 複数区間を別々の倍率にする

0〜1s等倍、1〜2sを2倍、2〜3s等倍、3〜4sを0.5倍、4〜6s等倍。出力は6.5秒になる。

```bash
ffmpeg -hide_banner -i in.mp4 -filter_complex "\
[0:v]setpts=PTS-STARTPTS,fps=30,setsar=1,split=5[vs0][vs1][vs2][vs3][vs4];\
[vs0]trim=start=0:end=1,setpts=PTS-STARTPTS[v0];\
[vs1]trim=start=1:end=2,setpts=(PTS-STARTPTS)/2,fps=30[v1];\
[vs2]trim=start=2:end=3,setpts=PTS-STARTPTS[v2];\
[vs3]trim=start=3:end=4,setpts=(PTS-STARTPTS)/0.5,fps=30[v3];\
[vs4]trim=start=4,setpts=PTS-STARTPTS[v4];\
[v0][v1][v2][v3][v4]concat=n=5:v=1:a=0[v];\
[0:a]asetpts=PTS-STARTPTS,asplit=5[as0][as1][as2][as3][as4];\
[as0]atrim=start=0:end=1,asetpts=PTS-STARTPTS[a0];\
[as1]atrim=start=1:end=2,asetpts=PTS-STARTPTS,atempo=2[a1];\
[as2]atrim=start=2:end=3,asetpts=PTS-STARTPTS[a2];\
[as3]atrim=start=3:end=4,asetpts=PTS-STARTPTS,atempo=0.5[a3];\
[as4]atrim=start=4,asetpts=PTS-STARTPTS[a4];\
[a0][a1][a2][a3][a4]concat=n=5:v=0:a=1[a]" \
-map '[v]' -map '[a]' -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac out.mp4
```

セグメントを増やす場合は `split` / `asplit` の数、`concat` の `n`、ラベルの番号を揃えて増やす。

## テロップ

### 位置と背景

```text
drawtext=fontfile=/path/font.ttf:text='>> x3':fontcolor=white:fontsize=72:
  box=1:boxcolor=black@0.55:boxborderw=24:
  x=(w-text_w)/2:y=h-text_h-90
```

- 下部中央: `x=(w-text_w)/2`、`y=h-text_h-Y`。`Y` が下端からの余白。
- 上部中央: `y=Y`。
- 背景ボックス: `box=1`、`boxcolor=black@不透明度`、`boxborderw` が文字の周囲の余白。
- 複数行は `textfile=` に改行を入れる。行間は `line_spacing`。
- 文字サイズは元動画の高さに対する比率で決めると解像度違いでも同じ見た目になる（例: 高さ1252pxで72px ≈ 5.75%）。

### 文字列の渡し方

`textfile=` を使うと `%`、`'`、`:`、`,` をエスケープしなくてよい。複数行もそのまま書ける。

```text
drawtext=fontfile=/path/font.ttf:textfile=/tmp/telop.txt:expansion=none:...
```

`expansion=none` は `%{...}` の展開を無効にする。ファイル内容はUTF-8で保存する。

### フェード

`alpha` は式で指定する。`t` はそのフィルタに入るストリームのタイムスタンプ。フェードアウトに使える `T` は drawtext では使えないため、区間の尺を直接書く。2秒の区間で0.4秒フェードする例。

```text
drawtext=...,alpha='if(lt(t,0.4),t/0.4,if(gt(t,1.6),(2.0-t)/0.4,1))'
```

### 表示区間だけ出す

倍速区間だけでなく、出力タイムライン上のある区間だけテロップを出す場合は、連結後の映像に `drawtext` を付けて `enable` を使う。

```text
drawtext=...,enable='between(t,1,3)'
```

`t` は出力タイムラインの秒。倍速区間の位置は「前半の尺 + 倍速区間の尺」で変わる点に注意する。

## 手動時の注意

- 入力側の `-ss` / `-t` とフィルタの `trim` を併用しない。二重に切れて尺がずれる。
- `-shortest` を付けない。音声の方が短いときに映像が切れる。
- セグメントの解像度・fps・SAR・音声形式が揃っていないと `concat` が失敗する。先頭で揃える。
- `drawtext` はフレームを再エンコードする。GPUエンコードを使う場合も `drawtext` はCPU側で動くため、フィルタ順序に注意する。
