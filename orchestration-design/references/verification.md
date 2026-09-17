# Verification Design

検証は、成果物がsuccess criteriaを満たしたことを確認する工程である。

「reviewerを置くこと」自体を検証とみなさず、何をどの証拠で判定するかを先に決める。

## 検証の優先順位

可能なら次の順に使う。

1. 機械的に判定できる検証
2. 再現可能な確認手順
3. 独立したレビュー
4. 作成者自身の確認

上位で判定できる項目を、下位の曖昧な判断だけに置き換えない。

## 機械検証

例:

- unit / integration / e2e test
- type check
- lint
- schema validation
- build
- static analysis
- benchmark threshold
- snapshot / golden test

機械検証は高速で再現しやすいが、要件自体が間違っていれば正しくても失敗を見逃す。

「テストが通った」だけで、要求適合まで証明したとはみなさない。

## 再現可能な確認

自動化しにくいが、同じ手順で他者が確認できるもの。

例:

- 特定入力に対するCLI出力
- UI操作手順と期待状態
- API request / response
- before / after measurement

確認手順と期待結果を残す。

## 独立レビュー

独立レビューが有効なのは、作成Taskが持つ前提や見落としを別の入力境界で確認できる場合である。

Verifierへ渡すものは必要最小限にする。

例:

- requirement
- diff / patch
- public contract
- test result
- known constraints

Producerの長い会話履歴や自己評価は、必要な理由がなければ渡さない。

## 独立性の強さ

独立性は二値ではない。

強くなりやすい要素:

- fresh context
- 独立したsuccess criteria
- 別の証拠取得経路
- 異なるtool access
- 異なる専門観点
- 必要なら異なるModel

弱い例:

- 同じ会話の末尾で「reviewerとして再確認」する
- Producerの結論をそのまま要約する
- 何を見るか定義せず「問題がないか確認」だけ依頼する

同一Modelでも、fresh contextと入力境界を分ければ検証価値は得られる場合がある。

## Verification Contract

Verifierには最低限、次を定義する。

- target: 何を検証するか
- criteria: 何を満たす必要があるか
- evidence: 何を根拠として使えるか
- output: pass / fail / blocked と理由
- scope: 今回確認しないこと

例:

```yaml
target: pull-request-diff
criteria:
  - issue requirements are satisfied
  - no correctness regression is introduced
  - required tests exist and pass

evidence:
  - issue
  - diff
  - test-result

output:
  - status
  - findings
  - failed-criteria
  - evidence
```

形式は固定しない。

## 観点別レビュー

複数Verifierを並列化する場合、同じ「総合レビュー」を複製するより、異なる検証責務へ分ける。

例:

- correctness
- security
- performance
- API compatibility
- accessibility

ただし、各観点が小さすぎる場合は1つのVerifierへまとめる。

## Findingの品質

修正が必要な指摘には、可能な範囲で次を含める。

- failed criterion
- affected artifact / location
- observed evidence
- expected state
- severityまたはblockerかどうか

単なる好みや改善案を、完了を妨げるfailureと混同しない。

## 統合後の検証

並列Taskでは個別検証だけで終わらない。

fan-in後に次を確認する。

- build / test
- interface consistency
- merged behavior
- cross-component regression
- requirement coverage

個別Taskがpassでも、統合時に壊れる可能性がある。

## 停止判定

Verifierは「もっと良くできる」を理由に無限に修正を要求しない。

次を分ける。

- success criteriaを満たすために必要な修正
- riskとして残すべき事項
- follow-upで扱う改善

完了条件を満たし、blockerがなければ現在のTaskを終了できるようにする。
