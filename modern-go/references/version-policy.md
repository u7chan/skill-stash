# Version Policy

Goのversion-sensitiveな判断を行うための基準。

## Resolve the applicable module

変更対象fileから上位へ辿り、そのfileを所有する`go.mod`を特定する。

`go.work`がある場合も、workspace全体へ一つのGo versionを仮定しない。対象fileが属するmoduleの`go.mod`を基準にする。

monorepoで複数moduleを同時に変更する場合は、moduleごとにversionを解決する。

## `go` and `toolchain` directives

`go` directiveはmoduleが要求するGo language versionを示す。

`toolchain` directiveは推奨toolchain選択に関係するが、より新しいtoolchainが使えることを理由に、moduleの`go` directiveより新しいlanguage featureやstdlib APIを無断で使わない。

## Explicit user constraints

ユーザーが「Go 1.24互換」等を明示した場合は、それを上限として扱う。

repositoryがより新しいversionを宣言していても、依頼の互換性要件を破らない。

逆に「Go 1.27へ上げる」こと自体が依頼なら、version bumpとmodernizationを同じ変更として扱えるが、migration scopeを明示する。

## Local toolchain

projectがversionを宣言していない場合のみ、`go version`等のlocal toolchain情報をfallbackとして利用する。

local toolchainが新しいだけではproject compatibilityの根拠にならない。

## High-value version gates

以下は代表例であり、網羅表ではない。利用前に対象versionと現在の公式仕様を確認する。

| Go | Representative additions relevant to modernization |
| --- | --- |
| 1.18 | `any`, generics, `bytes.Cut` |
| 1.20 | `strings.CutPrefix`, `errors.Join`, cancellation causes |
| 1.21 | `slices` / `maps`, `clear`, `min` / `max`, `sync.OnceFunc` / `OnceValue` |
| 1.22 | integer `range`, per-iteration loop variables, `reflect.TypeFor`, enhanced `http.ServeMux`, `cmp.Or` |
| 1.23 | iterator-based `maps.Keys` / `maps.Values` patterns |
| 1.24 | `strings.SplitSeq` / `FieldsSeq`, `testing.T.Context`, JSON `omitzero` |
| 1.25 | `sync.WaitGroup.Go`, `testing.B.Loop` |
| 1.26 | `new(expr)`, typed `errors.AsType`, modernized `go fix` workflow |
| 1.27 | generic methods, `encoding/json/v2` for new JSON code |

この表にない機能を禁止するものではない。新しいversionほど情報が変わりやすいため、公式release notes・package docs・compiler behaviorを確認する。

## Version upgrades

modern idiomを使いたいという理由だけでversionを上げない。

version bumpが必要なら独立した判断として扱い、最低限以下を確認する。

- production / CI toolchain compatibility
- dependency constraints
- build images
- deployment environment
- code generation tools
- linters / analyzers

upgradeが今回の完了条件に不要ならfollow-upへ分離する。
