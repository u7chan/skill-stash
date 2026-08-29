# Network / Edge Validation

対象例: VPC、Subnet、Route Table、Security Group、NACL、ELB/ALB/NLB、Route 53、CloudFront、API Gatewayなど。

network系resourceでは「Terraform resourceを作成できること」と「AWSと同じ通信制御が働くこと」を分ける。

## L1-L3で確認する

- CIDRや参照関係
- subnet / route / gateway association
- security rule definition
- listener / target group / routing rule configuration
- DNS / distribution / API resource definition
- provider APIがconfigurationを受理すること
- Flociが返すidentifierやstate shape

## L4へ残す

原則として実AWSで確認する。

- Security Group / NACLのpacket filtering
- route tableによる実packet routing
- NAT Gateway / Internet Gatewayの実到達性
- VPC DNS behavior
- load balancer health checkとtraffic distributionのAWS固有挙動
- Route 53 public/private DNS propagation
- CloudFront edge distribution / cache / TLS
- WAFとの実traffic integration
- cross-VPC / cross-account connectivity

## Smoke test

Flociがruntime behaviorを提供している場合でも、今回の変更に直接必要な範囲だけ確認する。

例:

- listener/resourceが作成される
- API Gateway routeが定義される
- expected DNS name / identifierが返る

localhost上で通信できたことを、VPC routingやSecurity Group enforcementの証拠として扱わない。

## Guardrail

Flociでnetwork enforcementが再現されないことを理由に、Security Groupを広げたりrouteを単純化したりしない。

network policyの正しさはTerraform definitionとして維持し、runtime verificationをL4へ残す。
