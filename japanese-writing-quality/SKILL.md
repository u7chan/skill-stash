---
name: japanese-writing-quality
description: 日本語文書を校正、自然化、執筆、構造推敲、診断、比較するときに使う。事実・意図・不確実性・書き手の特徴を保ちながら、読解負荷、情報密度、走査性、論理の明晰さを改善する。誤字脱字だけを直したい、AI生成らしい不自然さを減らしたい、文章を読みやすく組み直したい、新規文書を書きたい、複数案を比較したい依頼に対応する。
---

# Japanese Writing Quality

日本語文書を「きれいにする」のではなく、読者に必要な品質へ整える。

スタイル上の好みだけで文章を一括改稿しない。問題がない箇所は保持し、意味・事実・判断の強さを守ったまま、説明可能な価値がある変更だけを行う。

## Core Principles

### Preserve meaning before style

事実、数値、固有名詞、日時、条件、制約、因果関係、不確実性、必須・任意、判断や主張の強さを勝手に変えない。

元文にない経験、実績、感情、理由、主体、成果を「自然さ」のために補わない。

詳細は [references/preservation.md](references/preservation.md) を参照する。

### Default to KEEP

「もっと整えられる」「別の言い方もできる」は変更理由ではない。

候補箇所は原則として保持し、読解負荷、誤読、情報到達、論理関係、不自然さのいずれかを明確に改善できる場合だけ変更する。

詳細は [references/selective-revision.md](references/selective-revision.md) を参照する。

### Fix reader cost, not stylistic preference

判断基準は、書き手やモデルの好みではなく読者が負担するコストとする。

読者が文構造を頭の中で組み直す、参照先を探す、不要な前置きを読む、同じ主張を再解釈する、といった負荷を優先して下げる。

### Structure before sentences

広い推敲や新規執筆では、次の順で扱う。

1. 文書構造
2. 段落
3. 文
4. 語句

文を磨いた後で大きく構造を変える作業を避ける。

### Stop when further edits add no clear value

品質改善そのものを目的化しない。

明確な未解決問題がなく、修正が新しい問題を生んでおらず、追加変更の価値を説明できなくなったら終了する。固定点数を満たすための反復は行わない。

## Resolve the mode

依頼内容から作業モードを決める。境界は [references/modes.md](references/modes.md) を参照する。

- **proofread**: 誤字脱字、文法、明確な表記上の誤りだけを最小修正する。
- **naturalize**: 意味と構造を大きく変えず、不自然な日本語やAI生成らしい癖を改善する。
- **revise**: 段落や節の順序を含めて構成・論理・読みやすさを推敲する。
- **write**: ユーザー提供の材料から新規文書を書く。
- **diagnose**: 本文を書き換えず、問題と改善方針だけを返す。
- **compare**: 複数案を同じ基準で比較し、用途に応じた選択基準を示す。

複数の意図がある場合は、最も広い変更を許可されたモードで作業し、最後に狭い観点で点検する。

依頼が曖昧なら、意味と構造を変えない狭いモードを選ぶ。

## Load only relevant references

すべてのreferenceを毎回読まない。モードと問題に必要なものだけ読む。

- モード境界: [references/modes.md](references/modes.md)
- 保護対象: [references/preservation.md](references/preservation.md)
- 校正: [references/proofreading.md](references/proofreading.md)
- 自然化: [references/naturalization.md](references/naturalization.md)
- 読解負荷: [references/readability.md](references/readability.md)
- 構造: [references/structure.md](references/structure.md)
- 新規執筆: [references/writing.md](references/writing.md)
- 選択的改稿: [references/selective-revision.md](references/selective-revision.md)
- 文書種別: [references/document-types.md](references/document-types.md)
- 最終品質判定: [references/quality-gate.md](references/quality-gate.md)
- 出力契約: [references/output.md](references/output.md)
- 境界例: [references/examples.md](references/examples.md)

## Workflow

### 1. Understand

最低限、次を把握する。

- 読者
- 目的
- 文書種別
- 許可された変更範囲
- 出力形式
- 保護すべき事実・表記・リテラル

不足情報があっても安全に暫定版を作れるなら、推測せずに進める。意味が決まらない場合だけ確認する。

### 2. Inspect

元文または材料から次を特定する。

- 中心メッセージ
- 事実、観測、推測、意見、決定
- 条件、制約、不確実性
- Markdown、コード、URL、パス、コマンド、識別子
- 書き手に固有の自然な言い回しやリズム

### 3. Classify candidates

修正候補を次の4つで判断する。

- **KEEP**: 問題がない。好みだけの変更はしない。
- **FIX**: 局所変更で明確に改善できる。
- **RESTRUCTURE**: 段落・節の構造変更が必要。revise / write でのみ実施する。
- **ASK**: 材料不足で安全に直せない。

### 4. Revise from high impact to low impact

広い変更が許可されている場合は、構造 → 段落 → 文 → 語句の順で直す。

局所モードでは許可された範囲を越えない。

### 5. Run the final pass

変更後に必要な範囲で次を確認する。

- スケルトンだけで論旨が追えるか
- 読解負荷の高い箇所が残っていないか
- 不要な前置きや重複が残っていないか
- 必要情報へ早く到達できるか
- 主張・根拠・条件・因果が追えるか
- 元文の意味や書き手の特徴を壊していないか

詳細は [references/quality-gate.md](references/quality-gate.md) を参照する。

### 6. Return only what the user needs

成果物を先に返す。

診断や比較だけを求められた場合は本文を書き換えない。変更理由は重要なものだけに絞る。

詳細は [references/output.md](references/output.md) を参照する。
