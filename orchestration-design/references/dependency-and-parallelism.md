# Dependency and Parallelism

並列化は「同時にできそう」ではなく、依存関係・共有状態・統合コストから判断する。

## 依存関係の種類

### Data dependency

前Taskの成果物がなければ開始できない。

例:

- API仕様決定 → 実装
- 調査結果 → 採用判断
- 実装diff → レビュー

この関係は原則として逐次実行する。

### Decision dependency

前Taskの判断が後続Taskの前提になる。

成果物が物理的にはなくても、判断が確定するまで並列化しない方がよい。

### Write dependency

同じファイル、設定、branch、DB、共有状態などを変更する。

worktreeやbranchを分けても、論理的な競合は消えない。後でmergeできることと、独立して設計できることは別である。

### Integration dependency

個々のTaskは独立していても、共通interfaceや統合後の挙動で結合する。

並列実行できる場合でも、fan-in後の統合検証を必須にする。

## 並列候補の判定

次を満たすほど並列化しやすい。

- 入力がすでに確定している
- Task間に直接のデータ依存がない
- 判断待ちがない
- write scopeが重ならない
- interfaceが先に定義されている
- 各Taskを単独で検証できる
- 統合方法が明確である
- 同時実行による時間短縮が統合コストを上回る

1つでも満たさなければ禁止、というチェックリストではない。競合や再作業の可能性を含めて全体コストで判断する。

## Read set / Write setで考える

コード変更では、Taskごとに大まかなread setとwrite setを考えると競合を見つけやすい。

例:

| Task | Read | Write |
| --- | --- | --- |
| frontend | API spec, client code | `client/**` |
| backend | API spec, server code | `server/**` |
| tests | API spec, public behavior | `e2e/**` |

write setが独立していても、共通のAPI specが未確定なら並列開始しない。

逆にread setが重なっていても、確定済み仕様を読むだけなら問題にならない。

## 並列化しやすい例

### 独立調査

異なる候補、異なるサブシステム、異なるデータソースを調べ、最後に比較する。

### 明確なinterfaceを挟んだ実装

API contractなどが確定済みで、frontend / backendの変更範囲が分離されている。

### 異なる観点の検証

correctness、security、performanceなど、評価対象は同じでも観点と証拠が異なる。

ただし同じ入力を同じ基準で重複確認するだけなら、並列化による追加価値は小さい。

## 並列化しにくい例

### 前Taskの発見で作業内容が変わる

調査 → 方針決定 → 実装のように、上流結果で下流の範囲が大きく変わる場合。

### 同じ変更面を触る

複数Taskが同じmodule、schema、設定を独立変更する場合。

### interfaceが未確定

frontend / backendを同時に始めても、契約変更で双方がやり直しになる。

### 統合判断が本体

候補ごとの成果物より、全体を見た一貫した判断が重要な場合。

### 小さすぎる作業

並列起動・説明・回収・統合の方が実作業より重い場合。

## worktree / branchの扱い

worktreeやbranchは物理的な編集競合を減らす手段であり、Task間の設計依存を消すものではない。

利用前に確認する。

- write scopeは論理的にも分離されているか
- shared schemaやinterfaceを同時変更しないか
- merge順序へ暗黙の依存がないか
- 統合後に必ず全体検証できるか

「別worktreeだから並列可能」と判断しない。

## Fan-out前のGate

並列実行へ進む前に、必要なら次をGateとして確定する。

- requirement
- interface / schema
- shared assumptions
- acceptance criteria
- ownership / write scope
- integration point

Gateを増やしすぎない。並列Taskが同じ前提で動くために必要なものだけ固定する。

## Fan-in後の確認

並列Taskがすべて成功しても、次を確認する。

- 成果物が同じ前提に基づいているか
- interfaceが一致しているか
- 重複や矛盾がないか
- merge後のbuild / testが通るか
- 一方の成果が他方のsuccess criteriaを壊していないか

個別成功の集合を、そのまま全体成功とみなさない。
