# Collections and Iteration

slices、maps、strings、loop、iteratorに関するmodern Go判断。

各項目は`Requires / Use when / Avoid when`で評価する。

## `slices.Contains` / `slices.Index`

**Requires:** Go 1.21+

**Use when:**

- comparableな要素の存在確認だけが目的
- 最初に一致するindexを求めるだけ

**Avoid when:**

- loop内で追加処理や複数条件を評価している
- indexとvalueを同時に別用途で使う
- custom equalityが必要

## `slices.Sort` / `slices.SortFunc`

**Requires:** Go 1.21+

**Use when:**

- sliceをin-placeでsortする
- element比較を直接表現できる

`SortFunc`ではboolean comparatorを移植するだけでなく、比較結果`< 0 / 0 / > 0`を正しく返す。

**Avoid when:**

- stable sortが必要なのに同等性を無視する
- existing ordering contractが複雑

## `slices.Min` / `slices.Max`

**Requires:** Go 1.21+

**Use when:** 単純なordered sliceの最小・最大値を求める。

**Avoid when:**

- empty sliceを許容する必要がある
- custom comparisonやtie handlingがある
- indexも必要

## `slices.Reverse` / `slices.Compact`

**Requires:** Go 1.21+

**Use when:** 手書きloopがAPIの意味と完全に一致する。

**Avoid when:**

- reverseと同時に変換処理をしている
- duplicate除去が「連続要素」ではなく集合全体を意味する

`slices.Compact`は連続した重複をまとめるAPIであり、set化とは異なる。

## `maps.Clone`

**Requires:** Go 1.21+

**Use when:** mapのshallow copyを作るだけ。

**Avoid when:**

- valueのdeep copyが必要
- copy loop中にfilter / transformしている

## `maps.DeleteFunc`

**Requires:** Go 1.21+

**Use when:** predicateに一致するentryを削除するだけ。

**Avoid when:** deletion以外のside effectがloopにある。

## `maps.Keys` / `maps.Values`

**Requires:** iterator APIが利用できるGo version。代表的にはGo 1.23+。

**Use when:**

- lazy iterationで十分ならiteratorをそのままrangeする
- sliceが必要なら`slices.Collect(...)`でmaterializeする

**Avoid when:**

- deterministic orderが必要
- allocation-free iterationが目的なのに一度slice化してしまう

map iteration orderは保証されない。sliceへ集めても自動的に安定順序にはならない。

## `clear`

**Requires:** Go 1.21+

**Use when:**

- mapの全entryを削除する
- sliceの全要素をzero valueへ戻す

**Avoid when:** loopにcleanupやrelease等のside effectがある。

## `min` / `max`

**Requires:** Go 1.21+

**Use when:** 単純な値比較を結果として返す。

**Avoid when:** branchごとに別処理を行う、またはNaN等の挙動差を意識する必要がある。

## Integer `range`

**Requires:** Go 1.22+

Prefer:

```go
for i := range n {
    // ...
}
```

Use when a classic loop is exactly `0 <= i < n` with unit increment.

**Avoid when:**

- non-zero start
- stepが1以外
- loop variableを特殊に更新する

## Loop variable capture

**Requires:** Go 1.22+ semantics

Go 1.22+のmoduleでは、range / for loopのiteration variable capture回避のためだけの`v := v`は通常不要。

**Avoid removing when:** その再束縛にcapture回避以外の意味がある、または対象moduleが古いlanguage versionを使う。

## `strings.CutPrefix`

**Requires:** Go 1.20+

`HasPrefix`で確認してから同じprefixを`TrimPrefix`するだけなら`CutPrefix`を優先する。

**Avoid when:** prefix判定とtrimが異なる条件・値を使う。

## `strings.SplitSeq` / `strings.FieldsSeq`

**Requires:** Go 1.24+

**Use when:** split結果をsliceとして保持せず一度だけiterationする。

**Avoid when:**

- lengthやrandom accessが必要
- resultを複数回使う
- API境界でsliceが必要

iterator化はallocation削減のために意図を複雑にしない範囲で使う。

## `cmp.Or`

**Requires:** Go 1.22+

**Use when:** comparable valueについてzero valueなら次候補へfallbackする意図を表す。

**Avoid when:**

- zero value自体が有効な値
- fallback条件がzero-value判定ではない
- candidate計算のevaluation timingが重要
