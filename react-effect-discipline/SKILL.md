---
name: react-effect-discipline
description: React / React NativeでuseEffectを設計・実装・レビューするときに使う。Effectを外部システムとの同期に限定し、derived state、イベント処理、データ取得、外部購読、DOM連携、依存配列、Strict Mode、useEffectEventなどの適切な代替・実装を判断する。
---

# React Effect Discipline

`useEffect` を禁止しない。**外部システムとの同期が必要なときだけ使う。**

Effectを書く前に、必ず「Reactの外にある何と同期するのか」を説明する。
説明できないならEffectを使わない。

## Decision Gate

次の順で判定する。

1. **render中に計算できるか**
   - props/stateから導出できる値はその場で計算する
   - 高コストな計算だけ `useMemo` を検討する
2. **ユーザー操作や明確なイベントが原因か**
   - submit、click、change、navigationなどが原因ならイベント側で処理する
3. **外部データの取得か**
   - frameworkのloader / Server Component / query libraryなど、既存のデータ取得機構を優先する
4. **外部storeの購読か**
   - `useSyncExternalStore` を優先する
5. **props変更でローカルstateを初期化したいだけか**
   - component identityを分け、`key` によるresetを優先する
6. **DOM nodeのattach/detachそのものに反応したいか**
   - callback refを検討する
7. **それでも外部システムとの同期が残るか**
   - ここで初めて `useEffect` / `useLayoutEffect` を使う

具体例は [references/patterns.md](references/patterns.md) を参照する。

## Valid Effect

Effectを残す場合、次を説明できなければならない。

- **External system**: 何と同期しているか
- **Setup**: Effectが何を開始・接続・反映するか
- **Cleanup**: setupしたものをどう解除・中止・巻き戻すか
- **Reactive dependencies**: どの値が変わると再同期が必要か

典型例:

- browser API / global event listener
- WebSocket / SSE / subscription
- timer
- third-party widget
- imperative DOM integration
- client-only network synchronizationで他の取得機構が適さない場合

Cleanupは形式的に付けるものではない。**setupが継続的な影響を作るなら、そのsetupに対応するcleanupを持たせる。**

## Dependency Rule

依存配列を「実行タイミングを調整するノブ」として使わない。

Effect内で読むreactive valueは、再同期の必要性を表す依存値として扱う。
望む実行回数に合わせるために依存値を削除したり、lintを無効化したりしない。

```tsx
useEffect(() => {
  const connection = connect(serverUrl, roomId);
  return () => connection.disconnect();
}, [serverUrl, roomId]);
```

`[]` は「一度だけ実行したい」の意味ではない。**Effectがreactive valueに依存せず、component lifetimeだけに同期している結果として空になる**場合に使う。

## Effect Event

Effect内の処理の一部だけが「最新値は読みたいが、再同期の原因にはしたくない」場合は `useEffectEvent` を検討する。

**先にプロジェクトのReact / React Native環境でAPIが利用可能か確認する。`useEffectEvent` は React 19.2 以降でのみ候補にする。** React Nativeでも、実際に利用しているReactバージョンが対応していることを確認する。未対応なら無理に置換せず、dependency contractを維持したEffect設計や用途に適した別手段を選ぶ。

ただし、依存値を隠すために使わない。

- reactiveな同期条件 → Effect dependency
- Effectから発火する非reactiveな処理 → `useEffectEvent`

`useEffectEvent` が返す関数はdependency arrayへ入れない。

## Strict Mode Rule

開発時の `setup -> cleanup -> setup` を壊れた挙動として回避しない。

次を禁止する。

- `hasRun.current` で二重実行を握り潰す
- `eslint-disable` でdependency不足を隠す
- genericな `useMountEffect` で空依存配列を隠す

代わりに、Effectを再接続可能にし、cleanupをsetupと対称にする。

## Data Fetching

データ取得をEffectへ直書きすることをデフォルトにしない。

優先順位:

1. frameworkのデータ取得機構
2. Server Component / loader等のrendering architecture
3. TanStack Query / SWR等のquery library
4. 必要ならside effectをcustom hookへ隔離
5. 最後の手段としてcomponent Effect

Effectでfetchする場合はrace conditionとstale resultを考慮し、`AbortController` やcleanupを使う。

`use()` はpromise/resourceを受け取る構成では有効だが、単純な `fetch + useEffect` の機械的置換として扱わない。

## Event vs Effect

「何がこの処理を起こしたか」で判断する。

- ユーザーが操作した → event handler
- componentが表示されていること自体が同期理由 → Effect候補
- 値が計算できた → render
- 外部systemの状態を購読する → specialized hook / Effect

stateをフラグとして立て、その変化をEffectが監視して本処理を行う設計は避ける。

## Review Mode

既存コードをレビューするときは、各Effectを次のどれかに分類する。

- **keep**: 外部同期として妥当。dependencies / cleanupも正しい
- **replace**: render、event handler、`useMemo`、`useSyncExternalStore`、`key`、callback ref等へ置換できる
- **redesign**: データフローや責務配置そのものを変えるべき

指摘では「Effectが悪い」ではなく、**何を同期しているか / なぜ代替の方が自然か**を説明する。

## Custom Hook Rule

外部同期の再利用にはcustom hookを使ってよい。

ただし、custom hookはEffectを隠すためではなく、**同期対象とlifecycle契約を名前で表現するため**に使う。

良い例:

- `useOnlineStatus()`
- `useChatConnection(roomId)`
- `useDocumentTitle(title)`

避ける:

- `useMountEffect(fn)`
- `useOnce(fn)`
- `useEffectWithoutDeps(fn)`

## Final Check

Effectを追加・変更したら確認する。

- 外部システムを一文で説明できる
- render/event handlerで代替できない
- dependenciesはコードから導かれている
- lintを回避していない
- setupとcleanupが必要な範囲で対称
- Strict Modeの再接続で壊れない
- race / stale closure / reconnect loopを考慮した
- specialized APIがあるならそちらを優先した
- `useEffectEvent` を使う場合はReactバージョン/API availabilityを確認した

詳細なパターンとBefore/After例は [references/patterns.md](references/patterns.md) を参照する。
