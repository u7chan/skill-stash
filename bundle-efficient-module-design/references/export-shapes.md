# Export Shapes

Tree-shakingの成否はimport構文だけではなく、exportされた値がbundlerからどのように見えるかで変わる。

## Independent bindings

最も追跡しやすい基本形は、機能ごとに独立したESM exportを持つ構造である。

```ts
export function parse(input: string) {
  // ...
}

export function format(value: Value) {
  // ...
}
```

consumerが`parse`だけを使う場合、bundlerは`format`が未使用であることをexport単位で判断しやすい。

```ts
import { parse } from "pkg";
```

## Aggregate object exports

複数機能を1つのobjectへ束ねると、export単位ではobject全体が1つのbindingになる。

```ts
export const toolkit = {
  parse,
  format,
  validate,
};
```

consumerが次のように使っても、未使用propertyまで除去できるかはbundlerと生成コード次第になる。

```ts
import { toolkit } from "pkg";
toolkit.parse(input);
```

この形が必要なAPIなら保持してよい。bundle削減が目的なら、独立exportをprimary APIとして追加し、aggregate objectをcompatibility facadeとして残せるか検討する。

## Namespace imports are not automatically better

以下の2つを構文だけで優劣判定しない。

```ts
import { parse } from "pkg";
```

```ts
import * as pkg from "pkg";
pkg.parse(input);
```

ESM namespaceのproperty参照をbundlerが静的に追跡できることは多いが、最終結果はpackageのexport graph、transpilation、CommonJS interop、bundler設定に依存する。

特に、library側が次のようなnamespace風objectをnamed exportしているケースと、ESM module namespace importを混同しない。

```ts
export const api = {
  parse,
  format,
};
```

```ts
import { api } from "pkg";
```

`api`はmodule namespaceではなく、通常のJavaScript objectである。

## Default exports

単一機能のdefault export自体は問題ではない。

注意するのは、多数の機能をdefault objectへ集約する形である。

```ts
export default {
  parse,
  format,
  validate,
};
```

bundle-sensitiveなlibrary APIでは、独立したnamed exportまたはdocumented subpath exportを優先する。

## Dynamic access

computed property accessは静的解析を難しくする。

```ts
pkg[name](input);
```

`name`がbuild時に確定しない場合、bundlerは複数候補を残す必要がある。

最適化のためだけに動的dispatchを排除する必要はないが、hot pathやbundle-critical boundaryで本当に必要か確認する。

## Review questions

- consumerが使う機能は独立exportとして表現できるか
- exported objectを作る必要が本当にあるか
- compatibilityのためobject APIを残しつつ、tree-shakable APIを追加できるか
- dynamic property accessが未使用コード除去を妨げていないか
- ESM sourceがpublish時に別形式へ変換されていないか
