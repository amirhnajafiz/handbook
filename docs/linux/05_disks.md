# Disks

## Quick Description (QD)

This page covers inspecting disks, creating filesystems, and tracking down disk space usage on Linux.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### Listing Disks

To see only physical disks (no partitions), run:

```sh
lsblk -d
```

If you want to see more details, run:

```sh
sudo lshw -class disk
```

### Preparing a Disk

Before using a disk, create a new filesystem.

```sh
sudo mkfs.ext4 /dev/sdXN
```

Replace `sdXN` with your partition (e.g., `sdb1`). This erases the data on it, so double check the name with `lsblk` first. Then mount it.

```sh
sudo mkdir -p /mnt/device
sudo mount /dev/sdXN /mnt/device
```

### Capacity Check

A quick command to check free space on disks is:

```sh
df -h
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda2       200G  198G  2G   100% /
```

By running `du` we can dig deeper into space usage:

```sh
sudo du -xhd1 / | sort -hr | head -20
# 45G /var
# 32G /home
# 12G /usr
```

- `du` stands for disk usage.
- The `-x` flag tells it to stay on the same filesystem only.
- The `-h` flag tells it to print human-readable sizes.
- The `-d1` flag (`--max-depth=1`) tells it to go one level deep.
- `sort -hr` sorts human-readable sizes, biggest first.

> An alternative is `ncdu`, an interactive disk usage browser.

### Hidden Files

Often the `du` output doesn't match the `df` output. In that case, space may be held by files that `du` cannot see:

- Files that were deleted but are still open by a running process. The space is freed only when the process closes them or exits. List them with `lsof` (list open files):

```sh
sudo lsof +L1
```

- Files hidden under a mount point: if you wrote data into `/mnt/x` before mounting something on it, that data is still on the root disk but invisible. See the bind mount trick below.
- Docker data. If you have Docker on a machine, `docker system df` shows how much space images, containers and volumes take.
- Loop devices backed by big files. You can see them using:

```sh
sudo losetup -a
```

### Ultimate Solution

Both `du` and `ncdu` take too much time (overhead and permission issues). When you start scanning from root, you have too many virtual filesystems like `/proc` or `/sys`. You might also have separate partitions, like having `/home` on NFS. The partitions are actually causing this overhead and these permission issues.

A good solution is to use a bind mount to mount your root filesystem onto a new mount point. A plain bind mount (`-o bind`, not recursive) does not carry the other filesystems mounted below `/`, so `/proc`, `/sys` and separate partitions are left out. This results in having only the actual files of your root disk mirrored in the new mount point, including any files hidden under other mount points.

```sh
sudo mkdir /mnt/os
sudo mount -o bind / /mnt/os
sudo du -sh /mnt/os/* | sort -h
```

This returns a response in a few seconds. When you are done, run `sudo umount /mnt/os`.

## Examples (e.g.,)

_Nothing here yet._

## References

- [lsblk(8)](https://man7.org/linux/man-pages/man8/lsblk.8.html)
- [mke2fs(8)](https://man7.org/linux/man-pages/man8/mke2fs.8.html)
- [df(1)](https://man7.org/linux/man-pages/man1/df.1.html)
- [du(1)](https://man7.org/linux/man-pages/man1/du.1.html)
- [lsof(8)](https://man7.org/linux/man-pages/man8/lsof.8.html)
- [losetup(8)](https://man7.org/linux/man-pages/man8/losetup.8.html)
- [mount(8)](https://man7.org/linux/man-pages/man8/mount.8.html) (see "Bind mounts")
- [docker system df](https://docs.docker.com/reference/cli/docker/system/df/)
