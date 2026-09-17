# Replanning and Stop Conditions

再計画は、失敗したTaskを機械的に繰り返すことではない。

失敗した条件と影響範囲を特定し、必要な境界だけを変更する。

## まず失敗を分類する

### Execution failure

Taskの設計は妥当だが、実行に失敗した。

例:

- 一時的なtool error
- flaky test
- network failure
- command typo

同じ前提でretryしてよい可能性がある。

### Artifact failure

成果物がsuccess criteriaを満たしていない。

例:

- test failure
- requirement漏れ
- review finding
- interface mismatch

原因Taskを修正して再検証する。

### Contract failure

Task Contract自体が不足・矛盾している。

例:

- 必要なinputがなかった
- write scopeが狭すぎた
- success criteriaが判定不能だった
- outputに後続が必要な情報がなかった

retryより先にContractを修正する。

### Decomposition failure

Taskの分け方が現実の依存関係と合っていない。

例:

- 独立だと思ったTaskが同じ状態を変更する
- interface決定を待たずに並列化した
- 統合時に大量の再作業が発生した

Task graphまで戻って再分解する。

### Assumption failure

上流の前提が誤っていた。

例:

- 要件解釈が違った
- 利用可能だと思ったAPIが存在しない
- 技術制約が後から判明した

影響する下流Taskを無効化し、前提が成立する地点まで戻る。

## 影響範囲を追う

失敗したら次の順に確認する。

1. failed criterionは何か
2. 直接原因となるArtifactは何か
3. そのArtifactを作ったTaskは何か
4. そのTaskのContractは妥当か
5. そのArtifactを利用した後続Taskは何か
6. 上流の前提まで変更する必要があるか

最小の再実行範囲を選ぶ。

## RetryとRe-planを分ける

同じ入力・同じ手順で再実行して改善が見込めるならretry。

次のいずれかならre-planを検討する。

- 同種のfailureが繰り返される
- 追加情報で前提が変わった
- Task境界が原因で修正できない
- write conflictが繰り返される
- integration costが想定より大きい
- Verifierが同じ構造的問題を繰り返し指摘する

「もう一度やれば通るかもしれない」を無制限に続けない。

## Repair Loop

局所修正で対応できる場合はbounded repair loopを使う。

```text
Artifact
   |
 Verify
   |
  fail
   v
 Repair
   |
 Re-verify
```

Repair TaskにはVerifierの全会話ではなく、必要なfindingを渡す。

最低限:

- failed criterion
- evidence
- expected state
- affected scope

## 上流へ戻る条件

次の場合は局所修正を続けず上流へ戻る。

- requirementが矛盾している
- interfaceが成立していない
- 共通前提が誤っている
- 同じ箇所で複数Taskが競合している
- 成功条件そのものが現実的でない

戻る地点は必要最小限にする。

## 停止条件

オーケストレーションは停止できなければならない。

状況に応じて次を設定する。

### Success stop

- 必須success criteriaをすべて満たした
- 統合後検証がpassした
- blockerが残っていない

改善余地があっても、現在のGoalを満たしていれば終了してよい。

### Budget stop

- retry上限
- review round上限
- token / cost上限
- tool-call上限
- wall time上限

上限到達時は、成果物を捨てず現在地と未解決事項を返す。

### Escalation stop

次の場合は自律継続せず、判断材料をまとめて上位へ返す。

- 破壊的・不可逆な判断が必要
- 要件が矛盾して解消できない
- 必要な権限や情報がない
- 複数案に重大なtrade-offがあり、Task Contractから選べない
- budget内で収束しない

## 終了時に残すもの

成功・失敗にかかわらず、後続が再開できる形で残す。

- completed tasks
- generated artifacts
- verification results
- failed / unresolved criteria
- invalidated artifacts
- remaining risks
- recommended next boundary

失敗を会話の最後の一文だけに閉じ込めない。

## 過剰改善を止める

完了後に見つかった改善案は次へ分類する。

- 今回のsuccess criteriaに必要: 今回直す
- blockerではないrisk: 記録する
- unrelated improvement: Follow-upへ分離する

オーケストレーションの目的は「これ以上改善点がない状態」ではなく、定義したGoalへ確実に収束することである。
