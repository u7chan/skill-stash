# Performance Diagnostics

「Dockerが重い」「遅い」「diskを使いすぎる」といった依頼で最初に参照する。

## Start with Classification

症状を先に分類する。

```text
disk pressure
  -> docker system df

CPU / memory pressure
  -> docker stats --no-stream

slow build
  -> build context / cache invalidation / dependency install

large image / slow pull
  -> image layers / base image / runtime dependencies

slow file access
  -> bind mount / host filesystem / volume

slow HTTP response
  -> application / database / external I/O / resource pressure

slow startup
  -> image pull / initialization / dependency readiness / application boot
```

複数原因があり得るが、最初から全部変更しない。

## Disk Usage

まず確認する。

```sh
docker system df
docker ps -a
docker images
docker volume ls
```

reclaimableが多くても、即pruneしない。

停止containerやimageがrollback / debugging用に必要な可能性がある。

## Runtime Resources

```sh
docker stats --no-stream
```

確認する。

- CPUが特定containerだけ突出しているか
- memory usage / limit
- block I/O
- network I/O

一つのapplication containerだけ異常なら、Docker daemonではなくapplication code、DB query、loop、cache miss等を疑う。

## Build Performance

slow buildでは次を分ける。

- context transfer
- base image pull
- dependency download
- compilation
- cache miss
- multi-platform build

Dockerfile変更前に、どのstepで時間を使っているかbuild outputから確認する。

## HTTP Latency

Docker設定変更でapplication responseを改善したい場合は、同一endpointを複数回測る。

warm-up、cache、外部APIのばらつきを考慮し、1回の値で判断しない。

可能ならmedianとtail latencyを比較する。

browser表示時間とHTTP server response timeを混同しない。frontend asset、browser cache、third-party requestは別要因。

## Logs

disk pressureの原因がcontainer logsの場合は、logging driverとrotationを確認する。

log量が多い原因そのものがapplication error loopである場合、rotationだけでは根本解決にならない。

## Cleanup

cleanupは診断結果として不要resourceが特定できた場合だけ検討する。

危険度の高い一括削除より、対象を限定した削除を優先する。

## Compare One Change at a Time

performance改善では原則として一度に一つの主要因を変更する。

変更前後で同じ条件を使う。

- same workload
- same endpoint
- same build target
- same cache state
- comparable host load

複数変更をまとめると何が効いたか分からなくなる。

## Report No-Change Honestly

再計測で改善しなかった場合は、その結果を報告する。

performance impactがない変更を「最適化できた」と扱わない。
