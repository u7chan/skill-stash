# Go Tooling

検証目的に応じて最小のtoolを選ぶ。

## Format

```bash
gofmt -w <files...>
```

Goの標準formatter。format議論を人間の好みへ寄せず、標準形式へ揃える。

repository全体で `go fmt ./...` を使う運用もあるため、既存projectのcommandを優先する。

## Test

```bash
go test ./...
```

package testを実行する基本形。

特定packageだけ確認できれば十分な変更では、必要以上に全体testを回さない。

## Vet

```bash
go vet ./...
```

compilerが受理するコードのうち、疑わしいconstructを静的に検査する。

`go vet` を万能lintと考えず、projectがStaticcheck等を導入している場合は既存設定を優先する。

## Race detector

concurrencyに関係する変更ではrace detectorを検討する。

```bash
go test -race ./...
```

race detectorは**実際に実行されたpath上のdata race**を検出する。通っていないpathのraceを証明できるわけではない。

実運用に近いtest pathを通すことが重要。

## Fuzzing

parser、protocol、serializer、boundary input、外部入力処理など、入力空間が広い処理ではfuzzingが有効な場合がある。

例:

```go
func FuzzParse(f *testing.F) {
    f.Add("seed")

    f.Fuzz(func(t *testing.T, input string) {
        _, _ = Parse(input)
    })
}
```

実行例:

```bash
go test -fuzz=FuzzParse ./path/to/package
```

通常の小さなbusiness logicへ儀式的にfuzz testを追加しない。

## Benchmarks

性能が論点になった場合だけbenchmarkで確認する。

```go
func BenchmarkParse(b *testing.B) {
    for b.Loop() {
        Parse("input")
    }
}
```

projectの対象Go versionで利用できるbenchmark APIを確認する。

実行:

```bash
go test -bench=. ./path/to/package
```

pointer receiver、allocation削減、pooling、goroutine数などを「速そう」で変更せず、benchmark / profile / requirementで根拠を持つ。

## Coverage

```bash
go test -cover ./...
```

coverage率そのものを品質目標にしない。

boundary、error path、concurrency lifecycleなど、壊れると困るbehaviorがtestされているかを見る。

## Build

```bash
go build ./...
```

testを実行せずcompile/buildだけ確認したい場合に使う。

ただし `go test` でもpackage compilationは行われるため、何を証明したいかで選ぶ。

## Module checks

依存関係を変更した場合:

```bash
go mod tidy
```

を検討する。

既存repositoryのpolicyなしに、無関係なdependency updateまで広げない。

## Suggested Validation Matrix

| Change | Minimum useful validation |
| --- | --- |
| formatting only | `gofmt` |
| pure logic | focused `go test` |
| package/API change | `go test ./...` |
| suspicious static construct | `go vet ./...` |
| goroutine/shared state | relevant tests + `-race` |
| parser/untrusted input | unit tests + fuzzing検討 |
| performance claim | benchmark/profile |
| dependency change | tests + module consistency check |

## Source Notes

- Go command documentation  
  https://go.dev/cmd/go/
- Data Race Detector  
  https://go.dev/doc/articles/race_detector
- Fuzzing  
  https://go.dev/doc/security/fuzz/
- Testing package  
  https://pkg.go.dev/testing

version依存のflagやAPIは、対象projectのGo versionと最新公式docsを確認する。
