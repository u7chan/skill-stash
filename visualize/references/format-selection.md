# Format Selection

理解したい対象から出力形式を選ぶ。

## Decision table

| 理解したい対象 | 第一候補 |
| --- | --- |
| ディレクトリ構成 | File Tree |
| コンポーネント構造 | Component Tree |
| 関数呼び出し | Call Tree |
| 単純な依存・関係 | ASCII Diagram |
| 実装変更 | Diff / Before-After |
| アルゴリズム | Pseudocode |
| コードの要点 | Annotated Code |
| API・サービス間通信 | Mermaid Sequence |
| 処理フロー | Mermaid Flowchart |
| 状態遷移 | Mermaid State |
| データ関係 | Mermaid ER |
| クラス関係 | Mermaid Class |
| UI・空間レイアウト | HTML |
| 複雑な比較レイアウト | HTML |
| 概念図・教育用ビジュアル | Image Generation |
| プレゼン・記事向け視覚資料 | Image Generation |

## Selection rules

### Prefer text-native when possible

構造、差分、短いフローはASCII / Tree / Code / Diffを優先する。

レンダラーがなくても読め、編集・引用もしやすい。

### Use Mermaid for relationships over time or state

時系列、分岐、状態遷移、複数ノードの関係を線で追う必要がある場合に使う。

単純な親子構造だけならTreeを優先する。

### Use HTML for layout, not ordinary diagrams

カード配置、ダッシュボード風比較、UIモックなど、空間的な配置そのものが意味を持つ場合に使う。

通常のフロー図をHTMLで再実装しない。

### Use image generation for human-facing visual communication

概念を直感的に伝える、資料に載せる、視覚的な比喩を使うなど、テキスト図より画像としての表現価値が高い場合に使う。

画像生成の利用条件は [image-generation.md](image-generation.md) に従う。

## Tie breaker

2つの形式が同程度に有効なら、次の順で選ぶ。

**理解しやすさ → 出力の軽さ → 編集しやすさ → 描画コスト → 装飾性**

「豪華に見える」ことだけを理由に重い形式を選ばない。
