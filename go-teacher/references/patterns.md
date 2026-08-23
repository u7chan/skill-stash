# Go Teaching Patterns

比較や典型的な誤解を説明するときの具体例。

## Array vs Slice

- **Mental model**: arrayは長さを含む値、sliceはbacking arrayを見るdescriptor
- **Default**: 通常の可変長sequenceはslice
- **Choose array when**: 固定長そのものが型・意味として重要
- **Choose slice when**: 一般的なcollection、subrange、API引数
- **Common mistake**: sliceの代入で要素全体がdeep copyされると思う

```go
a := []int{1, 2, 3}
b := a
b[0] = 9
fmt.Println(a) // [9 2 3]
```

## Value receiver vs Pointer receiver

- **Mental model**: value receiverはreceiver値のcopy、pointer receiverはpointer値のcopy
- **Default**: 型の意味とmethod setを揃える
- **Choose value when**: 小さく、値として扱う型で、変更しない
- **Choose pointer when**: receiver変更、大きい値、copy禁止field、API一貫性
- **Common mistake**: 「pointerの方が必ず高速」だけで決める

```go
type Counter struct {
    n int
}

func (c *Counter) Inc() {
    c.n++
}
```

## Nil slice vs Empty slice

- **Mental model**: どちらもlength 0だがnilnessは異なる
- **Default**: 内部処理では過度に区別しない
- **Choose nil when**: zero valueをそのまま使いたい、契約上問題ない
- **Choose empty when**: JSON/API等で空collectionとして明示したい
- **Common mistake**: あらゆる場所でどちらか一方を絶対ルールにする

```go
var a []string
b := []string{}

fmt.Println(len(a), len(b)) // 0 0
fmt.Println(a == nil)       // true
fmt.Println(b == nil)       // false
```

## Concrete type vs Interface

- **Mental model**: interfaceは実装の親クラスではなく、必要な振る舞いのboundary
- **Default**: concrete type
- **Choose interface when**: 利用側が複数実装を同じ契約で扱う必要がある
- **Choose concrete when**: 実装差し替えの必要がなく、APIが十分単純
- **Common mistake**: 将来の拡張やmockのためだけに1実装1interfaceを作る

```go
type Store interface {
    Get(ctx context.Context, id string) (Item, error)
}
```

interfaceは実装packageではなく、利用側の必要最小限から生まれることが多い。

## errors.Is vs ==

- **Mental model**: `==` はその値との直接比較、`errors.Is` はwrap chainも含めて意味上の一致を調べる
- **Default**: wrapされ得るerror APIなら `errors.Is`
- **Choose == when**: 値が直接そのsentinelである契約が明確でwrapを扱わない
- **Choose errors.Is when**: error chainを維持したまま分類する
- **Common mistake**: `%w` でwrapした後も `==` で比較する

```go
if errors.Is(err, fs.ErrNotExist) {
    // not found
}
```

## errors.As vs Type assertion

- **Mental model**: type assertionは現在のdynamic type、`errors.As` はerror chain上の型を探索する
- **Default**: wrapped errorを含むAPIでは `errors.As`
- **Choose assertion when**: 現在値だけを見る意図が明確
- **Choose errors.As when**: wrapされた具体errorの情報を取り出す
- **Common mistake**: wrap後に `err.(*MyError)` だけを見る

```go
var pathErr *fs.PathError
if errors.As(err, &pathErr) {
    fmt.Println(pathErr.Path)
}
```

## Error vs Panic

- **Mental model**: errorは通常の失敗を呼び出し元へ返す値、panicは通常制御フローを中断する
- **Default**: error
- **Choose error when**: 入力不正、I/O失敗、外部依存失敗などcallerが判断可能
- **Choose panic when**: programmer errorや内部不変条件違反など、通常の回復契約ではない
- **Common mistake**: error handlingが面倒という理由でpanicする

## Channel vs Mutex

- **Mental model**: channelはcommunication / coordination、mutexはshared stateのcritical section保護
- **Default**: 問題の形に合わせる
- **Choose channel when**: work queue、ownership transfer、stream、completion signaling
- **Choose mutex when**: 小さな共有stateを複数goroutineから同期して触る
- **Common mistake**: 「Goらしさ」のために単純なmutexをchannel architectureへ変える

### Mutex example

```go
type Counter struct {
    mu sync.Mutex
    n  int
}

func (c *Counter) Inc() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.n++
}
```

### Channel example

```go
jobs := make(chan Job)

go func() {
    for job := range jobs {
        process(job)
    }
}()
```

## Buffered vs Unbuffered Channel

- **Mental model**: unbufferedはsend/receiveが直接同期、bufferedはcapacity分だけdecoupleできる
- **Default**: synchronization semanticsを先に決める
- **Choose unbuffered when**: handoffそのものを同期点にしたい
- **Choose buffered when**: bounded queueやburst吸収が要件としてある
- **Common mistake**: deadlockを消すために適当なbuffer sizeを付ける

buffer sizeは設計上の意味を説明できる値にする。

## make vs new

- **Mental model**: `new(T)` はzero valueの `T` を確保して `*T` を返す。`make` はslice/map/channelの内部構造を初期化して値を返す
- **Default**: slice/map/channelの利用可能な初期化は `make`
- **Choose new when**: zero valueへのpointerが本当に必要
- **Choose make when**: slice/map/channelを初期化する
- **Common mistake**: C/C++のallocation APIの対応物として機械的に使い分ける

```go
m := make(map[string]int)
s := make([]byte, 0, 1024)
ch := make(chan int, 8)
```

## Goroutine without cancellation

### Suspicious

```go
func watch(ch <-chan Event) {
    go func() {
        for event := range ch {
            handle(event)
        }
    }()
}
```

`ch` がcloseされない場合、goroutineは終了しない。

### Better when caller owns lifecycle

```go
func watch(ctx context.Context, ch <-chan Event) {
    go func() {
        for {
            select {
            case <-ctx.Done():
                return
            case event, ok := <-ch:
                if !ok {
                    return
                }
                handle(event)
            }
        }
    }()
}
```

ただし、単に `context` を追加することが目的ではない。誰がcancelするかまで設計する。

## Typed nil interface

### Problem

```go
type MyError struct{}

func (*MyError) Error() string { return "boom" }

func run() error {
    var err *MyError
    return err
}
```

`run()` の戻り値interfaceにはdynamic typeが入るため、`nil` ではない。

### Better

「errorなし」を返すなら明示的にnil interfaceを返す。

```go
func run() error {
    var err *MyError
    if err != nil {
        return err
    }
    return nil
}
```

## Slice append aliasing

```go
base := make([]int, 2, 4)
base[0], base[1] = 1, 2

a := append(base, 3)
b := append(base, 4)

fmt.Println(a)
fmt.Println(b)
```

`a` と `b` が同じbacking array領域を再利用すると、後のappendが先の結果へ影響する可能性がある。

「appendは常に新しいsliceを作る」と覚えない。

独立したcopyが必要なら意図を明示する。

```go
copyOfBase := append([]int(nil), base...)
```

## Context as option bag

### Avoid

```go
ctx = context.WithValue(ctx, "pageSize", 100)
ctx = context.WithValue(ctx, "sort", "name")
```

通常のfunction parameterやoptions structで表現できる設定値をContextへ隠さない。

### Prefer

```go
type ListOptions struct {
    PageSize int
    Sort     string
}

func List(ctx context.Context, opts ListOptions) error {
    // ...
    return nil
}
```

Contextはcancellation/deadline/request scopeの伝播を主用途にする。
