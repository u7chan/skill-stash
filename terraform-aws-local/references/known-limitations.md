# Known Limitations

Flociはlocal AWS-compatible emulatorであり、AWSそのものではない。

## Service coverage changes

対応service / operationは継続的に変わる。

固定された「対応サービス数」をskill内の判断根拠にしない。実行時に公式Service Matrixを確認する。

https://floci.io/floci/services/

## Service support is not resource support

serviceが対応一覧にあっても、Terraform resourceが内部で利用する全AWS API operationが実装されているとは限らない。

L3失敗時はoperation未対応かTerraform defectかを分類する。

## AWS Provider custom endpoints are best effort

Terraform AWS Providerはcustom endpoint / AWS-compatible solutionへの接続をサポートするが、provider側のintegration testはdefault AWS endpointを基準としている。

そのためProvider version更新でFlociとの互換差が出る可能性を考慮する。

## Read-after-write and defaults may differ

emulatorではAWSと異なるdefault値、computed attribute、read-after-write behaviorが返る場合がある。

結果として、apply後のplanに差分が残ることがある。

Floci上で常にno-op planになることをcompletion criterionにしない。

## Runtime fidelity varies

serviceによっては実containerやlocal engineを利用してruntime behaviorまで確認できるが、AWS managed serviceの完全な再現ではない。

次は原則L4扱いにする。

- real IAM enforcement
- network isolation / routing
- autoscaling / failover
- quota / throttling
- AZ / region behavior
- cross-account behavior
- AWS-managed asynchronous lifecycle
- production performance / durability

## Backend is outside provider emulation assumptions

Terraform backendはAWS Providerとは独立して初期化・利用される。

Floci endpointを設定しただけでstateが安全にlocalへ隔離されたと考えない。

remote backendやHCP Terraform `cloud` blockを持つrootでは、local integration用のisolated root / fixtureが必要になる場合がある。

## Saved plans and state can contain sensitive data

local環境でもTerraform stateやsaved planにはsecret相当値が入る可能性がある。

検証用artifactをcommitしない。既存`.gitignore`やrepository policyを尊重する。

## Do not hide limitations

Flociで検証できなかった場合の正しい対応は、無理にgreenにすることではない。

completion reportで次を分離する。

- verified locally
- not verified due to emulator/tooling
- real AWS verification required

## Upstream references

- Floci Service Matrix: https://floci.io/floci/services/
- Terraform AWS Provider custom endpoints: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/custom-service-endpoints
- Terraform validate: https://developer.hashicorp.com/terraform/cli/commands/validate
- Terraform provider mocking: https://developer.hashicorp.com/terraform/language/tests/mocking
