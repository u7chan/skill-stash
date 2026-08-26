---
name: modern-go
description: Goコードを実装・修正・リファクタ・レビューするときに使う。対象モジュールのGoバージョンを基準に、利用可能な言語機能と標準ライブラリのmodern idiomを選び、挙動と互換性を保った最小変更として適用する。
---

# Modern Go

対象プロジェクトが実際に要求するGoバージョンに合わせて、古い慣用表現へ戻らずmodernでidiomaticなGoを書く。

「新しい書き方を使うこと」自体を目的にしない。correctness、behavior compatibility、対象Goバージョン、既存設計を優先する。

## Core Principles

### Resolve the target version first

Goの機能を選ぶ前に、変更対象ファイルへ適用されるGoバージョンを確定する。

優先順位:

1. ユーザーが明示したversion constraint
2. 変更対象を含むmoduleの`go.mod`にある`go` directive
3. workspace構成を確認したうえで対象moduleの`go.mod`
4. projectがversionを宣言していない場合のみlocal toolchain

`toolchain` directiveと`go` directiveを混同しない。言語・標準ライブラリ機能の利用可否は、原則としてmoduleが要求するGo versionを基準に判断する。

複数moduleがあるrepositoryでは、repository rootのversionを一律適用せず、変更対象を所有するmoduleを解決する。

詳細は [references/version-policy.md](references/version-policy.md) を参照する。

### Prefer modern idioms within the allowed version

対象versionで利用可能なら、同じ意図をより直接表現できるlanguage featureやstandard library APIを優先する。

ただし、既存コードが古いという理由だけで周辺まで一括modernizeしない。

### Preserve behavior before style

modernなAPIへの置換で以下が変わる可能性がある場合は、単純置換しない。

- public API
- error matching semantics
- nil / zero-value behavior
- ordering
- allocation / aliasing
- wire format
- concurrency / cancellation behavior
- benchmark semantics

新しいAPIの方が短くても、現在の処理意図を失うなら既存実装を維持する。

### Treat new code and migration differently

新規コードでは対象versionで使えるmodern idiomを最初から選ぶ。

既存コードでは、今回触る範囲に明確に適用できる置換だけを行う。wire behaviorやpublic behaviorが変わり得るmigrationは、ユーザーがmigrationを明示した場合のみ行う。

### Keep modernization scoped

modernization候補を見つけても、今回の目的に不要なら実装しない。

- **Apply now**: 今回触るコードに直接適用でき、挙動を保ったまま明確になる
- **Follow-up**: 価値はあるが独立したmigrationや広い変更になる
- **Skip**: style preferenceだけ、または挙動差分のリスクが利益を上回る

原則として`Apply now`のみ実装する。

## Workflow

### 1. Inspect

変更前に最低限確認する。

- 対象`.go` file
- nearest applicable `go.mod`
- `go.work`の有無
- `go` / `toolchain` directives
- repository固有のAgent instructions
- formatter / linter / test / CI commands

### 2. Load only relevant references

変更内容に応じて必要なreferenceだけ読む。

- version resolution: [references/version-policy.md](references/version-policy.md)
- slices / maps / strings / iteration: [references/collections-and-iteration.md](references/collections-and-iteration.md)
- errors / context / sync / atomic: [references/errors-context-concurrency.md](references/errors-context-concurrency.md)
- types / language features: [references/types-and-language.md](references/types-and-language.md)
- tests / benchmarks: [references/testing-and-benchmarks.md](references/testing-and-benchmarks.md)
- time / fmt / JSON / HTTP: [references/stdlib-and-http.md](references/stdlib-and-http.md)

referenceは全項目を適用するチェックリストではない。

### 3. Evaluate each candidate

各modernization候補について以下を確認する。

1. `Requires`を対象Go versionが満たすか
2. `Use when`が現在の意図に一致するか
3. `Avoid when`に該当しないか
4. observable behaviorが維持されるか
5. 今回の変更スコープに含まれるか

一つでも不明なら、機械的に置換しない。

### 4. Use Go tooling as evidence

local toolchainでmodernization対応の`go fix`が利用可能なら、候補確認に使える。

```sh
go fix -diff ./...
```

小さい変更ではpackage scopeを絞る。

`go fix -diff`の出力は判断材料であり、自動適用命令ではない。提案を採用する前に挙動とscopeを確認する。

`go fix`を使うためだけに`go.mod`のGo versionを上げない。

mutatingな`go fix`は、modernization自体が依頼内容に含まれる場合のみ実行する。

### 5. Validate

repository既存のvalidation commandを優先する。

明示されたものがなければ、変更範囲に応じて最小限を選ぶ。

変更したGoファイルは対象を明示して`gofmt`する。引数なしの`gofmt`はstdinを処理するため、validation commandとして使わない。

```sh
gofmt -w path/to/changed.go
go test ./...
go vet ./...
```

`path/to/changed.go`は実際に変更した`.go`ファイルへ置き換える。複数ある場合は対象を列挙する。

repository全体を触っていない場合は、可能なら対象packageへ絞る。

## Decision Priority

競合する場合は次の順で判断する。

**correctness → behavior compatibility → target Go version → repository constraints → modern Go idiom → stylistic preference**

## Guardrails

禁止する。

- target Go versionを確認せず新APIを使う
- modernizeのためだけに`go` directiveを上げる
- 新しいという理由だけで既存コード全体を書き換える
- `go fix`の提案を無検証で適用する
- exact error identityが必要な処理を無条件に`errors.Is`へ変える
- JSON migration等でwire behaviorを無断変更する
- iterator化によって必要なcollection materializationやorderingを失う
- concurrency helperへの置換でlifecycleやpanic semanticsを変える
- unrelated refactoringを混ぜる

## Completion Report

完了時は簡潔に報告する。

- **Target Go**: 判断に使用したGo versionと根拠
- **Applied**: 採用したmodern idiom
- **Skipped**: 関連候補を適用しなかった理由があれば記載
- **Validation**: 実行した検証と結果
