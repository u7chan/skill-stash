# 実装ガイド

スクロール演出を実装するときの型と、ブラウザ差への対応をまとめる。カタログ本体は [catalog.md](catalog.md)、確認項目は [quality-checklist.md](quality-checklist.md)。

## 1. CSS ファーストの判断

| 実現したいこと | 第一候補 | 理由 |
| --- | --- | --- |
| 「入ったら再生」 | CSS の `transition` / `@keyframes` + クラス付与 | 再生そのものは CSS が担当し、JS はトリガーだけを見る |
| スクロール量と連動 | CSS Scroll-driven Animations | スクロールイベント購読が不要で、メインスレッドを塞がない |
| 固定・重なり・送り | `position: sticky` / `scroll-snap` | JS なしで成立し、ブラウザ最適化の対象になる |
| 速度に反応する表現 | スクロール購読（`passive`）+ `rAF` | 速度は CSS では取得できない |
| 数値・文字の逐次表示 | CSS（`@keyframes` + `steps()`） | 文字列を JS で書き換える必要がなければ CSS で足りる |

ライブラリ（GSAP / ScrollTrigger など）は、複数の固定区間を連結する・タイムラインを細かく同期させる・スクロール位置に応じた複雑な状態機械を組む、といった要求があるときに初めて検討する。

## 2. 入場演出の基本形

```css
/* 1. 変形・フェードは transform と opacity に限定する */
.reveal {
  transition: opacity 700ms cubic-bezier(0.22, 1, 0.36, 1), transform 700ms cubic-bezier(0.22, 1, 0.36, 1);
}

/* 2. 初期状態は「動きを許容する環境」の中だけに置く */
@media (prefers-reduced-motion: no-preference) {
  .reveal {
    opacity: 0;
    transform: translate3d(0, 16px, 0);
  }

  .reveal.is-visible {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}
```

```js
/* 3. 監視は親に1つ、検出後は unobserve する */
const targets = document.querySelectorAll('.reveal');
if (!('IntersectionObserver' in window)) {
  targets.forEach((el) => el.classList.add('is-visible')); /* JS が使えなくても内容は読める */
} else {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });
  targets.forEach((el) => observer.observe(el));
}
```

要点:

- 初期状態は `no-preference` の内側に置く。reduce 環境では「何もしない = 見えている」が既定になる。
- `unobserve` して常時監視を避ける。スタッガーは親だけを監視し、遅延は `transition-delay: calc(var(--i) * 90ms)` で作る。
- 移動で横溢れが出る場合は、セクション側に `overflow-x: clip` を指定する（`overflow: hidden` と違いスクロールコンテナを作らない）。

### JS 無効時・スクリプト失敗時のフォールバック

CSS で初期非表示にして JS で表示する演出は、JS が動かないと内容が隠れたままになる。`<noscript>` の
`<style>` で初期非表示を解除しておく（`head` 内に置ける。演出本体の `<style>` より後に書くと上書きできる）。

```html
<noscript><style>
  /* JS が無効な環境では初期非表示を解除して内容を読めるようにする */
  .reveal {
    opacity: 1;
    transform: none;
  }
</style></noscript>
```

- マスク（`clip-path`）・押し上げ（`transform`）・`display: none` の切替も同じ考え方で解除する。
- 打ち出しテキストやカウントアップのように、JS が内容そのものを作る演出は、`sr-only` に置いた全文・確定値を
  `<noscript>` で可視化する（`examples/css/07-typewriter.html`、`08-count-up.html` が雛形）。
- `scripts/check-reduced-motion.py` が「CSS で隠して JS で表示する構成に `<noscript>` があるか」を検証する。

## 3. スクロール進捗の2系統

CSS Scroll-driven Animations が使える環境では CSS だけで動かし、非対応環境では同じ進捗を JS で再現する。

```css
.section {
  view-timeline-name: --scrub;
  view-timeline-axis: block;
}

@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .progress {
      animation: grow linear both;
      animation-timeline: --scrub;
      /* 固定区間を使う場合: cover の何%から何%までを進捗に対応させるか */
      animation-range: cover 25% cover 75%;
    }
  }
}

@keyframes grow {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

```js
const bar = document.querySelector('[data-progress]'); /* 進捗バーの要素 */
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
const supportsTimeline = CSS.supports && CSS.supports('animation-timeline: view()');
if (!supportsTimeline && !reduce.matches) {
  let ticking = false;
  const update = () => {
    ticking = false;
    const max = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = `scaleX(${(max > 0 ? scrollY / max : 0).toFixed(4)})`;
  };
  addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }, { passive: true });
  addEventListener('resize', update);
  update();
}
```

要点:

- `view()` の既定範囲は `cover`（要素が入り切って出るまで）で、固定区間より広い。ピン留めと同期させるときは `animation-range` を明示する。
- スクロール購読は `{ passive: true }` + `rAF` + `ticking` フラグで間引く。`scroll` ハンドラ内で直接 DOM を書かない。
- 横スクロールのように移動量が内容に依存する場合は、JS で `スクロール枠の幅` と `トラック幅` から実距離を計算し、CSS 変数（`--travel`）として渡す。CSS は計算結果をアニメーションする役割に限定する。
- 画像シーケンス（`examples/css/12-*.html`）はフレームを rAF で計算し、変化したフレームだけを差し替える。外部画像を使わずインライン SVG の `data:` URI で完結させると、オフラインでも動作する。

## 4. ブラウザ差とフォールバック

| 機能 | 対応状況 | 代替 |
| --- | --- | --- |
| `animation-timeline: scroll()` / `view()` | Chrome/Edge 115+、Safari 26+、Firefox 未対応（フラグ付き） | `@supports` で判定し、rAF による進捗計算（`09,10,11,14,18,22`） |
| `position: sticky` | 全モダンブラウザ | なし（`overflow: hidden` の親に注意） |
| `scroll-snap-type` | 全モダンブラウザ（Safari 15+） | 通常スクロール |
| `clip-path: inset()` | モダンブラウザ | `@supports not` でフェードに差し替え（`05`） |
| `background-clip: text` | `-webkit-` 接頭辞が必要なブラウザあり | `@supports not` で通常テキスト色（`14`） |
| `filter: blur()` | 全モダンブラウザ | 対象を小さく保つ。reduce では適用しない（`06`） |
| `getTotalLength()` | モダンブラウザ | 未対応時は描画済みの線を表示（`13`） |

## 5. Tailwind CSS 版の書き方

Tailwind 版は「呼び出し元に Tailwind が導入済み」という前提のサンプル。無理にユーティリティへ変換せず、役割で分ける。

- **ユーティリティ**: レイアウト（`grid` / `gap-*` / `sm:grid-cols-*`）、余白、色（`bg-white` / `border-slate-200`）、タイポグラフィ、角丸。
- **カスタム CSS**: `@keyframes`、`animation-timeline`、`clip-path`、`position: sticky` の調整、`prefers-reduced-motion` の分岐、CSS 変数。
- **JS**: トリガー（`IntersectionObserver`）、進捗計算（`rAF`）、文字列の逐次表示。CSS 版と同じロジックを使う（`scripts/check-pair-equivalence.py` が差分を検出する）。
- デモ枠（`examples/_shared/demo-frame.css`）は単体表示用。Tailwind プロジェクトではアプリ側のレイアウトに置き換える。

## 6. 組み合わせの指針

- 1つのセクションに複数の連続アニメーションを重ねない。ピン留め区間の内側に入場演出を置くと、固定中に要素が動いて読みにくくなる。
- 入場演出 → スクロール連動 → 固定の順に、ページ全体を「静 → 動 → 静」と配置すると、スクロール中の負荷と読みにくさを抑えられる。
- 装飾は積み増しせず、1ページあたり 2〜3 種類に絞る。
