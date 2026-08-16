# OpenCode

OpenCode 用の正規化と native args の組み立て。

## Agent kind

`herdr agent start` の `--kind` は `opencode`。

## Model の正規化

| 指定 | model |
| --- | --- |
| DeepSeekFlash / DeepSeekFrash / deepseek flash / deepseek-v4-flash | `deepseek-v4-flash` |
| DeepSeekPro / deepseek pro / deepseek-v4-pro | `deepseek-v4-pro` |

## Native args

```text
--model opencode-go/<model>
```

model には `opencode-go/` を前置する。対話セッションは reasoning effort 非対応のため、effort が指定されていても渡さず model のみで起動し、その旨を報告する。

## 例

```bash
herdr agent start oc-worker --kind opencode --pane <pane-id> -- --model opencode-go/deepseek-v4-flash
```
