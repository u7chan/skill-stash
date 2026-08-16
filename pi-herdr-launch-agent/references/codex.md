# Codex

pi を OpenAI Codex プロバイダーで起動するための対応。

## Provider

`--provider` は `openai-codex`。

## Model の正規化

| 指定 | model |
| --- | --- |
| gpt-5.6-sol / sol | `gpt-5.6-sol` |
| gpt-5.6-luna / luna | `gpt-5.6-luna` |
| gpt-5.6-terra / terra | `gpt-5.6-terra` |

## 起動

```bash
herdr agent start <name> --kind pi --pane <pane-id> -- --provider openai-codex --model <model> --thinking <level>
```

## 例

```bash
herdr agent start pi-cx-luna-max --kind pi --pane <pane-id> -- --provider openai-codex --model gpt-5.6-luna --thinking max
```
