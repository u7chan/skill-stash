# Package Entry Points

公開packageでは、tree-shakingだけでなく「consumerがどのmodule boundaryへ到達できるか」を設計する。

## Root entry point

小規模packageではroot entry pointだけで十分なことが多い。

```ts
export { parse } from "./parse";
export { format } from "./format";
```

pure ESMとして独立exportが保たれ、対象bundlerが解析できるなら、root importだけでもtree-shakingできる。

## Subpath exports

大きなpackageや独立機能群では、documented subpath exportを提供するとconsumerが必要なboundaryへ直接到達できる。

```json
{
  "exports": {
    ".": "./dist/index.js",
    "./parse": "./dist/parse.js",
    "./format": "./dist/format.js"
  }
}
```

consumer:

```ts
import { parse } from "pkg/parse";
```

subpath exportはtree-shakingが失敗する設計の万能な回避策ではない。次の目的で使う。

- 独立機能を安定したpublic APIとして公開する
- root entry pointの依存graphを通さず利用できるようにする
- internal file layoutへのdeep importを防ぐ

## Avoid undocumented deep imports

次のようにpackage内部の実ファイルへ直接依存させない。

```ts
import { parse } from "pkg/dist/internal/parser.js";
```

短期的にbundleが減っても、package内部構造をpublic contractとして固定し、version updateで壊れやすい。

必要なら正式なsubpath exportを追加する。

## ESM and CommonJS

sourceがESMでもpublish artifactがCommonJSへ変換されている場合、consumer bundlerがexportを同じ粒度で追跡できるとは限らない。

確認する。

- package.jsonの`type`
- `exports` condition
- `import` / `require`で異なるartifactを出しているか
- `main` / `module`等のlegacy field
- 実際にpublishされる`dist`内容

source treeだけを見てtree-shaking可能と断定しない。

## Dual package boundaries

ESMとCommonJSを両方提供する場合、同じpublic APIでも別build artifactになる。

bundle-sensitiveな変更では、対象consumerがどちらを解決するか確認する。意図しないCommonJS fallbackが起きているなら、consumer import構文よりpackage resolutionの方が本質的な問題である。

## Public API compatibility

entry point変更では、bundle sizeより先に互換性を確認する。

- existing root importを壊さないか
- type declarationsが各entry pointで解決できるか
- runtimeとtypesのexport surfaceが一致するか
- Node / browser / bundler conditionが意図通りか

## Review questions

- root entry pointだけで十分にtree-shakableか
- subpath exportに独立した意味があるか
- consumerがinternal deep importへ逃げていないか
- publish artifactはsourceと同じmodule formatか
- package resolutionが意図したESM artifactを選んでいるか
