# Incremental Adoption

LLM-safe UI architectureは全面移行を前提にしない。既存UIで実際に起きているdriftから、小さく導入する。

## Start from Repeated Drift

最初に集める候補:

- code reviewで繰り返される同種の指摘
- arbitrary valueの増殖
- theme対応漏れ
- accessibility regression
- component variantの勝手な追加
- 同じUI patternの微妙な差分
- Agent instructionsに何度書いても再発する違反

一度しか起きていない問題は、すぐarchitecture ruleへ昇格させない。

## Adoption Sequence

### 1. Pick one invariant

例:

- application surfaceの色はsemantic token経由にする
- primary buttonのstate表現はshared componentに集約する
- form controlにはaccessible nameを必須にする

### 2. Define the allowed path

禁止する前に、正しい実装経路を使いやすくする。

- semantic tokenを追加
- constrained primitiveを用意
- component variantを整理
- migration helperを用意

### 3. Migrate a narrow surface

新規コードだけ、特定packageだけ、特定component群だけなど、適用範囲を限定する。

既存コード全体を一度に書き換えない。

### 4. Add enforcement

正しい経路が利用可能になった後で、必要な範囲だけlint / type / test / CIを有効にする。

warning期間を設けるか、new/changed codeだけgateする方法も検討する。

### 5. Observe escape hatches

escape hatch利用箇所は設計のフィードバックとして扱う。

- 同じ理由が複数回出る → vocabulary / primitive不足の可能性
- 一度だけの特殊ケース → 例外として維持
- workaroundが増える → 制約が強すぎる可能性

## Migration Guardrails

避ける:

- LLM向けという理由だけでstyling libraryを変更する
- design system再構築とvisual redesignを同時に行う
- 全componentを一括でprimitive化する
- 既存の正常なUIを「統一」のためだけに変更する
- enforcement導入前に大量のmigrationを行う
- migration完了を先に置き、再発防止の検証を後回しにする

## Completion Criteria

段階導入の一単位は、次を満たせば完了とする。

- 対象Invariantが明確
- 正しい利用経路が存在する
- 対象範囲の既存コードが必要な分だけ移行済み
- 同じ誤りをnegative testで再現し、検出できる
- semantic / accessibility / visual behaviorに意図しない差分がない
- 次のInvariantを今回のPRへ追加していない

改善候補が残っても、今回のInvariantが成立した時点で完了する。
