# React Effect Patterns

`SKILL.md` の判断ルールを適用するための具体例。

## 1. Derived stateはrenderで計算する

```tsx
// Avoid
const [fullName, setFullName] = useState("");

useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);

// Prefer
const fullName = `${firstName} ${lastName}`;
```

Effectでstateを同期すると、古い値で一度renderした後に追加renderが発生する。
既存のprops/stateから決定できる値はstateとして複製しない。

### 高コストな導出

```tsx
const visibleRows = useMemo(
  () => filterAndSort(rows, filter, sort),
  [rows, filter, sort],
);
```

`useMemo` も自動的に使わず、計測上必要な場合に使う。

---

## 2. User eventはevent handlerで処理する

```tsx
// Avoid
const [pendingSave, setPendingSave] = useState(false);

useEffect(() => {
  if (!pendingSave) return;
  saveDraft(draft);
  setPendingSave(false);
}, [pendingSave, draft]);

function handleSave() {
  setPendingSave(true);
}

// Prefer
async function handleSave() {
  await saveDraft(draft);
}
```

stateを「Effectを起動するためのフラグ」として使わない。
処理原因がclick / submit / changeなら、そのイベントに置く。

---

## 3. Parent notificationは同じ更新経路で行う

```tsx
// Avoid
function Toggle({ onChange }: { onChange: (value: boolean) => void }) {
  const [enabled, setEnabled] = useState(false);

  useEffect(() => {
    onChange(enabled);
  }, [enabled, onChange]);

  return <button onClick={() => setEnabled(v => !v)}>Toggle</button>;
}

// Prefer
function Toggle({ onChange }: { onChange: (value: boolean) => void }) {
  const [enabled, setEnabled] = useState(false);

  function updateEnabled(next: boolean) {
    setEnabled(next);
    onChange(next);
  }

  return <button onClick={() => updateEnabled(!enabled)}>Toggle</button>;
}
```

可能ならさらにcontrolled componentへ寄せる。

---

## 4. Identity変更でstateをresetするならkeyを使う

```tsx
// Avoid
function ProfileEditor({ userId }: { userId: string }) {
  const [note, setNote] = useState("");

  useEffect(() => {
    setNote("");
  }, [userId]);

  // ...
}

// Prefer
function ProfilePage({ userId }: { userId: string }) {
  return <ProfileEditor key={userId} userId={userId} />;
}
```

「別のentityになったら全部初期状態へ戻す」はcomponent identityの問題として扱う。

---

## 5. 外部接続は正当なEffect

```tsx
function ChatRoom({ roomId, serverUrl }: Props) {
  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.connect();

    return () => {
      connection.disconnect();
    };
  }, [serverUrl, roomId]);

  return <RoomView />;
}
```

このEffectは次を説明できる。

- external system: chat server
- setup: connectionを作ってconnectする
- cleanup: disconnectする
- dependencies: `serverUrl`, `roomId` が変われば別接続へ同期し直す

依存配列は「この頻度で実行したい」から決めるのではなく、同期対象を再構成するreactive valueから決まる。

---

## 6. Global event listenerも正当なEffect

```tsx
function useWindowSize() {
  const [size, setSize] = useState({ width: 0, height: 0 });

  useEffect(() => {
    function handleResize() {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return size;
}
```

初期renderでは `window` を参照せず、SSRでも同じinitial stateを使う。hydration後にEffectで実値へ同期する。
ただし、外部storeとして扱えるAPIなら `useSyncExternalStore` を優先する。

---

## 7. External storeはuseSyncExternalStoreを優先する

```tsx
function subscribe(onChange: () => void) {
  window.addEventListener("online", onChange);
  window.addEventListener("offline", onChange);

  return () => {
    window.removeEventListener("online", onChange);
    window.removeEventListener("offline", onChange);
  };
}

function useOnlineStatus() {
  return useSyncExternalStore(
    subscribe,
    () => navigator.onLine,
    () => true,
  );
}
```

手動の `useEffect + useState` で購読モデルを再実装しない。

---

## 8. DOM nodeのattach/detachはcallback refを検討する

特定DOM nodeが存在するときだけimperative APIを接続するなら、component mountよりnode lifecycleの方が正しい境界になることがある。

```tsx
function AutoFocusInput() {
  const inputRef = useCallback((node: HTMLInputElement | null) => {
    if (node) node.focus();
  }, []);

  return <input ref={inputRef} />;
}
```

計測結果をpaint前に反映しないとちらつくケースは `useLayoutEffect` を検討する。
`useLayoutEffect` は通常の `useEffect` より強い同期なので、必要性を説明できる場合だけ使う。

---

## 9. Data fetchingはEffectを第一選択にしない

### Prefer: framework / query library

```tsx
function Product({ productId }: { productId: string }) {
  const { data } = useQuery({
    queryKey: ["product", productId],
    queryFn: () => fetchProduct(productId),
  });

  return <ProductView product={data} />;
}
```

cache、dedupe、retry、stale state、SSR/hydrationなどをEffectで再発明しない。

### Effectが必要な場合

```tsx
function useProduct(productId: string) {
  const [product, setProduct] = useState<Product | null>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      try {
        const response = await fetch(`/api/products/${productId}`, {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(`Failed to load product: ${response.status}`);
        }

        const next = await response.json();
        setProduct(next);
        setError(null);
      } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") return;

        setError(
          error instanceof Error ? error : new Error("Failed to load product"),
        );
      }
    }

    void load();

    return () => controller.abort();
  }, [productId]);

  return { product, error };
}
```

client-onlyな同期としてEffect fetchを選ぶなら、少なくともrequest cancellation、stale result、error handlingを設計する。cleanupによるabortは正常な制御フローとして扱い、それ以外の失敗はアプリ側で処理する。

`use()` は既に用意されたPromise/resourceをcomponentで読む構成では候補になるが、render中に毎回新しいfetch Promiseを作るような機械的置換はしない。

---

## 10. Latest valueを読む非reactive処理はuseEffectEvent

`useEffectEvent` は React 19.2 以降で、プロジェクトのReact / React Native環境から実際に利用できる場合だけ候補にする。未対応ならdependencyを隠さず、同期契約を維持した設計を選ぶ。

```tsx
function ChatRoom({ roomId, theme }: Props) {
  const onConnected = useEffectEvent(() => {
    showToast("Connected", theme);
  });

  useEffect(() => {
    const connection = createConnection(roomId);
    connection.on("connected", onConnected);
    connection.connect();

    return () => connection.disconnect();
  }, [roomId]);
}
```

ここでは:

- `roomId` は接続先を変えるためreactive
- `theme` はtoast表示時に最新値を読みたいだけで、再接続理由ではない

`useEffectEvent` を依存値逃れに使わない。
本当に再同期が必要な値ならdependencyに残す。

---

## 11. Ref guardでStrict Modeを黙らせない

```tsx
// Avoid
const didConnect = useRef(false);

useEffect(() => {
  if (didConnect.current) return;
  didConnect.current = true;
  connect();
}, []);
```

このコードはcleanup不足や再接続不能を隠す。

```tsx
// Prefer
useEffect(() => {
  const connection = connect();
  return () => connection.disconnect();
}, []);
```

開発時に `setup -> cleanup -> setup` が行われても、ユーザー視点で壊れない設計にする。

---

## 12. genericなuseMountEffectを作らない

```tsx
// Avoid
function useMountEffect(fn: () => void | (() => void)) {
  useEffect(fn, []);
}
```

呼び出し側がreactive valueをclosureで読んでも、dependency contractがAPI上から消える。
「mount時に一度」という実行回数を先に決めるより、同期対象を表すcustom hookへする。

```tsx
// Prefer
function useDocumentTitle(title: string) {
  useEffect(() => {
    const previous = document.title;
    document.title = title;

    return () => {
      document.title = previous;
    };
  }, [title]);
}
```

custom hook名はlifecycleではなく**同期対象**を表す。

---

## 13. Effect chainを手続きロジックに使わない

```tsx
// Avoid
useEffect(() => {
  if (step === "validated") setStep("saving");
}, [step]);

useEffect(() => {
  if (step === "saving") void save();
}, [step]);
```

```tsx
// Prefer
async function handleSubmit() {
  const result = validate(form);
  if (!result.ok) return;

  setStatus("saving");
  await save(result.value);
  setStatus("saved");
}
```

ユーザー操作から始まる手続きはイベント側で順序を明示する。

---

## 14. App initializationをcomponent Effectに載せない

アプリ全体で一度だけ必要な初期化が特定componentの表示と無関係なら、entry point、framework lifecycle、server initializationなど適切な境界へ移す。

```tsx
// Suspicious
function App() {
  useEffect(() => {
    initializeTelemetry();
    loadGlobalConfig();
  }, []);

  return <Routes />;
}
```

「App componentがmountしたから」ではなく「application process/sessionが開始したから」が原因ならReact component lifecycleの責務ではない可能性が高い。

SSRではmodule-level side effectにも注意し、frameworkの初期化ポイントを優先する。

---

## 15. Analyticsは原因を分ける

### Interaction analytics

clickやsubmitが原因ならイベント側で記録する。

```tsx
function handlePurchase() {
  track("purchase_clicked", { productId });
  purchase(productId);
}
```

### View / impression analytics

「このviewが表示された」がイベントそのものならEffectが候補になる。

```tsx
useEffect(() => {
  trackImpression(pageId);
}, [pageId]);
```

ただしanalyticsは取り消せないため、Strict Modeや再mountで重複しても壊れないよう、analytics基盤側のdedupeやenvironment handlingを含めて設計する。

「cleanupが書けないから常に禁止」ではなく、component lifetimeとの因果関係とidempotencyで判断する。

---

## 16. Cleanupはsetupとの対称性で考える

Cleanupが必要な例:

| Setup | Cleanup |
| --- | --- |
| `addEventListener` | `removeEventListener` |
| `connect` | `disconnect` |
| `subscribe` | `unsubscribe` |
| `setInterval` | `clearInterval` |
| request開始 | abort / stale result無効化 |
| imperative widget生成 | destroy / dispose |

一方、外部状態へ単発で値を代入するだけなど「解除する継続的影響」が存在しない操作に、形だけのcleanupを捏造しない。

---

## 17. Effect review template

レビュー時は各Effectについて次の形で整理する。

```text
Effect: <location>
Classification: keep | replace | redesign
External system: <what React synchronizes with, or none>
Trigger: render lifecycle | user event | external subscription | other
Dependencies: <why each reactive value belongs>
Cleanup: <symmetry / cancellation, if needed>
Replacement: <render / handler / key / useSyncExternalStore / callback ref / query layer / none>
Reason: <short rationale>
```

### keep

外部同期として意味があり、dependenciesとcleanupが同期契約を正しく表している。

### replace

責務は妥当だがEffectより直接的なReact APIがある。

### redesign

Effectがアプリケーションロジック、データフロー、イベント手順の代替になっており、局所置換では改善しない。

---

## Decision Matrix

| やりたいこと | 第一候補 |
| --- | --- |
| props/stateから値を作る | render中に導出 |
| 重い導出 | `useMemo` |
| click/submit/change後の処理 | event handler |
| entity変更でstateを全reset | `key` |
| external store購読 | `useSyncExternalStore` |
| node attach時のimperative処理 | callback ref |
| paint前のDOM計測・同期 | `useLayoutEffect` |
| server/network data | framework / query layer |
| 外部connection/subscription | `useEffect` |
| Effect内で最新値だけ読む非reactive処理 | `useEffectEvent`（React 19.2+ / API利用可能時） |
| application-wide initialization | entry point / framework lifecycle |

---

## Source Notes

このスキルは次の考え方を参考にしつつ、そのままコピーせず現在のReact APIに合わせて再構成している。

- React: You Might Not Need an Effect  
  https://react.dev/learn/you-might-not-need-an-effect
- React: useEffect  
  https://react.dev/reference/react/useEffect
- React: useEffectEvent  
  https://react.dev/reference/react/useEffectEvent
- React: useSyncExternalStore  
  https://react.dev/reference/react/useSyncExternalStore
- uhyo: 過激派が教える！ useEffectの正しい使い方  
  https://zenn.dev/uhyo/articles/useeffect-taught-by-extremist
- alejandrobailo/no-use-effect  
  https://github.com/alejandrobailo/no-use-effect

参考元から意図的に変えた点:

- `useEffect` の直接利用を全面禁止しない
- cleanupを機械的な必須条件にせず、setupとの対称性で判断する
- dependency arrayを最適化用ではなくreactive synchronization contractとして扱う
- genericな `useMountEffect` / `useOnce` を推奨しない
- `useEffectEvent` はReact 19.2+かつAPI利用可能な環境でのみ候補にし、dependency逃れには使わない