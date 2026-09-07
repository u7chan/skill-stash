# Docker Security

Dockerfile、Compose、runtime permission、secret、network exposureに関係する場合だけ参照する。

## Run with Least Privilege

serviceがroot権限を必要としないならnon-root executionを優先する。

ただし`USER`だけ追加して終わらせない。

確認する。

- application filesのownership
- writable directories
- bound volume permissions
- privileged ports
- startup-time initialization

non-root化でruntimeを壊さない。

## Avoid Privileged Containers

`privileged: true`は強い権限を与える。

既存構成で使われている場合は、必要なkernel feature、device、capabilityを特定してから縮小を検討する。

単に動かすためのpermission workaroundとして追加しない。

## Capabilities

Linux capabilitiesは必要最小限にする。

`cap_drop` / `cap_add`を使う場合はapplicationが必要とするcapabilityを確認する。

一律の`cap_drop: [ALL]`でruntimeを壊すより、検証可能な最小変更を選ぶ。

## Secrets

secretを次へ直接保存しない。

- Dockerfile
- image layer
- source repository
- build argument
- committed Compose environment value

build時のsecretはbuild secret mechanismを使う。

runtime secretはrepositoryの既存secret management方式を優先する。Compose secretsが適する場合はservice単位で必要なsecretだけを渡す。

## Docker Socket

Docker socketへのmountはhost上のDocker daemonを操作できる強い権限を与える。

例:

```text
/var/run/docker.sock
```

必要性を確認せずmountしない。

read-only mountであってもAPI操作のriskが消えるとは限らない。

## Filesystem

applicationが対応するならread-only root filesystemを検討する。

writeが必要なpathは明示的に分離する。

host bind mountは必要なpathとmodeだけを公開し、不要なhost directory全体をmountしない。

## Network Exposure

内部通信にしか使わないservice portをhostへpublishしない。

`0.0.0.0`への公開が必要か、localhost bindingで足りるかを確認する。

開発用debug portをproduction構成へ残さない。

## Image Surface

runtimeに不要なcompiler、package manager、debug toolを減らすとattack surfaceも減る。

ただしsecurityを理由にobservabilityやincident responseを不可能にするほど削らない。

## Validation

security変更では機能確認だけでなく、意図した制限が実際に効いていることを確認する。

例:

- expected userでprocessが起動
- required pathへだけwrite可能
- unnecessary portが公開されていない
- secretがimage historyやrepositoryへ残っていない
- privileged / socket mountが不要なら除去されている
