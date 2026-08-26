# Testing and Benchmarks

Go test codeのmodern idiomを扱う。

## `testing.T.Context`

**Requires:** Go 1.24+

テストcaseのlifecycleに連動するcontextが必要なら`t.Context()`を優先する。

Prefer:

```go
func TestFoo(t *testing.T) {
    ctx := t.Context()
    // ...
}
```

**Use when:**

- `context.Background()`からtest専用contextを作っている
- cleanupをtest終了へ連動させたい

**Avoid when:**

- cancellation timingをtest自身が明示的に制御する必要がある
- parent contextに特殊なvalue / deadlineが必要

`t.Context()`を使うために、テストが検証しているcancellation scenarioを消さない。

## `testing.B.Loop`

**Requires:** Go 1.25+

benchmark bodyの反復には`b.Loop()`を優先する。

Prefer:

```go
func BenchmarkFoo(b *testing.B) {
    for b.Loop() {
        foo()
    }
}
```

**Use when:** classicな`for i := 0; i < b.N; i++`がbenchmark operationの反復だけを担う。

**Avoid when:**

- loop index `i`がbenchmark inputとして意味を持つ
- `b.N`を使った特殊なsetup / batching semanticsがある

migration後も「1 iterationで何を測っているか」を維持する。

## Test helpers

modernizationのために独自test frameworkを追加しない。

standard `testing` packageで十分な既存projectでは、assertion library導入等を混ぜない。

## Subtests and parallelism

loop variable semanticsがGo 1.22+で改善されていても、`t.Parallel()`導入は単なるsyntax modernizationではない。

parallelizationはshared state、test isolation、timing依存を確認した別判断として扱う。

## Validation

変更したtest / benchmarkを直接実行する。

Examples:

```sh
go test ./path/to/pkg
```

benchmark変更なら対象benchmarkを絞る。

```sh
go test -run '^$' -bench 'BenchmarkFoo' ./path/to/pkg
```

performance improvementを主張する場合は、単発値ではなく十分なsampleと比較方法を用いる。
