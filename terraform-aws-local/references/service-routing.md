# Service Routing

Terraform resourceをFloci検証へroutingするための基準。

Flociのサービス数やoperation数は変化するため、このrepositoryに固定一覧を複製しない。

## Step 1: Identify AWS services

変更対象のresource / data sourceを列挙する。

例:

```text
aws_ecs_cluster
aws_ecs_service
aws_lb
aws_security_group
aws_db_instance
aws_secretsmanager_secret
```

resource prefixだけで不明な場合はTerraform AWS Provider documentationから対応AWS serviceを確認する。

## Step 2: Route by validation characteristics

| Category | Typical services/resources | Reference |
| --- | --- | --- |
| Compute / runtime | EC2, ECS, EKS, Lambda, ECR, Batch | `compute-runtime.md` |
| Network / edge | VPC, Subnet, Route, SG, ELB, Route 53, CloudFront, API Gateway | `network-edge.md` |
| Database / storage | S3, RDS, DynamoDB, EFS, OpenSearch, ElastiCache, DocumentDB | `data-storage.md` |
| Messaging / event | SQS, SNS, EventBridge, Kinesis, MSK, Step Functions | `messaging-event.md` |
| Identity / security | IAM, STS, KMS, Secrets Manager, Cognito, ACM, WAF, Organizations | `identity-security.md` |

一つのresourceが複数categoryの性質を持つ場合、必要なreferenceだけ併用する。

## Step 3: Check current Floci coverage

公式Service Matrixを確認する。

https://floci.io/floci/services/

判定は次の3段階にする。

- **Supported candidate**: 対応serviceとして掲載され、必要operationも確認できる
- **Partial / unknown**: serviceは掲載されるが、resourceが必要とするoperationが不明または一部のみ
- **Unsupported**: serviceまたは必要operationが未対応

サービス名が掲載されているだけで`Supported candidate`と断定しない。

## Step 4: Let execution refine the classification

L3で失敗した場合、errorから次を切り分ける。

### Terraform / provider defect

例:

- invalid argument
- required attribute不足
- type mismatch
- dependency cycle

Terraform側を修正する候補。

### Floci unsupported operation

AWS-compatible endpointへ到達しているが、operation未対応を示すerror。

production Terraformを変更しない。`Not verified`または`AWS verification required`へ送る。

### Emulator behavior difference

createは成功するがread-back、runtime、network等がAWSと異なる。

Terraform defectとして扱わず、known limitationとして記録する。

## When to add service-specific references

初期状態ではserviceごとのreferenceを作らない。

以下を満たす場合のみ`references/services/<service>.md`の追加を検討する。

- category共通ルールだけでは安全に検証できない
- service固有のlocal runtimeやsidecar操作が必要
- 同じ手順を複数回再利用する
- 数行の注意書きでは説明できない

一度きりのFloci workaroundのためにservice-specific referenceを増やさない。

## Keep routing current

Flociの対応状況が変わってもSKILL.mdを更新せずに済むことを優先する。

固定するのは「判断方法」であり、「現在の対応サービス数」ではない。
