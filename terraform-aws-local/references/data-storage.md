# Database / Storage Validation

対象例: S3、RDS、DynamoDB、EFS、OpenSearch、ElastiCache、DocumentDBなど。

## L1-L2で確認する

- engine / version / class等のconfiguration
- encryption / retention / lifecycle definition
- subnet / security group参照
- backup / replication / TTL等のlogic
- naming / tags
- outputsとconsumer側の参照

## L3で確認する

Flociのcurrent supportとoperation coverageを確認したうえで、今回必要な最小CRUDまたはconnection smokeを行う。

例:

- S3: bucket作成、最小object put/get
- DynamoDB: table作成、最小item put/get
- RDS系: instance/resource作成、endpoint取得、可能なら最小connection
- cache / search系: endpoint取得、可能なら最小read/write/request

実データfixtureやschema migrationが依頼範囲に無ければ、検証のためだけに大きく追加しない。

## L4へ残す

Floci成功から次を保証しない。

- managed backup / restoreのproduction behavior
- Multi-AZ / failover
- replication lag
- performance / IOPS / throughput
- service quota
- maintenance window
- encryption key policy enforcement
- production durability
- IAM database authentication等のAWS固有認証
- network isolation

## State and read-back

emulatorではcreate後のread-back値やdefault値がAWSと完全一致しない場合がある。

その差分だけを理由にproduction Terraformへ不要な明示値を追加しない。

差分がTerraform/provider側の問題かFloci側の差かを分類してから変更する。
