# 構成パターン

実装製品ではなく、質問の性質から構成を考えるための例。

そのまま採用せず、不要な段は削る。

## 1. 文書検索

主な質問が「探す」の場合。

User
→ Query
→ Hybrid Search
→ Rerank
→ LLM
→ Answer + Citation

向いている:

- 社内文書検索
- FAQ
- 手順書
- 仕様書
- 過去問い合わせ

## 2. 全文コンテキスト

資料が小さく、全体を読む質問が多い場合。

Documents
→ Context
→ LLM
→ Answer

RAGのindex運用を持たずに成立するなら、その方が単純。

## 3. その場検索

更新が速い正本をその場で探す。

User
→ Agent
→ file search / grep / DB / API
→ sourceを読む
→ Answer

コード、頻繁に更新されるファイル、正確な識別子検索などで有力。

## 4. RAG + 集計

知識検索と数値集計が混在する。

User
→ Router
→ 知識検索: RAG → LLM
→ 数値集計: Semantic Layer / SQL

売上や利用者数などの定義はSQL生成時に毎回発明させず、あらかじめ固定する。

## 5. RAG + 履歴ストア

通常検索と過去時点の問い合わせが混在する。

User
→ Router
→ 通常検索: RAG
→ 過去時点: Temporal Store

検索indexに古い文書を残すだけでは履歴管理の代わりにならない。

## 6. 階層要約

全体傾向を繰り返し問い合わせる。

Raw Documents
→ Document Summaries
→ Group Summaries
→ Global Summary
→ LLM

上位要約から下位の根拠へ辿れるようにする。

## 7. 複合型の知識システム

複数種類の質問を1つの入口で扱う。

User
→ Question Router
→ RAG
→ SQL
→ Temporal Store
→ Direct Search
→ Whole-corpus / Summary

ルーターは単なる分類器ではなく、必要なら質問を複数タスクへ分解する。

例:

「この半年で増えた障害の原因について、過去の議論を調べて」

1. SQLで障害増加を特定
2. 対象カテゴリを決める
3. RAGで関連議論を検索
4. 必要なら時系列順に整理

## 構成を増やす順序

最初から複合構成にしない。

1. 代表質問を分類する
2. 最も多い質問型を最小構成で成立させる
3. 評価する
4. 解けない質問型だけ別経路を追加する
5. 必要になってからRouterを導入する

複雑さは要件から増やし、将来使うかもしれないという理由では増やさない。
