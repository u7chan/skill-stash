# Standard Library and HTTP

time、fmt、JSON、HTTP等のstandard library modernizationを扱う。

## `time.Since` / `time.Until`

`time.Since`: Go 1.0+

`time.Until`: Go 1.8+

Prefer intent-revealing helpers over manual subtraction when semantics are identical.

```go
elapsed := time.Since(start)
timeout := time.Until(deadline)
```

**Avoid when:** subtraction operandsが`time.Now()`以外、またはclock evaluation timing自体が重要。

## `fmt.Appendf`

**Requires:** Go 1.19+

`[]byte(fmt.Sprintf(...))`のようにformat結果をbytesへ変換するだけなら`fmt.Appendf`等のappend APIを検討する。

**Avoid when:** string resultも必要、またはallocation差より可読性を優先すべき小さなコード。

## JSON `omitzero`

**Requires:** Go 1.24+

zero value omissionの意味を表したい場合、`omitzero`を検討する。

**Do not mechanically replace `omitempty`.**

`omitempty`と`omitzero`はfield typeによってwire outputが変わり得る。既存API / persisted dataではserialized outputをtestしてから変更する。

新規schemaではdomain上の「empty」と「zero」のどちらを省略したいかを明示して選ぶ。

## `encoding/json/v2`

**Requires:** Go 1.27+

新規JSON codeでは、対象projectのcompatibility方針が許すなら`encoding/json/v2`を優先候補にする。

既存`encoding/json` codeは、明示的なmigration依頼がない限りimportを置き換えない。

理由:

- invalid UTF-8 handling
- duplicate object names
- nil slice / map encoding
- invalid JSON-related Go type handling

など、compileが通ってもwire behaviorが変わり得るため。

explicit migrationでは、既存wire behaviorのfixture / golden testを用意し、compatibility optionを使う場合も段階的に差分を確認する。

## Modern `http.ServeMux`

**Requires:** Go 1.22+

methodとpath parameterをrouting patternで直接表せる場合はmodern patternを使う。

Example:

```go
mux.HandleFunc("GET /users/{id}", func(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
    // ...
})
```

**Use when:**

- method checkとpath parsingをServeMux patternへ自然に移せる
- new routeを追加する

**Avoid automatic migration when:**

- legacy routing behaviorとの互換性が重要
- middleware / router abstractionが独自routing contractを持つ
- wildcard / precedence behaviorの差を未検証

routing migrationはtestでmethod、path params、404 / 405、precedenceを確認する。

## Standard library before helper packages

対象Go versionのstandard libraryが既存helperの目的を直接満たす場合、新規コードではstdlibを優先する。

ただし既存dependencyを消すためだけに広範囲をrewriteしない。dependency removalは利用箇所、API behavior、binary size、maintenance costを含む別判断として扱う。
