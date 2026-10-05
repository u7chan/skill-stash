# コンポーネント

公式コードスニペット（`digital-go-jp/design-system-example-components-html`、MIT License）の CSS を `assets/components/<name>.css` に同梱している。クラス名・`data-*` 属性は公式実装の契約であり、**独自のクラス名に置き換えない**。

読み込み順: `assets/dads-tokens.css` → `assets/dads-global.css` → 必要な `assets/components/*.css`。

```html
<link rel="stylesheet" href="assets/dads-tokens.css">
<link rel="stylesheet" href="assets/dads-global.css">
<link rel="stylesheet" href="assets/components/form-control-label.css">
<link rel="stylesheet" href="assets/components/input-text.css">
<link rel="stylesheet" href="assets/components/button.css">
```

## 同梱しているコンポーネント CSS

`accordion` `blockquote` `breadcrumb` `button` `calendar` `card` `carousel` `checkbox` `chip-label` `date-picker` `description-list` `disclosure` `divider` `drawer` `emergency-banner` `file-upload` `form-control-label` `hamburger-menu-button` `heading` `horizontal-menu` `image` `input-text` `language-selector` `link` `list` `menu-list` `menu-list-box` `modal-dialog` `notification-banner` `page-navigation` `progress-indicator` `radio` `resource-list` `search-box` `select` `step-navigation` `switch` `tab` `table` `textarea` `toc` `utility-link`

## JavaScript が必要なコンポーネント

CSS だけでは動作しない。静的な HTML で再現する場合は**使わないか、公式の JS を読み込む**。見た目だけ真似て壊れた操作を作らない。

| コンポーネント | 必要な実装 |
| --- | --- |
| `accordion` / `disclosure` | 開閉（`<details>` でも代替可） |
| `tab` | タブ切替（`role="tablist"` + キーボード操作） |
| `switch` | トグル |
| `modal-dialog` / `drawer` | `showModal()` とフォーカストラップ |
| `calendar` / `date-picker` | 日付選択 |
| `menu-list-box` / `combobox` | 候補絞り込み |
| `carousel` / `image-slider` | スライド操作 |
| `search-box`（ファイル/地図タブ等） | 一部の補助動作 |

代替手段が確立している場合はネイティブ要素を優先する。

- 開閉 → `<details>` / `<summary>`（`disclosure` の CSS は使わず独自に最小スタイル）
- モーダル → `<dialog>` + `showModal()`

## 各コンポーネントの最小マークアップ

### Heading

```html
<hgroup class="dads-heading" data-size="36">
  <p class="dads-heading__shoulder">ショルダーテキスト</p>
  <h2 class="dads-heading__heading">見出しテキスト</h2>
</hgroup>
```

`data-size` は `16` / `18` / `20` / `24` / `28` / `32` / `36` / `45` / `57` / `64`。`data-chip` で肩のラベルをチップ表示にする。

### Button

```html
<button class="dads-button" data-type="solid-fill" data-size="lg">予約を確定する</button>
<a class="dads-button" data-type="outline" data-size="md" href="/back">戻る</a>
```

`data-type`: `solid-fill`（主アクション）/ `outline`（副次）/ `text`。`data-size`: `lg` / `md` / `sm` / `xs`。
`solid-fill` は 1 画面に 1 つを原則とする。無効化は `disabled` または `aria-disabled="true"`。

### フォーム（ラベル + 入力 + エラー）

```html
<div class="dads-form-control-label" data-size="md">
  <label class="dads-form-control-label__label" for="patient-name">
    お名前
    <span class="dads-form-control-label__requirement" data-required="true">※必須</span>
  </label>
  <p id="patient-name-support" class="dads-form-control-label__support-text">保険証の記載どおりに入力してください。</p>
  <div>
    <span class="dads-input-text">
      <input id="patient-name" class="dads-input-text__input" type="text" data-size="md"
             aria-invalid="true" aria-describedby="patient-name-error patient-name-support">
      <span id="patient-name-error" class="dads-input-text__error-text">＊お名前を入力してください。</span>
    </span>
  </div>
</div>
```

- `aria-describedby` にはサポートテキストとエラーテキストの ID を両方並べる（読み上げ順 = 記述順）。
- エラーは「色 + テキスト + アイコン」で示す。色だけで伝えない。
- 必須は `data-required="true"`。任意項目には任意であることを明示する。

### Select / Checkbox / Radio / Textarea

```html
<span class="dads-select">
  <span class="dads-select__control">
    <select class="dads-select__select" data-size="md" aria-describedby="dept-error">
      <option value="">選択してください</option>
      <option value="internal">内科</option>
    </select>
    <svg class="dads-select__chevron" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 17L3 8L4 7L12 15L20 7L21 8L12 17Z" fill="currentcolor"/>
    </svg>
  </span>
  <span id="dept-error" class="dads-select__error-text">＊診療科を選択してください。</span>
</span>

<label class="dads-checkbox" data-size="md">
  <span class="dads-checkbox__checkbox">
    <input class="dads-checkbox__input" type="checkbox">
  </span>
  <span class="dads-checkbox__label">初めて受診します</span>
</label>

<label class="dads-radio" data-size="md">
  <span class="dads-radio__radio">
    <input class="dads-radio__input" type="radio" name="visit-type">
  </span>
  <span class="dads-radio__label">再診</span>
</label>

<span class="dads-textarea">
  <textarea class="dads-textarea__textarea" data-size="md" aria-describedby="symptom-error"></textarea>
  <span id="symptom-error" class="dads-textarea__error-text">＊症状を入力してください。</span>
</span>
```

チェックボックス群・ラジオ群は `<fieldset>` + `<legend>` でまとめ、`dads-form-control-label` を付ける。

### Breadcrumb

```html
<nav class="dads-breadcrumb" aria-labelledby="breadcrumb-label">
  <span id="breadcrumb-label" class="dads-u-visually-hidden">現在位置</span>
  <p class="dads-breadcrumb__list">
    <span class="dads-breadcrumb__item">
      <a class="dads-breadcrumb__link" href="/">ホーム</a>
      <span class="dads-breadcrumb__separator">
        <svg class="dads-breadcrumb__separator-icon" width="12" height="12" viewBox="0 0 12 12" aria-hidden="true">
          <path d="M4.5 11L4 10.5L8 6.5L4 2.5L4.5 2L9 6.5L4.5 11Z" fill="currentcolor"/>
        </svg>
      </span>
    </span>
    <span class="dads-breadcrumb__item" aria-current="page">Web予約</span>
  </p>
</nav>
```

`aria-current="page"` は現在ページのみ。リンクにしない。

### Step navigation

```html
<ol class="dads-step-navigation" data-orientation="horizontal" data-size="normal">
  <li class="dads-step-navigation__step" data-state="completed">
    <span class="dads-step-navigation__header">
      <span class="dads-step-navigation__number">1</span>
      <span class="dads-step-navigation__state-label">完了</span>
    </span>
    <span class="dads-step-navigation__title">患者情報の入力</span>
  </li>
  <li class="dads-step-navigation__step" data-state="editing" aria-current="step">
    <span class="dads-step-navigation__header">
      <span class="dads-step-navigation__number">2</span>
      <span class="dads-step-navigation__state-label">入力中</span>
    </span>
    <span class="dads-step-navigation__title">日時の選択</span>
  </li>
</ol>
```

`data-state`: `completed` / `reached` / `editing` / `error` / `skipped`。現在ステップに `aria-current="step"`。

### Notice（通知・緊急）

```html
<div class="dads-notification-banner" data-style="standard" data-type="info-1" role="status">
  <h2 class="dads-notification-banner__heading">
    <svg class="dads-notification-banner__icon" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true">…</svg>
    <span class="dads-notification-banner__heading-text">予約受付時間が変更になりました</span>
  </h2>
  <div class="dads-notification-banner__body">
    <p class="dads-notification-banner__timestamp"><time datetime="2026-04-01">2026年4月1日</time></p>
    <p>本文。</p>
  </div>
</div>
```

`data-type`: `info-1` / `info-2` / `warning` / `error` / `success`。緊急時は `dads-emergency-banner` を使い、`role="alert"` を付ける。

### Table

```html
<div class="dads-table">
  <table class="dads-table__table" data-cell-border="bottom">
    <caption class="dads-table__caption">予約可能な診療科と担当医</caption>
    <thead>
      <tr>
        <th scope="col" class="dads-table__col-header">診療科</th>
        <th scope="col" class="dads-table__col-header">担当医</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th scope="row" class="dads-table__row-header">内科</th>
        <td>佐藤 一郎</td>
      </tr>
    </tbody>
  </table>
</div>
```

キャプションを表の外に出す場合は `<figure class="dads-table"><figcaption class="dads-table__caption">…</figcaption><table class="dads-table__table" data-cell-border="bottom">` とする。

`data-size="dense"`（管理画面向け）、`data-cell-border="bottom"`（行の罫線）、`data-border="hidden"`、`data-width="full"`、`data-layout="fixed"`。

### Card / List / Description list

`dads-card` という単一コンポーネントはなく、**6 種類の作例**（`dads-card-example-1` 〜 `dads-card-example-6`）が `assets/components/card.css` に含まれる。作例ごとに構造が異なるため、近い作例の CSS を選び、`dads-card-example-N` のクラス名とマークアップの組を**そのまま**使う。

| 作例 | 構造の特徴 |
| --- | --- |
| 1 | カード全体が 1 つのリンク。メイン領域の角を丸める |
| 2 | ヘッダー + リンク付きタイトル + フッター |
| 3 | 画像 + 見出し + 本文 + アクション |
| 4 | 横並び（画像 + テキスト） |
| 5 | リスト形式 |
| 6 | チェックボックス付き選択カード |

```html
<ul class="dads-card-example-1-list">
  <li>
    <a class="dads-card-example-1" href="/departments">
      <div class="dads-card-example-1__image" aria-hidden="true">…</div>
      <div class="dads-card-example-1__body">
        <p class="dads-card-example-1__title">診療科から選ぶ</p>
        <p class="dads-card-example-1__text">診療科ごとに担当医と予約枠を確認できます。</p>
      </div>
    </a>
  </li>
</ul>
```

正確なクラス名は `assets/components/card.css` の該当作例を参照する。

```html
<ul class="dads-list">
  <li>診療時間は平日 9:00〜17:00 です。</li>
</ul>

<dl class="dads-description-list">
  <dt>診察日時</dt>
  <dd>2026年4月10日（金）10:00</dd>
</dl>
```

`dads-list` はリスト全体に付ける単一クラス（`data-marker="number"` で番号付き、`data-spacing="4|8|12"`）。`dads-description-list` も同様に単一クラスで、`dt` / `dd` のスタイルは要素セレクタで当たる。子要素にクラスを足さない。

### Search box / Utility link / Page navigation / Divider

```html
<div class="dads-search-box" data-size="md"> … </div>
<a class="dads-utility-link" href="#main">本文へ</a>
<div class="dads-divider" data-style="solid" data-width="1" data-color="solid-gray-420"></div>
```

`dads-divider` は `data-style="solid|dashed"` / `data-width="1|2|3|4"` / `data-color="black|solid-gray-420|solid-gray-536"`。
`dads-utility-link` はヘッダー右上などに置く小さなリンク。`dads-page-navigation` は前後ページへの遷移。

## 規約

- 1 画面 1 つの主要アクション（`solid-fill`）。副次アクションは `outline`、補助は `text`。
- 操作要素は **44×44 CSS px 以上**（`lg` はこれを満たす。`xs` / `sm` を主要操作に使わない）。
- 状態は `aria-*` と `data-*` の両方で表現する（例: 無効 = `disabled`、現在 = `aria-current`）。
- アイコンは `assets/icons/*.svg`。`fill` は `currentColor` なので文字色を継承する。
- 公式実装にないクラスを足す場合は `dads-` 接頭辞を付けず、レイアウト調整用の小さいユーティリティに限定する。
