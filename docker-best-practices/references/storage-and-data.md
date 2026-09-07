# Storage / I/O / Persistent Data

bind mount、named volume、database、cache、persistent dataに関係する場合だけ参照する。

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

1. current data locationを特定
2. backupを作成
3. isolatedな場所へrestoreして読めることを確認
4. Compose / mount設定を変更
5. serviceを再作成
6. dataをrestoreまたはcopy
7. applicationからread/write確認
8. restart / recreate後もdataが残ることを確認
9. old dataを削除するかは別判断

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
