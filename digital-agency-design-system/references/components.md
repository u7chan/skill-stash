# コンポーネント

公式コードスニペット（`digital-go-jp/design-system-example-components-html`、MIT License）の CSS を `assets/components/` に同梱している。クラス名・`data-*` 属性は公式実装の契約であり、**独自のクラス名に置き換えない**。

`card` と `switch` は同名の CSS を持たないため、`card-example-N.css` / `switch-mode.css` / `switch-on-off.css` として同梱している。`<name>.css` を探しても見つからない場合は下の一覧を見る。

読み込み順: `assets/dads-tokens.css` → `assets/dads-global.css` → 必要な `assets/components/*.css`。

```html
<link rel="stylesheet" href="assets/dads-tokens.css">
<link rel="stylesheet" href="assets/dads-global.css">
<link rel="stylesheet" href="assets/components/form-control-label.css">
<link rel="stylesheet" href="assets/components/input-text.css">
<link rel="stylesheet" href="assets/components/button.css">
```

## 同梱しているコンポーネント CSS

48 ファイル。すべて公式リポジトリの `src/components/<dir>/<file>.css` と**バイト単位で一致**している（検証方法は `NOTICE.md`）。

```
accordion blockquote breadcrumb button calendar carousel checkbox chip-label
card-example-1 card-example-2 card-example-3 card-example-4 card-example-5 card-example-6
date-picker description-list disclosure divider drawer emergency-banner file-upload
form-control-label hamburger-menu-button heading horizontal-menu image input-text
language-selector link list menu-list menu-list-box modal-dialog notification-banner
page-navigation progress-indicator radio resource-list search-box select step-navigation
switch-mode switch-on-off tab table textarea toc utility-link
```

`card` と `switch` は単一の `<name>.css` を持たないため、公式の内訳どおり複数ファイルで同梱している。

| 同梱ファイル | クラスの接頭辞 | 用途 |
| --- | --- | --- |
| `card-example-1.css` 〜 `card-example-6.css` | `.dads-card-example-N` | カードの 6 作例（構造は作例ごとに異なる） |
| `switch-on-off.css` | `.dads-switch-on-off` | ON/OFF スイッチ |
| `switch-mode.css` | `.dads-switch-mode` | モード切替スイッチ |

### JavaScript が必要なコンポーネント

CSS だけでは動作しない。静的な HTML で再現する場合は**使わないか、公式の JS を読み込む**。見た目だけ真似て壊れた操作を作らない。

| 同梱 CSS | 必要な実装 |
| --- | --- |
| `accordion.css` / `disclosure.css` | 開閉（`<details>` でも代替可） |
| `tab.css` | タブ切替（`role="tablist"` + キーボード操作） |
| `switch-on-off.css` / `switch-mode.css` | トグル |
| `modal-dialog.css` / `drawer.css` | `showModal()` とフォーカストラップ |
| `calendar.css` / `date-picker.css` | 日付選択 |
| `menu-list-box.css` | 候補の絞り込み・選択 |
| `carousel.css` | スライド操作 |
| `file-upload.css` | ファイル選択 UI の連動 |
| `hamburger-menu-button.css` | メニューの開閉 |
| `search-box.css` | 検索対象の切替など一部の補助動作 |

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

Select は `dads-form-control-label` と組にする（`for` + `id`）。Checkbox / Radio は公式どおり **`<label>` で入力要素を内包する**形でよい。

```html
<div class="dads-form-control-label" data-size="md">
  <label class="dads-form-control-label__label" for="department">診療科</label>
  <div>
    <span class="dads-select">
      <span class="dads-select__control">
        <select id="department" name="department" class="dads-select__select" data-size="md" aria-describedby="department-error">
          <option value="">選択してください</option>
          <option value="internal">内科</option>
        </select>
        <svg class="dads-select__chevron" width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M12 17L3 8L4 7L12 15L20 7L21 8L12 17Z" fill="currentcolor"/>
        </svg>
      </span>
      <span id="department-error" class="dads-select__error-text">＊診療科を選択してください。</span>
    </span>
  </div>
</div>

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

<div class="dads-form-control-label" data-size="md">
  <label class="dads-form-control-label__label" for="symptom">症状</label>
  <div>
    <span class="dads-textarea">
      <textarea id="symptom" class="dads-textarea__textarea" data-size="md" aria-describedby="symptom-error"></textarea>
      <span id="symptom-error" class="dads-textarea__error-text">＊症状を入力してください。</span>
    </span>
  </div>
</div>
```

Select / Textarea / Input text は「`dads-form-control-label` の `for` と入力要素の `id`」で結ぶ。Checkbox / Radio は `<label>` で内包する公式形でよい。

チェックボックス群・ラジオ群は `<fieldset>` + `<legend>` でまとめ、`dads-form-control-label` を付ける。

### Switch

カスタム要素（`<dads-switch-on-off>`）と公式 JS の組で使う。`role="switch"` は自分で書かず、公式 JS が付与する属性も含めて公式マークアップをそのまま使う。

```html
<dads-switch-on-off class="dads-switch-on-off">
  <button id="notify-switch" class="dads-switch-on-off__button" type="button" role="switch"
          aria-checked="false" aria-labelledby="notify-label" data-js-toggle>
    <span class="dads-switch-on-off__track" aria-hidden="true">
      <span class="dads-switch-on-off__thumb">
        <svg class="dads-switch-on-off__icon" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true">
          <path d="m10.4 16.3-4.1-4.1 1.2-1.3 2.9 2.9 6-6.1 1.3 1.2z" fill="currentcolor"/>
        </svg>
      </span>
    </span>
  </button>
</dads-switch-on-off>
```

2 択のモード切替は `switch-mode.css`（`.dads-switch-mode`）。ON/OFF の 2 値なら `switch-on-off.css`。JS がないと切替できないため、静的なページではチェックボックスとラベルで代替する。

### Breadcrumb

```html
<nav class="dads-breadcrumb" aria-labelledby="breadcrumb-label">
  <span id="breadcrumb-label" class="dads-breadcrumb__label">現在位置</span>
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

`dads-breadcrumb__label` は CSS の `::after` で「：」を補う。ラベルを視覚的に出したくない場合のみ `dads-u-visually-hidden` に差し替える（`aria-labelledby` は維持する）。

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
    <svg class="dads-notification-banner__icon" width="24" height="24" viewBox="0 0 24 24" role="img" aria-label="インフォメーション">…</svg>
    <span class="dads-notification-banner__heading-text">予約受付時間が変更になりました</span>
  </h2>
  <div class="dads-notification-banner__body">
    <p class="dads-notification-banner__timestamp"><time datetime="2026-04-01">2026年4月1日</time></p>
    <p>本文。</p>
  </div>
</div>
```

`data-type`: `info-1` / `info-2` / `warning` / `error` / `success`。

種別アイコン（info / warning / error / success）は**種別情報を単独で伝えるため `role="img"` + `aria-label` を付ける**。ラベル併記の装飾アイコンとは扱いが違う（`references/foundations.md` 参照）。

緊急時は `dads-emergency-banner` を使い、`role="alert"` を付ける。

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

`dads-card` という単一コンポーネントは存在せず、公式実装も `card.css` を持たない。**6 種類の作例**が `assets/components/card-example-1.css` 〜 `card-example-6.css` として別々に同梱されている。作例ごとに構造もクラス名も違うため、**使う作例を 1 つ選び、そのマークアップと CSS を組でそのまま使う**。

| CSS | クラス接頭辞 | 構造 |
| --- | --- | --- |
| `card-example-1.css` | `.dads-card-example-1` | カード全体が 1 リンク。`__image`（アイコン面）+ `__main`（見出し + 本文） |
| `card-example-2.css` | `.dads-card-example-2` | `__main-header`（見出し + メニュー）+ 本文 + `__links` |
| `card-example-3.css` | `.dads-card-example-3` | タイトルリンク + `__label` + `__avatar` の記事カード |
| `card-example-4.css` | `.dads-card-example-4` | 見出し + `__function` + `__contents` + `__actions` の機能カード |
| `card-example-5.css` | `.dads-card-example-5` | 画像 + 日付ラベル + `__label` のニュース・イベントカード |
| `card-example-6.css` | `.dads-card-example-6` | チェックボックス付きの選択カード（表内の複数選択に使う） |

作例 1 の最小形（公式 `example-1.html` より）:

```html
<ul class="dads-card-example-1-list">
  <li>
    <a class="dads-card-example-1" href="/departments">
      <div class="dads-card-example-1__image">
        <svg width="64" height="64" viewBox="0 0 64 64" fill="none" aria-hidden="true">…</svg>
      </div>
      <div class="dads-card-example-1__main">
        <h2>診療科から選ぶ</h2>
        <p>診療科ごとに担当医と予約枠を確認できます</p>
      </div>
    </a>
  </li>
</ul>
```

見出しは作例内の `<h2>` に直接入れる（`dads-card-example-1__title` のようなクラスは存在しない）。正確なクラスは使う作例の CSS を読んで確かめる。

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
- アイコンは `assets/icons/*.svg`。色の制御方法は `references/foundations.md` を参照。
- 公式実装にないクラスを足す場合は `dads-` 接頭辞を付けず、レイアウト調整用の小さいユーティリティに限定する。
