# Dependency Security

依存関係、実行環境の再現性、Supply Chain Riskを扱う。

## Runtime and package manager

可能な範囲でruntime version、package manager、package manager versionを明示する。

開発者、CI、Agentが異なるversionを暗黙利用する状態を避ける。ただし既存のversion managementがある場合は新しい仕組みを重複して導入しない。

## Dependency versions

依存バージョンの管理方針を確認する。

評価対象:

- direct dependencyのversion policy
- lockfileの管理
- executable packageのversion
- CIで実行されるthird-party tooling

`latest` や暗黙的な最新版参照を、再現性が必要な処理で利用しない。

## Newly published packages

公開直後のpackage versionを自動的に取り込む必要があるか検討する。

更新速度よりSupply Chain Riskの低減を優先する環境では、一定期間経過したversionのみ採用する仕組みを検討する。

ただし緊急のsecurity updateまで妨げない。例外は明示的・狭い範囲・一時的であることを優先する。

## Dependency automation

dependency update automationが存在する場合、package manager側のpolicyと矛盾しないことを確認する。

評価するもの:

- update frequency
- grouping
- version policy
- security updates
- CI validation

Botが更新できてもCIが検証できない状態を作らない。

## CI dependencies

CI上で第三者コードを実行する場合、mutable referenceを避けられるか検討する。

固定revisionを使う場合でも更新不能な運用にしない。安全性と保守性の両方を考える。

## Agent tooling

MCP server、CLI、code generator等をpackage runner経由で実行する場合もdependencyとして扱う。

再現性が重要ならversionを明示し、Agentが毎回異なる最新版toolingを取得する構成を無意識に導入しない。
