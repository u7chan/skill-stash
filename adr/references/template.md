# ADR Template

既存repositoryにADRテンプレートがある場合は、必ずそちらを優先する。

以下はconventionが存在しない場合の最小テンプレート。

```markdown
# ADR NNNN: <判断を端的に表すタイトル>

- Status: Proposed
- Date: YYYY-MM-DD

## Context

<なぜこの判断が必要か。必要十分な背景だけを書く。>

## Decision

<何を決めたかを明確に書く。>

## Consequences

- <得られるもの>
- <受け入れる制約・trade-off>
```

必要な場合だけ、以下を追加する。

- `Alternatives`: 採用しなかった現実的な案が判断理解に必要な場合
- `Revisit`: 見直す条件が明確な場合
- `Supersedes`: 既存ADRを置き換える場合
- `References`: Issue / PR / 関連ADRへの参照が必要な場合

## 書き方

- 原則 `1 decision = 1 file`
- Decisionは1文から数文で言い切る
- Contextを長い経緯説明にしない
- 実装手順、TODO、議論ログを書かない
- amendmentやchangelogを積み上げない
- 過去の変更履歴はGitに任せる
- 判断を理解するために不要なsectionは追加しない
