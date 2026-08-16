# DeepSeek

pi を DeepSeek プロバイダーで起動するための対応。

## Provider

`--provider` は `deepseek`。

## Model の正規化

| 指定 | model |
| --- | --- |
| DeepSeekFlash / DeepSeekFrash / deepseek flash / deepseek-v4-flash | `deepseek-v4-flash` |
| DeepSeekPro / deepseek pro / deepseek-v4-pro | `deepseek-v4-pro` |

## 起動

```bash
herdr agent start <name> --kind pi --pane <pane-id> -- --provider deepseek --model <model> --thinking <level>
```

## 例

```bash
herdr agent start pi-ds-flash-max --kind pi --pane <pane-id> -- --provider deepseek --model deepseek-v4-flash --thinking max
```
