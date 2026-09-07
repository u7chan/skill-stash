# Dockerfile / Build / Image

Dockerfile、build performance、image設計に関係する場合だけ参照する。

SKILL.mdのtask mode gateを優先する。Review / Design / Diagnose modeではDockerfileのinspectionと提案に留め、`docker compose build`などimage / cacheを変更するvalidationは実行しない。

## Build Context

build contextは必要最小限にする。

`.dockerignore`では、対象projectに不要なものを除外する。

代表例:

```text
.git
node_modules
*.log
tmp
coverage
```

ただし、buildで必要なgenerated fileやconfigurationまで除外しない。

context削減は主にbuild転送量、cache invalidation、不要ファイル混入の抑制に効く。稼働中applicationのresponse time改善とは分けて考える。

## Cache-Friendly Layer Ordering

変更頻度の低いdependency metadataを、頻繁に変わるsourceより先に扱う。

例:

```dockerfile
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build
```

lock fileが存在するprojectでは、reproducible installを維持する。

cache効率のためだけにdependencyの意味やinstall modeを変更しない。

## Cache Mounts

package managerやcompiler cacheをbuild間で再利用できる場合は、BuildKit cache mountを検討する。

例:

```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=cache,target=/root/.npm npm ci
```

cache pathは言語・package managerごとに異なる。推測で指定しない。

BuildKitを使っている環境へ、追加効果のないlegacyな有効化設定を機械的に追加しない。

## Multi-Stage Builds

build toolsやsource tree全体がruntimeに不要ならmulti-stage buildを検討する。

final stageにはruntimeで必要なものだけを含める。

確認対象:

- application artifact
- runtime dependencies
- shared libraries
- CA certificates
- timezone data
- configuration
- static assets
- file ownership
- executable permission

image sizeが減っても、runtime behaviorが壊れるなら失敗。

## Base Image Selection

「小さいほどよい」ではなく、用途に必要なcompatibilityと運用性で選ぶ。

評価する。

- required runtime
- libc / native dependency compatibility
- package availability
- security update path
- debugging needs
- architecture support
- image size

`slim`やminimal imageは候補になり得るが、変更後にruntime smoke testを行う。

Alpineはmusl由来の互換性差があり得るため、既存imageから機械的に置換しない。

## Dependency Hygiene

runtimeに不要なbuild packageをfinal imageへ残さない。

OS package managerを使う場合は、不要なrecommended packageを避け、package metadataやtemporary fileを同一layer内で片付ける。

package削減でruntime troubleshootingに必要なものまで除去しない。

## Reproducibility

可能な範囲で次を維持する。

- dependency lock files
- explicit base image version
- deterministic build steps
- stable build inputs

base image digest固定は強い再現性を得られる一方、security updateの取り込み運用が必要になる。repositoryの更新方針なしに一律適用しない。

## Build Secrets

token、password、private keyを`ARG`、`ENV`、`COPY`でimage layerへ残さない。

build中だけ必要なsecretはBuildKit secret mountまたはSSH mountを使う。

例:

```dockerfile
RUN --mount=type=secret,id=token \
    some-command --token-file /run/secrets/token
```

secret値の変更は通常のsource変更と同じcache invalidation特性ではないため、secret更新とbuild cacheの関係も確認する。

## Validation

変更に応じて比較する。

```sh
docker compose build
docker images
```

必要ならcacheなしbuildと通常buildを分けて測り、何を比較したか明示する。

build最適化とruntime性能改善を混同しない。
