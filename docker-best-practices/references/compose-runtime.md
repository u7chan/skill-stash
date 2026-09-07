# Compose / Runtime / Operability

Compose、service lifecycle、health、logs、resource usageに関係する場合だけ参照する。

SKILL.mdのtask mode gateを優先する。Review / Design / Diagnose modeではnon-mutating validationだけを行い、`up`、recreate、restart等でDocker stateを変更しない。

## Validate Effective Configuration

Compose変更後は、まず設定をstdoutへrenderせずvalidationする。

```sh
docker compose config -q
```

通常の`docker compose config`はenvironment interpolationやservice `env_file`を解決し、secret値をstdoutへ含める可能性がある。エージェントのtool output / transcriptへ実値を流さない。

実効設定の確認が必要な場合は、目的に応じて次を使う。

- `--no-interpolate`: environment variableを展開しない
- `--no-env-resolution`: service `env_file`を解決しない
- `--services` / `--images` / `--networks`等: 必要な情報だけ出力する
- sanitized output: secret-bearing fieldを含めない形で確認する

secretを含まないと確認できない限り、resolved model全体をstdoutへ出力しない。

## Readiness Is Not Startup Order

container processが起動したことと、serviceが利用可能なことを区別する。

DBやAPIのready待ちが必要ならhealthcheckを用意し、依存service側でhealth conditionを利用できる構成を検討する。

healthcheckは対象serviceの実際のready条件へ寄せる。

避ける例:

- processが存在するだけ
- 常に0を返すcommand
- dependencyを大量に巻き込む高コストcheck

timeout、interval、retries、start periodはservice特性に合わせる。

## Graceful Shutdown

container停止時にapplicationがsignalを受け取り、必要なcleanupを行えることを確認する。

shell wrapperがsignalを握りつぶす構成に注意する。

必要に応じてexec formの`CMD` / `ENTRYPOINT`やinit processを検討するが、既存lifecycleを理解せず変更しない。

## Logging

logの無制限増加を放置しない。

選択肢:

- automatic rotationを持つlogging driver
- `json-file`へ`max-size` / `max-file`を設定
- external logging基盤

例:

```yaml
services:
  web:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "5"
```

保持量を減らすと過去調査可能期間も短くなる。容量だけで決めない。

既存containerへのlogging変更は再作成を伴い得るため、停止影響を確認する。

## Restart Policy

restart policyはfailure recovery要件に合わせる。

無条件restartでapplication crash loopを隠さない。

healthcheck failureとcontainer restartが同義ではないことにも注意する。

## CPU and Memory

`docker stats --no-stream`等でresource pressureを確認してから制約を調整する。

resource limitは安定性のために有効な場合があるが、根拠なく小さくするとOOM、GC増加、timeoutなど別の問題を作る。

性能改善のためにlimitを増やす場合も、host側の余力を確認する。

## Ports and Networks

必要なportだけpublishする。

service間通信だけで済むportをhostへ公開する必要はない。

network分割はsecurity boundaryとして価値がある場合だけ行い、単純なlocal stackへ不必要なnetwork topologyを追加しない。

## Read-Only Runtime

applicationが対応できる場合はread-only filesystemを検討できる。

書き込みが必要なpathはnamed volumeやtmpfs等として明示する。

permission errorを見て無条件にread-onlyを解除せず、必要なwrite pathを特定する。

## Validation

変更後は必要に応じて確認する。

```sh
docker compose config -q
docker compose up -d
docker compose ps
docker compose logs --tail=100
docker stats --no-stream
```

`up`等のstate-changing commandは、SKILL.mdのpreflightで操作対象が意図したlocal daemonだと確認できた場合だけ実行する。

さらにrestart、graceful shutdown、health遷移、主要requestを確認する。
