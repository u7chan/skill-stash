---
name: pi-herdr-launch-agent
description: pi経由でプロバイダー・モデル・thinkingレベルが指示されたら、その設定でpiをHerdrの新規ペインに起動する。
---

# Launch Agent

指定されたプロバイダー・モデル・thinkingレベルで、pi を Herdr の新規ペインに起動する。

## Preflight

```bash
test "${HERDR_ENV:-}" = 1 || exit 1
test -n "${HERDR_PANE_ID:-}" || exit 1
command -v herdr >/dev/null || exit 1
```

pane の確保・分割は Herdr スキルに従う。

## 1. 解決

指定されたプロバイダーに対応する reference だけを読む。

| 指定 | provider | reference |
| --- | --- | --- |
| codex | `openai-codex` | `references/codex.md` |
| opencode-go / OpenCode Go | `opencode-go` | `references/opencode-go.md` |
| deepseek / DeepSeek | `deepseek` | `references/deepseek.md` |

model の正規化はそのファイルに従う。

thinking（effort）は pi の `--thinking` に渡す。値は `off` / `minimal` / `low` / `medium` / `high` / `xhigh` / `max`。表記ゆれ（`xhight` など）は `xhigh` に補正する。

プロバイダー未指定、または model/thinking の値が読み取れない場合は勝手に補完せず確認する。プロバイダーのみ指定で model/thinking 未指定なら、`--provider` のみ指定して起動する。

## 2. 起動

```bash
herdr agent start <name> --kind pi --pane <pane-id> -- --provider <provider> --model <model> --thinking <level>
herdr pane rename <pane-id> <name>
```

- `<name>` は `^[a-z][a-z0-9_-]{0,31}$`、workspace 内一意の責任ベース名。
- 起動後 `herdr pane get <pane-id>` で kind と状態を確認する。

## 3. 報告

起動した pane ID・provider・model・thinking を報告する。タスク投入は `herdr agent prompt` を使う。
