# Providers

プロバイダーごとの正規化と native args の組み立て。サポートするプロバイダーが増えるごとにこのファイルを更新する。

## Agent kind

| 指定 | `--kind` |
| --- | --- |
| codex | `codex` |
| opencode / opencode-go | `opencode` |

## Model の正規化

| 指定 | model |
| --- | --- |
| gpt-5.6-sol / sol | `gpt-5.6-sol` |
| gpt-5.6-luna / luna | `gpt-5.6-luna` |
| DeepSeekFlash / DeepSeekFrash / deepseek flash / deepseek-v4-flash | `deepseek-v4-flash` |
| DeepSeekPro / deepseek pro / deepseek-v4-pro | `deepseek-v4-pro` |

## Effort の正規化

| 指定 | effort |
| --- | --- |
| xhight / xhigh | `xhigh` |
| high | `high` |
| low | `low` |
| max | `max` |

## Native args

`herdr agent start --` の後ろへ渡す各argv。

### codex

```text
--model <model> -c 'model_reasoning_effort="<effort>"'
```

effort なしなら `--model <model>` のみ。`-c` の値は `model_reasoning_effort="<effort>"`（内側の二重引用符を含む1つのargv）。

### opencode

```text
--model opencode-go/<model>
```

model には `opencode-go/` を前置する。opencode の対話セッションは reasoning effort 非対応のため、effort が指定されていても渡さず model のみで起動し、その旨を報告する。

## 例

```bash
# codex + gpt-5.6-sol + xhigh
herdr agent start cx-review --kind codex --pane <pane-id> -- --model gpt-5.6-sol -c 'model_reasoning_effort="xhigh"'

# opencode + deepseek-v4-flash（effort 指定は無視）
herdr agent start oc-worker --kind opencode --pane <pane-id> -- --model opencode-go/deepseek-v4-flash
```
