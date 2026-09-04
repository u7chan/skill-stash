# Text Visuals

ASCII、Tree、Code、Diffなど、テキストだけで完結する可視化を扱う。

## Use cases

- File Tree
- Component Tree
- Call Tree
- Dependency Tree
- ASCII Architecture
- Before / After
- Diff
- Pseudocode
- Annotated Code

## Principles

### Keep hierarchy explicit

親子関係や所有関係はインデントと枝で表す。

```text
App
├── API
│   ├── Auth
│   └── Users
└── Database
```

### Keep flows directional

短い処理フローは矢印で十分。

```text
Client -> BFF -> API -> DB
            |
            +-> Auth
```

複数の往復や並行処理が増えたらMermaid Sequenceを検討する。

### Use Diff for change

「何が変わったか」が主目的なら、完成形だけでなくDiffまたはBefore / Afterを優先する。

コード差分そのものが重要でない場合は、構造差分に簡略化してよい。

### Prefer meaningful labels

`A`、`B`、`C`のような抽象ラベルより、役割が分かる名前を使う。

### Do not force ASCII

線の交差、循環、状態遷移、複数主体の時系列が中心になると読みにくい。

その場合はMermaidへ切り替える。
