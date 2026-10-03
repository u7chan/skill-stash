---
name: adr
description: 実装・設計・レビューで、将来「なぜそうしたか」を失うと再議論や誤った巻き戻しが起きる技術判断を検出し、必要なときだけ短いArchitecture Decision Record（ADR）を作成・更新する。必要に応じてAGENTS.mdにはADRへの最小限の入口だけを追加する。
---

# ADR

ADRは実装履歴ではなく、**現在有効な重要判断と理由**を短く残すための記録である。

目的は文書を増やすことではない。人間やAIエージェントが、背景を知らずに重要な設計判断を推測・巻き戻すことを防ぐ。

## 原則

- ADRは必要な判断だけ残す
- 原則 `1 decision = 1 file`
- ADR本文は短く保つ
- 現在の判断と理由を中心に書く
- 変更履歴や議論ログはGit、Issue、PRへ任せる
- `AGENTS.md` は薄く保ち、ADR本文を重複させない

## ADRを作る判断

次のような、コードだけでは理由を復元しづらい重要判断をADR候補とする。

- system boundary、data ownership、storage、integration、auth/security、deploymentなどの横断方針
- 複数の妥当な選択肢から、意図的なtrade-offで選んだ設計
- 主要dependency、runtime、framework、serviceの採用・置換
- repository全体や今後の実装を制約する方針
- 将来の人間やAIが善意で「単純化」「cleanup」して戻しそうな判断
- 既存ADRの判断を変更・廃止・置換する場合

次は原則ADRにしない。

- bug fix
- UI styling、copy、formatting
- test-only change
- 局所的で容易に戻せるrefactor
- 既存ADRや明文化済み方針に従うだけの実装
- 短命なspike / experiment

迷ったら、「半年後にコードだけで理由を復元できるか」「背景を知らないAIが誤って戻しそうか」で判断する。

## Workflow

### 1. 既存ルールを確認する

最初に既存のADR、`AGENTS.md`、README、CONTRIBUTINGなどを確認する。

既存conventionがあれば優先する。なければ既定値として次を使う。

```text
docs/adr/NNNN-kebab-case-title.md
```

### 2. 判断を1つに絞る

ADRを書く前に次だけ確定する。

- Context: なぜ判断が必要か
- Decision: 何を決めたか
- Consequences: 何を得て、何を受け入れるか

独立した判断が複数あるなら分ける。

### 3. 最小限で書く

`references/template.md` を使う。

背景説明、alternatives、見直し条件は、判断の理解に必要な場合だけ追加する。

実装手順、TODO、PR差分、長い議論履歴をADRへ入れない。

### 4. AGENTS.mdは入口だけにする

エージェントがADRの存在や扱いを知らない場合だけ、`AGENTS.md` に短い入口を追加する。

`references/agents-md-snippet.md` を参考にし、次だけ伝える。

- ADRの場所
- statusの意味
- Accepted ADRとタスクが衝突した場合の行動

ADRの内容や詳細ルールを`AGENTS.md`へコピーしない。

### 5. 衝突を無理に回避しない

statusは既存conventionを優先する。既定では次のように扱う。

- `Accepted`: 現在有効な判断
- `Proposed`: 検討中。実装上の拘束力はない
- `Superseded`: 過去の判断。現在の実装を制約しない

タスクとAccepted ADRが衝突する場合、ADRを守るためだけの迂回実装や不要な抽象化を追加しない。

衝突を明示し、タスクまたはADRのどちらを見直すべきか判断する。根拠が不足する場合だけ人間に確認する。

## 更新ルール

- amendmentやchangelogをADR本文へ積み上げない
- 意味の変わらない修正を除き、Accepted ADRを過去ログ化しない
- 判断が変わる場合は既存conventionに従う
- conventionがなければ新しいADRを作り、旧ADRを`Superseded`にする
- 同じルールを複数ADRや`AGENTS.md`へ重複記載しない

## 完了確認

- Decisionを1文で説明できる
- ADRが1つの判断に集中している
- 判断理由より実装詳細の方が長くなっていない
- 不要な履歴や議論ログがない
- statusが現在の扱いと一致している
- Accepted ADRとの衝突を隠していない
- `AGENTS.md` を更新した場合、詳細を重複させていない

ADRを作成・更新した場合は、判断とfile pathだけ簡潔に報告する。
