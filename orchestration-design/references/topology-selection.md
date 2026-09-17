# Topology Selection

実行トポロジーは、エージェント数ではなくTaskの依存構造から選ぶ。

最初から複雑な構成を選ばず、成立する最小の形を使う。

## 1. Single

1つの実行主体で、理解・変更・検証まで自然に完了できる場合。

向いているケース:

- 小さく局所的な変更
- 強い逐次依存がある作業
- 分割すると説明・統合コストの方が大きい作業
- 同じコンテキストを保った方が一貫性が高い作業

multi-agent化できることを理由に分割しない。

## 2. Sequential Pipeline

前Taskの成果物を次Taskが利用する構造。

```text
A -> B -> C
```

向いているケース:

- 調査 -> 判断 -> 実装
- specification -> implementation -> verification
- implementation -> review -> correction

各境界では、次Taskが必要とする成果物を明示する。

会話履歴の継承をpipelineのinterfaceにしない。

## 3. Parallel Fan-out / Fan-in

独立Taskを並列に実行し、最後に統合する。

```text
      -> B -\
A ->  -> C ---> E
      -> D -/
```

向いているケース:

- 複数候補の独立調査
- interface確定後の分離実装
- サブシステムごとの分析
- 異なる観点からの独立検証

必要条件:

- fan-out前に共有前提が十分確定している
- write scopeや責務が衝突しない
- fan-in担当または統合方法が明確である
- 統合後の全体検証がある

## 4. Planner / Workers

分解・依存整理と、実際のTask実行を分離する。

```text
Planner
  |-- Worker A
  |-- Worker B
  `-- Worker C
```

向いているケース:

- 作業範囲が広く、最初にTask構造を明示する価値がある
- 異なる能力・ツール・変更範囲を割り当てたい
- 並列実行の調停が必要

避けるケース:

- Plannerの出力が実作業より重い
- 作業途中で分解が頻繁に無効になる
- 小さなTaskまで毎回Plannerを通す

Plannerは詳細な手順書ではなく、Goal、Task、dependency、boundary、verificationを定義する。

## 5. Producer / Verifier

成果物を作るTaskと、その成果物を検証するTaskを分離する。

```text
Producer -> Artifact -> Verifier
```

向いているケース:

- correctnessの確認が重要
- 実装者の前提を引きずらずに確認したい
- diff、テスト結果、仕様など検証対象を明確に渡せる

Verifierには必要以上のProducer会話履歴を渡さない。

同一Modelでもfresh contextと独立した評価基準を使えるなら価値がある。ただし機械検証できる項目まで人間的レビューへ置き換えない。

## 6. Bounded Repair Loop

検証失敗時だけ、修正と再検証を繰り返す。

```text
Produce -> Verify
             |
          fail
             v
           Repair
             |
             `----> Verify
```

必ず上限を持つ。

例:

- review 3 rounds
- retry 2 times
- 同じ失敗が2回続いたらre-plan
- budget超過で停止

同じ方法を繰り返して改善しない場合はretryではなく分解・前提・担当・検証方法を見直す。

## 組み合わせ

実際の作業では複数Topologyを組み合わせてよい。

例:

```text
            -> frontend -\
Plan -> Gate -> backend ---> Integrate -> Verify
            -> tests ----/                 |
                                          fail
                                           v
                                         Repair
```

ただし図が複雑になるほど良い設計ではない。

各NodeがTask Contractを持ち、各Edgeが必要な成果物の受け渡しとして説明できることを優先する。

## 選択基準

迷ったら次の順に確認する。

1. Singleで成立するか
2. 強い依存があるならSequentialで十分か
3. 独立Taskに時間短縮や品質向上の価値があるか
4. 作成と検証を分ける価値があるか
5. 失敗修正ループが必要か
6. PlannerやSupervisorを置くほど調停が必要か

複雑なTopologyへ進むには、追加構造による明確な利益が必要である。

## 異質性の考え方

複数実行主体の価値は、名前や人格の違いだけでは決まらない。

価値を生みやすい差には次がある。

- 異なる入力
- fresh context
- 異なる評価基準
- 異なるtool access
- 異なる専門知識
- 異なるModel特性
- 独立した証拠の取得経路

同じModelを使うこと自体は問題ではない。

重要なのは、同じ前提をそのまま反復するだけになっていないことである。

## Supervisorを置く判断

常駐SupervisorやOrchestratorは次が必要な場合に使う。

- 複数Taskの依存解除を判断する
- 実行結果から次Taskを動的に選ぶ
- budgetやretryを管理する
- fan-in時の統合を調停する
- failureから局所的に再計画する

単純な固定pipelineなら、状態機械や通常のworkflowで十分な場合がある。

LLM Orchestratorを使うこと自体を目的にしない。
