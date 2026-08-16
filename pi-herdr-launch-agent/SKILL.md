---
name: pi-herdr-launch-agent
description: pi経由で特定のプロバイダー・モデル・推論effortが指示されたら、対応するエージェントをHerdrの新規ペインに起動する。
---

# Launch Agent

pi経由で指定されたプロバイダー・モデル・推論effortに解決し、対応するエージェントを Herdr の新規ペインに起動する。

## Preflight

```bash
test "${HERDR_ENV:-}" = 1 || exit 1
test -n "${HERDR_PANE_ID:-}" || exit 1
command -v herdr >/dev/null || exit 1
```

pane の確保・分割は Herdr スキルに従う。

## 1. 解決

プロバイダー・モデル・推論effort の正規化と native args の組み立ては `references/providers.md` に従う。

agent 未指定、または model/effort の値が読み取れない場合は勝手に補完せず確認する。agent のみ指定で model/effort 未指定なら、引数なしで起動しエージェント側の既定設定を使う。

## 2. 起動

```bash
herdr agent start <name> --kind <kind> --pane <pane-id> -- <native-args...>
herdr pane rename <pane-id> <name>
```

- `<name>` は `^[a-z][a-z0-9_-]{0,31}$`、workspace 内一意の責任ベース名。
- 起動後 `herdr pane get <pane-id>` で kind と状態を確認する。

## 3. 報告

起動した pane ID・agent kind・model・effort を報告する。タスク投入は `herdr agent prompt` を使う。
