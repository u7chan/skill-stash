# Messaging / Event Validation

対象例: SQS、SNS、EventBridge、Kinesis、MSK、Step Functionsなど。

## L1-L2で確認する

- queue / topic / stream / bus / state machine definition
- subscription / target / source mapping
- retry / DLQ / retention設定
- filter / event pattern
- orderingやFIFOに関するconfiguration
- resource referencesとoutputs

## L3で確認する

Flociが必要operationを実装している場合、今回の変更に対応する最小flowを確認する。

例:

- SQS: send -> receive
- SNS: publish -> local inspectionまたは対応subscriber
- EventBridge: event投入 -> target定義確認
- Kinesis: put -> read
- Step Functions: state machine作成 -> 最小execution
- MSK: cluster/runtimeが利用できる場合の最小produce/consume

consumer applicationや大規模fixtureが必要になる場合、Terraform変更の検証に必要かを先に判断する。

## L4へ残す

Floci成功から次を保証しない。

- at-least-once deliveryのproduction timing
- retry/backoffの完全互換
- cross-account delivery
- IAM resource policy enforcement
- high-throughput ordering
- partition rebalance
- service quota / throttling
- regional failure behavior

## Guardrail

local smokeを簡単にするためにretry、DLQ、encryption、policy等のproduction設定を削らない。

Flociが一部integrationを再現できない場合は、resource definitionまでをL3 evidenceとして残し、delivery semanticsはL4へ送る。
