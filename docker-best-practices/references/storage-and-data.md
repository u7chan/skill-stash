# Storage / I/O / Persistent Data

bind mount、named volume、database、cache、persistent dataに関係する場合だけ参照する。

SKILL.mdのtask mode gateを優先する。migration、writer停止、restore、mount切替はImplement / Improve modeでユーザーが実変更を求めた場合だけ行う。Review / Design / Diagnose modeでは手順の提案までに留める。

## Choose Storage by Responsibility

### Bind mount

hostとcontainerで同じfile treeを直接共有する必要がある場合に使う。

典型例:

- source code editing
- local configuration
- generated artifact inspection

host filesystem性能やpermission semanticsの影響を受ける。

### Named volume

Docker管理下でpersistent dataを保持したい場合に使う。

典型例:

- database data
- package / application cache
- high-frequency mutable data

named volumeだから常に高速・安全とは限らない。用途とhost環境で判断する。

### tmpfs

永続化不要で、高頻度な一時書き込みに向く場合がある。

再起動で消えてよいデータだけに使う。

## Diagnose Before Migrating

I/O性能を疑う場合は、先に以下を確認する。

- 問題のpath
- current mount type
- host-side path
- read/write frequency
- application behavior
- database-specific requirements

大量の小file I/Oがある開発環境では、hostとLinux VM間のfilesystem境界が原因になる場合がある。

## Persistent Data Migration

bind mountからnamed volume等へ移行する場合は、直接置換しない。

基本順序:

1. current data locationとwriterを特定
2. rollback用backupが必要なら作成する。writer稼働中に取得したbackupは、整合性が保証される方式でない限りmigration sourceとして使わない
3. writerを停止またはquiesceし、移行中にsourceへ新規書き込みが発生しない状態にする
4. quiesce後のsourceからfinal copy / snapshot / consistent backupを取得する
5. final migration sourceをisolatedな場所で検証できる場合は、restoreまたはread testを行う
6. target volume / storageを作成する
7. serviceを起動しないまま、step 4のfinal migration sourceからtargetへpopulate / restoreする
8. target data、ownership、permissionsを確認する
9. Compose / mount設定をtargetへ切り替える
10. serviceをrecreate / startする
11. applicationからread/write確認
12. restart / recreate後もdataが残ることを確認
13. old dataを削除するかは別判断

移行元の基準点はwriter停止 / quiesce後に固定する。停止前に取得した通常backupをそのままmigration sourceにすると、その後の成功書き込みを欠落させる可能性がある。

空のtargetをmountしたserviceを先に起動し、その後で旧dataをrestoreしない。application initializationによる新規stateとの混在や上書きを避ける。

databaseの場合は、この一般手順よりengine固有のconsistent backup / dump / restore、snapshot、shutdown手順を優先する。engine固有手順がwriterを稼働させたままconsistent snapshotを保証する場合は、その整合性保証をmigration boundaryとして扱う。

backup commandのexit 0だけではrestore可能性を証明できない。

## Database Volumes

database directoryをfile単位で雑にcopyすると、整合性を壊す場合がある。

database固有のdump / restore、snapshot、shutdown手順がある場合はそれを優先する。

database engine、version、storage formatを確認せずmigration手順を一般化しない。

## Destructive Commands

persistent dataがある環境では特に注意する。

```sh
docker volume prune
docker compose down -v
```

「不要そう」という推測で実行しない。

削除対象volumeがapplication dataを持たないことを確認できない場合は停止する。

## Permissions

mount変更後はUID/GID、ownership、write permissionを確認する。

permission問題への対処として`chmod -R 777`を一般解にしない。

必要なuserとpathだけを修正する。

## Validation

storage変更後は少なくとも次を確認する。

- existing data can be read
- new data can be written
- restart後もdataが存在
- recreate後も期待通り保持
- backupからrestore可能
- file ownership / permissions
- I/O症状が実際に改善したか
