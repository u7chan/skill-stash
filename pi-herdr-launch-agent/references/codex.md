# Codex

Codex 用の正規化と native args の組み立て。

## Agent kind

`herdr agent start` の `--kind` は `codex`。

## Model の正規化

| 指定 | model |
| --- | --- |
| gpt-5.6-sol / sol | `gpt-5.6-sol` |
| gpt-5.6-luna / luna | `gpt-5.6-luna` |

## Effort の正規化

| 指定 | effort |
| --- | --- |
| xhight / xhigh | `xhigh` |
| high | `high` |
| low | `low` |
| max | `max` |

## Native args

```text
--model <model> -c 'model_reasoning_effort="<effort>"'
```

effort なしなら `--model <model>` のみ。`-c` の値は `model_reasoning_effort="<effort>"`（内側の二重引用符を含む1つのargv）。

## 例

```bash
herdr agent start cx-review --kind codex --pane <pane-id> -- --model gpt-5.6-sol -c 'model_reasoning_effort="xhigh"'
```
