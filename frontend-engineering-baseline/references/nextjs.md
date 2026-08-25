# Next.js

Next.js repositoryでのみ使用する。

Next.jsの仕様は変化が速いため、installed versionを確認せずに最新の慣習を適用しない。

## Inspect

最低限確認する。

- Next.js version
- React version
- App Router / Pages Router
- deployment environment
- authentication strategy
- data fetching strategy
- caching strategy
- mutation strategy

## Routing

現在利用しているNext.js versionのrouting conventionsを確認する。

旧形式から新形式への移行をbaseline改善のついでに実施しない。migrationが必要なら独立した変更として扱う。

## Type safety

frameworkが提供するroute typingやgenerated typesが利用可能なら導入価値を検討する。

experimentalまたはversion-dependentな機能は、現在の公式仕様を確認してから利用する。

## Authentication and authorization

routing layerのauthenticationとdata accessのauthorizationを区別する。

UIやrequest interceptionだけで重要データのアクセス制御を完結させない。protected dataは実際のdata-access boundaryでもauthorizationを確認する。

## Server-side mutations

server-side mutationも通常のAPI endpointと同じtrust boundaryとして扱う。

入力値を信用せず、必要に応じてauthentication、authorization、validationを行う。

## Cache

cacheは性能改善のための手段であり、必須のbaselineではない。

導入前に以下を説明できることを確認する。

- 何をcacheするか
- 誰のデータか
- いつ期限切れになるか
- mutation後にどうinvalidationするか

理解できないcacheを追加しない。user-specific dataでは特に慎重に扱う。

## Environment variables

clientとserverの境界を確認し、秘密情報をclient bundleに含めない。

可能であれば起動時またはbuild時に必須environment variablesを検証する。
