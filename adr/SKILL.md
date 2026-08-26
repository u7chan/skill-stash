---
name: adr
description: 実装・設計・レビューで、将来「なぜそうしたか」を失うと再議論や誤った巻き戻しが起きる技術判断を検出し、必要なときだけArchitecture Decision Record（ADR）を作成・更新するときに使う。技術選定、境界設計、データ配置、主要依存、横断ルール、既存方針の置き換えなど、複数の妥当な選択肢とトレードオフがある判断に適用する。
---

# ADR

ADRは「何を実装したか」ではなく、**なぜその判断を選び、何を受け入れ、いつ見直すか**を未来へ残すための記録である。

目的は文書を増やすことではない。半年後の自分や別のAIエージェントが、コードだけを見て善意で設計判断を巻き戻すことを防ぐ。

## Decision Gate

非自明な実装・設計・レビューを完了する前に、ADRが必要か必ず判定する。

次のいずれかに当てはまり、理由がコードから自明でないならADR候補とする。

- 妥当な選択肢が複数あり、意図的なトレードオフを選んだ
- system boundary、data ownership、storage、integration、auth/security、concurrency、deploymentなど横断的な方針を決めた
- 主要なdependency、runtime、framework、serviceを追加・削除・置換した
- repository全体または今後の実装が従うconventionを決めた
- 一見すると単純化・置換できそうだが、あえて現在の形にしている
- 将来の人間やAIが「cleanup」として元に戻しそうな判断である
- 変更コスト、移行コスト、運用リスク、lock-inなどにより簡単には戻せない
- 既存ADRの判断を変更・廃止・置換する

### 半年後テスト

迷ったら次の2問で判定する。

1. 半年後、コードだけを読んでこの判断理由を正しく復元できるか？
2. 将来の人間やAIが、背景を知らずに善意で元へ戻す可能性があるか？

1が「いいえ」または2が「はい」なら、ADRを残す価値が高い。

## Skip

次の変更では原則ADRを作らない。

- 既存仕様へ戻すだけのbug fix
- UI styling、copy edit、formatting
- test-only change
- observable behaviorや境界を変えない局所refactor
- 既存のAccepted ADRや明文化済みconventionに従うだけの実装
- 採用判断に至っていない短命なspike / experiment
- 理由が自明で、安価かつ安全に巻き戻せる局所判断

ADRを書かない理由をADRとして記録しない。

## Workflow

### 1. Inspect existing conventions

最初にrepository内の既存ADRとルールを探す。

確認対象の例:

- `docs/adr/`
- `docs/adrs/`
- `adr/`
- `architecture/decisions/`
- README / AGENTS.md / CONTRIBUTING.md
- 既存ADRの番号、filename、status、section構成

既存conventionがあれば必ずそちらを優先する。

conventionが存在せず新規導入する場合のみ、既定値として以下を使う。

```text
docs/adr/NNNN-kebab-case-title.md
```

番号は既存最大値 + 1 とし、再利用しない。

### 2. Reconstruct the decision context

ADRを書くためだけに、ユーザーへ既に分かっている情報を聞き直さない。

必要な背景は可能な範囲で以下から復元する。

- Issue / PR / discussion
- code / tests
- repository documentation
- benchmark / experiment result
- 外部仕様・公式documentation

推測で理由を作らない。判断理由が本当に不明でADRの意味が変わる場合のみ確認する。

### 3. Freeze one decision

ADRは原則 **1 decision = 1 file** とする。

書き始める前に以下を確定する。

- **Decision**: 何を決めたかを1文で言えるか
- **Context**: なぜ今この判断が必要か
- **Drivers / Constraints**: 判断を動かした条件は何か
- **Alternatives**: 他に現実的な選択肢は何だったか
- **Trade-offs**: 何を得て、何を諦めるか
- **Revisit criteria**: 何が変われば判断を見直すか

複数の独立した判断が混ざるならADRを分ける。

### 4. Write the minimum durable record

テンプレートは [references/template.md](references/template.md) を使う。

すべてのsectionを埋めることを目的にしない。未来の判断復元に必要な情報だけ残す。

特に省略しない。

- 明確なDecision
- 選択理由
- 採用しなかった現実的な案と、その理由
- negative consequence / accepted trade-off
- 制約
- 見直し条件

実装手順、TODO一覧、PR差分説明をADRへ詰め込まない。それらはIssue、design doc、PR、runbookへ置く。

### 5. Preserve decision history

AcceptedになったADRは、誤字・壊れたlinkなど意味を変えない修正を除き、原則として書き換えない。

判断が変わった場合は新しいADRを作り、旧ADRを`Superseded`として参照する。

過去の判断が現在は誤りでも、当時なぜ妥当だったかという履歴を消さない。

### 6. Validate the ADR

完了前に以下を確認する。

- Decisionを新しく参加した人が1文で言い直せる
- Contextが特定の選択肢を最初から正当化する文章になっていない
- alternativesに現実的な案が含まれる
- status quoが現実的な選択肢なら比較対象に含めた
- 「なぜ採用しなかったか」が分かる
- positiveだけでなくnegative consequenceも書かれている
- revisit criteriaが「必要になったら」ではなく具体的なsignal / eventになっている
- implementation detailで判断理由が埋もれていない
- 既存ADRとの関係が必要なら明示されている

## Status Policy

既存conventionがなければ次を使う。

- `Proposed`: 判断案。まだ確定していない
- `Accepted`: 現在有効な判断
- `Superseded`: 新しいADRに置き換えられた
- `Deprecated`: 現在は推奨しないが、直接の後継ADRがない

実装済みという理由だけで自動的に`Accepted`へしない。repositoryのreview / merge運用に従う。

## Guardrails

禁止する。

- trivialな変更までADR化して文書を増やす
- 結論を正当化するためだけにalternativesを後付けする
- 実際には検討していない案を「検討した」と書く
- trade-offやnegative consequenceを隠す
- ADRを詳細設計書や実装計画の代わりにする
- Accepted ADRの履歴を都合よく書き換える
- 根拠がない将来予測を事実として書く
- repositoryの既存ADR conventionを無視して独自形式を持ち込む

## Completion Report

ADRを作成・更新した場合は簡潔に報告する。

- **Decision**: 記録した判断
- **ADR**: file path / number
- **Why now**: ADRが必要だった理由
- **Trade-off**: 明示した主要な代償
- **Revisit**: 見直し条件

ADR不要と判断した場合、通常は報告を増やさない。ユーザーがADR要否の判定を求めた場合のみ理由を説明する。
