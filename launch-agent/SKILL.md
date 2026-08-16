---
name: launch-agent
description: pi経由で特定のプロバイダー・モデル・推論effortが指示されたら、対応するエージェントをHerdrの新規ペインに起動する。
---

# Launch Agent

指定されたエージェントを、モデル・推論effort付きで Herdr の新規ペインに起動する。cagent は使わず、`herdr agent start` へ native args を直接渡す。

## Preflight

```bash
test "${HERDR_ENV:-}" = 1 || exit 1
test -n "${HERDR_PANE_ID:-}" || exit 1
command -v herdr >/dev/null || exit 1
```

pane の確保・分割は Herdr スキルに従う。

## 1. 指定の正規化

| 指定 | 値 |
| --- | --- |
| codex | kind `codex` |
| opencode / opencode-go | kind `opencode` |
| gpt-5.6-sol / sol | model `gpt-5.6-sol` |
| gpt-5.6-luna / luna | model `gpt-5.6-luna` |
| DeepSeekFlash / DeepSeekFrash / deepseek flash / deepseek-v4-flash | model `deepseek-v4-flash` |
| DeepSeekPro / deepseek pro / deepseek-v4-pro | model `deepseek-v4-pro` |
| xhight / xhigh | effort `xhigh` |
| high | effort `high` |
| low | effort `low` |
| max | effort `max` |

agent 未指定、または model/effort の値が読み取れない場合は勝手に補完せず確認する。agent のみ指定で model/effort 未指定なら、引数なしで起動しエージェント側の既定設定を使う。

## 2. native args の組み立て

`herdr agent start --` の後ろへ渡す各argv。

codex:

```text
--model <model> -c 'model_reasoning_effort="<effort>"'
```

effort なしなら `--model <model>` のみ。`-c` の値は `model_reasoning_effort="<effort>"`（内側の二重引用符を含む1つのargv）。

opencode:

```text
--model opencode-go/<model>
```

model には `opencode-go/` を前置する。opencode の対話セッションは reasoning effort 非対応のため、effort が指定されていても渡さず model のみで起動し、その旨を報告する。

## 3. 起動

```bash
herdr agent start <name> --kind <kind> --pane <pane-id> -- <native-args...>
herdr pane rename <pane-id> <name>
```

- `<name>` は `^[a-z][a-z0-9_-]{0,31}$`、workspace 内一意の責任ベース名。
- 起動後 `herdr pane get <pane-id>` で kind と状態を確認する。

例:

```bash
# codex + gpt-5.6-sol + xhigh
herdr agent start cx-review --kind codex --pane <pane-id> -- --model gpt-5.6-sol -c 'model_reasoning_effort="xhigh"'

# opencode + deepseek-v4-flash（effort 指定は無視）
herdr agent start oc-worker --kind opencode --pane <pane-id> -- --model opencode-go/deepseek-v4-flash
```

## 4. 報告

起動した pane ID・agent kind・model・effort を報告する。タスク投入は `herdr agent prompt` を使う。
