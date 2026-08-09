---
name: agent-ui-streaming
description: AIエージェントUIのリアルタイム通信を設計・実装するときに使う。SSEを第一選択とし、Agent RunとHTTP接続の分離、Snapshot + Event Log、再接続、複数エージェントの状態同期、Fetch textStream、NDJSON/SSEイベント設計を扱う。WebSocketは双方向通信が不可欠な場合のみ検討する。
---

# Agent UI Streaming

AIエージェントの実行状態・メッセージ・ツール実行結果を、切断やブラウザリロードに耐えられる形でUIへリアルタイム配信する。

## 原則

1. **SSEを第一選択にする**
2. **Agent Runの寿命をHTTP接続から分離する**
3. **Snapshot + Event Logで状態を復元可能にする**
4. **TransportではなくAgent Eventを中心に設計する**
5. **WebSocketは双方向通信が本当に必要な場合のみ使う**

## 推奨アーキテクチャ

```text
User
 │
 │ POST /messages
 ▼
Backend
 │
 ├─ Message保存
 └─ Agent Run作成
       │
       │ Browser接続とは独立して継続
       ▼
   Agent Runtime
       │
       ├─ State
       └─ Event Log
            seq: 1..N
                │
                ▼
             SSE
                │
                ▼
            Agent UI
```

メッセージ送信とストリーム購読を分離する。

```text
POST /sessions/:sessionId/messages
GET  /runs/:runId
GET  /runs/:runId/events
```

## RunとConnectionを分離する

避ける:

```text
HTTP Request
    │
    └─ Agent Process
```

HTTP接続が切れたことでAgentまで停止する設計にしない。

推奨:

```text
Browser Connection
        │
        ▼
     SSE Stream

        ×

    Agent Run
```

ブラウザリロード、ネットワーク切断、タブ終了が発生してもAgent Runは継続できるようにする。

## Session / Run / Event

責務を分ける。

```text
Session
└─ Conversation
   ├─ Message
   └─ Run
      ├─ State
      └─ Events
```

### Session

会話や作業単位を表す。

### Run

1回のAgent実行を表す。

```json
{
  "id": "run_123",
  "sessionId": "session_456",
  "status": "running",
  "lastSeq": 381
}
```

代表的な状態:

```text
queued
running
waiting
completed
failed
cancelled
```

### Event

Run内で発生した変更を表す。

すべてのイベントに単調増加する `seq` を付ける。

```json
{
  "seq": 381,
  "runId": "run_123",
  "type": "agent_status",
  "agent": "impl",
  "data": {
    "status": "working"
  }
}
```

## Agent Eventを中心に設計する

代表イベント:

```text
run_started
run_completed
run_failed

agent_started
agent_status
agent_completed

message_started
message_delta
message_completed

tool_started
tool_result
tool_failed

file_changed

test_started
test_result

error
```

複数Agentを扱う場合は、対象を必ず識別可能にする。

```json
{
  "seq": 120,
  "type": "agent_status",
  "agent": "review",
  "data": {
    "status": "working"
  }
}
```

## SSE

Agent → UI の一方向リアルタイム通信ではSSEを優先する。

例:

```text
id: 381
event: agent_status
data: {"agent":"review","status":"working"}

id: 382
event: tool_started
data: {"agent":"review","tool":"github"}
```

SSEの `id` にはEvent Logの `seq` を使用する。

```text
id = seq
```

これにより再接続時の再開位置を明確にする。

## 再接続

接続断後は最後に受信済みのEvent IDより後を送る。

```text
Event Log

378
379
380
381  ← 最後に受信済み
382
383
384
```

再接続:

```text
after = 381
```

サーバー:

```text
382
383
384
...
```

同一ページ内の通信断ではSSEの再接続機構を利用してよい。

ただしブラウザリロード後も復元できるよう、SSEクライアント自体の状態だけには依存しない。

## Snapshot + Event Log

ブラウザリロード時にEvent Logを最初から再生しない。

まずSnapshotを取得する。

```http
GET /runs/run_123
```

例:

```json
{
  "id": "run_123",
  "status": "running",
  "lastSeq": 380,
  "agents": {
    "impl": "completed",
    "review": "working",
    "pr_fb_impl": "idle"
  },
  "messages": []
}
```

その後、

```http
GET /runs/run_123/events?after=380
```

で新しいイベントだけ購読する。

```text
Reload
   │
   ▼
Snapshot
seq = 380
   │
   ▼
SSE after 380
   │
   ├─ 381
   ├─ 382
   └─ ...
```

### 重要

Snapshot取得とSSE接続の間にイベントが発生しても欠落しないよう、必ず `lastSeq` を基準にEvent Logから再開する。

## UI側の責務

通信、イベント解析、状態更新、表示を分離する。

```text
SSE / Fetch
    │
    ▼
Transport
    │
    ▼
Agent Event
    │
    ▼
Reducer / Store
    │
    ▼
UI
```

推奨構成:

```text
connectRunEvents()
parseAgentEvent()
reduceAgentEvent()
AgentStore
AgentView
```

UIコンポーネント内で直接通信状態やイベント解析を管理しない。

## 状態更新

イベントはState Storeへ適用する。

```ts
function reduceAgentEvent(state, event) {
  switch (event.type) {
    case "agent_status":
      // Agent状態更新
      break;

    case "message_delta":
      // Streaming message更新
      break;

    case "tool_started":
      // Tool状態更新
      break;
  }

  return state;
}
```

同じイベントが再送されても壊れないよう、`seq` を使って重複適用を防ぐ。

```text
event.seq <= lastAppliedSeq
→ ignore
```

## メッセージ送信

ユーザー入力は通常のHTTP POSTを使う。

```text
UI
 │
 │ POST message
 ▼
Backend
 │
 └─ Run作成
      │
      └─ runId返却
```

例:

```json
{
  "message": "Issue #123を進めて"
}
```

レスポンス:

```json
{
  "runId": "run_123"
}
```

その後UIがRunのSSEへ接続する。

```text
POST → Command
SSE  → Events
```

このCommand/Event分離を基本とする。

## EventSourceとfetch

単純なGETベースのSSEでは `EventSource` を優先してよい。

より柔軟な認証、ヘッダー制御、AbortController、独自再接続制御が必要なら `fetch()` ベースのストリーミングを検討する。

対応環境では `Response.textStream()` を利用できる。

```ts
const response = await fetch(url);

for await (const chunk of response.textStream()) {
  consume(chunk);
}
```

未対応環境では:

```ts
const stream =
  response.body!.pipeThrough(new TextDecoderStream());

for await (const chunk of stream) {
  consume(chunk);
}
```

`textStream()` は新しい通信方式ではない。

```text
ReadableStream<Uint8Array>
        ↓
UTF-8 decode
        ↓
ReadableStream<string>
```

を簡潔に扱うAPIとして位置付ける。

## NDJSON

SSEが不要なケースではNDJSONも選択肢。

```text
{"seq":1,"type":"agent_started"}
{"seq":2,"type":"message_delta","text":"調査"}
{"seq":3,"type":"message_delta","text":"中です"}
```

ただしネットワークchunkとJSON行の境界は一致しない。

避ける:

```ts
JSON.parse(chunk);
```

必ずバッファしてイベント境界を復元する。

## 複数エージェント

Agentごとに接続を乱立させるより、基本はRun単位の1本のイベントストリームを使う。

```text
Run SSE
 │
 ├─ orchestrator event
 ├─ impl event
 ├─ review event
 └─ pr_fb_impl event
```

イベント側でAgentを識別する。

```json
{
  "seq": 201,
  "agent": "impl",
  "type": "tool_started"
}
```

UI:

```text
orchestrator   running
├─ impl        completed
├─ review      working
└─ pr_fb_impl  idle
```

## Heartbeat

長時間イベントが発生しないRunでは、プロキシやインフラによる接続切断を避けるためHeartbeatを検討する。

例:

```text
: heartbeat
```

HeartbeatはAgent EventとしてStateに保存しなくてよい。

## Event Log

再接続を保証したいイベントは、配信前または配信と整合する形で永続化する。

避ける:

```text
Agent
 ↓
SSE送信
 ↓
Event保存
```

送信後に保存失敗すると再接続時にイベントを復元できない。

Event Logを再生可能な履歴として扱う。

## WebSocketを使う条件

以下のような要件がある場合のみ検討する。

* サーバーとクライアント双方が高頻度に送信する
* インタラクティブな端末操作
* リアルタイム共同編集
* 非常に低遅延な双方向イベント交換
* 1接続上で双方向通信を維持する必要がある

通常のAgent UI:

```text
User Command → POST
Agent Events → SSE
```

で十分ならWebSocketを導入しない。

## 避けること

* HTTP接続終了でAgent Runまで停止する
* Agent実行状態をブラウザだけに保持する
* Event Logなしで再接続可能とみなす
* ネットワークchunkをイベント境界と仮定する
* `chunk` を直接 `JSON.parse()` する
* Agent状態を自由形式テキストだけで表現する
* UIコンポーネントにTransportとState管理を混在させる
* 複数Agentごとに不要な接続を増やす
* 一方向通信で十分なのにWebSocketを導入する
* `textStream()` を通信プロトコルとして扱う

## 判断基準

### 通常HTTP

結果が揃ってから表示すればよい。

### SSE

第一選択。

適する用途:

* LLM逐次出力
* Agent進捗
* Tool実行状況
* テストログ
* 長時間タスク
* 複数Agentの状態更新
* Run完了通知
* 再接続可能なAgent UI

### NDJSON

HTTP Streamingは必要だがSSE仕様が不要な場合。

### WebSocket

継続的な双方向通信が設計上不可欠な場合。

## 最終原則

Agent UIでは次を分離する。

```text
Command
  POST

State
  Snapshot

Events
  SSE

Execution
  Agent Run
```

ブラウザはAgentを実行する主体ではなく、Agent Runを観測・操作するクライアントとして扱う。

**Agent Runは接続から独立させる。**

**現在状態はSnapshotから復元する。**

**以降の変更はSSE Event Logから追従する。**

**WebSocketではなく、まず `HTTP POST + SSE` で成立する設計を選ぶ。**
