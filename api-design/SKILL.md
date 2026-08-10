---
name: api-design
description: HTTP/Web APIを設計・レビューするときに使う。RFCとIETF仕様を優先し、HTTP semantics、リソース設計、エラー、認証、ページネーション、冪等性、Rate Limit、バージョニング、廃止、OpenAPIを一貫した判断基準で扱う。
---

# API Design

HTTP/Web APIを、独自ルールより標準を優先して設計・レビューする。

## 判断の優先順位

迷ったときは次の順で判断する。

1. Published RFC / official standard
2. Active IETF specification
3. Established industry practice
4. Project-local convention
5. Custom design

標準で解決できる問題に独自プロトコルを作らない。

既存APIとの互換性が必要な場合は、破壊的に標準へ寄せずプロジェクト規約を優先する。

IETF Draftを根拠にする場合は、現在もActiveか確認する。DraftをPublished RFCとして扱わない。

## HTTP Semantics

RFC 9110のHTTP semanticsに従う。

- HTTP methodは定義された意味に沿って使う。
- Safe / idempotentなmethodの性質を壊さない。
- Status codeは本来の意味に沿って使う。
- Application errorを成功した`2xx`として返さない。

URLはresource-orientedを基本とする。

```text
/users
/users/{userId}/orders
```

resourceには名詞を使う。

操作がresource semanticsへ自然に落とせない場合のみaction-style endpointを検討する。

## Error

新規APIのエラー表現はRFC 9457 Problem Detailsを第一候補にする。

```http
Content-Type: application/problem+json
```

```json
{
  "type": "https://example.com/problems/insufficient-credit",
  "title": "Insufficient credit",
  "status": 403,
  "detail": "The account does not have enough credit."
}
```

- `type`をmachine-readableな問題種別として扱う。
- Clientが必要とするdomain-specific情報はextension memberとして追加する。
- 理由なく独自error envelopeを新設しない。
- 既存のdomain-specific error formatがある場合は互換性を考慮する。

## Date and Time

API境界のtimestampはRFC 3339形式を使う。

UTCで表現できる時刻は`Z`を優先する。

```text
2026-08-10T12:34:56Z
```

local time自体に意味がある場合はtimezone / offsetの要件を明示する。

## Authentication and Authorization

OAuthを使う場合はRFC 9700のSecurity Best Current Practiceを確認する。

Authorization Code GrantではPKCEを基本とする。

- Public clientはPKCEを使う。
- Confidential clientでもPKCEを推奨する。
- PKCEでは`S256`を使う。
- Authentication / user identityが必要ならOpenID Connectを使う。
- 新規設計で非推奨・脆弱な古いflowを採用しない。

AuthenticationとAuthorizationを混同しない。

## Pagination

大量または更新頻度の高いcollectionではcursor-based paginationを優先する。

```json
{
  "items": [],
  "nextCursor": "opaque-token"
}
```

- Cursorはclientからopaqueとして扱えるようにする。
- Offset paginationは単純さや任意ページ移動が明確な要件の場合に使う。
- 並び順を安定させる。
- Cursorが何をencodeしているかをclient contractにしない。

## Idempotency and Retry

GET / PUT / DELETEなどHTTP上idempotentなmethodのsemanticsを尊重する。

POSTなど副作用のある操作を安全にretryさせる必要がある場合は、idempotency key方式を検討する。

```http
Idempotency-Key: "<unique-key>"
```

ただし`Idempotency-Key`をPublished RFCとして扱わない。採用時は現在の標準化状況と業界実装を確認し、次をcontractとして定義する。

- keyのscope
- keyの有効期限
- 同一key + 異なるpayloadの扱い
- 処理中retryの扱い
- response再現方法

## Rate Limiting

制限超過には`429 Too Many Requests`を使う。

retry可能時刻または待機時間を示せる場合は`Retry-After`を使う。

RateLimit系headerを採用する場合はIETF仕様の現在のstatusを確認する。Draft段階のfieldをPublished Standardとして扱わない。

独自headerを増やす前に、既存標準・標準化中仕様・広く採用されたpracticeを確認する。

## Versioning

互換性を維持できる変更ではversionを増やさない。

明示的なmajor versionが必要な場合は、一貫した単純な方式を選ぶ。

```text
/v1/users
```

`/v1`を絶対ルールにはしない。Public APIの互換性モデル、client更新頻度、deploy方式に応じて判断する。

minor implementation changeをAPI versionとして公開しない。

## Deprecation and Sunset

APIを廃止する場合は暗黙に消さず、移行期間とreplacementを明示する。

標準HTTP fieldを優先する。

- `Deprecation`: RFC 9745
- `Sunset`: RFC 8594

replacementがある場合はmigration pathをdocumentする。

`Deprecation`と`Sunset`は同義ではない。deprecatedになった時点と利用不能になる予定時点を分けて扱う。

## API Contract

外部から利用されるHTTP APIはOpenAPIでcontractを記述する。

Implementation / validation / documentation / OpenAPIの挙動を一致させる。

Contractで最低限明示する。

- method / path
- request parameters / body
- response schemas
- error responses
- authentication requirements
- pagination
- retry / idempotency semantics
- rate-limit behavior
- compatibility / deprecation policy

## Design Workflow

API設計時は次の順で進める。

1. Resourceとoperationを特定する。
2. HTTP semanticsへ自然にmappingする。
3. Request / response / error contractを定義する。
4. Authentication / authorization境界を定義する。
5. Retry・pagination・rate limitなど運用時のsemanticsを定義する。
6. Compatibilityとdeprecation方針を確認する。
7. OpenAPIへ反映する。
8. 独自仕様が残った場合、その理由を説明できるか確認する。

## Review Checklist

APIレビューでは最低限確認する。

- HTTP method semanticsは正しいか
- Status codeは適切か
- Resource namingは一貫しているか
- Request / response schemaは明確か
- ErrorはRFC 9457を利用できないか
- Authentication / authorization境界は明確か
- Pagination方式はdata特性に合っているか
- Retry時に重複副作用が起きないか
- Rate limit時のclient behaviorが定義されているか
- Timestamp / timezone semanticsは明確か
- Versioningが不要に増えていないか
- Deprecation / Sunset / migration pathが定義されているか
- OpenAPIと実装が一致しているか
- 標準がある領域で独自仕様を作っていないか

## Standards Baseline

仕様を実装・レビューするときは番号だけを盲信せず、必要に応じて現在のstatus・後継RFC・errataを確認する。

主要な基準:

- RFC 9110: HTTP Semantics
- RFC 9457: Problem Details for HTTP APIs
- RFC 3339: Date and Time on the Internet
- RFC 7636: Proof Key for Code Exchange (PKCE)
- RFC 9700: Best Current Practice for OAuth 2.0 Security
- RFC 9745: Deprecation HTTP Response Header Field
- RFC 8594: Sunset HTTP Header Field
- OpenAPI Specification
