---
name: docker-best-practices
description: Dockerfile、Compose、ローカルDocker環境を設計・実装・レビュー・改善するときに使う。correctnessと安全性を優先し、計測で原因を特定してからbuild、runtime、storage、security、host環境の必要な観点だけを適用し、最小変更と再検証で改善する。
---

# Docker Best Practices

Dockerfile、Compose、Dockerベースの開発・実行環境を、推測ではなく観測結果に基づいて改善する。

imageを小さくすることや設定を増やすこと自体を目的にしない。correctness、data safety、security、reproducibility、performance、operability、maintainabilityのバランスを取る。

## Core Principles

### Measure before optimizing

「Dockerが重い」「buildが遅い」「containerが遅い」を同じ問題として扱わない。

最初に現象を測り、原因を次のどこへ分類するか判断する。

- disk / stale resources
- build context / build cache
- image size / dependency footprint
- container CPU / memory
- application processing
- logs
- bind mount / volume I/O
- host / Docker Desktop / WSL2

計測せずにDockerfileやComposeを一括変更しない。

### Protect correctness and data before performance

最適化によって次を壊してはならない。

- runtime dependencies
- file ownership / permissions
- service readiness
- persistent data
- backup / restore path
- application behavior
- security boundary

特にvolume変更、prune、container再作成は、性能改善よりデータ保全を優先する。

### Apply only relevant practices

ベストプラクティスをチェックリストとして全適用しない。

候補は次に分類する。

- **Apply now**: 現在の問題へ直接効き、影響範囲が限定的
- **Follow-up**: 有効だが独立したmigrationや運用変更が必要
- **Skip**: 効果が未計測、style preferenceだけ、またはriskが利益を上回る

`Apply now`は「実装する価値がある」という分類であり、常に変更を実行する意味ではない。実際に適用するかはtask modeで決める。

### Preserve project constraints

repository固有のDockerfile、Compose、CI、deployment、runtime要件を先に確認する。

一般論を理由に既存設計を無視しない。

## Workflow

### 0. Resolve task mode

ユーザーの依頼から、変更を許可するmodeを先に確定する。

- **Review**: Dockerfile / Compose / runtime構成を評価し、findingと改善案を返す。file mutation、build、container再作成、cleanupは行わない。
- **Design**: 望ましい構成や変更案を設計する。提案までに留め、fileやDocker stateを変更しない。
- **Implement**: ユーザーが作成・修正・実装を明示した範囲だけfileを変更する。state-changing validationは必要性とlocal daemonを確認してから行う。
- **Improve**: ユーザーが既存環境の改善・最適化と実変更を明示した場合だけ、計測結果に基づく最小変更を適用できる。
- **Diagnose**: 原因調査だけが依頼ならread-only diagnosticsまで。修正や再作成へ進まない。

依頼がreview / design / diagnosisに留まる場合は、後続の`Apply safely`を実行せず、提案とnon-mutating validationで完了する。

state-changing commandを実行できるのは、**Implement / Improve modeで、その操作が依頼スコープに含まれ、意図したlocal daemonだと確認できた場合だけ**。

### 1. Inspect

daemonへ接続する前に、CLIが向くcontext / endpointを確認する。

```sh
docker --version
docker compose version
docker context show
docker context inspect "$(docker context show)" --format '{{ .Endpoints.docker.Host }}'
printf 'DOCKER_CONTEXT=%s\nDOCKER_HOST=%s\n' "${DOCKER_CONTEXT:-<unset>}" "${DOCKER_HOST:-<unset>}"
```

`DOCKER_CONTEXT`、`DOCKER_HOST`、`--context`、`--host`によるoverrideを含め、今回操作してよいlocal daemonだと確定する。

remote、staging、production、共有daemonの可能性がある場合は、`build`、`up`、`rm`、`prune`等のstate-changing commandへ進まない。contextを推測で切り替えない。

local daemonだと確認できた後に、利用可能な範囲で現状を確認する。

```sh
docker version
docker system df
docker stats --no-stream
docker compose config -q
```

`docker compose config`のrendered outputは、environment interpolationや`env_file`の値を展開してsecretをtool output / transcriptへ露出させる可能性がある。validation目的では`-q`を既定とする。実効設定を確認する必要がある場合は、secretを出力しないことを確認したうえで`--no-interpolate` / `--no-env-resolution`や対象を限定したsanitized outputを使う。

加えて対象に応じて確認する。

- Dockerfile / Containerfile
- Compose files
- `.dockerignore`
- entrypoint / startup scripts
- dependency / lock files
- healthcheck
- volumes / bind mounts
- logging
- exposed / published ports
- repository固有のAgent instructions
- existing validation / CI commands

### 2. Define the observed problem

改善依頼では、変更前に可能な範囲でbaselineを残す。

例:

- build time
- build context
- image size
- startup / readiness time
- CPU / memory
- disk usage
- HTTP latency
- file I/O symptoms

診断方法は [references/performance-diagnostics.md](references/performance-diagnostics.md) を参照する。

### 3. Load only relevant references

必要な領域だけ読む。

- Dockerfile / build / image: [references/dockerfile-build.md](references/dockerfile-build.md)
- Compose / runtime / logs / readiness: [references/compose-runtime.md](references/compose-runtime.md)
- bind mount / volume / persistent data: [references/storage-and-data.md](references/storage-and-data.md)
- privilege / secrets / exposure: [references/security.md](references/security.md)
- Docker Desktop / Windows / WSL2: [references/host-and-wsl2.md](references/host-and-wsl2.md)

referenceは全項目を適用するためのチェックリストではない。

### 4. Select the minimum effective change

変更候補ごとに確認する。

1. 観測した問題へ直接作用するか
2. projectのruntime要件を維持できるか
3. data migrationが必要か
4. securityを弱めないか
5. rollback可能か
6. 同じ方法で効果を再計測できるか

効果を説明できない変更は追加しない。

### 5. Apply safely

このstepはImplement / Improve modeでのみ実行する。Review / Design / Diagnose modeではskipする。

安全な変更から行う。

一般に、次のような変更は比較的局所的に適用できる。

- `.dockerignore`で不要contextを除外
- cache invalidationを減らすDockerfile順序
- multi-stage buildでbuild dependencyをfinal imageから分離
- log rotation設定
- explicit healthcheck / readiness dependency
- unnecessary package / port / privilegeの削減

一方、storage移行、resource cleanup、base image family変更は影響確認を先に行う。

### 6. Validate

repository既存のvalidation commandを優先する。

Review / Design / Diagnose modeではnon-mutating validationだけを使う。例えば`docker compose config -q`や静的なfile inspectionに留め、`build`、`up`、recreate、cleanupは実行しない。

Implement / Improve modeでは、変更内容と依頼スコープに応じて次を選ぶ。

```sh
docker compose config -q
docker compose build
docker compose up -d
docker compose ps
```

state-changing commandを実行する直前にも、操作対象がpreflightで確認したlocal daemonから変わっていないことを確認する。

さらに必要に応じて確認する。

- service health
- application smoke test
- logs
- DB connection
- persistence after restart / recreate
- file ownership / permissions
- image size
- build time
- CPU / memory
- request latency

optimizationでは変更前と同じ条件で再計測する。

改善を確認できなければ「ベストプラクティスだから」という理由だけで変更を正当化しない。

## Decision Priority

競合する場合は次の順で判断する。

**correctness → data safety → security → reproducibility → operability → measured performance → image size → stylistic preference**

## Destructive Operations

以下を一般的な最適化として自動実行しない。

```sh
docker system prune
docker system prune -a
docker builder prune
docker volume prune
docker compose down -v
```

実行が必要な場合は、削除対象、復元方法、persistent dataへの影響を先に確認する。

volume migrationでは、backup fileの作成だけを成功条件にしない。restore可能であることを確認してから切り替える。

## Guardrails

禁止する。

- review / design / diagnosis依頼でfileやDocker stateを変更する
- user intentを確認せず`build`、`up`、recreate、cleanupへ進む
- baselineなしで複数の性能変更をまとめて適用する
- image sizeだけを理由にbase imageを変更する
- Alpineへ機械的に変更する
- runtime dependencyを確認せずmulti-stage化する
- active context / endpointを確認せずdaemonへstate-changing commandを実行する
- rendered Compose configをsecret露出の確認なしにtool output / transcriptへ出力する
- secretsをDockerfile、build args、image layerへ埋め込む
- non-root化で必要なfilesystem permissionを壊す
- healthcheckを単なるprocess存在確認で済ませる
- bind mountとnamed volumeを用途を見ずに置換する
- resource limitを根拠なく設定する
- Dockerの問題とapplicationの問題を混同する
- cleanupのためにpersistent volumeを推測で削除する
- WSL2固有の最適化を他platformへ適用する
- 依頼にない大規模なDocker構成再編を行う

## Completion Report

完了時は簡潔に報告する。

- **Observed**: 変更前に確認した問題またはrisk
- **Changed**: 実際に変更した内容
- **Reason**: その変更を選んだ根拠
- **Validation**: 実行した検証と結果
- **Measured impact**: 比較できた場合の変更前後
- **Follow-up**: 今回は実施しなかった独立課題があれば記載
