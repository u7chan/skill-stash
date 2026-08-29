# Preflight

Flociを使う`plan` / `apply`の前に、local-only executionであることを確認する。

このreferenceはセットアップガイドではない。必要なtoolが無い場合は自動インストールせず、実行可能なvalidation levelへ降格する。

## 1. Terraform

```sh
terraform version
```

利用不可ならTerraform CLIを使う検証は未実施として扱う。

## 2. Docker

```sh
docker info
docker compose version
```

Docker daemonへ接続できない場合、Floci integrationは行わない。

## 3. Floci

Flociは既存のproject-defined起動方法を優先する。

health check:

```sh
curl -fsS http://localhost:4566/_floci/health
```

停止している場合、repositoryに既存のCompose serviceや起動commandがあり、今回の作業で起動してよいと判断できる場合のみそれを使う。

独自のDocker構成を勝手に追加してpreflightを通さない。

## 4. Provider endpoint safety

Flociの標準endpointを使う場合の代表例:

```sh
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_REGION=us-east-1
export AWS_DEFAULT_REGION=us-east-1
export AWS_EC2_METADATA_DISABLED=true
```

AWS Providerはprovider block、environment、shared configなど複数経路からendpointとcredentialsを解決する。環境変数だけ見て安全と判定しない。

`plan` / `apply`前に最低限確認する。

- provider blockに`access_key` / `secret_key` / `token`が直書きされていないか
- provider blockに`profile`や実環境向け`assume_role`が固定されていないか
- provider blockの`endpoints`が実AWSや別環境を向いていないか
- `AWS_IGNORE_CONFIGURED_ENDPOINT_URLS`がcustom endpointを無効化していないか
- `AWS_PROFILE`、web identity、role関連environmentが実credential pathを有効化していないか

provider内の明示設定がlocal executionと競合する場合、production providerをFloci向けに書き換えない。既存のlocal test root / fixture / provider injection方法が無ければL3をスキップする。

## 5. Use dummy credentials for L3

可能ならlocal commandではreal credential sourcesを除外したうえでdummy credentialsを明示する。

例:

```sh
env \
  -u AWS_PROFILE \
  -u AWS_SESSION_TOKEN \
  -u AWS_WEB_IDENTITY_TOKEN_FILE \
  -u AWS_ROLE_ARN \
  AWS_ENDPOINT_URL=http://localhost:4566 \
  AWS_ACCESS_KEY_ID=test \
  AWS_SECRET_ACCESS_KEY=test \
  AWS_REGION=us-east-1 \
  AWS_DEFAULT_REGION=us-east-1 \
  AWS_EC2_METADATA_DISABLED=true \
  AWS_IGNORE_CONFIGURED_ENDPOINT_URLS=false \
  terraform plan
```

これは安全性を補強する例であり、repository固有wrapperが同等以上の隔離をしている場合はそちらを優先する。

## 6. Backend safety

provider endpointとTerraform backendは別物として確認する。

### Static validation

remote backendへ接続せずvalidationする場合:

```sh
terraform init -backend=false
terraform validate
```

### Local integration

L3の`plan` / `apply`は、以下のどちらかでのみ行う。

- root moduleがdefault/local backendを利用している
- repositoryにlocal integration専用root / fixtureがあり、stateがlocalに隔離される

production向けremote backendや`cloud` blockを持つroot moduleでは、local testのためだけにbackend typeを変更しない。

必要なら既存moduleを呼び出す小さなlocal test rootを利用する。新規作成が必要な場合は、今回の検証価値に対して最小限であることを確認する。

## 7. Existing working directory safety

`.terraform/`には過去に初期化したbackend情報が残る。

既存working directoryがproduction backendで初期化済みか不明な場合、そのままL3を実行しない。

projectが許すならisolated working copyや専用test directoryを使う。

## Preflight result

次の形式で内部判断する。

| Check | Result | Effect |
| --- | --- | --- |
| Terraform | pass/fail | L1-L2可否 |
| Docker | pass/fail | L3可否 |
| Floci health | pass/fail | L3可否 |
| Provider local-only | pass/fail | L3可否 |
| Backend local-only | pass/fail | L3可否 |

L3は全てpassの場合のみ実行する。

## Upstream references

- Floci Service Matrix: https://floci.io/floci/services/
- Terraform AWS Provider custom endpoints: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/custom-service-endpoints
- Terraform backend overview: https://developer.hashicorp.com/terraform/language/backend
