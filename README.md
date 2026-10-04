# skill-stash

必要なときに参照・引用して使うスキルの保管場所です。その場の思い付きでカジュアルに追加しており、精度検証は未実施のため、グローバルスキルとしての導入は非推奨です。

## スキル一覧

カテゴリは目安です。境界が曖昧なスキルは、実際に使う場面に近い方へ置いています。カテゴリ内は名前順です。

| スキル名 | 概要 |
| --- | --- |
| **AIエージェント / LLMシステム** | エージェントの設計・診断・実行基盤 |
| [agent-ui-streaming](agent-ui-streaming/SKILL.md) | AIエージェントUIのリアルタイム通信をSSE基準で設計・実装する |
| [frontier-harness-diagnosis](frontier-harness-diagnosis/SKILL.md) | フロンティアモデル向けハーネスの過剰指示・常時ロード・停止条件を診断し、最小改善案を出す |
| [issue-pr-orchestrator](issue-pr-orchestrator/SKILL.md) | Issue実装からPRレビュー完了までを委譲・管理する |
| [orchestration-design](orchestration-design/SKILL.md) | 複雑な作業をTask・依存関係・検証条件へ分解し、必要最小限の実行トポロジーを設計する |
| [pi-herdr-launch-agent](pi-herdr-launch-agent/SKILL.md) | pi経由で指定されたプロバイダー・モデル・thinkingレベルでpiをHerdrに起動する |
| [rag-system-design](rag-system-design/SKILL.md) | RAGありきにせず、質問とデータの性質から知識取得方式を壁打ち・設計する |
| **開発 / 設計・品質** | 言語・フロントエンド・API・設計判断 |
| [adr](adr/SKILL.md) | 重要な技術判断を短いADRとして残し、必要に応じてAGENTS.mdから参照させる |
| [api-design](api-design/SKILL.md) | HTTP/Web APIをRFC・IETF仕様基準で設計・レビューする |
| [bundle-efficient-module-design](bundle-efficient-module-design/SKILL.md) | JS/TSのmodule boundaryをtree-shakingしやすく設計し、bundle削減を実測で検証する |
| [development-simplicity-review](development-simplicity-review/SKILL.md) | 社内・個人開発の開発中プロジェクトをKISSの観点でレビューし、不要な互換・移行・残骸・過剰実装を抑える |
| [frontend-engineering-baseline](frontend-engineering-baseline/SKILL.md) | TypeScriptフロントエンドの開発基盤を調査し、必要な品質・安全性・再現性を最小変更で整える |
| [llm-safe-ui-architecture](llm-safe-ui-architecture/SKILL.md) | LLMが生成・変更するUIの設計判断を実行可能な制約へ落とし込み、UI driftを防ぐ |
| [modern-go](modern-go/SKILL.md) | 対象Goバージョンに合わせてmodern idiomを選び、挙動を保った最小変更として適用する |
| [react-effect-discipline](react-effect-discipline/SKILL.md) | useEffectを外部システムとの同期に限定し、適切な代替・依存関係・cleanupを判断する |
| **基盤 / インフラ** | Docker・IaC・ローカル検証 |
| [docker-best-practices](docker-best-practices/SKILL.md) | Docker環境を計測して原因を特定し、build・runtime・storage・security・hostの必要な改善だけを安全に適用する |
| [terraform-aws-local](terraform-aws-local/SKILL.md) | Docker + FlociでAWS向けTerraform IaCを実AWSなしに段階的に設計・検証する |
| **AI活用 / 業務変革** | AI導入・業務設計・意思決定 |
| [ai-business-opportunity-finder](ai-business-opportunity-finder/SKILL.md) | 業界と自社の強みからAI事業化領域を探索する |
| [ai-impact-diagnosis](ai-impact-diagnosis/SKILL.md) | 仕事内容とAI活用状況からAI活用レベルを診断する |
| [ai-transformation-team-designer](ai-transformation-team-designer/SKILL.md) | 社内AI推進チームを事業成果に直結する形で設計する |
| [ai-workflow-redesign](ai-workflow-redesign/SKILL.md) | 業務フローをAI前提で再設計する |
| [company-decision-guide](company-decision-guide/SKILL.md) | 経営者の判断基準を整理し意思決定の補助線を作る |
| [daily-ai-work-orchestrator](daily-ai-work-orchestrator/SKILL.md) | 予定一覧から1日の生産性と仕事の質を最大化する |
| [meeting-to-actions](meeting-to-actions/SKILL.md) | 会議ログを次のアクションに使える形へ整理する |
| **表現 / 可視化** | 文章品質・図解 |
| [japanese-writing-quality](japanese-writing-quality/SKILL.md) | 日本語文書を意味と書き手の特徴を保ちながら、校正・自然化・執筆・構造推敲し、読解負荷と情報密度を改善する |
| [visualize](visualize/SKILL.md) | 理解したい対象から最適な可視化形式を選び、ASCII・Mermaid・HTML・画像生成へ振り分ける |
| **学習 / 実験** | 教育スキル・チュートリアル |
| [go-teacher](go-teacher/SKILL.md) | Goを構文暗記ではなくメンタルモデルから学習・解説・レビューする |
| [language-teacher-template](language-teacher-template/SKILL.md) | プログラミング言語向け教師スキルをメンタルモデル中心で設計する |
| [tutorial-muska-roleplay](tutorial-muska-roleplay/SKILL.md) | ムスカ大佐になりきり、知的かつ尊大な口調で受け答えする |
| [tutorial-reverse-string](tutorial-reverse-string/SKILL.md) | 入力された文字列を厳格に逆順変換し結果のみを出力する |
| [tutorial-zundamon-roleplay](tutorial-zundamon-roleplay/SKILL.md) | ずんだもんになりきり、元気で分かりやすく受け答えするのだ |
