---
name: visualize
description: 概念、システム、コード、変更、処理フローを「最も理解しやすい見せ方」に変換するときに使う。ユーザーに出力形式の選択を要求せず、ASCII/Tree/Code/Diff、Mermaid、HTML、画像生成から目的に十分な最軽量形式を選び、同じ情報の過剰な多重表現を避ける。
---

# Visualize

説明対象をそのまま文章で長く説明するのではなく、**何を理解したいか**を先に捉え、理解に必要な最小の視覚表現へ変換する。

ユーザーは ASCII、Mermaid、画像などの形式を指定する必要がない。形式が明示されていない場合は、このスキルが選ぶ。

## Core Principles

### Intent first

「何を描くか」より先に「何を理解したいか」を特定する。

例:

- 構造を知りたい
- 実行順序を知りたい
- 変更前後を比べたい
- 状態の遷移を追いたい
- UIの配置を見たい
- 概念を直感的に理解したい

### Lightest representation wins

同じ理解を得られるなら、より軽く単純な形式を選ぶ。

基本優先度:

1. ASCII / Tree / Code / Diff
2. Mermaid
3. HTML
4. Image Generation

ただし、用途に明らかに適した形式がある場合は順番に機械的に従わない。例えばAPI間の時系列通信はMermaid Sequenceを直接選んでよい。

詳細は [references/format-selection.md](references/format-selection.md) を参照する。

### One visual by default

同じ内容をASCII、Mermaid、画像の3種類で重複して出さない。

複数の視点が理解を明確に改善するときだけ複数形式を使う。単に「より親切そう」という理由で増やさない。

### Explain only what the visual needs

図の前後に長い説明を付けない。

必要なら以下だけ補足する。

- 図の読み方
- 重要な境界や前提
- 図では省略した重要事項

### Respect explicit format requests

ユーザーが出力形式を指定した場合は、その形式が実行可能で安全なら優先する。

指定形式が利用できない場合は、理由を短く伝え、最も近い代替形式を選ぶ。

## Workflow

### 1. Identify the understanding goal

ユーザーの依頼から、主目的を1つ選ぶ。

- structure
- interaction / execution
- change
- state
- data relationship
- spatial / UI layout
- conceptual / presentation

目的が複数ある場合でも、最初から全形式を生成せず、中心となる理解対象を優先する。

### 2. Select the representation

[references/format-selection.md](references/format-selection.md) に従い、目的を十分に伝えられる最軽量形式を選ぶ。

- text-native表現: [references/text-visuals.md](references/text-visuals.md)
- Mermaid: [references/mermaid.md](references/mermaid.md)
- HTML: [references/html-visuals.md](references/html-visuals.md)
- 画像生成: [references/image-generation.md](references/image-generation.md)

必要なreferenceだけ読む。全referenceを毎回読む必要はない。

### 3. Scope the visual

1つの図で伝える中心メッセージを決める。

完全なシステムを網羅するより、依頼された理解に必要な範囲へ絞る。

### 4. Generate

選んだ形式で可視化する。

構造や因果関係を優先し、装飾のためだけの情報を追加しない。

### 5. Verify readability

出力前に確認する。

- ラベルだけで意味を追えるか
- 不要なノードや線がないか
- 同じ情報を重複表現していないか
- 文章の方が簡単な内容を無理に図にしていないか
- 画像生成の場合、現在の環境で実際に生成可能か

## Guardrails

禁止する。

- ユーザーに毎回「ASCII / Mermaid / 画像のどれにするか」を選ばせる
- 5行程度のASCIIで十分な内容を巨大なMermaidへする
- 同じ情報を複数形式で繰り返す
- 完全性のためだけに図を肥大化させる
- 画像生成能力がないのに画像を生成したと装う
- 利用できない描画機能を推測で存在すると扱う
- 可視化と無関係な実装・設計変更までスコープを広げる

## Completion

可視化そのものを主成果物とする。

必要な場合だけ、選んだ形式や重要な省略事項を1〜2文で補足する。
