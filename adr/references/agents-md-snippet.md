# AGENTS.md snippet

ADRを利用するrepositoryで、エージェント向けの入口が存在しない場合だけ追加する。

```markdown
## Architecture Decisions

設計判断は `docs/adr/` を参照する。

- `Accepted`: 現在有効
- `Proposed`: 検討中
- `Superseded`: 過去の判断

Accepted ADRとタスクが衝突する場合、迂回実装で無理に両立させず、衝突を明示してタスクまたはADRの見直しを判断する。
```

repository固有のADR pathやstatus conventionがある場合は、それに合わせて最小限だけ変更する。

ADR本文、背景説明、詳細な運用ルールは`AGENTS.md`へコピーしない。
