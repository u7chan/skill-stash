# Compute / Runtime Validation

対象例: EC2、ECS、EKS、Lambda、ECR、Batchなど。

目的はresource definitionだけでなく、Flociで再現可能な範囲のruntime接続まで確認すること。

## Validate

L1-L2では主に確認する。

- image / runtime / architecture
- task / function / node configuration
- environment variables
- port mapping
- execution role参照
- subnet / security group参照
- scaling条件やcount / for_each logic
- outputs

L3ではFlociのcurrent supportを確認したうえで、今回の変更に必要な最小operationを実行する。

代表的なsmoke test:

- resourceが作成されstateへ反映される
- expected identifier / endpoint / ARN相当値が得られる
- Flociが実runtimeを提供するserviceでは、起動状態または最小requestを確認する
- image参照やdependencyが解決できる

## Do not overclaim

Floci上のruntime成功から、次を保証しない。

- AWS scheduler placement
- production autoscaling
- capacity shortage behavior
- Fargate / EC2 launch typeの完全互換
- EKS control plane / managed node groupのAWS固有挙動
- Lambda concurrency / cold start / service quota
- IAM enforcement
- AZ failure behavior

これらが変更のcorrectnessに重要ならL4項目へ残す。

## ECS / EKS / Lambdaなどの実container

FlociがDocker containerやlocal runtimeを利用するserviceでは、containerが起動した事実を追加証拠にできる。

ただしcontainer implementation detailへTerraform production designを合わせない。

## Image-dependent validation

ECRやcontainer imageが必要な構成では、今回のTerraform変更と無関係なimage build/publish pipelineまで拡張しない。

既存fixture/imageがあれば利用する。無ければresource configurationの検証までで止め、runtime smoke未実施を報告する。
