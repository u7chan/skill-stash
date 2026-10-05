# 出典・ライセンス

同梱アセットはすべてデジタル庁が公開しているものです。改変内容も併記します。

## デザイントークン

- 出典: [`@digital-go-jp/design-tokens`](https://github.com/digital-go-jp/design-tokens) v2.0.1
- ファイル: `assets/dads-tokens.css`（`dist/tokens.css` をそのまま同梱）
- ライセンス: MIT License（Copyright (c) Digital Agency）
- 改変: なし

## コンポーネント CSS / グローバル CSS

- 出典: [digital-go-jp/design-system-example-components-html](https://github.com/digital-go-jp/design-system-example-components-html) `src/components/*/[name].css` および `src/global.css`
- ファイル: `assets/components/*.css`、`assets/dads-global.css`
- ライセンス: MIT License（Copyright (c) 2025 デジタル庁）
- 改変:
  - `assets/components/*.css` は無改変で同梱。
  - `assets/dads-global.css` は `src/global.css` からデザイントークン定義（`:root` ブロック）を分離し、末尾に公式アイコン用の `.dads-icon` / `.dads-icon-mask` 補助クラスを追加したもの。

## アイコン素材

- 出典: [イラストレーション・アイコン素材｜デジタル庁](https://www.digital.go.jp/policies/servicedesign/designsystem/Illustration_Icons)（配布 ZIP: `designsystem-assets.zip`）
- ファイル: `assets/icons/*.svg`（`designsystem-assets/icon/svg/` の 120 ファイル）
- 規約: [イラストレーション・アイコン素材利用規約](https://www.digital.go.jp/policies/servicedesign/designsystem/Illustration_Icons/terms_of_use)
- 改変: SVG 内の描画色 `#1A1A1C` を `currentColor` に置換（CSS の `color` を継承させるため）。形状は変更していない。
- 同梱ライセンス: `assets/icons-LICENSE.txt`

イラストレーション（`illustration/png/`）はサイズが大きいため同梱せず、`python3 scripts/setup-icons.py --illustrations` で取得する。

## ドキュメント（`references/`、`SKILL.md`）

- 出典: [デジタル庁デザインシステムβ版](https://design.digital.go.jp/dads/) および同サイトの Markdown 一式（2026年9月9日版）
- 内容: 上記ドキュメントの記述を、実装時に必要な規則へ要約・再構成したもの。数値は上記アセットの値を正とする。

## 更新手順

1. `npm pack @digital-go-jp/design-tokens` で最新の `dist/tokens.css` を取得し `assets/dads-tokens.css` を差し替える。
2. `design-system-example-components-html` を clone し、`src/components/*/[name].css` を `assets/components/` へ、`src/global.css` の変更を `assets/dads-global.css` へ反映する。
3. `python3 scripts/setup-icons.py --refresh` でアイコンを再取得する。
4. `references/tokens.md` の数値表と、この文書のバージョン表記を更新する。
