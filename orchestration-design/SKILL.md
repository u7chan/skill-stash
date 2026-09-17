---
name: orchestration-design
description: 複雑な作業を複数タスクや複数エージェントへ分解するとき、並列化・役割分担・成果物の受け渡し・統合・検証・再計画を設計するときに使う。エージェント数を増やすことを目的にせず、依存関係と完了条件から必要最小限の実行トポロジーを選ぶ。
metadata:
  guidance-as-of: "2026-09"
  last-reviewed: "2026-09-17"
---

# Orchestration Design

複雑な作業を、検証可能なタスクと依存関係へ分解し、必要な部分だけ委譲・並列化する。

目的はエージェント数や工程数を増やすことではない。最小の構造で作業を前へ進め、途中成果を検証しながら完了条件へ収束させる。

## 基本原則

- 単一の実行主体で十分なら、オーケストレーションを追加しない。
- 先にTaskを設計し、その後でAgent・Model・Toolを割り当てる。
- 実行順序は役割名ではなく依存関係から決める。
- 並列化は独立性と統合コストの両方を確認してから行う。
- タスク間では会話履歴より、明示した成果物を境界として使う。
- 重要な成果物は、作成と検証を可能な範囲で分離する。
- 並列作業の完了と、統合後の全体完了を分けて考える。
- 失敗時は影響範囲だけを再計画し、無条件に全体をやり直さない。
- retry・review・改善ループには停止条件を持たせる。

## 設計の進め方

### 1. 完了条件を決める

最初に「何が成立すれば終わりか」を確認する。

最低限、次を明確にする。

- 成立させたい結果
- 必須成果物
- 検証方法
- 変更してよい範囲
- 失敗時に許容できないこと

完了条件が曖昧なまま、ロールやエージェント構成から決め始めない。

### 2. 検証可能なTaskへ分解する

作業を、独立して説明・実行・確認できるTaskへ分ける。

各Taskには必要な範囲で次を持たせる。

- objective
- dependencies
- inputs
- allowed actions
- write scope
- success criteria
- outputs
- limits

Task Contractの詳細は `references/task-contract.md` を参照する。

Taskを細かくしすぎない。単独では意味のある成果や検証条件を持てない分割は避ける。

### 3. 依存関係と競合を整理する

Task同士について次を確認する。

- 前提となる成果物は何か
- 一方の判断結果を待つ必要があるか
- 読み書きする対象が重なるか
- 同じ共有状態を更新しないか
- 同時実行した場合に統合が難しくならないか

依存がないTaskを並列候補にするが、依存がないだけで並列実行を決めない。

詳細は `references/dependency-and-parallelism.md` を参照する。

### 4. 実行トポロジーを選ぶ

Task構造に合う最小の実行形を選ぶ。

候補には次がある。

- single: 1つの実行主体で完結する
- sequential: 前工程の成果を次工程へ渡す
- parallel fan-out / fan-in: 独立Taskを並列実行して統合する
- planner / workers: 分解と実行を分離する
- producer / verifier: 作成と独立検証を分離する
- bounded repair loop: 検証失敗時だけ局所修正する

必要なら組み合わせるが、固定の構成を最初から当てはめない。

選択基準は `references/topology-selection.md` を参照する。

### 5. 成果物を受け渡し境界にする

後続Taskには、必要な成果物と判断材料だけを渡す。

例:

- patch / diff
- test result
- investigation result
- specification
- decision record
- structured findings
- unresolved issues

前段の会話全文や推論履歴をそのまま継承することを前提にしない。

必要な前提が成果物に含まれていなければ、Task Contract側を改善する。

### 6. 統合点を明確にする

複数成果物をまとめる場合は、統合を独立した責務として扱う。

統合時には少なくとも次を確認する。

- 成果物同士の矛盾
- 重複変更
- interface / contractの不整合
- 前提条件の違い
- 統合後のテスト・検証
- 未解決事項

複数Taskが成功していても、統合後の検証が通るまでは全体成功としない。

### 7. 作成と検証を分離する

重要な成果物では、作成者自身の自己評価だけで完了判定しない。

優先する証拠は次の順とする。

1. 機械的に判定できる検証
2. 再現可能な確認手順
3. 独立したレビュー
4. 作成者自身の確認

同じModelを使う場合でも、入力・コンテキスト・評価基準を分離することで検証価値が高まる場合がある。

一方、役割名だけを変えて同じ前提を追認する構成は独立検証として弱い。

詳細は `references/verification.md` を参照する。

### 8. 失敗時は局所的に再計画する

検証に失敗したら、まず失敗した条件と影響範囲を特定する。

- どのsuccess criteriaが失敗したか
- どのTaskまたは成果物が原因か
- どの後続Taskが影響を受けるか
- 上流の前提まで戻る必要があるか

修正可能なら関係Taskだけを再実行する。

前提・分解・interface自体が崩れている場合は、必要な地点まで戻って再計画する。

詳細は `references/replanning.md` を参照する。

### 9. 停止条件を適用する

retry、review、改善を無制限に続けない。

必要に応じて次を上限として持つ。

- retry count
- review rounds
- token / cost budget
- tool-call budget
- wall time
- unresolved issue threshold

成功条件を満たした後の追加改善は、現在のTaskへ混ぜずFollow-upとして分離する。

## 設計結果のまとめ方

必要な項目だけ使う。

### Goal

- 成立させたいこと:
- 完了条件:

### Tasks

| Task | Objective | Dependencies | Outputs | Success criteria |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### Execution

- 選択したトポロジー:
- 並列実行するTask:
- 逐次実行するTask:
- 統合ポイント:

### Verification

- 機械検証:
- 独立検証:
- 統合後検証:

### Re-plan / Stop

- 再計画条件:
- retry上限:
- 停止条件:

## 参照先

必要なものだけ読む。

| 状況 | 参照先 |
| --- | --- |
| Taskの入出力と完了条件を定義したい | `references/task-contract.md` |
| 並列化できるか判断したい | `references/dependency-and-parallelism.md` |
| 実行構造を選びたい | `references/topology-selection.md` |
| 検証担当や証拠を設計したい | `references/verification.md` |
| 失敗時の再実行範囲を決めたい | `references/replanning.md` |

## 避けること

- multi-agent化そのものを目的にする
- Agentの役割名からTask構造を逆算する
- 依存関係のある作業を無理に並列化する
- 書き込み競合をworktreeやbranchだけで解決したことにする
- Task間で不要な会話履歴を丸ごと引き継ぐ
- 成果物と完了条件を定義せず委譲する
- 複数成果物の統合責任を曖昧にする
- reviewerという名前だけで独立性があるとみなす
- 検証できないTaskを大量に作る
- 失敗のたびに全工程を最初からやり直す
- review / fix / improveを無制限に繰り返す
- 完了条件を満たした後も同じTaskで改善を続ける
