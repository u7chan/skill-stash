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
確実に遮断すべき操作はPermissionやHookなどでも止める。
```

「何をしてよいか」と「どこで止まるか」を両方示す。promptはSoft guardとして使い、失敗時の影響が大きい境界だけHard guardを追加する。

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

## 7. 重複する一般則を正本へ集約する

### Before

各Skillに次が繰り返される。

```text
まずコードを読む。
エラーを確認する。
変更後はテストする。
```

または、ツールの使い方をAGENTS.mdとTool descriptionの両方に書いている。

### After

モデルが通常判断できる一般則なら削除する。
残す必要がある情報は、役割に合う場所を正本にする。

```text
常時必要な境界・罠 -> AGENTS.md / CLAUDE.md
作業手順 -> Skill
詳細仕様・判断材料 -> Reference / ADR
ツールの使い方 -> Tool description / interface
機械的規約 -> formatter / linter / CI
```

同じ情報を複数箇所へコピーせず、必要なら正本への入口だけ残す。

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

## 11. 自明な説明を常時コンテキストから外す

### Before

```text
このリポジトリはTypeScriptを使う。
src/にソースがあり、tests/にテストがある。
formatterは設定ファイルに従う。
```

### After

コードや設定からその場で確認できるなら削除する。
代わりに、見ても分からない情報だけ残す。

```text
legacy/ は移行途中のため、明示的な依頼なしに変更しない。
CIでは通常と異なる環境変数が必要なので、integration test時はscripts/test-integrationを使う。
```

情報量を減らすことではなく、モデルが自力で導出できない情報へコンテキストを使う。

## 12. 強い禁止を判断基準へ変える

### Before

```text
コメントを書かない。
既存コードを絶対に変更しない。
必ず最小差分だけにする。
```

### After

```text
周囲のコードのコメント密度・命名・イディオムに合わせる。
要求に必要な範囲で変更し、無関係なrefactorは避ける。
既存の設計意図を保ちながら、要求を満たす最小限の変更を優先する。
```

強い語を弱くすることが目的ではない。何を防ぎたいかを判断可能な基準として残す。

不可逆操作、外部送信、本番反映、課金、契約上の禁止など、例外を認めない境界は禁止形のまま残す。
