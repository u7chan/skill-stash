# Language Teacher Skill Skeleton

言語固有の教師スキルを作るときの雛形。

そのまま穴埋めするのではなく、対象言語で本当に重要な概念だけを残す。

## SKILL.md

```md
---
name: <language>-teacher
description: <language>の学習・解説・デバッグ・レビューで使う。構文だけでなく、<主要mental model>を使ってコードの挙動と設計判断を説明する。
---

# <Language> Teacher

<Language>を構文暗記ではなく、挙動を予測できるメンタルモデルから教える。

## Teaching Flow

1. 結論
2. 最小例
3. 何が起きるか
4. なぜそうなるか
5. よくある間違い
6. 実務でどう選ぶか
7. 必要なら深掘り

## Core Mental Models

- <value / reference / ownership model>
- <type system model>
- <error model>
- <abstraction model>
- <concurrency / resource lifecycle model>
- <zero/default/null model>

詳細は `references/mental-models.md`。

## Comparisons

重要な比較では必ず Default / Choose A when / Choose B when を示す。

- <A> vs <B>
- <C> vs <D>

## Error Explanation

1. 何が起きたか
2. なぜ処理系が拒否 / 失敗したか
3. 問題の最小箇所
4. 最小修正
5. idiomaticな改善
6. 再発防止ルール

## Review Mode

- correctness
- language model
- idiom
- lifecycle / concurrency
- error semantics
- simplicity

## Tooling

検証が必要なら `references/tooling.md` の最小コマンドを使う。

## Final Check

- コードの動きを説明できる
- 選択理由を説明できる
- errorを原因モデルから理解できる
- 高度なabstractionを自動的に勧めない
```

## references/mental-models.md

概念ごとに次の形式を使う。

```md
## <Concept>

### Mental model
<一文でどう考えるべきか>

### What actually happens
<代入、引数渡し、型検査、runtime等で何が起きるか>

### Predict
<短いコードを見て結果を予測する問い>

### Common mistake
<他言語から持ち込みやすい誤解>

### Decision rule
<実務上いつどう使うか>
```

## references/patterns.md

カタログ化しすぎない。頻出する比較や誤解だけ置く。

```md
## <A> vs <B>

- Mental model:
- Default:
- Choose A when:
- Choose B when:
- Common mistake:

### Minimal example
<小さなコード>
```

典型的な候補:

- value vs reference/pointer
- mutable vs immutable
- concrete type vs interface/trait/protocol
- exception/error/result型
- sync vs async/concurrent
- collectionの似た型
- allocation / resource ownership

対象言語に存在しない比較は削除する。

## references/tooling.md

コマンド名の羅列ではなく、**何を証明したいときに使うか**を書く。

```md
## Format

Command: `<formatter command>`
Use when: source formattingを標準化する。

## Test

Command: `<test command>`
Use when: behaviorを検証する。

## Static analysis

Command: `<lint/static analysis command>`
Use when: compilerだけでは拾わない疑わしいコードを検査する。

## Concurrency / memory / sanitizer

Command: `<optional command>`
Use when: 対象言語で必要な場合のみ。
```

## Adaptation Checklist

新しい言語へ転用するときは、最低限次を差し替える。

- 言語が最も強く保証するもの
- 初学者が最も誤解しやすい値・型モデル
- エラーの表現と伝播方法
- abstractionの標準的な境界
- concurrency / async / resource lifecycle
- 主要な比較対象
- 公式toolchain

逆に、次は共通骨格として残せる。

- 結論 → 最小例 → mental model の説明順
- 比較時の判断基準
- エラーの原因 → 修正 → 再発防止
- progressive disclosure
- simplicityを優先するreview観点

## Source Notes

このテンプレートの教育設計は、Rustを構文ではなくメンタルモデルから教える `rust-teacher.md` の考え方を出発点に、他言語へ転用できるよう再構成している。

- koutyuke / rust-teacher.md  
  https://gist.github.com/koutyuke/e2a68888bd9db30fa25c05f1bd030112

文面や言語固有の内容を複製するのではなく、教育フローと設計原則だけを抽象化する。
