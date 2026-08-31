---
name: bundle-efficient-module-design
description: TypeScript/JavaScriptのモジュール、共有ライブラリ、npm package、フロントエンドコードでtree-shakingやbundle sizeを改善するときに使う。import文だけを機械的に変えず、export shape、barrel、side effect、package entry point、module formatを確認し、production bundleの実測で効果を検証する。
---

# Bundle-Efficient Module Design

JavaScript / TypeScriptのmodule boundaryを、bundlerが不要コードを除去しやすい形へ整える。

目的は「特定のimport構文を使うこと」ではない。静的解析可能なexport graphを保ち、public APIやruntime behaviorを壊さず、実際のproduction bundleで効果を確認する。

## Core Principles

### Optimize module shape before import style

`import { x }`、`import * as x`、default importのどれが有利かは、library側のexport構造とbundlerの解析能力で変わる。

import構文だけを見てtree-shaking可否を断定しない。まず以下を確認する。

- exportされた値が独立したbindingか
- 複数機能を1つのobjectへ束ねていないか
- re-export経路に副作用がないか
- package entry pointが不要なmoduleまで到達させていないか
- ESMとCommonJSの境界がどこにあるか

詳細は [references/export-shapes.md](references/export-shapes.md) を参照する。

### Prefer statically analyzable boundaries

bundlerが「どのexportが使われたか」を静的に追跡できる構造を優先する。

代表例:

```ts
// Prefer when each feature can stand alone.
export { parse } from "./parse";
export { format } from "./format";
```

以下は必要性がなければ避ける。

```ts
export const toolkit = {
  parse,
  format,
};
```

後者が常にtree-shaking不能とは限らないが、property accessやobject constructionを跨いだ除去はbundler依存になりやすい。

### Treat barrels as a graph boundary, not an anti-pattern

`index.ts`や`export *`自体を禁止しない。

問題はbarrel経由で不要moduleの評価、副作用、CommonJS境界、大きな依存graphまで到達する場合である。barrelを消す前に実際の依存graphを確認する。

詳細は [references/side-effects-and-barrels.md](references/side-effects-and-barrels.md) を参照する。

### Preserve side effects intentionally

`sideEffects: false`をbundle削減のためだけに追加しない。

module evaluation時に必要な処理、CSS import、polyfill、registration、global mutationなどが存在する場合、誤ったside-effect宣言はproduction behaviorを壊し得る。

### Design package entry points deliberately

公開packageではroot entry pointだけでなく、必要に応じてsubpath exportsを提供する。

```json
{
  "exports": {
    ".": "./dist/index.js",
    "./parse": "./dist/parse.js"
  }
}
```

subpath exportはtree-shakingの代替ではない。consumerが必要な機能へ直接到達できる安定したpublic boundaryとして使う。

詳細は [references/package-entrypoints.md](references/package-entrypoints.md) を参照する。

### Measure instead of assuming

source codeだけを見て「小さくなるはず」で完了しない。

production条件で代表的なconsumer entryをbuildし、before / afterのartifactを比較する。可能ならbundle analyzerやmetafile等で、どのmoduleが残ったかも確認する。

詳細は [references/verification.md](references/verification.md) を参照する。

## Workflow

### 1. Establish the bundle context

最低限確認する。

- browser / edge / libraryなどのtarget
- bundlerとproduction build command
- ESM / CommonJSの出力形式
- `package.json`の`exports` / `main` / `module` / `sideEffects`
- bundler固有のtree-shaking設定
- bundle sizeに関する既存budgetやCI

Node.jsだけで実行されbundleされないコードなら、このスキルを機械的に適用しない。

### 2. Trace the relevant module graph

変更対象から必要な範囲だけ追跡する。

候補:

- aggregate object export
- default exportへ多数機能を集約
- namespace objectをnamed export
- barrelから広い依存graphをre-export
- import時にregister / mutate / polyfillするmodule
- root entry pointしか公開されていないpackage
- ESMからCommonJSへ落ちる境界
- computed property accessなど静的解析しにくい参照

### 3. Classify the candidate

各候補を以下へ分類する。

- **Apply now**: public behaviorを保ち、変更範囲内で静的解析性を明確に改善できる
- **Measure first**: 理論上は候補だが、現bundlerで削減効果が不明
- **Follow-up**: public API変更、package再設計、広いmigrationが必要
- **Skip**: bundle対象外、効果なし、またはbehavior riskが高い

原則として`Apply now`と`Measure first`だけを今回扱う。

### 4. Make the smallest coherent change

優先順位:

1. 不要なaggregate objectを独立exportへ分離
2. side effectを必要なmoduleへ局所化
3. barrel経由の不要評価を減らす
4. 必要ならstableなsubpath exportを追加
5. consumer importを新しいpublic boundaryへ合わせる

bundle削減だけを理由にprivate pathへのdeep importを導入しない。

### 5. Validate behavior and bundle output

最低限、以下を確認する。

- repository既存test / typecheck / lint
- production build成功
- public import pathが維持されているか、または意図したmigrationか
- before / afterのbundle size
- 可能なら残存moduleの差分

raw byteだけでなく、利用環境で意味がある場合はminified / compressed sizeも比較する。

## Decision Priority

競合する場合は次の順で判断する。

**correctness → runtime behavior → public API compatibility → static analyzability → measured bundle impact → stylistic preference**

## Guardrails

禁止する。

- `import * as`やnamed importを一律に推奨する
- source syntaxだけでtree-shaking成功を断定する
- `sideEffects: false`を副作用確認なしで追加する
- barrel fileを存在だけで削除する
- packageの非公開pathへconsumerを依存させる
- bundle削減のためにpublic APIを無断で破壊する
- development buildだけでサイズ効果を判断する
- bundle size以外の無関係なcode splittingやasset最適化まで広げる

## Completion Report

完了時は簡潔に報告する。

- **Context**: target / bundler / module format
- **Changed**: export / side effect / entry pointの変更
- **Evidence**: before / after bundle sizeと確認方法
- **Compatibility**: public APIやruntime behaviorへの影響
- **Follow-up**: 今回扱わなかったbundle候補があれば記載
