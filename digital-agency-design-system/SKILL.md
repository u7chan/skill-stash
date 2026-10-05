---
name: digital-agency-design-system
description: デジタル庁デザインシステム（DADS β版）を再現して、行政・公共系のWebページや画面をHTML/CSSで作成・改修・レビューするときに使う。デザイントークン、タイポグラフィ、余白、角丸、エレベーション、公式アイコン素材、UIコンポーネントのマークアップ、WCAG/JISを前提としたアクセシビリティ要件を、同梱アセットだけで再現する。「デジタル庁デザインシステムで作って」「DADSに寄せて」「政府標準のUIで」といった依頼で使う。
---

# デジタル庁デザインシステム（DADS）

デジタル庁デザインシステムβ版（https://design.digital.go.jp/dads/）に準拠した画面を、このスキルのアセットだけで再現する。

「雰囲気が似ている」ではなく、**公式のデザイントークン・公式コンポーネントCSS・公式アイコン素材をそのまま使う**ことが目的。数値や色を目分量で近似しない。

## 同梱アセット

| パス | 内容 | 出典 |
| --- | --- | --- |
| `assets/dads-tokens.css` | デザイントークン（色・書体・サイズ・行高・角丸・エレベーション） | `@digital-go-jp/design-tokens` v2.0.1 |
| `assets/dads-global.css` | リンク、フォーカスリング、テキストスタイルユーティリティ（`dads-u-*`） | `design-system-example-components-html` `src/global.css` |
| `assets/components/*.css` | 公式コンポーネント CSS 42 種 | 同上 |
| `assets/icons/*.svg` | 公式アイコン素材 120 種（24×24、`fill` は `currentColor` に正規化） | デジタル庁「イラストレーション・アイコン素材」 |
| `assets/page-template.html` | ヘッダー / 本文 / フッター / スキップリンク入りの雛形 | — |

```bash
# アイコンを公式ZIPから再取得したいとき（通常は同梱済みで不要）
python3 scripts/setup-icons.py                    # SVGアイコン
python3 scripts/setup-icons.py --illustrations    # イラストPNGも
python3 scripts/setup-icons.py --list             # 収録アイコン一覧
```

## 作業手順

1. **画面の目的と登場要素を決める。** 誰が何をする画面か、必要な部品（フォーム / 表 / カード / 手順表示 / 通知 など）を列挙する。
2. **雛形をコピーする。** `assets/page-template.html` を起点にする。`lang="ja"`・viewport・skin link・スキップリンク・ランドマークは消さない。
3. **使うコンポーネント CSS だけを `<link>` する。** `references/components.md` でクラス名と `data-*` 属性を確認し、**公式のクラス名とマークアップの組をそのまま**使う。
4. **色・サイズ・角丸・影は必ずトークン（`var(--...)`）で書く。** 生の HEX を書かない。`references/tokens.md` に一覧がある。
5. **余白は 8 CSS px 基準で 3〜5 段階に絞る。** 例: `8 / 24 / 64`。要素ごとに思いつきの値を入れない。
6. **アクセシビリティ要件を満たす。** `references/accessibility.md` の「必須」を上から確認する。
7. **機械的に検査する。** `python3 scripts/check-page.py <file>` で ERROR を 0 にする。

## 再現の原則

### トークン以外の色を使わない

```css
/* OK */ .card { background-color: var(--color-neutral-white); border: 1px solid var(--color-neutral-solid-gray-200); }
/* NG  */ .card { background: #f5f5f5; border: 1px solid #ddd; }
```

キーカラーを変えたい場合は、コンポーネントを書き換えず `--color-key-*` の定義（`dads-tokens.css`）だけを差し替える。

### タイポグラフィは `dads-u-*` ユーティリティで当てる

```html
<h1 class="dads-u-std-36B-140">見出し</h1>
<p class="dads-u-std-16N-170">本文</p>
<span class="dads-u-oln-16B-100">ボタンラベル</span>
```

- 本文・UI は **16 CSS px 以上**。14px は付随情報のみ。14px 未満は禁止。
- `line-height` は単位なしの数値で書く。
- 見出しは `dads-heading` コンポーネント、本文は素の `<p>` + ユーティリティを使う。

### アクセシビリティは後付けしない

- フォーカスリング（黒 4px + 黄 2px）は DADS の中核。消さない・弱めない。
- アイコンは必ずラベルと併記する。単体利用は 44×44 CSS px と代替テキストが条件。
- エラーは色だけで示さない。`aria-invalid` + `aria-describedby` を必ず組にする。
- 無効（`disabled`）と `readonly` と `placeholder` は原則使わない。

### アイコンの色

`<img src="assets/icons/xxx.svg">` で読み込んだ SVG の `currentColor` は SVG 自身の `color`（既定は黒）で解決され、**ページの `color` は継承しない**。色を変える場合は `.dads-icon-mask` を使う。

```html
<img class="dads-icon" src="assets/icons/search_line.svg" alt="" width="24" height="24">
<span class="dads-icon-mask" aria-hidden="true" style="--dads-icon-src: url('assets/icons/search_line.svg')"></span>
```

### 公式にないものを作らない

DADS にないコンポーネントが必要な場合は、既存コンポーネントの組み合わせ、またはトークンを使った素の HTML で組む。見た目だけ似せた独自コンポーネント（独自のボタンクラス、独自のフォーカス表現など）を増やさない。

## よくある失敗

| 失敗 | 正しい対応 |
| --- | --- |
| 色を HEX で直書きする | `var(--color-*)` を使う |
| Bootstrap / Tailwind のクラスを混ぜる | `dads-*` クラスに統一する |
| ボタンを `<div>` + `onclick` で作る | `<button>` または `<a>` を使う |
| エラーを赤文字だけで示す | エラーテキスト + アイコン + `aria-describedby` |
| JS が必要なコンポーネント（タブ・モーダル・アコーディオン）を CSS だけで組む | 公式 JS を読むか、`<details>` / `<dialog>` で代替する |
| アイコンを装飾目的で `aria-label` 付きにする | ラベル併記のアイコンは `aria-hidden="true"`（`<img>` は `alt=""`） |
| 固定幅レイアウトにする | 12 カラム + リキッド。ブレークポイントは 768px |
| フォントサイズを 12px にする | 16px 基準。最小でも 14px、それ以下は不可 |

## リファレンス

- `references/tokens.md` — 全トークン（色 / タイポグラフィ / 角丸 / エレベーション / 余白）
- `references/foundations.md` — レイアウト・アイコン・リンク・カラー設計・エレベーションの規則
- `references/components.md` — 同梱コンポーネント一覧、JS 要否、最小マークアップ
- `references/accessibility.md` — 必須のアクセシビリティ要件とチェック手順
- `NOTICE.md` — 出典・ライセンス・同梱バージョン

## 検証

```bash
python3 scripts/check-page.py page.html          # ERROR/WARN を表示
python3 scripts/check-page.py page.html --quiet  # ERROR のみ
python3 scripts/check-page.py page.html --json   # 機械可読
```

ERROR が 1 件でもあれば未完了。WARN は意図的な逸脱かを人が判断する。

機械判定に加えて、次を目視・操作で確認する。

- ブラウザ幅 320px / 768px / 1280px でレイアウトが破綻しない
- 200% ズームで内容が欠けない
- Tab キーだけで全操作要素に到達でき、フォーカスリングが見える
- ブラウザの強制カラーモード（あれば）で境界線が消えない
