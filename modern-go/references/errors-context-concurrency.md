# Errors, Context, and Concurrency

error matching、context cancellation、sync、atomicに関するmodern Go判断。

## `errors.Is`

**Requires:** Go 1.13+

**Use when:** wrapped errorを含めてsentinelやsemantic identityを判定したい。

Prefer:

```go
if errors.Is(err, os.ErrNotExist) {
    // ...
}
```

**Avoid automatic replacement when:**

- exact error instance identityだけを判定すること自体が要件
- custom `Is` methodによる広いmatchingを許可したくない

`err == target`と`errors.Is(err, target)`は常に完全同義ではない。

## `errors.As`

**Requires:** Go 1.13+

**Use when:** wrapped error chainから特定型を取り出す。

manual type assertionはwrapped errorsを見ないため、semantic intentを確認してから置換する。

## Typed error matching

**Requires:** Go 1.26+

Go 1.26+でtyped helperが利用できる場合は、単純な`errors.As` boilerplateよりtype-safeなAPIを検討する。

**Use when:** error chainから具体型を取得するだけ。

**Avoid when:** existing codeがtarget変数の再利用や特殊なmatching flowを必要とする。

## `errors.Join`

**Requires:** Go 1.20+

**Use when:** 複数operationのerrorを一つのerror chainとして返し、`errors.Is` / `errors.As`で各errorを追跡可能にしたい。

**Avoid when:**

- error順序や文字列表現がexternal contract
- first errorだけ返すことが意図
- custom aggregate typeに追加metadataがある

## Cancellation causes

`context.WithCancelCause`: **Go 1.20+**

`context.WithTimeoutCause`: **Go 1.21+**

**Use when:** cancellationの理由を上位で診断・伝播する価値がある。

**Avoid when:** reasonを追加してもconsumerが利用せず、API complexityだけ増える。

`context.Cause`を使うconsumerとセットで設計する。

## `context.AfterFunc`

**Requires:** Go 1.21+

**Use when:** context終了時にcleanupを起動するためだけのgoroutineを置き換えられる。

**Avoid when:** goroutine側がcleanup以外のstate machineやselect処理を持つ。

stop functionやrace semanticsを理解したうえで使う。

## `sync.WaitGroup.Go`

**Requires:** Go 1.25+

**Use when:**

```go
wg.Add(1)
go func() {
    defer wg.Done()
    work()
}()
```

という典型patternをそのまま表現できる。

**Avoid when:**

- Add / Doneのtiming自体に特殊な意味がある
- goroutine lifecycleを別の仕組みで管理している
- panic behaviorの差が重要

error propagationが必要なら、`WaitGroup`を短く書くことよりtask group設計自体を優先する。

## `sync.OnceFunc` / `sync.OnceValue`

**Requires:** Go 1.21+

**Use when:** 一度だけ実行するfunctionやlazy value初期化を直接表現できる。

**Avoid when:** retry、reset、複数state等が必要。

## Typed atomic values

**Requires:** Go 1.19+ for typed atomic families used by the project.

意図を直接表現できる場合はtype-safeなatomic wrapperを優先する。

Examples:

- `atomic.Int32`
- `atomic.Int64`
- `atomic.Uint32`
- `atomic.Uint64`
- `atomic.Bool`
- `atomic.Pointer[T]`

**Avoid automatic migration when:** existing `atomic.Value` intentionally stores multiple concrete representations or relies on its specific semantics.

atomic化をlock-free設計への全面書き換えの口実にしない。
