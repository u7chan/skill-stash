# Mechanical Checks

文章品質のうち、機械的に観測できるものと文脈判断が必要なものを分ける。

## Use deterministic checks for observable properties

次のような項目は、必要ならスクリプトや既存ツールで確認する。

- 極端に長い文や段落
- 同一語尾や同一パターンの過度な反復
- Markdown、URL、コード、パス、識別子の破損
- 禁止された表記や必須表記の欠落
- 見出し階層や箇条書き構造の崩れ
- ユーザーが明示した文字数、行数、形式上の制約

機械的に確認できる問題を、LLMの印象だけで判定しない。

## Keep contextual judgment in the model

次は単純なlint規則へ落とし込まない。

- 文が長いから悪い
- 読点が多いから悪い
- 箇条書きが多いから悪い
- 特定語があるからAI生成らしい
- 非生物主語だから不自然
- 同じ語尾が続いたら必ず直す

これらは文書種別、読者、意味、周辺文脈によって適否が変わる。

## Treat findings as signals, not automatic failures

機械的チェックの結果は、原則として修正候補を見つけるためのシグナルとして扱う。

固定閾値を普遍的な品質基準にしない。たとえば文長や箇条書き比率の閾値を使う場合でも、文書種別やユーザー指定に合わせて判断する。

検出結果があっても、意味保持や読みやすさの観点で変更価値がなければ KEEP とする。

## Prefer existing tools before adding a custom checker

既存のformatter、linter、Markdown validator、文字数検査などで確認できる場合はそれを使う。

専用スクリプトを追加するのは、繰り返し使う決定的な検査であり、手作業やLLM判断より再現性が高くなる場合に限る。
