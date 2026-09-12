# 改善パターン

診断で問題を見つけたとき、削除だけを選ばず、最も小さい変更で改善する。

## 1. 広すぎるSkill descriptionを発火条件へ変える

### Before

```text
API、DB、認証、デプロイなどバックエンド開発全般で使う。
```

### After

```text
API契約の追加・変更、または既存APIの互換性をレビューするときに使う。
```

機能紹介ではなく「いつ読み込むか」を書く。

## 2. Always readを条件付き参照へ変える

### Before

```text
作業前に architecture.md、database.md、deployment.md をすべて読む。
```

### After

```text
サービス境界を変更するときは architecture.md を読む。
schemaを変更するときは database.md を読む。
deploymentへ影響するときは deployment.md を読む。
```

常時コンテキストから、必要時の遅延ロードへ移す。

## 3. 詳細recipeをGoal / Constraints / Boundary / Doneへ変える

### Before

```text
1. ファイル一覧を取得する
2. READMEを読む
3. 実装ファイルを読む
4. テストを読む
5. 修正する
6. テストする
```

### After

```text
Goal: Issueの要求を実装する。
Constraints: public APIを壊さず、無関係なrefactorをしない。
Boundary: 本番操作や破壊的変更は行わない。
Done: 要求を満たし、変更に必要な検証が通っている。
```

順序そのものが重要でない部分はモデルへ任せる。

## 4. 全テスト強制をリスクベースへ変える

### Before

```text
変更後は必ずlint、unit、integration、e2e、buildをすべて実行する。
```

### After

```text
変更を証明するために必要な検証を行う。
リポジトリで必須の品質ゲートは省略しない。
```

ただしCI契約、release gate、規制要件など、プロジェクトとして必須の検証は残す。

## 5. 広すぎるapprovalを安全境界へ変える

### Before

```text
ファイル変更やコマンド実行の前に必ず確認する。
```

### After

```text
通常のソース編集、formatter、local testは確認不要。
本番操作、破壊的変更、secret変更、課金を伴う操作は確認する。
```

「何をしてよいか」と「どこで止まるか」を両方示す。

## 6. Skill本体の知識をReferenceへ分離する

### Before

```text
SKILL.mdに設計、実装、テスト、運用、例外処理をすべて記載する。
```

### After

```text
SKILL.md
  -> 状況を判断
  -> 必要なreferenceだけ読む

references/
  design.md
  testing.md
  operations.md
```

分割単位は文書サイズではなく、判断や作業の境界で決める。

## 7. 重複する一般則を削る

### Before

各Skillに次が繰り返される。

```text
まずコードを読む。
エラーを確認する。
変更後はテストする。
```

### After

モデルが通常判断できる一般則なら削除する。
リポジトリ固有の例外がある場合だけ、その例外を書く。

## 8. 不明瞭なDoneを完了証明へ変える

### Before

```text
機能を実装する。
```

### After

```text
要求を実装し、今回の変更に必要な検証を行う。
変更起因のfailureがあれば修正して再検証し、要求を満たす状態まで進める。
```

Howより、どの状態まで進めれば完了かを明確にする。

## 9. モデル固有補正を分離する

### Before

```text
必ず最後まで自律的に進めること。
```

この指示が特定モデルの停止しやすさを補うためだけに追加されている。

### After

一般のDone条件は共通ハーネスへ残し、モデル固有の補正が本当に必要なら別設定・別Referenceへ分離する。

## 10. 全面改修を局所改善へ変える

ハーネス診断はリファクタリング競争ではない。

問題が1箇所なら1箇所だけ直す。変更前後で効果を比較できない大規模な書き換えは避ける。
