---
name: terraform-aws-local
description: AWS向けTerraform IaCを設計・実装・レビュー・検証するときに使う。Docker上のFlociをAWS互換endpointとして利用し、AWSアカウントや実credentialsがなくても静的検証からlocal plan/applyまで進め、実AWSでのみ確認できる事項を明確に残す。
---

# Terraform AWS Local

AWS向けTerraform IaCを、実AWSアカウントに依存せず可能な範囲まで設計・検証する。

FlociはAWSそのものではない。local validationを前倒しするために使い、Flociを通すためにproduction Terraformの意味を変えない。

## Core Principles

### Prove local safety before provider execution

`terraform plan`や`apply`、実providerを使う`terraform test`の前に、Terraform、Docker、Floci、AWS endpoint、credentials、backendを確認する。

実AWSやproduction stateへ接続しないことを確認できない場合、providerを実行する検証は行わない。

詳細は [references/preflight.md](references/preflight.md) を参照する。

### Validate progressively

検証は軽いものから順に進める。

1. **L1 Static**: `fmt` / `validate`
2. **L2 Logic**: mock providerを使う`terraform test`
3. **L3 Local integration**: Flociに対する`plan` / `apply` / real-provider test / smoke test
4. **L4 Real AWS**: IAM enforcement、実network、managed runtime、quota等

L1-L3で確認できることとL4でしか確認できないことを混同しない。

詳細は [references/validation-levels.md](references/validation-levels.md) を参照する。

### Route by validation characteristics, not by service count

対象resourceをAWSサービス単位で大量の個別手順へ分解しない。まず検証特性でcategoryへ振り分け、必要なreferenceだけ読む。

- compute / runtime: [references/compute-runtime.md](references/compute-runtime.md)
- network / edge: [references/network-edge.md](references/network-edge.md)
- database / storage: [references/data-storage.md](references/data-storage.md)
- messaging / event: [references/messaging-event.md](references/messaging-event.md)
- identity / security: [references/identity-security.md](references/identity-security.md)

Floci対応状況の判断方法は [references/service-routing.md](references/service-routing.md) を参照する。

### Do not optimize production code for the emulator

Flociの未対応APIや挙動差に遭遇しても、emulatorを通すためだけに以下を行わない。

- production resourceの意味を変更する
- security設定を弱める
- module境界を増やす
- Floci専用条件分岐を本番resourceへ埋め込む
- unsupportedな機能を別AWSサービスへ置き換える

local-only harnessやtest fixtureで分離できる場合のみ、検証用構成を追加する。

## Workflow

### 1. Inspect

変更前に最低限確認する。

- root moduleとchild modules
- `required_version`
- AWS Provider version constraint
- provider設定とalias
- backend / `cloud` block
- variables / locals / outputs
- 対象`aws_*` resourceとdata source
- `.tftest.hcl`の有無とproviderの種類
- repository固有のformat / lint / test / CI command

既存構成を理解する前にmodule分割やbackend変更を提案しない。

### 2. Run preflight

[references/preflight.md](references/preflight.md) に従い、利用可能なvalidation levelを決める。

Preflightが失敗しても作業全体を停止する必要はない。安全に実行できる上限まで降格する。

- Terraformのみ利用可: L1中心
- mock/local-onlyと確認できるTerraform test: L2まで
- Docker + Floci + local-safe backend/providerを確認: L3まで
- 実AWS: このスキルのlocal workflowでは実行しない

### 3. Inventory and route resources

変更対象の`aws_*` resource / data sourceを列挙し、[references/service-routing.md](references/service-routing.md) でcategoryとFloci coverageを確認する。

service supportの有無だけでL3成功を保証しない。resourceが利用するoperationまでFlociが実装しているかは、必要に応じて公式Service Matrixを確認するか実行結果で判定する。

### 4. Design the minimum viable IaC

Terraform設計では以下を優先する。

1. correctness
2. production AWS semantics
3. existing repository constraints
4. testability
5. local emulator convenience

local検証のためだけの抽象化を追加しない。既存moduleで表現できるなら再利用する。

### 5. Validate from L1 upward

repository既存のvalidation commandを優先する。なければ変更範囲に応じて最小限を選ぶ。

典型的なL1:

```sh
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
```

L2として`terraform test`を実行する前に、対象testが`mock_provider`やoverrideによってAWS Provider APIを呼ばないことを確認する。

```sh
terraform test
```

Terraform testはデフォルトで`apply`を実行し得る。実providerを使うtestはL2ではなくL3として扱い、preflightを通してFlociへ隔離できた場合のみ実行する。実AWSを向く可能性があるtestは実行しない。

L3はpreflightで安全を証明できた場合のみ行う。実行方法は [references/preflight.md](references/preflight.md) と各category referenceに従う。

### 6. Classify failures before changing code

失敗を次に分類する。

- **Terraform configuration**: syntax、type、dependency、invalid expression
- **Provider validation**: AWS Provider schemaやprovider configuration
- **Floci unsupported**: service / operation未対応
- **Emulator difference**: read-after-write、runtime、network等のAWSとの差
- **Local environment**: Terraform / Docker / Floci / port / dependency
- **Real AWS required**: local emulatorでは証明できない

Floci由来の失敗をTerraform defectとして修正しない。

### 7. Smoke test only what matters

L3 applyが成功したら、今回の変更に対応する最小のsmoke testを行う。

resource数を増やすためのテストや、依頼と無関係なend-to-end環境は作らない。

### 8. Cleanup

local test用に作成したstateやFloci resourceが不要なら、今回作成した範囲だけ削除する。

共有Floci環境の他resourceを推測で削除しない。

## Guardrails

禁止する。

- 実AWSへの`terraform apply`をlocal validationとして実行する
- provider利用形態を確認せず`terraform test`を実行する
- 実credentialsをlocal Floci testへ流用する
- remote production backendへlocal test stateを書き込む
- Floci対応サービス一覧を固定値として信頼する
- FlociでapplyできたことをAWS動作保証と表現する
- `terraform plan`のno-opだけをFloci検証の成功条件にする
- emulator limitationを隠すためproduction Terraformを変更する
- 依頼にないlint/security toolを導入する
- local testのためだけに大規模なmodule再編を行う

既知の制約は [references/known-limitations.md](references/known-limitations.md) を参照する。

## Completion Report

完了時は簡潔に報告する。

- **Scope**: 設計・変更したTerraform
- **Preflight**: 利用できたTerraform / Docker / Flociと安全確認
- **Verified**: L1-L3で実際に確認した内容
- **Not verified**: 未実行またはFloci制約で確認できなかった内容
- **AWS verification required**: AWSアカウント発行後に確認すべきL4項目

local validation成功をproduction readinessと同義にしない。
