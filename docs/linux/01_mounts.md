# Mounts

## Quick Description (QD)

Mounting is the process of making a filesystem accessible at a certain point in the Linux directory tree. When you mount a device, such as a hard drive, USB stick, or network share, its filesystem becomes available for use under a specified directory, known as the mount point.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### Common Mount Commands

- `mount`: attaches filesystems to the directory tree.
- `umount`: detaches filesystems (it fails with "target is busy" while a process is using the mount point; `lsof /mnt/usb` shows which).
- `findmnt`: shows mounted filesystems as a tree.

### Persistent Mounts

To make mounts persistent across reboots, add an entry to the `/etc/fstab` file:

```txt
/dev/sdb1   /mnt/usb   ext4   defaults   0   2
```

The fields are: device, mount point, filesystem type, mount options, dump flag (`0` means no backup by `dump`), and fsck pass number (`0` skip, `1` for the root filesystem, `2` for others). This makes the device mount automatically at boot. Device names like `/dev/sdb1` can change between boots, so prefer `UUID=<uuid>` (find it with `blkid`). You can test an entry without rebooting using `sudo mount -a`.

### Viewing Mounted Filesystems

Use `df`, `mount` or `findmnt` to see currently mounted filesystems:

```bash
df -h
mount
findmnt
```

## Examples (e.g.,)

### Mounting a USB Drive

```bash
sudo mount /dev/sdb1 /mnt/usb
```

This command mounts the device `/dev/sdb1` to the directory `/mnt/usb`.

### Unmounting

```bash
sudo umount /mnt/usb
```

This command unmounts the filesystem from `/mnt/usb`.

## References

- [mount(8)](https://man7.org/linux/man-pages/man8/mount.8.html)
- [umount(8)](https://man7.org/linux/man-pages/man8/umount.8.html)
- [fstab(5)](https://man7.org/linux/man-pages/man5/fstab.5.html)
- [findmnt(8)](https://man7.org/linux/man-pages/man8/findmnt.8.html)
