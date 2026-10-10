---
name: scroll-motion
description: スクロールに応じた演出（入場・パララックス・ピン留め・横スクロール・スクロールスパイ等24種）を、要求から演出IDへ対応づけてCSSファーストで実装する。スクロール演出の追加・選定・実装・レビュー時に使う。
---

# scroll-motion

スクロール演出24種を「選ぶ → 実装する → 品質を確認する」ためのスキル。CSS を先に検討し、JS は必要な演出だけに絞る。React / Next.js は必須ではない。

## 正本（single source of truth）

| ファイル | 役割 |
| --- | --- |
| `catalog.json` | 24演出の正本（ID・名称・概要・必要技術・ブラウザ制約・reduce 対応・サンプルパス） |
| `references/catalog.md` | `catalog.json` から生成した人間向けカタログ（手編集しない） |
| `examples/css/NN-*.html` | 生の HTML/CSS（＋必要最小限の JS）による実装サンプル |
| `examples/tailwind/NN-*.html` | Tailwind CSS 導入済みプロジェクト向けの実装サンプル |
| `examples/_shared/demo-frame.css` | サンプル共通のデモ枠（演出本体ではない） |
| `showroom/index.html` | 24演出をカテゴリ別に試せる静的ショールーム（生成物） |
| `references/implementation.md` | 実装パターン・ブラウザ差・フォールバックの書き方 |
| `references/quality-checklist.md` | reduce・モバイル・性能・アクセシビリティの確認項目 |

ショールームは静的ファイルのみで動作し、外部 CDN・外部フォント・外部画像を読み込まない（オフライン可）。

## 手順

### 1. 要求を演出 ID へ対応づける

`references/catalog.md` の「一覧」から候補を選ぶ。キーワード（例: 「フェード」「パララックス」「ピン留め」「目次」）で検索してよい。複数の演出を組み合わせるときは、同じスクロール位置で2つ以上の連続アニメーションが競合しないか確認する（例: ピン留め区間の内側に別の入場演出を置かない）。

### 2. 実装環境を確認する

- 既存プロジェクトの CSS 環境を優先する。Tailwind が導入済みなら `examples/tailwind/`、それ以外は `examples/css/` を使う。
- 既存の固定ヘッダー・スクロール枠・`overflow` の有無を確認する（`overflow: hidden` の親の下では `position: sticky` が効かない）。
- 依存を増やす前に、CSS だけで実現できないかを確認する。

### 3. サンプルを適用する

1. `examples/{css|tailwind}/NN-*.html` を開き、演出本体（`<style>` の演出ブロックと `<script>`）を確認する。
2. クラス名・`data-*` フック・初期状態・`prefers-reduced-motion` の分岐をそのままプロジェクトへ移す。
3. Tailwind 版では、レイアウト・余白・色・タイポグラフィはユーティリティ、アニメーション・マスク・スクロールタイムライン・`reduce` 分岐はカスタム CSS に置く（無理にユーティリティへ変換しない）。
4. デモ枠（`demo-frame.css` のクラス、`.demo-back` などのナビゲーション）はサンプル表示用なのでコピーしない。

### 4. 技術選択の判断

| 目的 | 第一候補 | 次候補 |
| --- | --- | --- |
| 画面に入ったら再生 | CSS の `transition` + `IntersectionObserver` | `animation` + `@keyframes` |
| スクロール量と連動 | CSS Scroll-driven Animations（`animation-timeline: scroll()/view()`） | スクロール購読（passive）+ `requestAnimationFrame` |
| 固定・重なり・ページ送り | `position: sticky` / `scroll-snap` | JS による位置制御 |
| 数値・文字の逐次表示 | CSS（`@keyframes`, `steps()`） | JS（`rAF` / タイマー） |
| 大量の要素の出現検出 | `IntersectionObserver`（親要素に1つ） | — |

- 常時 `scroll` イベントを監視しない。使う場合も `{ passive: true }` と `requestAnimationFrame` で間引く。
- GSAP / ScrollTrigger などのライブラリは、**ユーザーが要求したとき、または複数のピン留め・複雑なタイムラインを連結する必要があるときだけ**提案する。24演出のサンプルはすべて標準 API と CSS で成立している。
- CSS Scroll-driven Animations は Chrome/Edge 115+、Safari 26+。Firefox は未対応（フラグ付き）なので、`@supports (animation-timeline: view())` で判定し、非対応環境向けに JS フォールバックを用意する（`examples/css/09,10,11,14,18,22` が雛形）。

### 5. 品質を確認する

`references/quality-checklist.md` を通す。最低限、次は必須。

- `prefers-reduced-motion: reduce` で、必須の情報が隠れ続けない・動き続けない。
- 375px 幅で横溢れ・操作不能が起きない。
- キーボードだけでナビゲーションと主要操作ができる。
- 演出は装飾として扱い、内容は演出なしでも読める。

## ケアが必要な組み合わせ

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| カード内でデモが止まる | ピン留め・横スクロールは十分なスクロール領域が必要 | 詳細デモ（`examples/` を直接開く）で確認し、埋め込みカードでは再現しない |
| スクロールできない・指が抜けない | ネストしたスクロール枠（`scroll-snap`・横スクロール） | 枠を画面高さの 60% 以下にし、`reduce` では通常スクロールへ戻す |
| 内容が消えたまま | 初期非表示のまま JS が動かなかった | 初期非表示は `@media (prefers-reduced-motion: no-preference)` の中だけに置き、`<noscript><style>` で JS 無効時の初期非表示を解除する |
| カクつく | `width` / `top` / `background-position` の連続更新 | `transform` / `opacity` / `clip-path` に置き換えるか、更新頻度を落とす |
| ピン留めが最後まで進まない | `view()` の既定 `cover` 範囲は固定区間より広い | `animation-range: cover 25% cover 75%` のように固定区間だけを指定する |

## ショールームの操作

- 生成: `python3 scripts/build-showroom.py`（`--check` で生成物と正本の差分を検出）
- ライブデモはカード内 iframe で `examples/css/` をそのまま表示する。Tailwind ランタイムを読み込まないため、CSS / Tailwind の切替はコード表示とコピーに限定している。
- `file://` でも `python3 -m http.server` でも動作する（fetch を使わず、コードは生成時に HTML へ埋め込んでいる）。

## 検証スクリプト

`python3 scripts/check-all.py` で以下をまとめて実行できる（個別実行も可）。

| スクリプト | 検証内容 |
| --- | --- |
| `check-catalog.py` | ID 01–24・名称・使用技術・サンプルパスの欠落/重複/未知IDなし |
| `check-references.py` | SKILL.md / references / examples / showroom / README の相対参照が実在する |
| `check-external-deps.py` | 外部 CDN・外部フォント・外部画像・外部 API を読み込んでいない |
| `check-reduced-motion.py` | 全サンプルで reduce 対応が成立し、CSS で隠して JS で表示する構成は `<noscript>` のフォールバックを持つ |
| `check-mobile.py` | 375px 想定で横溢れパターンが無い |
| `check-pair-equivalence.py` | 全演出で CSS版 / Tailwind版 のフック・keyframes・reduce 対応が一致する |
| `check-hooks.py` | コード切替・コピー・再実行・詳細デモのフックと、examples を正本とする単一性 |
| `build-showroom.py --check` | ショールームとカタログMarkdownが正本から再生成できる |
