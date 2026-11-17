# Linux RAID

## Quick Description (QD)

**mdraid** (Linux "multiple devices" RAID, the kernel `md` driver, managed with `mdadm`) combines several disks or partitions into one virtual block device such as `/dev/md0`. That device looks like a single disk and does not know what is stored on it. It works at the **block level, below the file system**, so you create any file system (ext4, XFS, Btrfs, ...) on top.

```text
File system (ext4, XFS...)
        ↓
/dev/md0  (mdraid virtual block device)
        ↓
/dev/sda, /dev/sdb, /dev/sdc  (physical disks)
```

Its main purpose is RAID (redundancy and/or performance), not just pooling capacity. For pooling without RAID semantics, LVM is the more typical tool.

### mdraid vs. "Linux RAID"

"Linux RAID" or "Linux software RAID" almost always means mdraid. Loosely, it can cover any RAID on Linux:

- **Btrfs RAID**: built into the file system (RAID 0/1/10 solid, 5/6 problematic).
- **ZFS mirrors / RAID-Z**: ZFS's own redundancy, separate from `md`.
- **LVM RAID**: uses the `md` kernel code through device-mapper.
- **Hardware RAID**: a controller presents a ready-made array, no `md` involved.
- **Firmware ("BIOS") RAID**: e.g. Intel RST, often handled by mdraid with Intel's metadata format.

### Common RAID Levels

| Level | Min disks | Redundancy | Notes |
| ----- | --------- | ---------- | ----- |
| RAID 0 | 2 | none | Striping; fastest, any disk failure loses everything |
| RAID 1 | 2 | n-1 disks | Mirroring |
| RAID 5 | 3 | 1 disk | Striping with distributed parity |
| RAID 6 | 4 | 2 disks | Double parity |
| RAID 10 | 4 | 1+ per mirror | Striped mirrors |
| linear | 1+ | none | Concatenates disks end to end; rarely used |

> RAID is not a backup. It protects against disk failure, not deletion, ransomware, or a failed controller.

### Limitations

- No data checksums: if a disk silently returns corrupted data, mdraid usually cannot tell which copy is correct.
- No snapshots or compression of its own (use LVM or the file system on top).
- Plain RAID 5 can suffer from the "write hole" after a crash.

### Difference from ZFS and Btrfs

| | mdraid | ZFS | Btrfs |
| --- | --- | --- | --- |
| Layer | Block device only | File system + volume manager | File system + volume manager |
| Detects corrupted data | No | Yes (checksums) | Yes (checksums) |
| Self-heals | No | Yes | Yes (with redundancy) |
| Snapshots | No (LVM or file system) | Yes | Yes |
| Compression | No | Yes | Yes |
| In mainline kernel | Yes | No | Yes |
| Parity RAID (5/6) | Yes, mature | Yes (RAID-Z), mature | Not recommended |

Use **mdraid + ext4/XFS** when you want simple, mature, low-overhead redundancy without advanced features.

## Installation

On Ubuntu/Debian:

```sh
sudo apt install mdadm
```

## Useful Tips/Commands (UToC)

### Creating an Array

```sh
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc
sudo mkfs.ext4 /dev/md0
sudo mount /dev/md0 /mnt/raid
```

> Warning: Creating an array overwrites the member devices.

### Status

```sh
cat /proc/mdstat
sudo mdadm --detail /dev/md0
sudo mdadm --examine /dev/sdb
```

### Persisting the Configuration

```sh
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf
sudo update-initramfs -u
```

Then mount by UUID in `/etc/fstab` (get it from `blkid`).

### Handling a Failed Disk

```sh
sudo mdadm /dev/md0 --fail /dev/sdb
sudo mdadm /dev/md0 --remove /dev/sdb
sudo mdadm /dev/md0 --add /dev/sdd     # rebuild starts automatically
watch cat /proc/mdstat
```

### Combining with ZFS or Btrfs

ZFS and Btrfs take raw devices and manage the blocks themselves; they do not use mdraid underneath. You *can* hand them `/dev/md0`, but it is generally a bad idea (the ZFS docs recommend against it):

- They can only self-heal if they see the redundant copies. On top of md they see one device, so they detect corruption but cannot repair it, and md cannot tell which copy is right.
- You pay for redundancy twice and lose the main benefit of the file system.

Acceptable case: single-device Btrfs/ZFS on a mature mdraid RAID 5/6 array (Btrfs's own RAID 5/6 is not recommended). You get snapshots and corruption detection, but no self-healing. Otherwise give ZFS/Btrfs the raw disks and use their own mirrors/RAID-Z/RAID1/10.

### Growing and Stopping

```sh
sudo mdadm --grow /dev/md0 --raid-devices=3 --add /dev/sde
sudo mdadm --stop /dev/md0
sudo mdadm --assemble /dev/md0 /dev/sdb /dev/sdc
sudo mdadm --zero-superblock /dev/sdb    # wipe RAID metadata from a disk
```

## Examples (e.g.,)

### Virtual Disks

Build a RAID 1 array from loop devices and simulate a failure.

```bash
truncate -s 1G d0.img d1.img d2.img
L0=$(sudo losetup --find --show d0.img)
L1=$(sudo losetup --find --show d1.img)
L2=$(sudo losetup --find --show d2.img)

sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 $L0 $L1
sudo mkfs.ext4 /dev/md0
sudo mount /dev/md0 /mnt

# fail one member, replace it, watch the rebuild
sudo mdadm /dev/md0 --fail $L0
sudo mdadm /dev/md0 --remove $L0
sudo mdadm /dev/md0 --add $L2
cat /proc/mdstat
```

Clean up:

```bash
sudo umount /mnt
sudo mdadm --stop /dev/md0
sudo losetup -d $L0 $L1 $L2
rm d0.img d1.img d2.img
```

## References

- [Linux RAID Wiki](https://raid.wiki.kernel.org/)
- [mdadm(8) manual](https://man7.org/linux/man-pages/man8/mdadm.8.html)
- [md (Linux kernel docs)](https://docs.kernel.org/admin-guide/md.html)
