# Verification

Bundle最適化は、production artifactのbefore / afterで証明する。

## Use the real production path

repository既存のproduction build commandを優先する。

例:

```sh
npm run build
```

```sh
pnpm build
```

```sh
bun run build
```

開発サーバーのmodule graphやdevelopment bundleは、production時のminify / tree-shaking / chunking条件と異なることがあるため、サイズ判定の根拠にしない。

## Define a representative consumer

library packageでは、package自身のdist sizeだけではconsumer bundleへの影響を測れない場合がある。

必要なら最小consumer entryを用意する。

```ts
import { parse } from "pkg";

console.log(parse("example"));
```

before / afterで同じconsumer、同じbundler、同じbuild設定を使う。

## What to compare

最低限:

- build成功
- entry chunkまたは対象chunkのbyte size
- before / after差分

利用環境に応じて追加する。

- minified size
- gzip / brotli size
- bundle analyzer
- bundler metafile / stats
- included module list
- chunk count

source mapは比較対象から除外するか、別項目として扱う。

## Verify code removal, not only bytes

数KBの差だけでは原因を誤認することがある。

analyzerやmetafileが利用できる場合、狙ったmodule / dependencyが実際に消えたか確認する。

例:

```text
Before
entry
└─ package/index
   ├─ parse
   ├─ format
   └─ heavy-validator

After
entry
└─ package/parse
   └─ parse
```

狙ったmoduleが残っているなら、minifier差やchunk配置変更によるサイズ差をtree-shaking成功と誤認しない。

## Preserve runtime behavior

bundleが小さくなっても、必要なside effectが消えたら失敗である。

実行する。

- unit / integration test
- typecheck
- relevant smoke test
- package consumer testがあればそれも実行

特に`sideEffects`変更時は、registration、CSS、polyfill、global setupなどをproduction相当で確認する。

## Avoid noisy comparisons

before / afterで以下を変えない。

- dependency lockfile
- bundler version
- minifier設定
- target browser / runtime
- environment flag
- unrelated source code

無関係な変更が混ざる場合、bundle差分を今回のmodule設計変更の成果として扱わない。

## No measurable improvement

期待した削減が確認できなければ、変更を正当化する別の理由がない限り無理に採用しない。

可能性:

- bundlerが既に同等の最適化をしている
- 対象moduleが元々bundleへ含まれていない
- public API facadeを保持した結果、依存graphが変わっていない
- side effectによりmoduleを除去できない
- CommonJS境界で解析粒度が落ちている

この場合は`Measure first`を`Skip`または`Follow-up`へ分類し直す。

## Completion evidence

報告例:

```text
Context: Vite production build / ESM
Changed: aggregate exportを独立exportへ分離
Bundle: 42.1 kB -> 35.8 kB minified (-6.3 kB, -15.0%)
Evidence: analyzerでunused validator moduleが除外されたことを確認
Compatibility: existing root importは維持、tests passed
```

数値を取得できない場合は推測値を書かず、何を確認できなかったか明記する。
