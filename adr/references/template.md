# ADR Template

既存repositoryにADRテンプレートがある場合は、必ずそちらを優先する。

以下はconventionが存在しない場合の最小テンプレート。

```markdown
# ADR NNNN: <判断を端的に表すタイトル>

- Status: Proposed
- Date: YYYY-MM-DD

## Context

<なぜ今この判断が必要なのか。現状、課題、制約を価値中立的に書く。>

## Decision Drivers

- <判断に強く影響した条件>
- <優先した品質・コスト・運用上の制約>

## Decision

**<何を採用・変更・維持するかを1文で明確に書く。>**

## Rationale

<なぜこの選択肢がdriversとconstraintsに最も合うのか。>

<何を優先し、何を最適化しないと決めたのかも明示する。>

## Alternatives Considered

### <Option A>

- Pros:
  - <利点>
- Cons:
  - <欠点>
- Rejected because:
  - <採用しなかった理由>

### <Option B / Status quo>

- Pros:
  - <利点>
- Cons:
  - <欠点>
- Rejected because:
  - <採用しなかった理由>

## Consequences

### Positive

- <得られるもの>

### Negative / Accepted Trade-offs

- <受け入れる代償・制限・運用負荷>

## Constraints / Non-goals

- <この判断で守る制約>
- <このADRでは決めないこと>

## Revisit Criteria

次のsignal / eventが発生したら判断を見直す。

- <具体的な条件>
- <具体的な条件>

## References

- <Issue / PR / benchmark / documentation / related ADR>

## Supersedes

<必要な場合のみ、置き換えるADRを記載する。>
```

## 書き方の目安

- Contextは結論ありきで書かない
- Decisionは1文で言い切る
- Alternativesは実際に検討した現実的な案だけを書く
- status quoが現実的なら選択肢に含める
- Negative / Accepted Trade-offsを空にしない
- Revisit Criteriaは「必要になったら」ではなく観測可能な条件にする
- ADR本文を実装手順やTODO一覧で肥大化させない
