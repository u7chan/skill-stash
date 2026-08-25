# Automation and CI

ローカルフィードバックとCI品質ゲートを扱う。

## Local feedback

commit前のautomationは高速であることを優先する。

向いているもの:

- formatter
- lint auto-fix
- staged-file validation
- inexpensive static checks

commitのたびに長時間待たされる構成を避ける。

## CI responsibilities

CIはrepositoryの主要な完了条件を再現する。

候補:

- dependency installation
- typecheck
- lint
- format check
- dead-code analysis
- unit tests
- integration tests
- production build

すべてを必須にする必要はない。プロジェクトのfailure riskに応じて選択する。

## Local vs CI

高速なfeedbackはlocal hook、完全性の確認はCIという責務分離を基本にする。

重いbuildやE2Eを無条件にpre-commitへ配置しない。

## Scripts

CI commandをworkflow内へ直接大量に書かず、可能であればrepository scriptとして定義する。

例:

- `typecheck`
- `lint`
- `format:check`
- `test`
- `build`
- `check`

ローカルとCIが別の検証方法になる状態を避ける。

## Quality gate

CIを成功させるために、lint disableを増やす、type errorを無視する、testsをskipする、build validationを削除するといった変更を行わない。

品質ゲート自体が不適切なら、理由を説明したうえで設計を変更する。

## GitHub Actions

GitHub Actionsを使用している場合は以下を確認する。

- third-party Actions
- permissions
- secrets
- cache
- dependency installation
- concurrency

workflowが動くことだけでなく、必要以上の権限を持っていないことも確認する。
