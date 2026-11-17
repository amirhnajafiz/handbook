# ZFS

## Quick Description (QD)

**ZFS** is a combined file system and volume manager, created at Sun Microsystems in the mid-2000s and now developed as **OpenZFS** (Linux, FreeBSD, illumos, others). It manages raw disks and files in one layer, so it does not need mdraid underneath. Its CDDL license is incompatible with the Linux kernel's GPL, so on Linux it is an out-of-tree module installed separately, which can occasionally lag behind new kernel releases.

ZFS builds a **pool** (`zpool`) out of **vdevs**; each vdev is a group of disks (a single disk, a mirror, or a RAID-Z set). Redundancy is defined per vdev and the pool stripes data across vdevs. From the pool you carve **datasets** (file systems) or **zvols** (block devices).

### Key Features of ZFS

- Copy-on-write (CoW): Data is never overwritten in place, so the on-disk state is always consistent.
- End-to-end checksums: Every block is checksummed, and bad blocks are repaired automatically from redundancy (self-healing).
- Storage pools (`zpool`): Disks are grouped into vdevs (single, mirror, raidz1/2/3) inside a pool, and datasets share the pool's space.
- Snapshots and clones: Cheap, instant, and read-only (snapshots) or writable (clones).
- Send/receive: Replicate snapshots, incrementally, to another pool or host.
- Compression, deduplication, encryption: Configured per dataset.
- ARC/L2ARC/SLOG/special vdevs: RAM cache (uses a large share of memory by default, released under pressure), SSD second-level read cache, a separate write log for synchronous writes, and fast metadata vdevs. The "1 GB RAM per TB" rule is exaggerated, but ZFS likes memory, especially with dedup.
- RAID-Z1/2/3: one, two, or three disks of parity (like RAID 5/6) without the RAID 5 write hole.

### Downsides and Quirks

- Out-of-tree on Linux (licensing), and uses a fair amount of RAM.
- Rigid layout: a vdev is mostly fixed once created, mixed disk sizes waste space, and you grow mainly by adding whole vdevs. Mirror vdevs can be removed; RAID-Z vdevs cannot, and pools cannot shrink. OpenZFS 2.3+ added RAID-Z expansion (add a disk to an existing RAID-Z vdev).
- Performance degrades as the pool fills; stay under about 80% full.
- No offline `fsck`; it relies on copy-on-write consistency and scrubs.

### ZFS vs. Btrfs

| | ZFS | Btrfs |
| --- | --- | --- |
| Checksums and self-healing | Yes | Yes (with redundant copies) |
| Snapshots | Read-only snapshots, writable clones | Subvolume snapshots, writable by default |
| Send/receive | Yes, very mature | Yes |
| Compression | lz4, zstd, gzip | zlib, lzo, zstd (per file possible) |
| Deduplication | Built in (inline, memory-hungry) | Offline only (e.g. `duperemove`) |
| Encryption | Native, per dataset | None native (use LUKS) |
| Reflink / fast copies | Block cloning (2.2+) | Long supported |
| Shrink | Limited | Yes |
| Mixed-size disks | Poor | Good |
| Parity RAID | Mature (RAID-Z) | Not recommended |
| Platforms | Linux, FreeBSD, illumos, others | Linux (mainly) |
| Kernel integration | Out-of-tree on Linux | Mainline |

Pick ZFS for NAS/servers where integrity is the priority, especially with parity RAID, mature replication, or native encryption.

### ZFS and mdraid

Give ZFS the raw disks and use its own mirrors/RAID-Z. Putting ZFS on top of `/dev/md0` works, but ZFS then sees one device: it can detect corruption but not repair it, you pay for redundancy twice, and tuning gets harder. See [Linux RAID](linux/07_raid.md).

## Installation

On Ubuntu/Debian:

```sh
sudo apt install zfsutils-linux
```

Check that the module is loaded:

```sh
sudo modprobe zfs
zfs version
```

## Useful Tips/Commands (UToC)

### Pools

```sh
# mirror pool
sudo zpool create tank mirror /dev/sdb /dev/sdc

# raidz1 pool (like RAID5)
sudo zpool create tank raidz1 /dev/sdb /dev/sdc /dev/sdd

zpool status
zpool list
```

> Warning: Creating a pool erases the disks. Prefer `/dev/disk/by-id/...` paths so the pool survives device renames.

### Datasets

```sh
sudo zfs create tank/data
sudo zfs set compression=lz4 tank/data
sudo zfs set quota=10G tank/data
zfs list
zfs get all tank/data
```

### Snapshots and Replication

```sh
sudo zfs snapshot tank/data@before-upgrade
zfs list -t snapshot
sudo zfs rollback tank/data@before-upgrade

# replicate to another pool/host
sudo zfs send tank/data@before-upgrade | ssh host sudo zfs receive backup/data
# incremental
sudo zfs send -i @snap1 tank/data@snap2 | ssh host sudo zfs receive backup/data
```

### Health and Maintenance

```sh
sudo zpool scrub tank      # verify all checksums and repair
zpool status -v tank
sudo zpool replace tank /dev/sdb /dev/sde
sudo zpool export tank
sudo zpool import tank
```

## Examples (e.g.,)

### Virtual Disks

Build a mirrored pool from file-backed vdevs to experiment safely.

```bash
truncate -s 1G /tmp/zfs0.img /tmp/zfs1.img

sudo zpool create testpool mirror /tmp/zfs0.img /tmp/zfs1.img
sudo zfs create testpool/demo
echo hello | sudo tee /testpool/demo/file.txt

# snapshot, change, roll back
sudo zfs snapshot testpool/demo@s1
echo changed | sudo tee /testpool/demo/file.txt
sudo zfs rollback testpool/demo@s1
cat /testpool/demo/file.txt

# simulate corruption on one side, then scrub
sudo zpool scrub testpool
zpool status testpool
```

Clean up:

```bash
sudo zpool destroy testpool
rm /tmp/zfs0.img /tmp/zfs1.img
```

## References

- [OpenZFS Documentation](https://openzfs.github.io/openzfs-docs/)
- [zpool(8) manual](https://openzfs.github.io/openzfs-docs/man/master/8/zpool.8.html)
- [zfs(8) manual](https://openzfs.github.io/openzfs-docs/man/master/8/zfs.8.html)
