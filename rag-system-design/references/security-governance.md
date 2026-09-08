# 権限・安全性・ガバナンス

企業内資料や非公開情報を扱うRAGでは、検索精度より先に誰が何を検索できるかを設計する。

## 権限は検索前に適用する

避ける流れ:

全資料から検索
→ LLMへ渡す
→ 回答時に隠す

推奨する流れ:

利用者の権限を確定
→ 権限範囲内だけを検索
→ LLMへ渡す

LLMに渡した時点で情報露出が起きたものとして扱う。

## 権限の単位

必要に応じて設計する。

- tenant
- organization
- team
- project
- document
- row
- classification
- user / group

元システムの権限モデルと検索index側の権限表現を対応させる。

## 権限変更

閲覧権限を外した後も古いindexから検索できる状態を残さない。

確認する。

- 権限変更の反映時間
- user / group同期
- cache
- 再indexの必要性
- 退職・異動・tenant削除

## 機密情報・個人情報

取り込み前に確認する。

- index化してよい情報か
- embedding providerへ送信してよいか
- 保存地域
- 保存期間
- ログに残る内容
- 削除要求へ対応できるか
- backupからの削除要件

検索できるから入れてよいとは考えない。

## Retrieved Prompt Injection

検索した文書も信頼できる命令とは限らない。

文書中にsystem promptの無視、秘密の表示、外部送信、tool実行などを求める文章があっても、資料内容として扱い、システム命令へ昇格させない。

外部から取り込む資料ほど注意する。

## Poisoned Documents

悪意ある文書や誤った資料がindexへ混入すると、検索精度が高くても答えは誤る。

対策候補:

- 取り込み元を限定する
- source provenanceを保持する
- 承認済み資料を区別する
- 文書状態をmetadata化する
- 低信頼sourceを回答根拠に使わない
- 重要回答は複数根拠を要求する

## Citation / Provenance

回答から原文へ辿れるようにする。

最低限:

- source
- document id
- version
- section / chunk
- 更新日時

重要判断では、どの正本のどの記述を使ったかを確認できるようにする。

## Logging

監査に必要な範囲で記録する。

候補:

- user
- query
- selected route
- filters
- retrieved document ids
- answer
- citations
- model / prompt version
- index version

ログ自体が機密情報の複製になるため、保存範囲と期間を決める。

## 最低限の確認

- 権限外文書を検索できない
- 権限変更が反映される
- 削除要求をindexまで反映できる
- 文書中の命令をsystem instructionとして扱わない
- 回答から根拠へ辿れる
- ログに不要な機密情報を残さない
- tenant間で検索結果が混ざらない
