# Codex

pi を OpenAI Codex プロバイダーで起動するための対応。

## Provider

`--provider` は `openai-codex`。

## Model の正規化

ID は必ず `pi --list-models` のマスタ一覧で確認した正確な値を使う（タイプしない）。下表は指定語を正規化するための対応で、正規化結果がマスタに無い場合は `pi --list-models "<指定語>"` で実際の ID を探す。

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
