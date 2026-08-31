# Side Effects and Barrels

Tree-shakingは「未使用exportを消す」だけではなく、module自体を安全に除外できるかにも依存する。

## Module side effects

importしただけでobservable behaviorが発生するmoduleは、未使用に見えても削除できない。

例:

```ts
registerPlugin();
```

```ts
globalThis.__feature = feature;
```

```ts
import "./styles.css";
```

```ts
import "./polyfill";
```

これらが必要なら副作用として保持する。問題は、副作用を持つmoduleとpureな機能exportを同じentry pointへ無関係に集約することである。

## Localize side effects

可能ならpureな定義とregistrationを分ける。

```ts
// parser.ts
export function parse(input: string) {
  // ...
}
```

```ts
// register-parser.ts
import { parse } from "./parser";
register("parser", parse);
```

consumerが`parse`だけを必要とするとき、registrationまで評価させないboundaryを作れる。

## `sideEffects` metadata

package.jsonの`sideEffects`は、package内のmoduleを未使用時に削除してよいかbundlerへ伝えるために使われることがある。

```json
{
  "sideEffects": false
}
```

これは「たぶんpureだから付ける」最適化フラグではない。import時に必要な処理が1つでもあるpackageで誤って指定すると、production buildで必要コードが消える可能性がある。

副作用fileが限定される場合は、利用bundlerが対応する形式に従って対象を明示することを検討する。

## Barrel files

barrelは複数moduleを1つの入口からre-exportする。

```ts
export * from "./parse";
export * from "./format";
```

barrelそのものはanti-patternではない。pure ESMの独立exportだけならtree-shaking可能なことも多い。

確認すべきなのはbarrelから到達するmodule graphである。

### Risk patterns

```ts
export * from "./parse";
export * from "./register-all";
```

`register-all`に副作用があれば、`parse`だけ使うconsumerにも影響し得る。

また、barrelがCommonJS moduleや巨大なthird-party dependencyを経由すると、bundlerが細粒度に解析できない場合がある。

## Internal barrels vs package boundaries

repository内部のimport整理だけを目的とするbarrelと、published packageのpublic entry pointは分けて考える。

package boundaryでは次を確認する。

- consumerがrootから必要機能だけ取得できるか
- root import時に不要な副作用が走らないか
- subpath exportが必要か
- internal pathをpublic APIとして偶発的に固定していないか

## Review questions

- import時に実行されるtop-level codeはあるか
- CSS / polyfill / registration / global mutationを見落としていないか
- barrel経由で副作用moduleへ到達していないか
- `sideEffects` metadataと実装が一致しているか
- barrel削除ではなく副作用分離で解決できないか
