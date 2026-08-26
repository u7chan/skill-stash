# Types and Language Features

型・reflection・language featureに関するmodern Go判断。

## `any`

**Requires:** Go 1.18+

新規コードではempty interfaceの意図を`any`で表す。

既存の`interface{}`は、今回触るsignatureやimplementationに自然に含まれる場合だけ置換する。大量のcosmetic migrationを行わない。

## `reflect.TypeFor`

**Requires:** Go 1.22+

Prefer:

```go
t := reflect.TypeFor[MyType]()
```

over sentinel pointer patterns such as:

```go
t := reflect.TypeOf((*MyType)(nil)).Elem()
```

**Use when:** compile-time type parameter / concrete typeの`reflect.Type`取得が目的。

**Avoid when:** runtime value自体のdynamic typeを調べる必要がある。

## `new(expr)`

**Requires:** Go 1.26+

値を初期化したpointerが必要なだけなら、temporary variableやhelper functionより`new(expr)`を優先できる。

Example:

```go
p := new(42)
```

**Use when:**

- literalや式の値へのpointerを直接作りたい
- temporary bindingに他の意味がない

**Avoid when:**

- 変数名がdomain meaningを伝える
- addressable localを後から変更する
- pointer生成自体を隠すべきでないAPI設計

短さだけを理由に意味のあるlocal variableを消さない。

## Generic methods

**Requires:** Go 1.27+

operationが特定のgeneric receiver typeへ自然に属する場合、package-level generic helperよりgeneric methodを検討する。

**Use when:**

- operationのnamespaceがreceiver typeに属する
- fluent / discoverable APIとして自然
- package-level helperよりownershipが明確

**Avoid when:**

- 複数の対等なtypeを扱い、receiverを一つ選ぶ意味がない
- stateless package operationとしての方が明確
- 既存public APIを破壊するmigrationになる

新規API設計ではmodern syntaxを使い、既存APIの全面移行は別taskとして扱う。

## Type aliases and generics

modern language featureを使えるからという理由で既存interfaceやconcrete typeをgeneric化しない。

genericsは重複実装を減らし、型関係を明確にできる場合に使う。単一実装しかない処理を抽象化するためだけに導入しない。

## Keep zero values meaningful

modern APIへの置換時も、Goのzero-value usabilityを壊さない。

pointer化、optional wrapper、constructor強制等をmodernizationに混ぜない。
