# Enforcement Patterns

制約は「最も強い仕組み」で守ればよいわけではない。**ルールの性質に合う、最小で保守しやすい強制境界を選ぶ。**

## Enforcement Ladder

### Type / schema

有限の選択肢を表現できる場合に向く。

```text
padding: compact | comfortable | spacious
surface: default | raised | interactive
```

向いている:

- token vocabulary
- component variants
- required combinations
- invalid prop combinations

向いていない:

- DOM tree全体の関係
- visual regression
- 文脈依存のdesign judgment

## Static analysis / lint

構文・import・API利用を検査できる場合に向く。

例:

- 特定領域でraw styling APIを禁止
- arbitrary value利用を禁止
- deprecated componentの新規利用を禁止
- escape hatchに理由を要求
- semantic primitiveを迂回する既知のpatternを検出

ruleを追加する前に、実際に繰り返し発生しているdriftか確認する。

## Component API

複数の判断を一つの意味ある操作へ束ねられる場合に向く。

例:

```text
Button(intent="danger")
```

が内部で以下を決める:

- semantic color
- hover / focus / disabled state
- contrast
- typography
- spacing

利用側へ毎回同じ低レベル判断を要求しない。

ただしAPIが増えすぎたら、単にCSSを別構文へ移しただけになっていないか確認する。

## Automated tests

runtime behaviorや複数要素の関係が重要な場合に向く。

候補:

- accessibility test
- keyboard interaction
- required semantics
- state transition
- theme switching

snapshotだけでdesign correctness全体を保証しようとしない。

## Visual regression

コード上は正しいが見た目が壊れる変更の検出に使う。

向いている:

- shared primitive変更
- token変更
- theme変更
- high-risk layout

すべての小さな画面をpixel-perfect gateにすると更新コストが高くなる。重要なsurfaceへ絞る。

## CI

CIは個別ルールの実装場所ではなく、**選んだ検証をrepository-wide contractとして必ず実行する場所**として扱う。

例:

```text
change
  -> typecheck
  -> lint/static rules
  -> accessibility tests
  -> selected visual regression
  -> merge allowed
```

## Documentation / Agent Instructions

以下に使う。

- なぜその制約があるか
- どのAPIを選ぶべきか
- judgmentが必要なケース
- escape hatchの利用条件

機械判定可能な禁止事項を文章だけで守らせない。

## Selecting the Boundary

次の順で考える。

1. 値の集合を狭めれば防げるか → type / schema / token
2. 意味ある操作へまとめられるか → component API
3. 構文や利用経路を検出できるか → lint / static analysis
4. runtime semanticsが必要か → automated test
5. 見た目そのものを比較する必要があるか → visual regression
6. 上記を継続的に実行すべきか → CI
7. 判断が残るか → documentation

## Negative Test

LLM-safeな制約では、正常系だけでなく意図的に誤った例を作って確認する。

例:

- 未許可tokenを指定 → rejectされる
- 禁止APIを使う → lint failure
- accessible nameを欠く → test failure
- theme-specific raw colorを直接指定 → static ruleで検出

「正しいコードが書ける」だけではなく、**繰り返し発生していた誤りが通らなくなったこと**を完了条件にする。
