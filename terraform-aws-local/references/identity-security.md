# Identity / Security Validation

対象例: IAM、STS、KMS、Secrets Manager、Cognito、ACM、WAF、Organizationsなど。

security系resourceでは「API/configurationが成立すること」と「AWSのsecurity boundaryとして実際に強制されること」を分ける。

## L1-L2で確認する

- policy document syntaxと参照
- role / policy / attachment構成
- trust relationship definition
- secret / key / certificate resource relationships
- Cognito client / pool configuration
- WAF rule structure
- Organizations / account-related Terraform logic

## L3で確認する

Flociが必要operationを実装している場合、API-level configurationを確認する。

例:

- IAM role / policy resourceが作成される
- STS requestがlocal endpointで処理される
- KMS key / aliasが作成される
- secret作成と最小put/get
- Cognito resource作成
- WAF rule resource作成

L3はsecurity enforcementの証拠ではない。

## L4へ残す

原則として実AWSで確認する。

- IAM allow/deny evaluation
- trust policyによる実assume role制御
- SCP / Organizations policy enforcement
- KMS key policy / grantsの実認可
- Secrets Manager resource policy enforcement
- Cognito federation / external IdP integration
- ACM validation / public certificate lifecycle
- WAFによる実traffic blocking
- cross-account security boundaries
- service-linked role behavior

## Policy review

emulatorがallowしてもpolicyが安全とは限らない。

Terraform変更にpolicyが含まれる場合は、local apply結果とは独立してleast privilege、principal、action、resource、conditionをレビューする。

ただし依頼にない大規模なsecurity redesignへ拡張しない。

## Guardrail

Flociで認可が再現されないことを理由にpolicyを広げたり、encryptionやaccess controlを外したりしない。

security semanticsが未検証なら、そのまま`AWS verification required`として明示する。
