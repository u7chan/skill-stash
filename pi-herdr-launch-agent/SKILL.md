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

## 1. マスタの取得

`pi --list-models` を実行して、利用可能なプロバイダー・モデルのマスタ一覧を取得する。model ID はタイプせず、必ずこの出力から正確な文字列を取る。

```bash
pi --list-models                 # 全一覧
pi --list-models "<model>"       # 部分一致で絞り込み
```

出力は `provider model context max-out thinking images` の表形式。1 列目が provider、2 列目が model ID の正確な値。

## 2. 解決

指定されたプロバイダーに対応する reference だけを読む。

- **codex** → `openai-codex` — [references/codex.md](references/codex.md)
- **opencode-go / OpenCode Go** → `opencode-go` — [references/opencode-go.md](references/opencode-go.md)
- **deepseek / DeepSeek** → `deepseek` — [references/deepseek.md](references/deepseek.md)

model の正規化はそのファイルに従う。正規化した model ID は必ずマスタ一覧（1）の同 provider の行に存在するか確認する。存在しない場合、`pi --list-models "<指定時の語>"` で実際の ID を探し、それでも見つからなければ勝手に補完せず確認する。

thinking（effort）は pi の `--thinking` に渡す。値は `off` / `minimal` / `low` / `medium` / `high` / `xhigh` / `max`。表記ゆれ（`xhight` など）は `xhigh` に補正する。

プロバイダー未指定、または model/thinking の値が読み取れない場合は勝手に補完せず確認する。プロバイダーのみ指定で model/thinking 未指定なら、`--provider` のみ指定して起動する。

## 3. 起動

```bash
herdr agent start <name> --kind pi --pane <pane-id> -- --provider <provider> --model <model> --thinking <level>
herdr pane rename <pane-id> <name>
```

- `<name>` は `^[a-z][a-z0-9_-]{0,31}$`、workspace 内一意の責任ベース名。
- 起動後 `herdr pane get <pane-id>` で kind と状態を確認する。

## 4. 報告

起動した pane ID・provider・model・thinking を報告する。タスク投入は `herdr agent prompt` を使う。
