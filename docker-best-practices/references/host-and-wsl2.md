# Host / Docker Desktop / WSL2

Docker Desktop、Windows、WSL2、host resource allocationが問題に関係する場合だけ参照する。

## Confirm the Platform First

WSL2固有の対策を適用する前に確認する。

- Windows + WSL2 backendか
- project fileがWindows filesystem側かLinux filesystem側か
- Docker daemon / Docker Desktopの実行方式
- CPU / memory pressure
- bind mountの対象path

Linux nativeやmacOSへWSL2用設定を適用しない。

## WSL2 File Location

大量の小fileを扱うdevelopment workloadでは、Windows filesystemとWSL2 Linux filesystemの境界をまたぐI/Oがbottleneckになる場合がある。

Node.js、PHP、Python等でsource tree、dependency tree、cache directoryを頻繁に読む構成では特に確認する。

projectを移動する場合は、変更前後で次を比較する。

- application response
- build time
- file watcher behavior
- hot reload
- bind mount I/O

速くなる前提で移動しない。

## Docker Desktop Resource Allocation

CPU / memoryを増やせば常に速くなるわけではない。

container側がresource不足か確認してから変更する。

増やしすぎるとhost OS、IDE、browser等を圧迫し、machine全体が遅くなる。

一度に大きく変えず、同じworkloadで比較する。

## WSL Resource Configuration

WSL全体のresource設定を変更する場合は、Dockerだけでなく他のWSL workloadへの影響も考慮する。

設定値を固定の推奨値として提示しない。

hostのphysical memory、CPU core、同時実行workloadに合わせる。

## Bind Mount Alternatives

Windows側pathのbind mountがI/O bottleneckなら、次を候補として比較する。

- projectをWSL2 Linux filesystemへ置く
- high-write directoryだけnamed volumeへ分離
- dependency/cache directoryだけcontainer-managed storageへ分離

source editingが必要なdirectoryまで無条件にnamed volumeへ移さない。

## Windows Command Differences

PowerShellではUnix系のcommand名がaliasになっている場合がある。

HTTP計測等で実行binaryが重要な場合は、実際に呼ばれるcommandを確認する。

platform差を理由にskill内へ大量のshell分岐を持ち込まず、必要な場面だけ明示する。

## Validation

host-level変更ではcontainer内部だけでなくmachine全体を見る。

- Docker workload
- IDE responsiveness
- browser responsiveness
- WSL memory usage
- host free memory
- file watcher latency

Dockerだけ速くなってhost全体が悪化した場合は成功とみなさない。
