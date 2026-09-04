# Mermaid

関係、時系列、分岐、状態を線で追う必要がある場合に使う。

## Diagram selection

- `sequenceDiagram`: API通信、イベント、複数主体の時系列
- `flowchart`: 処理フロー、条件分岐、データの流れ
- `stateDiagram-v2`: 状態と遷移
- `erDiagram`: エンティティと関係
- `classDiagram`: クラス・型の主要な関係

## Scope

1つの図は1つの問いへ答える。

「システム全体を全部載せる」より、ユーザーが理解したい経路・状態・関係だけを残す。

## Readability rules

- ノード名は短く役割が分かるものにする
- 補足文をノードへ詰め込みすぎない
- 線や分岐が増えすぎたら視点を分ける
- 実装詳細より境界と因果関係を優先する
- Mermaidで表現する意味がない単純なTreeはASCIIへ戻す

## Avoid decorative complexity

色、テーマ、特殊記法を理解に必要な場合以外は追加しない。

レンダリング上の見栄えより、コードを読んでも関係を追えることを優先する。
