# Btrfs

## Quick Description (QD)

**Btrfs** (B-tree file system, usually read "butter-FS") is a copy-on-write file system with built-in volume management. It was started at Oracle in 2007 and is developed inside the mainline Linux kernel (GPL). It is the default file system on distros like Fedora and openSUSE.

It is one file system that spans one or more devices, with **subvolumes** inside it. Redundancy is set by **profiles** (`single`, `raid1`, `raid10`, ...) applied to data and metadata separately, and you can change profiles later with a balance. It takes raw devices and does not use mdraid underneath.

```sh
grep btrfs /proc/filesystems
mkfs.btrfs --version
```

### Key Features of Btrfs

- Copy-on-write (CoW): Metadata and data are written to new locations, keeping the file system consistent.
- Subvolumes: Independent file trees inside one file system, mountable separately.
- Snapshots: Instant, space-efficient snapshots of subvolumes (writable or read-only).
- Checksums: Data and metadata are checksummed (crc32c by default) to detect corruption.
- Multi-device support: Profiles `single`, `dup`, `raid0`, `raid1`, `raid10` (raid5/6 are still considered unstable).
- Transparent compression: `zstd`, `lzo`, `zlib`.
- Send/receive: Incremental snapshot replication.
- Online resize, balance, and scrub.
- Uses the normal Linux page cache (light on RAM); no built-in tiered caching, but bcache or dm-cache can go underneath.

### Redundancy and Flexibility

- RAID 0, 1, 10 are solid, plus RAID1c3/c4 (three or four copies). RAID1 works at the chunk level, so mixed-size disks are used efficiently.
- RAID 5/6 still have documented reliability problems (the write hole, among others); avoid them for important data.
- Very flexible: add or remove devices online, shrink the file system, convert between profiles, then balance to redistribute data.

### Downsides and Quirks

- Odd out-of-space situations from chunk allocation; an occasional balance reclaims space.
- `btrfs check` exists but repair is risky.
- Seen as less battle-tested than ZFS for large, critical storage.
- No native encryption (use LUKS underneath) and no inline dedup (offline only, e.g. `duperemove`).

### Btrfs vs. ZFS

See the comparison table in [ZFS](file_systems/02_zfs.md). Pick Btrfs for desktops, laptops, and smaller servers that want snapshots and checksums with in-kernel support, flexible disk management, and mirror-based redundancy (RAID 1/10).

### Btrfs and mdraid

Give Btrfs the raw disks and use its RAID1/10 profiles. Btrfs on `/dev/md0` works but, as with ZFS, hides the redundant copies, so you get detection without self-healing. A common exception is single-device Btrfs on an mdraid RAID 5/6 array to get snapshots. See [Linux RAID](linux/07_raid.md).

## Installation

On Ubuntu/Debian:

```sh
sudo apt install btrfs-progs
```

## Useful Tips/Commands (UToC)

### Creating and Mounting

```sh
sudo mkfs.btrfs /dev/sdb

# multiple devices: mirror both data and metadata
sudo mkfs.btrfs -d raid1 -m raid1 /dev/sdb /dev/sdc

sudo mount /dev/sdb /mnt/btrfs
# with compression
sudo mount -o compress=zstd /dev/sdb /mnt/btrfs
```

> Warning: `mkfs.btrfs` erases existing data on the device.

### Subvolumes and Snapshots

```sh
sudo btrfs subvolume create /mnt/btrfs/data
sudo btrfs subvolume list /mnt/btrfs

sudo btrfs subvolume snapshot /mnt/btrfs/data /mnt/btrfs/data_snap
sudo btrfs subvolume snapshot -r /mnt/btrfs/data /mnt/btrfs/data_ro
sudo btrfs subvolume delete /mnt/btrfs/data_snap
```

### Space Usage

`df` is misleading on Btrfs; use:

```sh
sudo btrfs filesystem df /mnt/btrfs
sudo btrfs filesystem usage /mnt/btrfs
```

### Maintenance

```sh
sudo btrfs scrub start /mnt/btrfs
sudo btrfs scrub status /mnt/btrfs

sudo btrfs balance start -dusage=50 /mnt/btrfs

sudo btrfs device add /dev/sdd /mnt/btrfs
sudo btrfs filesystem resize max /mnt/btrfs
```

### Send/Receive

```sh
sudo btrfs send /mnt/btrfs/data_ro | sudo btrfs receive /mnt/backup
```

## Examples (e.g.,)

### Virtual Disk

```bash
truncate -s 2G btrfs_test.img
mkfs.btrfs -f btrfs_test.img

sudo mkdir /mnt/btrfstest
sudo mount -o loop,compress=zstd btrfs_test.img /mnt/btrfstest

# subvolume + snapshot
sudo btrfs subvolume create /mnt/btrfstest/vol
echo v1 | sudo tee /mnt/btrfstest/vol/file.txt
sudo btrfs subvolume snapshot /mnt/btrfstest/vol /mnt/btrfstest/vol_snap
echo v2 | sudo tee /mnt/btrfstest/vol/file.txt

cat /mnt/btrfstest/vol_snap/file.txt   # still v1
sudo btrfs filesystem usage /mnt/btrfstest
```

Clean up:

```bash
sudo umount /mnt/btrfstest
sudo rmdir /mnt/btrfstest
rm btrfs_test.img
```

## References

- [Btrfs Documentation](https://btrfs.readthedocs.io/)
- [Btrfs (Linux kernel docs)](https://docs.kernel.org/filesystems/btrfs.html)
- [btrfs(8) manual](https://man7.org/linux/man-pages/man8/btrfs.8.html)
- [mkfs.btrfs(8) manual](https://man7.org/linux/man-pages/man8/mkfs.btrfs.8.html)
