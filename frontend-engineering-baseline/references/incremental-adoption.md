# Incremental Adoption

既存リポジトリへengineering baselineを導入する際のscope controlを扱う。

## Do not modernize everything

baseline auditで複数の改善候補が見つかっても、一度にすべて実装しない。

例:

- package manager migration
- linter migration
- formatter migration
- TypeScript strictness migration
- CI redesign
- dependency policy
- framework migration

これらは互いに独立した変更になり得る。

## Use the skill-level scope classification

変更候補の分類と実装ゲートは、`SKILL.md` の `Identify gaps` を正とする。

このreferenceでは別の分類基準を定義しない。

段階導入では、`Required now` に分類された変更だけを今回の実装対象として扱い、`Useful follow-up` と `Optional` は明示的に今回のスコープへ含まれていない限りfollow-upへ分離する。

## Migration trigger

既存toolを別toolへ置き換える場合、少なくとも一つ明確な理由を示す。

例:

- 現在のtoolが保守されていない
- frameworkと互換性がない
- CI reliabilityに問題がある
- performanceが開発体験を明確に阻害している
- configuration complexityを大きく削減できる

「こちらの方が新しい」は理由にしない。

## One concern at a time

可能なら変更をconcern単位に分ける。

Good:

1. dependency reproducibility
2. static analysis
3. CI enforcement

Bad:

1. package manager、lint、framework、test runner、CIを全部交換

## Preserve green state

各段階でrepositoryが検証可能な状態を維持する。

変更後に最低限、install、relevant static checks、影響するtests、影響するbuildを確認する。

## Stop condition

今回定義した完了条件を満たしたら終了する。

追加で発見した改善は現在の変更へ混ぜずfollow-upとして報告する。

「ついでに改善できる」は実装理由にしない。
