# Constraint Model

LLM-safe UI architectureでは、UIの自由度を一律に減らさない。**すでに決まっている設計判断だけを、適切な層で有限の選択肢へ変換する。**

## Constraint Layers

### 1. Semantic vocabulary

raw valueではなく、意図を表す語彙を優先する。

例:

- `surface.default`
- `surface.elevated`
- `text.muted`
- `space.compact`
- `space.comfortable`
- `radius.control`

`gray.100` や `16px` を禁止すること自体が目的ではない。利用側が「どの値か」ではなく「何の役割か」を選べる状態を作る。

## 2. Constrained primitives

頻出するvisual/layout判断はprimitiveやcomponent APIで表現できる。

ただしprimitiveはCSSの完全なラッパーにしない。

良い方向:

- プロダクトで実際に使うspacingだけ選べる
- 意味のあるvariantだけ公開する
- semantic elementを維持できる
- state / theme behaviorを利用側が毎回再実装しない

避ける:

- CSS propertyを1対1ですべてprops化する
- 一つの万能componentですべてのUIを表現する
- primitiveを使うためにDOM semanticsを壊す

## 3. Composition contracts

個々の値が正しくても、組み合わせが壊れることがある。

例:

- dialog titleには対応するdialog semanticsが必要
- form fieldにはlabel relationが必要
- menu itemはmenu context内でのみ使う
- card actionの配置ルールが決まっている

この種のルールはcomponent composition、schema、static analysis、testsで表現する。

## 4. Theme and state contracts

light/dark、brand theme、hover、focus、disabled、errorなどの差分を、毎回LLMに選ばせない。

可能ならsemantic tokenやcomponent variant側で解決し、利用側は意図だけを指定する。

ただし特殊なstateが多い領域では隠蔽しすぎない。必要な状態遷移がコードから追えることも重要。

## 5. Accessibility contracts

accessibilityは見た目の制約とは別のinvariantとして扱う。

候補:

- semantic elementをデフォルトにする
- interactive elementのrole / keyboard behaviorをcomponent側で担保する
- accessible nameが必要なcomponent APIを設計する
- automated accessibility testを使う

視覚primitiveの統一を理由に `div` 相当へ寄せない。

## Escape Hatch Design

escape hatchは「何でもできる通常API」にしない。

望ましい性質:

- 明示的な名前を持つ
- 通常経路より少し手間がかかる
- repository searchで発見できる
- コメントや理由を要求できる
- lint disableなら対象ruleを局所化する
- 後から利用箇所を集計できる

例外が増えた場合は、利用者を責めるのではなくconstraint modelが現実に合っていない可能性を検討する。

## Avoid Accidental Constraints

以下はInvariantと決めつけない。

- 現在たまたま多いpadding値
- 一つの画面だけで使う特殊layout
- 実装都合で生まれたcomponent boundary
- designerがまだ判断していないresponsive behavior
- performance改善が未検証のstyling technique

LLM-safeは「選択肢が少ないほど良い」ではない。**正しい選択肢だけを狭くし、未決定部分の判断余地は残す。**
