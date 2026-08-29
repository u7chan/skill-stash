---
name: llm-safe-ui-architecture
description: LLMが生成・変更するUIでデザインの一貫性、安全性、アクセシビリティを保つためのアーキテクチャを設計・レビューするときに使う。特定のCSS手法やフレームワークに依存せず、デザイン上の意思決定をtoken、型、schema、component API、lint、test、CIなどの実行可能な制約へ落とし込み、自由度とescape hatchを意図的に設計する。
---

# LLM-safe UI Architecture

LLMにデザインルールを覚えさせるのではなく、**既に決まっているUI上の意思決定を、誤った表現を選びにくい実行可能な制約へ変換する。**

目的はLLMの自由を最大限奪うことではない。人間・LLMのどちらが実装しても、同じ設計意図へ収束しやすいUIアーキテクチャを作る。

## Core Principles

### Encode decisions, not preferences

すでにデザインシステムとして決まっていることだけを制約へ落とす。

- spacing scale
- semantic color roles
- typography roles
- radius / elevation
- supported variants
- interaction states
- accessibility invariants
- theme behavior

まだ判断が必要なものまで固定しない。

### Prefer intent over raw values

可能なら `16px`、`#f5f5f5` のような値ではなく、`space.large`、`surface.card` のように**用途・意味を表す語彙**を公開する。

raw valueを完全禁止するかはプロジェクトの成熟度に応じて判断する。

### Prefer executable constraints over instructions

機械的に判定できるルールは、Agent instructionsやstyle guideだけに置かない。

優先順位の目安:

1. type / schema / constrained API
2. compiler / static analysis / linter
3. automated test / accessibility test / visual regression
4. CI gate
5. documentation / prompt

文章は意図の説明に使い、守れるルールはツールで守る。

### Preserve semantics and accessibility

visual consistencyのためにsemantic structureやaccessibilityを犠牲にしない。

制約付きprimitiveを導入しても、見出し、landmark、list、button、link、form controlなどの意味を保持できる設計にする。

### Keep escape hatches explicit

現実のUIには例外がある。

escape hatchを完全に消して複雑な迂回を生むより、**局所的・明示的・検索可能・レビュー可能な例外経路**を用意する。

詳細は [references/constraint-model.md](references/constraint-model.md) を参照する。

## Workflow

### 1. Inspect

変更前に現在のUI実装を調べる。

- design token / theme
- UI primitive / component library
- raw styling APIと任意値の利用箇所
- component variants
- semantic HTML / accessibility conventions
- responsive / interaction state表現
- lint / static analysis / tests / CI
- Agent instructions / design documentation
- 実際に発生しているUI driftやレビュー指摘

特定技術への移行を前提にしない。

### 2. Identify design invariants

ルールを次の3つに分ける。

- **Invariant**: 破るとプロダクトの一貫性・安全性・accessibilityを損なう。機械的制約の候補
- **Guided choice**: 候補は絞れるが、文脈による判断が残る
- **Free choice**: 現時点では制約する根拠がない

`Invariant` を中心に設計する。LLM対策という理由だけで `Guided choice` や `Free choice` を固定しない。

### 3. Choose the enforcement boundary

Invariantごとに、最も自然な境界で制約する。

- visual vocabulary → semantic token / constrained value set
- component variants → typed or schema-validated API
- composition rule → component API / static rule
- forbidden escape path → lint / static analysis
- theme behavior → semantic token resolution
- accessibility → semantic primitive / automated test
- regression-sensitive appearance → visual regression
- repository-wide rule → CI gate

実装例は [references/enforcement-patterns.md](references/enforcement-patterns.md) を参照する。

### 4. Apply the smallest coherent change

一度にUI全体を作り直さない。

今回の問題を再発しにくくする最小の制約を追加する。

例:

- arbitrary colorのdriftが問題 → まずsemantic color vocabularyを狭める
- raw layoutの乱立が問題 → まず頻出layout primitiveだけ用意する
- dark mode漏れが問題 → theme差分をcomponent利用側から隠す
- 禁止APIへの回避が問題 → そのescape pathだけ静的検査する

既存システムへの導入は [references/incremental-adoption.md](references/incremental-adoption.md) を参照する。

### 5. Validate the constraint

正常系だけでなく、**誤った実装が実際に拒否されるか**を確認する。

最低限確認する。

- intended usageが過度に冗長でない
- forbidden / invalid usageがtype・lint・test・CIのいずれかで検出される
- semantic HTML / accessibilityが維持される
- responsive / theme / interaction stateが必要な範囲で表現できる
- escape hatchが通常経路より簡単になっていない
- 既存UIに意図しない見た目の差分を作っていない

## Review Mode

UIアーキテクチャをレビューするときは、まずLLM生成コードの見た目ではなく**選択可能な状態空間**を見る。

各問題を次のどれかに分類する。

- **Encoded**: 既に安全なAPI・token・primitiveで表現されている
- **Enforceable**: 機械的に判定できるのに文章ルールに留まっている
- **Judgment required**: 文脈依存なので人間/LLMの判断を残すべき
- **Escape hatch**: 例外経路として意図的に許可されている

同じレビュー指摘が繰り返される場合、プロンプト追加より先に `Enforceable` へ変換できないか検討する。

## Guardrails

禁止する。

- LLM対策だけを理由にフレームワークやCSS技術を移行する
- 全UIを単一の万能primitiveへ押し込む
- semantic HTMLを汎用containerへ置き換える
- design tokenを単なるraw valueの別名にする
- component propsを無制限に増やしてCSS全体を再実装する
- 実際のdriftが確認できないのに大量のlint ruleを追加する
- documentationで十分な判断事項までCI failureにする
- escape hatchを隠し、非公式な回避策を誘発する
- migrationと無関係なvisual redesignを同時に行う

## Completion Report

完了時は簡潔に報告する。

- **Invariants**: 今回制約へ変換した設計判断
- **Enforcement**: type / lint / test / CIなど、どこで強制したか
- **Escape hatches**: 意図的に残した自由度・例外
- **Validation**: valid / invalid usageをどう確認したか
- **Follow-ups**: 今回は制約しなかった候補
