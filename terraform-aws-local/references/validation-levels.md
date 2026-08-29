# Validation Levels

Terraform IaCの検証を4段階に分ける。

## L1: Static

目的: Terraform configuration自体の基本的な妥当性を確認する。

代表例:

```sh
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
```

確認できること:

- HCL syntax
- attribute name / type
- internal consistency
- module/provider plugin resolution

確認できないこと:

- provider APIとの実通信
- runtime behavior
- IAM enforcement
- network behavior

`terraform validate`はremote serviceを検証しない。

## L2: Logic

目的: moduleの条件分岐、variables、outputs、resource構成など、Terraform logicをAWS接続なしで検証する。

Terraform testが既にある場合は優先して利用する。

```sh
terraform test
```

Terraform 1.7+では`mock_provider`を利用できる。

向いている例:

- feature flagでresource数が変わる
- naming / tags / locals
- module output
- variable combination
- dependency shape

mock providerはAWS API behaviorを再現しない。L3の代替ではなく、logic testとして扱う。

## L3: Local integration

目的: AWS Providerを実際に動かし、FlociのAWS-compatible APIに対して`plan` / `apply`できることを確認する。

前提:

- Docker / Flociがhealthy
- providerがFlociのみを向く
- dummy credentialsを使用
- state/backendがlocalに隔離される

確認対象:

- provider configuration
- AWS API request shape
- resource dependency
- create/read/update/deleteのうち今回必要なoperation
- 最小限のruntime / CRUD smoke test

Floci service supportがあっても、対象resourceが必要とする全operationの実装を保証しない。

## L4: Real AWS

目的: emulatorでは証明できないAWS固有挙動を確認する。

代表例:

- IAM policy enforcement
- Security Group / NACL packet filtering
- VPC routing / NAT / IGW
- Route 53 / CloudFrontの実配信
- managed serviceのfailover / scaling
- service quota
- Organizations / SCP / account policy
- service-linked role
- cross-account behavior
- production-grade eventual consistency

このスキルのlocal workflowではL4を実行しない。必要項目をcompletion reportへ残す。

## Choosing the level

常に最高levelまで実行する必要はない。

- syntax修正だけ: L1で十分な場合がある
- module logic変更: L1 + L2
- AWS resource追加: 安全ならL1-L3
- network/security semantics変更: L1-L3 + L4項目を明示

「実行できるからL3まで行う」ではなく、変更リスクに対して必要な証拠を選ぶ。

## Evidence hierarchy

同じ主張を複数levelで検証できる場合、より直接的な証拠を優先する。

例:

- `aws_s3_bucket`がconfigurationに含まれる: L1/L2
- providerがbucket作成APIを受理する: L3
- production policyで期待どおりアクセス制御される: L4

## Upstream references

- Terraform validate: https://developer.hashicorp.com/terraform/cli/commands/validate
- Terraform tests: https://developer.hashicorp.com/terraform/language/tests
- Terraform provider mocking: https://developer.hashicorp.com/terraform/language/tests/mocking
