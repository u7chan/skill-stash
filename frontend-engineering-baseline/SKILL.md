---
name: frontend-engineering-baseline
description: TypeScriptフロントエンドの開発基盤を新規構築・改善・レビューするときに使う。依存関係の安全性、型安全性、静的解析、Git hooks、CI、依存更新、Next.js固有設定を、既存リポジトリを調査したうえで最小限かつ一貫した変更として整える。
---

# Frontend Engineering Baseline

TypeScriptフロントエンドの開発基盤を調査し、安全性・再現性・品質・保守性を継続的に担保できる状態へ整える。

特定のツール構成をテンプレートとして押し付けない。既存リポジトリの実態を優先し、不足している仕組みだけを最小の変更単位で追加する。

## Core Principles

### Inspect before changing

変更前に、最低限以下を確認する。

- `package.json` とlockfile
- package manager / runtimeのversion管理
- `tsconfig.json`
- lint / formatter設定
- test設定
- Git hooks
- `.github/workflows/`
- dependency update設定
- framework設定
- `AGENTS.md` / `CLAUDE.md` 等のAgent instructions
- 実際に利用されているscriptsとCI command

### Prefer repository reality over assumptions

一般的な推奨構成より、現在のコード・設定・運用を優先する。

既存の選択に明確な問題がなければ、新しいという理由だけで別ツールへ置き換えない。

### Prefer enforcement over reminders

機械的に判定できる品質条件は、Agent instructionsに文章として書くだけで済ませず、可能ならcompiler、linter、formatter、static analysis、tests、CI、dependency policyで自動検証する。

### Apply the smallest coherent change

一度にリポジトリ全体をmodernizeしない。

今回成立させたいことに必要な変更だけを行い、dependency、script、configuration、CI、documentationを一貫して更新する。関連しないmigrationやrefactoringは混ぜない。

### Verify volatile information

framework behavior、package version、configuration syntax、package manager feature、CI Action versionは変化する前提で扱う。

version-specificな判断が必要な場合は、現在のrepository versionと公式情報を確認する。

## Workflow

### 1. Inspect

現在のengineering baselineを次の観点で把握する。

- dependency management
- runtime reproducibility
- type safety
- lint / format
- unused code detection
- tests
- Git hooks
- CI
- dependency updates
- framework-specific conventions

### 2. Identify gaps

発見事項を次の3種類に分類する。この分類を変更スコープ判断の正とする。

- **Required now**: 今回の目的を成立させるために必要。correctness、security、reproducibility、CI reliabilityの明確な問題を含む
- **Useful follow-up**: 改善価値はあるが、今回の完了条件には不要
- **Optional**: 好み、チーム運用、規模、将来構想によって判断が変わる

今回実装するのは原則 `Required now` のみとする。`Useful follow-up` と `Optional` は、ユーザーが明示的に今回のスコープへ含めた場合を除き実装せず、必要ならfollow-upとして報告する。

### 3. Define scope

変更対象ごとに以下を明確にする。

- 解決する問題
- 変更する仕組み
- 完了を確認する方法

複数の独立したmigrationが必要なら、一つの変更にまとめない。

既存リポジトリへ段階導入する場合は [references/incremental-adoption.md](references/incremental-adoption.md) を参照する。

### 4. Apply

関心ごとに対応するreferenceを参照する。

- dependency / supply chain: [references/dependency-security.md](references/dependency-security.md)
- TypeScript / lint / format / dead code: [references/static-quality.md](references/static-quality.md)
- Git hooks / CI / tests: [references/automation-ci.md](references/automation-ci.md)
- Next.js: [references/nextjs.md](references/nextjs.md)

referenceはチェックリストではなく判断材料として使う。すべてを適用する必要はない。

### 5. Validate

既存のvalidation commandがある場合はそれを優先する。

変更内容に応じて以下を確認する。

- dependency installation
- typecheck
- lint
- format check
- static analysis
- tests
- production build
- CI configuration

検証を通すために品質ルールを無効化・緩和しない。問題が出た場合は、ルールが不適切なのかコードに問題があるのかを判断する。

## Completion Report

完了時は以下を簡潔に報告する。

- **Applied**: 今回追加・改善したbaseline
- **Validation**: 実行した検証と結果
- **Not applied**: 検討したが意図的に導入しなかった項目
- **Follow-ups**: 今回の完了条件には不要な将来候補

## Guardrails

禁止する。

- 新しいという理由だけでツールを置換する
- package managerを無断で変更する
- framework migrationを勝手に開始する
- lint ruleを大量に追加する
- unrelated refactoringを含める
- versionを記憶だけで決める
- validationを通すために設定を緩める
- `Useful follow-up` / `Optional` を明示合意なしに実装する
- repository全体のmodernizationを一度に行う
