# Go Mental Models

`SKILL.md` の判断ルールを支える詳細。必要な項目だけ参照する。

## Values and copies

Goでは「変数」より先に、**代入や引数渡しで値がコピーされる**ことを意識する。

```go
type User struct {
    Name string
}

func rename(u User) {
    u.Name = "Bob"
}

u := User{Name: "Alice"}
rename(u)
fmt.Println(u.Name) // Alice
```

`rename` が受け取るのは `User` 値のコピー。

pointerを渡すと、コピーされるのはpointer値であり、両者が同じ対象を参照できる。

```go
func rename(u *User) {
    u.Name = "Bob"
}
```

「pointer渡しならコピーされない」ではなく、**pointerという値がコピーされる**と考える。

## Arrays and slices

arrayは長さを型に含む値。

```go
var a [3]int
var b [4]int
// a と b は異なる型
```

sliceはarrayそのものではない。概念的には次の情報を持つdescriptorとして考える。

```text
pointer to backing array
length
capacity
```

```go
a := []int{1, 2, 3}
b := a[:2]
b[0] = 99
fmt.Println(a) // [99 2 3]
```

`a` と `b` は同じbacking arrayを共有しているため、要素変更が見える。

### append

`append` の結果が同じbacking arrayを使うか、新しいarrayへ移るかはcapacityに依存する。

```go
base := make([]int, 2, 4)
a := append(base, 1)
```

capacityに余裕があれば共有が続く可能性がある。

そのため、aliasingが重要なコードでは `len` だけでなく `cap` も意識する。

## Nil slice and empty slice

```go
var a []int       // nil slice
b := []int{}      // non-nil empty slice
c := make([]int, 0)
```

通常の `len`、`range`、`append` ではいずれも扱いやすい。

ただし、serializationやAPI契約で `nil` と空配列の違いが外部へ現れることがあるため、境界では契約を確認する。

「常にどちらかが正しい」と一般化しない。

## Maps

mapは内部構造への参照を持つ値として扱う。

```go
m1 := map[string]int{"a": 1}
m2 := m1
m2["a"] = 2
fmt.Println(m1["a"]) // 2
```

### Nil map

```go
var m map[string]int
fmt.Println(m["missing"]) // zero value
m["x"] = 1                // panic
```

readは可能だが、writeには初期化が必要。

### Concurrency

通常のmapへの同期なしの並行write、またはread/writeは安全と考えない。

共有mapが必要なら、ownershipを1 goroutineへ寄せるか、`sync.Mutex` / `sync.RWMutex`、用途によっては `sync.Map` を検討する。

`sync.Map` は一般的なmapの上位互換ではない。

## Interfaces

interfaceは必要なmethod setを満たす型を受け入れる。

```go
type Writer interface {
    Write([]byte) (int, error)
}
```

実装側で `implements Writer` の宣言は不要。

interfaceは「将来の拡張のため」に先回りして作るより、**利用側が必要とする最小の振る舞い**から導入する。

### Interface value

interface valueは概念的に次を持つと考えるとtyped nilを理解しやすい。

```text
dynamic type
dynamic value
```

```go
type MyError struct{}

func (*MyError) Error() string { return "boom" }

func f() error {
    var e *MyError = nil
    return e
}

fmt.Println(f() == nil) // false
```

dynamic typeが `*MyError` として入っているため、interface全体はnilではない。

「pointerがnilか」と「interfaceがnilか」を分けて考える。

## Methods and receivers

value receiverではreceiver値がコピーされる。

pointer receiverではpointer値がコピーされ、同じ対象を変更できる。

pointer receiverを選ぶ典型理由:

- methodがreceiverを変更する
- 大きな値のコピーを避ける必要がある
- method set / APIの一貫性上pointerで扱うべき
- mutex等、コピーすべきでないfieldを含む

value receiverを選ぶ典型理由:

- 小さくimmutable-likeな値
- methodが値を変更しない
- 値として扱う意味が自然

「pointer receiverの方が常に高速」とは決めない。

## Errors are values

Goの `error` はinterface。

```go
type error interface {
    Error() string
}
```

通常の値と同じく、作り、返し、保持し、分類できる。

```go
value, err := load()
if err != nil {
    return fmt.Errorf("load config: %w", err)
}
```

`%w` でwrapすると、呼び出し元が `errors.Is` / `errors.As` でerror chainを調べられる。

### errors.Is

既知のsentinelや、error chain上で特定のerrorと同等かを調べたい場合に使う。

```go
if errors.Is(err, fs.ErrNotExist) {
    // ...
}
```

### errors.As

error chainから特定の型を取り出したい場合に使う。

```go
var pathErr *fs.PathError
if errors.As(err, &pathErr) {
    fmt.Println(pathErr.Path)
}
```

error message文字列は人間向け情報として扱い、制御フローの安定したAPIにしない。

## Error vs panic

通常の失敗可能性は `error` で表す。

`panic` は、通常の呼び出し側判断では回復しにくいprogramming errorや、処理継続不能な内部不変条件違反など、限定的な場面で検討する。

library APIで利用者が普通に遭遇し得る入力エラーやI/Oエラーをpanicへ寄せない。

## Goroutines

`go f()` は、`f` の実行を別goroutineとして開始する。

```go
go serve(conn)
```

重要なのは開始方法よりlifecycle。

```text
start
  ↓
work / wait
  ↓
stop condition
  ↓
return
```

次が説明できないgoroutineはleak候補。

- stop condition
- cancellation path
- completion signaling
- error propagation
- owner

### Closure capture

loop変数や外側の可変状態をclosureから使う場合、どの値をcaptureしているか明示する。

必要なら引数として渡し、意図を固定する。

## Channels

channelはgoroutine間のcommunication / synchronizationを表す。

```go
ch := make(chan int)
```

unbuffered channelのsend/receiveは相手との同期点になる。

buffered channelは容量分だけsendを先行できる。

### Close ownership

原則として、**これ以上sendしないことを知っているsender側**がcloseする。

receiverが勝手にcloseすると、senderが後からsendしてpanicする可能性がある。

channelは「値がもう来ない」ことを伝えるためにcloseするのであり、GCのためにcloseするわけではない。

## Channel vs Mutex

channelが向く例:

- ownershipをgoroutine間で移す
- producer / consumerをcoordinationする
- completionやstreamを表現する

mutexが向く例:

- 共有stateの短いcritical sectionを守る
- counterやcache等を複数goroutineから操作する
- communication modelにする方がかえって複雑

「Goだからchannel」を判断基準にしない。

## Context

`context.Context` は処理チェーンにdeadline / cancellation / request-scoped valueを伝播する。

典型:

```go
func Handle(ctx context.Context, id string) error {
    return repository.Load(ctx, id)
}
```

### Rules

- 通常は第1引数として明示的に渡す
- `nil` Contextを渡さない
- optional argumentの代用にしない
- long-lived structへ安易に保存しない
- `WithCancel` / `WithTimeout` 等でcancel functionを作った側は、必要な範囲で確実に呼ぶ

```go
ctx, cancel := context.WithTimeout(parent, time.Second)
defer cancel()
```

Contextが止めるのは「Contextを監視し、停止に協力する処理」。goroutineを魔法のように強制終了するものではない。

## Zero values

Goではzero valueがそのまま有用な型を作れることが多い。

```go
var mu sync.Mutex
var buf bytes.Buffer
```

constructorを必須にする前に、zero valueで安全に使える設計にできるか考える。

ただし、必須dependencyや不変条件がある型ではconstructorが自然な場合もある。

## Source Notes

公式資料を優先する。

- Effective Go  
  https://go.dev/doc/effective_go
- Errors are values  
  https://go.dev/blog/errors-are-values
- Working with Errors in Go 1.13  
  https://go.dev/blog/go1.13-errors
- Go Memory Model  
  https://go.dev/ref/mem
- context package  
  https://pkg.go.dev/context

Effective Goには古い記述も含まれ得るため、version依存の機能や現在のAPIについては言語仕様・package docs・最新の公式資料を優先する。
