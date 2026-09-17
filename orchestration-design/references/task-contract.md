# Task Contract

Task Contractは、作業を誰に割り当てるかではなく、何を入力として何を成立させるかを定義する境界である。

形式そのものより、後続Taskが追加の会話履歴なしでも成果物を利用・検証できることを優先する。

## 最小項目

### objective

このTaskで成立させる結果を1つの目的として書く。

悪い例:

- backendを担当する
- 調査する
- レビューする

良い例:

- 認証APIへrefresh tokenの失効処理を追加する
- 既存実装が要件Aを満たすか、根拠付きで確認する
- PR差分からcorrectness上のblockerを特定する

Roleではなく成果で表す。

### dependencies

開始前に必要なTaskまたは成果物を列挙する。

依存がない場合は空でよい。

「同じプロジェクトだから」という理由だけで依存を追加しない。

### inputs

Taskが利用してよい入力を明示する。

例:

- Issue / requirement
- API specification
- existing code
- previous task artifact
- test result
- diff

後続Taskへ全会話を渡さなくてもよいよう、必要な前提は入力または成果物へ寄せる。

### success criteria

Taskの完了を判定できる条件を書く。

できるだけ観測可能な状態にする。

例:

- 対象endpointが仕様どおり応答する
- 指定テストがpassする
- 調査対象の候補と根拠が列挙されている
- blockerの有無をdiffと要件に基づいて判定できる

「十分に調査した」「品質が高い」のように、判定者によって結論が大きく変わる条件だけにしない。

### outputs

後続Taskへ渡す成果物を定義する。

例:

- patch
- commit
- test result
- structured findings
- decision
- specification
- unresolved issues

Task完了時に何を返すか曖昧なら、委譲境界も曖昧である。

## 必要に応じて追加する項目

### allowed actions

実行主体が使ってよい操作やツールを限定する必要がある場合に使う。

例:

- read only
- code edit
- test execution
- GitHub comment
- external research

通常の安全な操作まで細かく列挙しすぎない。

### write scope

変更可能な範囲を限定したい場合に使う。

例:

- `server/auth/**`
- docs only
- PR comments only

並列Taskで書き込み競合を避けたい場合に特に有効である。

write scopeが重なる場合は、並列化より先に責務分割または統合方法を見直す。

### limits

暴走や無限ループを防ぐ必要がある場合に使う。

例:

- retry count
- review rounds
- token / cost budget
- tool-call budget
- wall time

小さいTaskへ一律に細かいbudgetを設定しない。停止不能になり得る箇所へ使う。

### failure output

成功できなかった場合に返す情報を決める。

最低限、次があると再計画しやすい。

- failed criteria
- observed evidence
- unresolved blockers
- changed artifacts
- recommended next boundary

失敗時に「できませんでした」だけを返さない。

## Task Contractの例

表現形式は固定しない。YAMLで表すなら次のようにできる。

```yaml
id: auth-refresh-revocation
objective: refresh token失効処理を追加する

dependencies:
  - auth-behavior-spec

inputs:
  - auth specification
  - server/auth implementation

allowed_actions:
  - read
  - edit
  - test

write_scope:
  - server/auth/**

success_criteria:
  - revoked token is rejected
  - existing auth tests pass
  - new behavior has regression tests

outputs:
  - patch
  - test-result
  - unresolved-issues

limits:
  retries: 2
```

YAML化自体を目的にしない。小さなTaskなら自然言語の数行で十分である。

## 分割品質の確認

Taskを作ったら次を確認する。

- objective単独で意味が通るか
- inputsが揃えば開始できるか
- success criteriaで完了判定できるか
- outputsを後続が利用できるか
- write scopeを必要以上に共有していないか
- 別Taskとの責務境界が説明できるか

複数Taskが同じobjective、同じ入力、同じ変更範囲を持つなら、分割理由を見直す。

## 過剰分割を避ける

次のような分割は統合コストだけを増やしやすい。

- 1つの小さな変更をファイル単位で別Taskにする
- 単独では検証できない途中工程を大量に切り出す
- 同じコードを複数Taskが同時に理解・変更する
- 同じ調査を複数Taskへ重複して依頼する
- Role名を増やすためにTaskを作る

1つの実行主体が自然に完了できる範囲は、無理に分割しない。
