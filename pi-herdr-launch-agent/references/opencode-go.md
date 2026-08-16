# OpenCode Go

pi を OpenCode Go プロバイダーで起動するための対応。OpenCode Zen は別プロバイダー。

## Provider

`--provider` は `opencode-go`。

## Model の正規化

| 指定 | model |
| --- | --- |
| DeepSeekFlash / DeepSeekFrash / deepseek flash / deepseek-v4-flash | `deepseek-v4-flash` |
| DeepSeekPro / deepseek pro / deepseek-v4-pro | `deepseek-v4-pro` |

## 起動

```bash
herdr agent start <name> --kind pi --pane <pane-id> -- --provider opencode-go --model <model> --thinking <level>
```

## 例

```bash
herdr agent start pi-oc-flash-max --kind pi --pane <pane-id> -- --provider opencode-go --model deepseek-v4-flash --thinking max
```
