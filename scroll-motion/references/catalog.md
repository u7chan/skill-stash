# scroll-motion 演出カタログ

> このファイルは `catalog.json` から `scripts/build-showroom.py` が生成します。手で編集せず、`catalog.json` を変更して再生成してください（`python3 scripts/build-showroom.py --check` で差分を検出できます）。

- 演出数: 24
- 実装サンプル: `examples/css/`（HTML/CSS をそのまま使う版）/ `examples/tailwind/`（Tailwind CSS 導入済みプロジェクト向け）
- ショールーム: [`../showroom/index.html`](../showroom/index.html)

## カテゴリ

| カテゴリ | ID範囲 | 概要 |
| --- | --- | --- |
| 画面に入ると再生 | 01–08 | ビューポートへの進入を IntersectionObserver で検出し、再生は CSS の transition / animation に任せる。 |
| スクロール進捗と連動 | 09–16 | スクロール量を 0–1 の進捗に変換し、CSS Scroll-driven Animations か rAF の JS フォールバックで連続的に動かす。 |
| 固定・送り・ナビ | 17–24 | position: sticky とスクロール位置の検出を使い、固定表示・横送り・ナビゲーション状態を作る。 |

## 一覧

| ID | 演出 | カテゴリ | 使用技術 | CSS版 | Tailwind版 |
| --- | --- | --- | --- | --- | --- |
| 01 | [フェードイン](#01-fade-in) | 画面に入ると再生 | IntersectionObserver | [`01-fade-in.html`](../examples/css/01-fade-in.html) | [`01-fade-in.html`](../examples/tailwind/01-fade-in.html) |
| 02 | [スライドイン](#02-slide-in) | 画面に入ると再生 | IntersectionObserver | [`02-slide-in.html`](../examples/css/02-slide-in.html) | [`02-slide-in.html`](../examples/tailwind/02-slide-in.html) |
| 03 | [スタッガー](#03-stagger) | 画面に入ると再生 | IntersectionObserver | [`03-stagger.html`](../examples/css/03-stagger.html) | [`03-stagger.html`](../examples/tailwind/03-stagger.html) |
| 04 | [テキストリビール](#04-text-reveal) | 画面に入ると再生 | IntersectionObserver | [`04-text-reveal.html`](../examples/css/04-text-reveal.html) | [`04-text-reveal.html`](../examples/tailwind/04-text-reveal.html) |
| 05 | [マスクリビール](#05-mask-reveal) | 画面に入ると再生 | IntersectionObserver | [`05-mask-reveal.html`](../examples/css/05-mask-reveal.html) | [`05-mask-reveal.html`](../examples/tailwind/05-mask-reveal.html) |
| 06 | [ブラーイン](#06-blur-in) | 画面に入ると再生 | IntersectionObserver | [`06-blur-in.html`](../examples/css/06-blur-in.html) | [`06-blur-in.html`](../examples/tailwind/06-blur-in.html) |
| 07 | [タイプライター](#07-typewriter) | 画面に入ると再生 | IntersectionObserver + 素のJS | [`07-typewriter.html`](../examples/css/07-typewriter.html) | [`07-typewriter.html`](../examples/tailwind/07-typewriter.html) |
| 08 | [カウントアップ](#08-count-up) | 画面に入ると再生 | IntersectionObserver + 素のJS | [`08-count-up.html`](../examples/css/08-count-up.html) | [`08-count-up.html`](../examples/tailwind/08-count-up.html) |
| 09 | [スクロール連動](#09-scroll-linked) | スクロール進捗と連動 | CSS Scroll-driven + 素のJS | [`09-scroll-linked.html`](../examples/css/09-scroll-linked.html) | [`09-scroll-linked.html`](../examples/tailwind/09-scroll-linked.html) |
| 10 | [パララックス](#10-parallax) | スクロール進捗と連動 | CSS Scroll-driven + 素のJS | [`10-parallax.html`](../examples/css/10-parallax.html) | [`10-parallax.html`](../examples/tailwind/10-parallax.html) |
| 11 | [スクロールズーム](#11-scroll-zoom) | スクロール進捗と連動 | CSS Scroll-driven + 素のJS | [`11-scroll-zoom.html`](../examples/css/11-scroll-zoom.html) | [`11-scroll-zoom.html`](../examples/tailwind/11-scroll-zoom.html) |
| 12 | [画像シーケンス](#12-image-sequence) | スクロール進捗と連動 | 素のJS | [`12-image-sequence.html`](../examples/css/12-image-sequence.html) | [`12-image-sequence.html`](../examples/tailwind/12-image-sequence.html) |
| 13 | [SVGラインドロー](#13-svg-line-draw) | スクロール進捗と連動 | IntersectionObserver | [`13-svg-line-draw.html`](../examples/css/13-svg-line-draw.html) | [`13-svg-line-draw.html`](../examples/tailwind/13-svg-line-draw.html) |
| 14 | [テキストフィル](#14-text-fill) | スクロール進捗と連動 | CSS Scroll-driven + 素のJS | [`14-text-fill.html`](../examples/css/14-text-fill.html) | [`14-text-fill.html`](../examples/tailwind/14-text-fill.html) |
| 15 | [背景色トランジション](#15-bg-transition) | スクロール進捗と連動 | IntersectionObserver | [`15-bg-transition.html`](../examples/css/15-bg-transition.html) | [`15-bg-transition.html`](../examples/tailwind/15-bg-transition.html) |
| 16 | [マーキー（スクロール速度連動）](#16-marquee) | スクロール進捗と連動 | 素のJS | [`16-marquee.html`](../examples/css/16-marquee.html) | [`16-marquee.html`](../examples/tailwind/16-marquee.html) |
| 17 | [スティッキー](#17-sticky) | 固定・送り・ナビ | CSSのみ | [`17-sticky.html`](../examples/css/17-sticky.html) | [`17-sticky.html`](../examples/tailwind/17-sticky.html) |
| 18 | [ピン留め＋スクラブ](#18-pinned-scrub) | 固定・送り・ナビ | CSSのみ + CSS Scroll-driven + 素のJS | [`18-pinned-scrub.html`](../examples/css/18-pinned-scrub.html) | [`18-pinned-scrub.html`](../examples/tailwind/18-pinned-scrub.html) |
| 19 | [スクロールテリング](#19-scrollytelling) | 固定・送り・ナビ | IntersectionObserver + CSSのみ | [`19-scrollytelling.html`](../examples/css/19-scrollytelling.html) | [`19-scrollytelling.html`](../examples/tailwind/19-scrollytelling.html) |
| 20 | [カードスタック](#20-card-stack) | 固定・送り・ナビ | CSSのみ | [`20-card-stack.html`](../examples/css/20-card-stack.html) | [`20-card-stack.html`](../examples/tailwind/20-card-stack.html) |
| 21 | [スクロールスナップ](#21-scroll-snap) | 固定・送り・ナビ | CSSのみ | [`21-scroll-snap.html`](../examples/css/21-scroll-snap.html) | [`21-scroll-snap.html`](../examples/tailwind/21-scroll-snap.html) |
| 22 | [横スクロール](#22-horizontal-scroll) | 固定・送り・ナビ | CSSのみ + CSS Scroll-driven + 素のJS | [`22-horizontal-scroll.html`](../examples/css/22-horizontal-scroll.html) | [`22-horizontal-scroll.html`](../examples/tailwind/22-horizontal-scroll.html) |
| 23 | [隠れるヘッダー](#23-hide-header) | 固定・送り・ナビ | 素のJS | [`23-hide-header.html`](../examples/css/23-hide-header.html) | [`23-hide-header.html`](../examples/tailwind/23-hide-header.html) |
| 24 | [スクロールスパイ](#24-scrollspy) | 固定・送り・ナビ | IntersectionObserver | [`24-scrollspy.html`](../examples/css/24-scrollspy.html) | [`24-scrollspy.html`](../examples/tailwind/24-scrollspy.html) |

## 演出の詳細

<a id="01-fade-in"></a>

### 01 フェードイン

- スラッグ: `fade-in`
- カテゴリ: 画面に入ると再生
- 概要: ビューポートに入った要素の透明度を上げて表示する。最も基本的な入場演出。
- 向いている用途: 見出し・カードの入場 / セクションの切り替わり
- 検索キーワード: fade, フェードイン, opacity, 入場, 表示, appear
- 使用技術: IntersectionObserver（標準API・ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - 初期の非表示状態は @media (prefers-reduced-motion: no-preference) の中だけに置く
  - IntersectionObserver は一度検出したら unobserve して常時監視を避ける
  - transition は opacity と transform に限定し、レイアウトを動かさない
- ブラウザ制約:
  - IntersectionObserver はモダンブラウザ対応（Safari 12.1+）
- `prefers-reduced-motion`: 初期状態を作らないため、reduce 時は最初から表示される（no-preference でゲート）
- アクセシビリティ:
  - reduce 時に opacity: 0 が残らないようにする（本文が読めない事故を防ぐ）
- サンプル: [CSS版](../examples/css/01-fade-in.html) / [Tailwind版](../examples/tailwind/01-fade-in.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-01)

<a id="02-slide-in"></a>

### 02 スライドイン

- スラッグ: `slide-in`
- カテゴリ: 画面に入ると再生
- 概要: 要素を左右・上下から移動させながら表示する。方向のバリエーションを持つ。
- 向いている用途: 左右2カラムの同時入場 / リスト項目の入場
- 検索キーワード: slide, スライド, translate, 入場, 横から
- 使用技術: IntersectionObserver（標準API・ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - 方向は data-slide="up|left|right" で切り替える
  - translate3d を使い、合成レイヤーでの描画に任せる
  - 移動距離は 24–40px 程度に抑え、レイアウトは動かさない
- ブラウザ制約:
  - IntersectionObserver はモダンブラウザ対応
- `prefers-reduced-motion`: 移動をやめて常時表示にする（方向付きの初期状態も no-preference 内に限定）
- アクセシビリティ:
  - 左右から入る要素を画面外固定にしない（横スクロールを生まない）
- サンプル: [CSS版](../examples/css/02-slide-in.html) / [Tailwind版](../examples/tailwind/02-slide-in.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-02)

<a id="03-stagger"></a>

### 03 スタッガー

- スラッグ: `stagger`
- カテゴリ: 画面に入ると再生
- 概要: 複数要素を時間差で順に表示し、視線の流れを作る。
- 向いている用途: カードグリッド / ナビゲーション項目 / 価格表
- 検索キーワード: stagger, スタッガー, 順番, 遅延, delay, リスト
- 使用技術: IntersectionObserver（標準API・ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - CSS 変数 --i から transition-delay: calc(var(--i) * 90ms) を計算する
  - delay には上限を設け、長い待ち時間を作らない
  - Observer は親要素だけに付け、子要素ごとに作らない
- ブラウザ制約:
  - CSS 変数は全モダンブラウザ対応
- `prefers-reduced-motion`: 遅延を 0 にし、全要素を同時に表示する
- アクセシビリティ:
  - 遅延の合計は 400ms 程度に収め、読み始めを妨げない
- サンプル: [CSS版](../examples/css/03-stagger.html) / [Tailwind版](../examples/tailwind/03-stagger.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-03)

<a id="04-text-reveal"></a>

### 04 テキストリビール

- スラッグ: `text-reveal`
- カテゴリ: 画面に入ると再生
- 概要: 行ごとにマスクを掛け、下から押し上げるように文字を表示する。
- 向いている用途: ヒーローの見出し / 章タイトル
- 検索キーワード: text reveal, テキストリビール, 行, マスク, 見出し
- 使用技術: IntersectionObserver（標準API・ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - 行を span でラップし、overflow: hidden の親でマスクする
  - transform のみを動かし、行送りを変えない
  - テキストは選択・コピーできる状態のまま残す
- ブラウザ制約:
  - overflow: hidden + transform は全モダンブラウザ対応
- `prefers-reduced-motion`: マスクと移動をやめ、全文を静的表示する
- アクセシビリティ:
  - 行を分割しても読み上げ順が崩れない構造にする
- サンプル: [CSS版](../examples/css/04-text-reveal.html) / [Tailwind版](../examples/tailwind/04-text-reveal.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-04)

<a id="05-mask-reveal"></a>

### 05 マスクリビール

- スラッグ: `mask-reveal`
- カテゴリ: 画面に入ると再生
- 概要: 画像やカードを左から右へワイプするように表示する。
- 向いている用途: ヒーロー画像 / ギャラリー / バナー
- 検索キーワード: mask, マスク, wipe, ワイプ, clip-path, リビール
- 使用技術: IntersectionObserver（標準API・ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - clip-path: inset() の変化でマスクする（transition 可能・レイアウト非依存）
  - 画像を使わず CSS グラデーションで完結させ、外部リクエストを出さない
  - @supports not (clip-path: inset(0)) で非対応の環境ではフェードに差し替える
- ブラウザ制約:
  - clip-path: inset() はモダンブラウザ対応（IE 非対応）
- `prefers-reduced-motion`: マスクを掛けずに完成形を表示する
- アクセシビリティ:
  - マスク中も代替テキストの情報は失われないようにする
- サンプル: [CSS版](../examples/css/05-mask-reveal.html) / [Tailwind版](../examples/tailwind/05-mask-reveal.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-05)

<a id="06-blur-in"></a>

### 06 ブラーイン

- スラッグ: `blur-in`
- カテゴリ: 画面に入ると再生
- 概要: ぼかした状態からピントが合うように表示する。
- 向いている用途: 写真・図版の強調 / モーダルやポップオーバー
- 検索キーワード: blur, ブラー, ぼかし, filter, フォーカス
- 使用技術: IntersectionObserver（標準API・ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - filter: blur() は合成コストが高いので対象を小さく絞る
  - blur と同時に scale(1.02) を戻し、自然な収束に見せる
  - reduce ではぼかしを掛けずに表示する
- ブラウザ制約:
  - filter は全モダンブラウザ対応。ぼかし半径を大きくしすぎない
- `prefers-reduced-motion`: ぼかし・拡大を適用せず静止表示する
- アクセシビリティ:
  - ぼけた状態を長く維持せず、本文テキストには掛けない
- サンプル: [CSS版](../examples/css/06-blur-in.html) / [Tailwind版](../examples/tailwind/06-blur-in.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-06)

<a id="07-typewriter"></a>

### 07 タイプライター

- スラッグ: `typewriter`
- カテゴリ: 画面に入ると再生
- 概要: テキストを1文字ずつ打ち出す。カーソルは CSS で点滅させる。
- 向いている用途: キャッチコピー / ターミナル風UI / チャット風UI
- 検索キーワード: typewriter, タイプライター, 1文字, カーソル, typing
- 使用技術: IntersectionObserver（標準API・ライブラリ不要） / 素の JS（標準API・フレームワーク/ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - 1文字ずつの追記はタイマーで行い、速度を一定に保つ
  - aria-live は使わず、全文はスクリーンリーダー向けに別要素で持つ
  - 点滅カーソルは reduce で停止・非表示にする
- ブラウザ制約:
  - 標準APIのみ。ライブラリ不要
- `prefers-reduced-motion`: 打ち出しを行わず全文を即時表示し、カーソルの点滅も止める
- アクセシビリティ:
  - 1文字ずつ読み上げさせない（aria-hidden の装飾表現として扱う）
- サンプル: [CSS版](../examples/css/07-typewriter.html) / [Tailwind版](../examples/tailwind/07-typewriter.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-07)

<a id="08-count-up"></a>

### 08 カウントアップ

- スラッグ: `count-up`
- カテゴリ: 画面に入ると再生
- 概要: 数値を 0 から目標値まで増やして表示する。
- 向いている用途: 実績数値 / 料金 / 統計カード
- 検索キーワード: count up, カウントアップ, 数値, 数字, 統計
- 使用技術: IntersectionObserver（標準API・ライブラリ不要） / 素の JS（標準API・フレームワーク/ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - 値の更新は requestAnimationFrame で行い、DOM 書き換えは必要な1要素だけ
  - 書式（桁区切り・接頭辞・単位）は文字列として固定し、途中で崩さない
  - reduce では最終値を即時表示する
- ブラウザ制約:
  - IntersectionObserver + requestAnimationFrame（標準API）
- `prefers-reduced-motion`: アニメーションせず最終値を即時表示する
- アクセシビリティ:
  - 途中の値を読み上げさせない（aria-hidden の装飾扱いまたは確定値の併記）
- サンプル: [CSS版](../examples/css/08-count-up.html) / [Tailwind版](../examples/tailwind/08-count-up.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-08)

<a id="09-scroll-linked"></a>

### 09 スクロール連動

- スラッグ: `scroll-linked`
- カテゴリ: スクロール進捗と連動
- 概要: スクロール量に応じて進捗バーや強調線の幅を変える。
- 向いている用途: 記事の読了プログレス / 章の進捗表示
- 検索キーワード: progress, 進捗, スクロール連動, バー, 読了
- 使用技術: CSS Scroll-driven Animations（Chrome/Edge 115+・Safari 26+。非対応ブラウザ向けに JS フォールバックあり） / 素の JS（標準API・フレームワーク/ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - animation-timeline: scroll() を @supports で判定し、非対応時は rAF の JS フォールバックに切り替える
  - スクロール購読は passive: true + rAF で間引く
  - scaleX で描画し、width アニメーションで再レイアウトさせない
- ブラウザ制約:
  - CSS Scroll-driven Animations: Chrome/Edge 115+、Safari 26+、Firefox は未対応（フラグ付き）
  - フォールバックは requestAnimationFrame で完結し、依存ライブラリは不要
- `prefers-reduced-motion`: 進捗バーは表示するが、埋まるアニメーションは行わず現在位置を静的表示する
- アクセシビリティ:
  - 進捗は色だけでなく数値やテキストでも示す
- サンプル: [CSS版](../examples/css/09-scroll-linked.html) / [Tailwind版](../examples/tailwind/09-scroll-linked.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-09)

<a id="10-parallax"></a>

### 10 パララックス

- スラッグ: `parallax`
- カテゴリ: スクロール進捗と連動
- 概要: 背景と前景を異なる速度で動かし、奥行きを作る。
- 向いている用途: ヒーローセクション / ストーリー記事 / LP の中盤
- 検索キーワード: parallax, パララックス, 奥行き, 背景, 速度差
- 使用技術: CSS Scroll-driven Animations（Chrome/Edge 115+・Safari 26+。非対応ブラウザ向けに JS フォールバックあり） / 素の JS（標準API・フレームワーク/ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - translate3d のみを使い、レイアウトを動かさない
  - 背景は CSS グラデーションで作り、外部画像に依存しない
  - 移動量は ±15% 程度に抑え、本文の可読性を守る
- ブラウザ制約:
  - CSS Scroll-driven Animations: Chrome/Edge 115+、Safari 26+、Firefox 未対応
  - JS フォールバックは view() 相当の進捗を scrollY から算出する
- `prefers-reduced-motion`: 層の移動を止めて静的配置にする
- アクセシビリティ:
  - 動く背景の上に本文を直接置かない
- サンプル: [CSS版](../examples/css/10-parallax.html) / [Tailwind版](../examples/tailwind/10-parallax.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-10)

<a id="11-scroll-zoom"></a>

### 11 スクロールズーム

- スラッグ: `scroll-zoom`
- カテゴリ: スクロール進捗と連動
- 概要: スクロールに合わせて画像・カードを拡大縮小する。
- 向いている用途: ヒーロービジュアル / 製品ショット / 章の転換
- 検索キーワード: zoom, ズーム, 拡大, 縮小, scale
- 使用技術: CSS Scroll-driven Animations（Chrome/Edge 115+・Safari 26+。非対応ブラウザ向けに JS フォールバックあり） / 素の JS（標準API・フレームワーク/ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - view() タイムラインで拡大 → 縮小を制御する
  - scale は 0.9〜1.1 程度に留め、画像の再サンプリングを避ける
  - transform-origin を中央に固定し、起点の跳ねを防ぐ
- ブラウザ制約:
  - CSS Scroll-driven Animations: Chrome/Edge 115+、Safari 26+、Firefox 未対応
  - image-rendering は指定せず、等倍付近を中心に動かす
- `prefers-reduced-motion`: 拡大縮小をやめ、等倍で表示する
- アクセシビリティ:
  - 拡大中もテキストが読みやすいサイズを保つ
- サンプル: [CSS版](../examples/css/11-scroll-zoom.html) / [Tailwind版](../examples/tailwind/11-scroll-zoom.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-11)

<a id="12-image-sequence"></a>

### 12 画像シーケンス

- スラッグ: `image-sequence`
- カテゴリ: スクロール進捗と連動
- 概要: スクロール位置に応じて連番フレームを差し替え、動画のように見せる。
- 向いている用途: 製品の回転表示 / 工程の分解表示 / Apple 風スクラブ
- 検索キーワード: sequence, シーケンス, フレーム, 連番, 回転, スクラブ
- 使用技術: 素の JS（標準API・フレームワーク/ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - rAF で進捗を計算し、変化したフレームだけを差し替える
  - 画像はインライン SVG の data URI で生成し、外部リクエストを出さない
  - 先読みは最小限に留め、フレーム数は 12 前後から始める
- ブラウザ制約:
  - data URI の SVG は外部通信なしで描画できる（オフライン動作）
- `prefers-reduced-motion`: 代表フレームを1枚だけ静的に表示する
- アクセシビリティ:
  - フレーム差し替えは装飾。説明テキストを必ず併記する
- サンプル: [CSS版](../examples/css/12-image-sequence.html) / [Tailwind版](../examples/tailwind/12-image-sequence.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-12)

<a id="13-svg-line-draw"></a>

### 13 SVGラインドロー

- スラッグ: `svg-line-draw`
- カテゴリ: スクロール進捗と連動
- 概要: 線が引かれていくように SVG パスを描画する。
- 向いている用途: 図解・チャートの導入 / ロゴの描画 / 工程図
- 検索キーワード: svg, line draw, ラインドロー, パス, stroke
- 使用技術: IntersectionObserver（標準API・ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - stroke-dasharray / stroke-dashoffset を変化させて描く
  - パス長は getTotalLength() で取得し、数値をハードコードしない
  - reduce では完成形を即時表示する
- ブラウザ制約:
  - SVGGeometryElement.getTotalLength はモダンブラウザ対応
- `prefers-reduced-motion`: dash を初期化せず、完成した線を表示する
- アクセシビリティ:
  - 装飾 SVG には aria-hidden="true" を付ける
- サンプル: [CSS版](../examples/css/13-svg-line-draw.html) / [Tailwind版](../examples/tailwind/13-svg-line-draw.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-13)

<a id="14-text-fill"></a>

### 14 テキストフィル

- スラッグ: `text-fill`
- カテゴリ: スクロール進捗と連動
- 概要: スクロールに合わせて文字を色で塗りつぶしていく。
- 向いている用途: 引用・キーメッセージ / 章の導入文
- 検索キーワード: text fill, テキストフィル, 塗り, background-clip, 蛍光
- 使用技術: CSS Scroll-driven Animations（Chrome/Edge 115+・Safari 26+。非対応ブラウザ向けに JS フォールバックあり） / 素の JS（標準API・フレームワーク/ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - background-clip: text と background-size で塗り進める
  - 途中状態でも読めるよう、下地色にも十分なコントラストを確保する
  - reduce では最初から塗り切った状態で表示する
- ブラウザ制約:
  - background-clip: text は -webkit- 接頭辞が必要（Chrome/Safari）。Firefox は標準対応
  - CSS Scroll-driven Animations: Chrome/Edge 115+、Safari 26+、Firefox 未対応
- `prefers-reduced-motion`: 塗りの進行を止め、完成状態で表示する
- アクセシビリティ:
  - 色のコントラストは塗り前後とも WCAG AA を目安に確保する
- サンプル: [CSS版](../examples/css/14-text-fill.html) / [Tailwind版](../examples/tailwind/14-text-fill.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-14)

<a id="15-bg-transition"></a>

### 15 背景色トランジション

- スラッグ: `bg-transition`
- カテゴリ: スクロール進捗と連動
- 概要: セクションごとに背景色を切り替え、場面転換を示す。
- 向いている用途: 章の切り替え / LP のセクション区切り / ダーク/ライトの反転
- 検索キーワード: 背景色, bg, 色, セクション, トランジション
- 使用技術: IntersectionObserver（標準API・ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - 連続的な色補間ではなく、IntersectionObserver のしきい値で離散的に切り替える
  - CSS 変数を差し替えて transition で補間する
  - 色は意味の補助に留め、テキストのラベルも併記する
- ブラウザ制約:
  - IntersectionObserver + CSS 変数（モダンブラウザ対応）
- `prefers-reduced-motion`: 色は切り替えるが、補間アニメーションは行わず即時反映する
- アクセシビリティ:
  - 背景色の変化だけに意味を持たせない
- サンプル: [CSS版](../examples/css/15-bg-transition.html) / [Tailwind版](../examples/tailwind/15-bg-transition.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-15)

<a id="16-marquee"></a>

### 16 マーキー（スクロール速度連動）

- スラッグ: `marquee`
- カテゴリ: スクロール進捗と連動
- 概要: 流れる行の速度をスクロール速度に連動させる。
- 向いている用途: キーワードの帯 / ブランドのロゴ列 / 実績の連続表示
- 検索キーワード: marquee, マーキー, 流れる, 速度, ベルト
- 使用技術: 素の JS（標準API・フレームワーク/ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - scroll は passive: true で購読し、rAF 内で速度を平滑化する
  - translate3d で描画し、内容を複製して途切れを防ぐ
  - reduce では自動再生を止め、内容は静的に読める状態で残す
- ブラウザ制約:
  - 標準APIのみ。スクロール速度は scrollY の差分から算出する
- `prefers-reduced-motion`: 自動再生を停止し、行を折り返して静的表示する
- アクセシビリティ:
  - 流れるテキストは装飾扱いを基本とし、同一内容を通常テキストでも置く
- サンプル: [CSS版](../examples/css/16-marquee.html) / [Tailwind版](../examples/tailwind/16-marquee.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-16)

<a id="17-sticky"></a>

### 17 スティッキー

- スラッグ: `sticky`
- カテゴリ: 固定・送り・ナビ
- 概要: 追従する目次や情報パネルを固定表示する。
- 向いている用途: 記事の目次 / 商品情報パネル / フィルタUI
- 検索キーワード: sticky, スティッキー, 追従, 目次, 固定
- 使用技術: HTML/CSS のみ（JS 不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - position: sticky と親の高さだけで完結させ、JSを使わない
  - top の値は固定ヘッダーの高さと重ならないように決め、重なりを避ける
  - 親要素に overflow: hidden があると sticky が効かない点に注意する
- ブラウザ制約:
  - position: sticky は全モダンブラウザ対応（旧 Safari は -webkit- 接頭辞）
- `prefers-reduced-motion`: 動きを伴わないため常時固定のまま（reduce 専用の分岐は不要）
- アクセシビリティ:
  - sticky 内のリンクはキーボードで到達可能にする
- サンプル: [CSS版](../examples/css/17-sticky.html) / [Tailwind版](../examples/tailwind/17-sticky.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-17)

<a id="18-pinned-scrub"></a>

### 18 ピン留め＋スクラブ

- スラッグ: `pinned-scrub`
- カテゴリ: 固定・送り・ナビ
- 概要: セクションを固定し、スクロール量で進捗（スクラブ）を動かす。
- 向いている用途: 製品の工程説明 / タイムライン / ステップ表示
- 検索キーワード: pin, ピン留め, スクラブ, 固定, 進捗
- 使用技術: HTML/CSS のみ（JS 不要） / CSS Scroll-driven Animations（Chrome/Edge 115+・Safari 26+。非対応ブラウザ向けに JS フォールバックあり） / 素の JS（標準API・フレームワーク/ライブラリ不要）
- 任意ライブラリ: GSAP/ScrollTrigger は複数のピン留めを連結する場合の任意候補（本サンプルでは未使用）
- 実装の要点:
  - sticky の親に十分な高さ（例: 300vh）を確保し、animation-range で固定区間だけを進捗に対応させる
  - 進捗はスクロールタイムラインまたは rAF で 0–1 に正規化する
  - reduce では固定をやめ、要素を通常フローで順に表示する
- ブラウザ制約:
  - CSS Scroll-driven Animations: Chrome/Edge 115+、Safari 26+、Firefox 未対応
  - JS フォールバックでは sticky の親の位置から進捗を計算する
- `prefers-reduced-motion`: ピン留めを解除し、進捗に応じた内容を縦積みで表示する
- アクセシビリティ:
  - 固定中もコンテンツは DOM 順に読めるようにする
- サンプル: [CSS版](../examples/css/18-pinned-scrub.html) / [Tailwind版](../examples/tailwind/18-pinned-scrub.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-18)

<a id="19-scrollytelling"></a>

### 19 スクロールテリング

- スラッグ: `scrollytelling`
- カテゴリ: 固定・送り・ナビ
- 概要: 固定した舞台の上で、文章のステップに合わせて内容を切り替える。
- 向いている用途: データ解説 / インタラクティブ記事 / 製品ストーリー
- 検索キーワード: scrollytelling, スクロールテリング, ストーリー, ステップ, 解説
- 使用技術: IntersectionObserver（標準API・ライブラリ不要） / HTML/CSS のみ（JS 不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - ステップの検出は IntersectionObserver のしきい値で行い、連続イベントを使わない
  - ステップは DOM 順に並べ、スクリーンリーダーでも読める構造にする
  - reduce では固定を解除し、図と文を縦積みで対応させる
- ブラウザ制約:
  - IntersectionObserver + position: sticky（モダンブラウザ対応）
- `prefers-reduced-motion`: 固定を解除し、各ステップの直後に図を並べる
- アクセシビリティ:
  - 図の切り替えは aria-live を使わず、説明は本文側に置く
- サンプル: [CSS版](../examples/css/19-scrollytelling.html) / [Tailwind版](../examples/tailwind/19-scrollytelling.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-19)

<a id="20-card-stack"></a>

### 20 カードスタック

- スラッグ: `card-stack`
- カテゴリ: 固定・送り・ナビ
- 概要: カードが上に重なっていくように見せる。
- 向いている用途: 機能一覧 / ステップ紹介 / プラン比較
- 検索キーワード: card stack, カードスタック, 重なり, 積み上げ
- 使用技術: HTML/CSS のみ（JS 不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - sticky と top オフセットのずらしで表現し、JSを使わない
  - カードごとに top オフセットをずらして重なりを作り、transform の競合を避ける
  - reduce では重なりを止め、等間隔のカード一覧にする
- ブラウザ制約:
  - position: sticky は全モダンブラウザ対応
- `prefers-reduced-motion`: sticky を解除し、通常の縦積みカードとして表示する
- アクセシビリティ:
  - カードの並び順が DOM 順と一致するようにする
- サンプル: [CSS版](../examples/css/20-card-stack.html) / [Tailwind版](../examples/tailwind/20-card-stack.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-20)

<a id="21-scroll-snap"></a>

### 21 スクロールスナップ

- スラッグ: `scroll-snap`
- カテゴリ: 固定・送り・ナビ
- 概要: スクロールを1枚ずつで止め、ページ送りのように見せる。
- 向いている用途: スライドショー / オンボーディング / モバイルのカード送り
- 検索キーワード: scroll snap, スナップ, ページ送り, スライド
- 使用技術: HTML/CSS のみ（JS 不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - scroll-snap-type と scroll-snap-align の組み合わせで完結させる
  - スナップさせる枠の高さを固定し、ページ全体には掛けない
  - scroll-padding で固定ヘッダーとの重なりを調整する
- ブラウザ制約:
  - scroll-snap は全モダンブラウザ対応（Safari 15+）
- `prefers-reduced-motion`: スナップは位置決めであり動きの演出ではないため維持する（reduce 専用の分岐は不要）
- アクセシビリティ:
  - スナップ枠の中にフォーカス可能な要素を置き、キーボードで送れるようにする
- サンプル: [CSS版](../examples/css/21-scroll-snap.html) / [Tailwind版](../examples/tailwind/21-scroll-snap.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-21)

<a id="22-horizontal-scroll"></a>

### 22 横スクロール

- スラッグ: `horizontal-scroll`
- カテゴリ: 固定・送り・ナビ
- 概要: 縦スクロールを横方向の移動に置き換えて、パネルを送る。
- 向いている用途: ギャラリー / タイムライン / 比較パネル
- 検索キーワード: horizontal, 横スクロール, 横送り, パネル
- 使用技術: HTML/CSS のみ（JS 不要） / CSS Scroll-driven Animations（Chrome/Edge 115+・Safari 26+。非対応ブラウザ向けに JS フォールバックあり） / 素の JS（標準API・フレームワーク/ライブラリ不要）
- 任意ライブラリ: GSAP/ScrollTrigger は横送りと他のピン留めを連結する場合の任意候補（本サンプルでは未使用）
- 実装の要点:
  - sticky のビューポートと横長トラックの translateX を進捗に結びつける
  - 必要な移動量はスクロール枠の幅とトラック幅から計算し、リサイズ時に再計算する
  - reduce では translate をやめ、通常の縦スクロールで読ませる
- ブラウザ制約:
  - CSS Scroll-driven Animations: Chrome/Edge 115+、Safari 26+、Firefox 未対応
  - JS フォールバックでも横スクロール枠自体は通常の縦スクロールで機能する
- `prefers-reduced-motion`: 横送りをやめ、パネルを縦に積んで表示する
- アクセシビリティ:
  - 横送りでも本文は DOM 順に読めるようにする
- サンプル: [CSS版](../examples/css/22-horizontal-scroll.html) / [Tailwind版](../examples/tailwind/22-horizontal-scroll.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-22)

<a id="23-hide-header"></a>

### 23 隠れるヘッダー

- スラッグ: `hide-header`
- カテゴリ: 固定・送り・ナビ
- 概要: 下スクロールで隠れ、上スクロールで再表示するヘッダー。
- 向いている用途: 記事ページ / モバイルのヘッダー / 商品一覧
- 検索キーワード: header, ヘッダー, 隠れる, hide, 上スクロール
- 使用技術: 素の JS（標準API・フレームワーク/ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - scroll は passive + rAF で間引き、移動方向だけを見る
  - ヘッダーの高さぶんの余白を本文に確保し、レイアウトシフトを避ける
  - 隠れている間もキーボード操作は維持し、reduce では常時表示にする
- ブラウザ制約:
  - 標準APIのみ。transform: translateY で移動する
- `prefers-reduced-motion`: ヘッダーを隠さず、常時表示にする
- アクセシビリティ:
  - 隠れた状態でもヘッダー内リンクのフォーカス順を壊さない
- サンプル: [CSS版](../examples/css/23-hide-header.html) / [Tailwind版](../examples/tailwind/23-hide-header.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-23)

<a id="24-scrollspy"></a>

### 24 スクロールスパイ

- スラッグ: `scrollspy`
- カテゴリ: 固定・送り・ナビ
- 概要: 現在位置に対応する目次項目をハイライトする。
- 向いている用途: 長い記事の目次 / 設定画面 / ドキュメント
- 検索キーワード: scrollspy, スクロールスパイ, 目次, 現在位置, ナビ
- 使用技術: IntersectionObserver（標準API・ライブラリ不要）
- 任意ライブラリ: 不要（標準APIとCSSのみ）
- 実装の要点:
  - rootMargin でビューポート中央付近のセクションを検出対象にする
  - aria-current="true" を切り替え、視覚以外でも現在位置が分かるようにする
  - reduce では scroll-behavior: smooth を無効化する
- ブラウザ制約:
  - IntersectionObserver + CSS 変数（モダンブラウザ対応）
- `prefers-reduced-motion`: スムーススクロールを無効化し、移動を即時反映にする
- アクセシビリティ:
  - 現在地の強調は色だけでなく aria-current で伝える
- サンプル: [CSS版](../examples/css/24-scrollspy.html) / [Tailwind版](../examples/tailwind/24-scrollspy.html)
- ショールーム: [カードを開く](../showroom/index.html#effect-24)
