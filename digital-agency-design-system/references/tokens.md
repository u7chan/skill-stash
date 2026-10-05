# デザイントークン

出典: `@digital-go-jp/design-tokens` v2.0.1（`assets/dads-tokens.css` に同梱、MIT License）。
数値はすべて `assets/dads-tokens.css` の CSS カスタムプロパティが正であり、この文書はその一覧と使い分けの要約です。

## 色

### プリミティブカラー（基盤色）

50〜1200 の 13 階調。1200 が最も暗い。**原則として直接使わず**、キーカラー・セマンティックカラー・ニュートラルカラーを経由して使う。

| 色相 | 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 1000 | 1100 | 1200 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **blue** | `#e8f1fe` | `#d9e6ff` | `#c5d7fb` | `#9db7f9` | `#7096f8` | `#4979f5` | `#3460fb` | `#264af4` | `#0031d8` | `#0017c1` | `#00118f` | `#000071` | `#000060` |
| **light-blue** | `#f0f9ff` | `#dcf0ff` | `#c0e4ff` | `#97d3ff` | `#57b8ff` | `#39abff` | `#008bf2` | `#0877d7` | `#0066be` | `#0055ad` | `#00428c` | `#00316a` | `#00234b` |
| **cyan** | `#e9f7f9` | `#c8f8ff` | `#99f2ff` | `#79e2f2` | `#2bc8e4` | `#01b7d6` | `#00a3bf` | `#008da6` | `#008299` | `#006f83` | `#006173` | `#004c59` | `#003741` |
| **green** | `#e6f5ec` | `#c2e5d1` | `#9bd4b5` | `#71c598` | `#51b883` | `#2cac6e` | `#259d63` | `#1d8b56` | `#197a4b` | `#115a36` | `#0c472a` | `#08351f` | `#032213` |
| **lime** | `#ebfad9` | `#d0f5a2` | `#c0f354` | `#ade830` | `#9ddd15` | `#8cc80c` | `#7eb40d` | `#6fa104` | `#618e00` | `#507500` | `#3e5a00` | `#2c4100` | `#1e2d00` |
| **yellow** | `#fbf5e0` | `#fff0b3` | `#ffe380` | `#ffd43d` | `#ffc700` | `#ebb700` | `#d2a400` | `#b78f00` | `#a58000` | `#927200` | `#806300` | `#6e5600` | `#604b00` |
| **orange** | `#ffeee2` | `#ffdfca` | `#ffc199` | `#ffa66d` | `#ff8d44` | `#ff7628` | `#fb5b01` | `#e25100` | `#c74700` | `#ac3e00` | `#8b3200` | `#6d2700` | `#541e00` |
| **red** | `#fdeeee` | `#ffdada` | `#ffbbbb` | `#ff9696` | `#ff7171` | `#ff5454` | `#fe3939` | `#fa0000` | `#ec0000` | `#ce0000` | `#a90000` | `#850000` | `#620000` |
| **magenta** | `#f3e5f4` | `#ffd0ff` | `#ffaeff` | `#ff8eff` | `#f661f6` | `#f137f1` | `#db00db` | `#c000c0` | `#aa00aa` | `#8b008b` | `#6c006c` | `#500050` | `#3b003b` |
| **purple** | `#f1eafa` | `#ecddff` | `#ddc2ff` | `#cda6ff` | `#bb87ff` | `#a565f8` | `#8843e1` | `#6f23d0` | `#5c10be` | `#5109ad` | `#41048e` | `#30016c` | `#21004b` |

### ニュートラルカラー（共通カラー）

| トークン | 値 | 用途の目安 |
| --- | --- | --- |
| `--color-neutral-white` | `#ffffff` | 既定の背景 |
| `--color-neutral-black` | `#000000` | フォーカスリング、最も強い文字色 |
| `--color-neutral-solid-gray-50` | `#f2f2f2` | 淡い面 |
| `--color-neutral-solid-gray-100` | `#e6e6e6` | 淡い面、無効時の面 |
| `--color-neutral-solid-gray-200` | `#cccccc` | 淡い境界線 |
| `--color-neutral-solid-gray-300` | `#b3b3b3` | 無効時の面 |
| `--color-neutral-solid-gray-400` | `#999999` | 弱い文字（大きい文字のみ） |
| `--color-neutral-solid-gray-420` | `#949494` | 白背景でコントラスト比 3:1 を満たす下限（非テキスト） |
| `--color-neutral-solid-gray-500` | `#7f7f7f` | 弱い文字 |
| `--color-neutral-solid-gray-536` | `#767676` | 白背景でコントラスト比 4.5:1 を満たす下限（テキスト） |
| `--color-neutral-solid-gray-600` | `#666666` | 罫線、補助文字 |
| `--color-neutral-solid-gray-700` | `#4d4d4d` | 本文に近い補助文字 |
| `--color-neutral-solid-gray-800` | `#333333` | 既定の本文色 |
| `--color-neutral-solid-gray-900` | `#1a1a1a` | 見出し、強い文字 |

`--color-neutral-opacity-gray-50` 〜 `-900` は同じ階調の透過版（`rgba(0, 0, 0, 0.05)` 〜 `0.9`）。面の重なりを表現したいときだけ使う。

### キーカラー（ブランド色）

`--color-key-50` 〜 `--color-key-1200`。既定では `blue` の各階調を参照する。サイトのトーン＆マナーに合わせて別の色相へ差し替えてよいが、**差し替えるのは `dads-tokens.css` の `--color-key-*` の定義だけ**に留める。

| 用途 | トークン |
| --- | --- |
| 塗りボタンの既定面 | `--color-key-900` |
| 塗りボタンの hover | `--color-key-1000` |
| 塗りボタンの active | `--color-key-1200` |
| アウトラインボタンの hover 面 | `--color-key-200` |
| アウトラインボタンの active 面 | `--color-key-300` |

### セマンティックカラー

| トークン | 参照先 | 意味 |
| --- | --- | --- |
| `--color-semantic-success-1` | green-600 | 成功・完了（明） |
| `--color-semantic-success-2` | green-800 | 成功・完了（暗、テキスト向け） |
| `--color-semantic-error-1` | red-800 | エラー・危険（明） |
| `--color-semantic-error-2` | red-900 | エラー・危険（暗、テキスト向け） |
| `--color-semantic-warning-yellow-1` | yellow-700 | 警告（黄） |
| `--color-semantic-warning-yellow-2` | yellow-900 | 警告（黄、暗） |
| `--color-semantic-warning-orange-1` | orange-600 | 警告（橙） |
| `--color-semantic-warning-orange-2` | orange-800 | 警告（橙、暗） |

### 機能カラー（トークン化されていない固定値）

DADS のリンク色・フォーカス色は `dads-tokens.css` にトークンがないため、`dads-global.css` に直接埋め込まれている。値と使い分けは以下で固定する。

| 状態 | 色 | 実装 |
| --- | --- | --- |
| リンク既定 | `--color-primitive-blue-1000` | `:where(a):any-link` |
| リンク hover | `--color-primitive-blue-900` + 下線 3/16rem | `@media (hover: hover)` |
| リンク active | `--color-primitive-orange-800` | `:where(a):active` |
| リンク visited | `--color-primitive-magenta-900` | `:where(a):visited` |
| フォーカスリング | 外周 `--color-neutral-black` 4px / 内側 `--color-primitive-yellow-300` 2px | `:focus-visible` |

フォーカスインジケーターの「Yellow-300 + Black の 2 重構造」は**変更禁止**。

### コントラスト比の下限

- テキスト: 背景に対して **4.5:1 以上**
- 非テキスト（アイコン・枠線・ディバイダー）: 隣接する背景に対して **3:1 以上**
- 白背景のときの境界は `--color-neutral-solid-gray-536`（4.5:1）と `--color-neutral-solid-gray-420`（3:1）
- 黒背景のときの境界は `--color-neutral-solid-gray-536`（4.5:1）と `--color-neutral-solid-gray-600`（3:1）

## タイポグラフィ

フォントは **Noto Sans JP**（本文・見出し）と **Noto Sans Mono**（コード）。太さは N=`400` / B=`700` の 2 段のみ。

トークン名は `<種別>-<サイズ><太さ>-<行高>` の形式（例: `Std-17N-170`）。CSS では `dads-u-<種別>-<サイズ><太さ>-<行高>` ユーティリティクラスとして `dads-global.css` に定義済み。

### 種別

| 種別 | 記号 | 用途 |
| --- | --- | --- |
| Display | Dsp | ヘッドコピーなど視覚的インパクトが必要な大見出し |
| Standard | Std | 通常の見出し・本文（既定） |
| Dense | Dns | 管理画面・業務システムで情報量を優先する |
| Oneline | Oln | ボタンなど 1 行前提の UI テキスト |
| Mono | Mono | コード・等幅 |

### サイズ・行高

| トークン | size | 行高 | letter-spacing |
| --- | --- | --- | --- |
| `Dsp-64B-140` / `Dsp-64N-140` | 64px | 140% | 0 |
| `Dsp-57B-140` / `Dsp-57N-140` | 57px | 140% | 0 |
| `Dsp-48B-140` / `Dsp-48N-140` | 48px | 140% | 0 |
| `Std-45B-140` / `Std-45N-140` | 45px | 140% | 0 |
| `Std-36B-140` / `Std-36N-140` | 36px | 140% | 0.01em |
| `Std-32B-150` / `Std-32N-150` | 32px | 150% | 0.01em |
| `Std-28B-150` / `Std-28N-150` | 28px | 150% | 0.01em |
| `Std-26B-150` / `Std-26N-150` | 26px | 150% | 0.02em |
| `Std-24B-150` / `Std-24N-150` | 24px | 150% | 0.02em |
| `Std-22B-150` / `Std-22N-150` | 22px | 150% | 0.02em |
| `Std-20B-150` / `Std-20N-150` | 20px | 150% | 0.02em |
| `Std-18B-160` / `Std-18N-160` | 18px | 160% | 0.02em |
| `Std-17B-170` / `Std-17N-170` | 17px | 170% | 0.02em |
| `Std-16B-170` / `Std-16N-170` | 16px | 170% | 0.02em |
| `Std-16B-175` / `Std-16N-175` | 16px | 175% | 0.02em |
| `Dns-17B-130` / `Dns-17N-130` | 17px | 130% | 0 |
| `Dns-17B-120` / `Dns-17N-120` | 17px | 120% | 0 |
| `Dns-16B-130` / `Dns-16N-130` | 16px | 130% | 0 |
| `Dns-16B-120` / `Dns-16N-120` | 16px | 120% | 0 |
| `Dns-14B-130` / `Dns-14N-130` | 14px | 130% | 0 |
| `Dns-14B-120` / `Dns-14N-120` | 14px | 120% | 0 |
| `Oln-17B-100` / `Oln-17N-100` | 17px | 100% | 0.02em |
| `Oln-16B-100` / `Oln-16N-100` | 16px | 100% | 0.02em |
| `Oln-14B-100` / `Oln-14N-100` | 14px | 100% | 0.02em |
| `Mono-17B-150` / `Mono-17N-150` | 17px | 150% | 0 |
| `Mono-16B-150` / `Mono-16N-150` | 16px | 150% | 0 |
| `Mono-14B-150` / `Mono-14N-150` | 14px | 150% | 0 |

制約:

- **本文・UI は 16 CSS px 以上**が基準。14px はフッターなど付随情報か、領域制約がある場合のみ。**14px 未満は原則禁止**。
- 行高は本文で 150% 以上。見出しはサイズが大きいほど行高を狭める。
- `line-height` は単位なしの数値で書く（`1.7`。`170%` と書かない）。

### フォント関連トークン

| トークン | 値 |
| --- | --- |
| `--font-family-sans` | `'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif` |
| `--font-family-mono` | `'Noto Sans Mono', monospace` |
| `--font-weight-400` | `400` |
| `--font-weight-700` | `700` |
| `--font-size-14` 〜 `--font-size-64` | `0.875rem` 〜 `4rem`（14/16/17/18/20/22/24/26/28/32/36/45/48/57/64） |
| `--line-height-100` 〜 `--line-height-175` | `1` / `1.2` / `1.3` / `1.4` / `1.5` / `1.6` / `1.7` / `1.75` |

## 角の形状（border-radius）

| トークン | 値 | 目安 |
| --- | --- | --- |
| `--border-radius-4` | `0.25rem` | 小さなチップ・入力欄など |
| `--border-radius-6` | `0.375rem` | |
| `--border-radius-8` | `0.5rem` | 角丸スモール |
| `--border-radius-12` | `0.75rem` | 横長の角丸ミディアム |
| `--border-radius-16` | `1rem` | 正方形の角丸ミディアム / 横長の角丸ラージ |
| `--border-radius-24` | `1.5rem` | |
| `--border-radius-32` | `2rem` | 角丸ラージ |
| `--border-radius-full` | `624.9375rem` | 角丸フル（ピル形状） |

同じ半径でも図形が小さいほど丸く見える。コンポーネントの縦横比に応じて調整する。

## エレベーション

| トークン | 影 |
| --- | --- |
| `--elevation-1` | `0 2px 8px 1px rgba(0,0,0,0.1), 0 1px 5px 0 rgba(0,0,0,0.3)` |
| `--elevation-2` | `0 2px 12px 2px rgba(0,0,0,0.1), 0 1px 6px 0 rgba(0,0,0,0.3)` |
| `--elevation-3` | `0 4px 16px 3px rgba(0,0,0,0.1), 0 1px 6px 0 rgba(0,0,0,0.3)` |
| `--elevation-4` | `0 6px 20px 4px rgba(0,0,0,0.1), 0 2px 6px 0 rgba(0,0,0,0.3)` |
| `--elevation-5` | `0 8px 24px 5px rgba(0,0,0,0.1), 0 2px 10px 0 rgba(0,0,0,0.3)` |
| `--elevation-6` | `0 10px 30px 6px rgba(0,0,0,0.1), 0 3px 12px 0 rgba(0,0,0,0.3)` |
| `--elevation-7` | `0 12px 36px 7px rgba(0,0,0,0.1), 0 3px 14px 0 rgba(0,0,0,0.3)` |
| `--elevation-8` | `0 14px 40px 7px rgba(0,0,0,0.1), 0 3px 16px 0 rgba(0,0,0,0.3)` |

**影でコントラスト比を確保してはいけない。** 高さを持つ要素はボーダーを持ち、背景色との間で 3:1 以上を確保する。オーバーレイ要素は、下にある最も高いレベルより 2 段階上に置く。

## 余白

DADS は余白スケールを**トークン化していない**。基準単位 **8 CSS px** を決め、その倍数（例: `8 / 24 / 64`）を 3〜5 段階に絞ってプロジェクト内で統一する。

- 関連の強い要素は小さく、弱い要素は大きく離す。
- 情報の階層が上位なほど周囲の余白を大きく取る。
- 文字位置を揃えるために全角スペース・`&nbsp;`・`text-align: justify` を使わない。
