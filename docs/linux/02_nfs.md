# NFS

## Quick Description (QD)

NFS (Network File System) allows you to share directories and files with others over a network. It enables users to mount remote directories on their local machines and interact with them as if they were local files.

## Installation

On most Linux distributions, you can install NFS utilities with:

```bash
# client
sudo apt install nfs-common        # Debian/Ubuntu
sudo yum install nfs-utils         # CentOS/RHEL
# server
sudo apt install nfs-kernel-server # Debian/Ubuntu (nfs-utils on CentOS/RHEL)
```

## Useful Tips/Commands (UToC)

### Mounting an NFS Share

To mount an NFS share, use the `mount` command:

```bash
sudo mount server:/remote/path /mnt/nfs
```

- `server` is the hostname or IP address of the NFS server.
- `/remote/path` is the exported directory on the server.
- `/mnt/nfs` is the local mount point.

### Unmounting an NFS Share

```bash
sudo umount /mnt/nfs
```

### Persistent NFS Mounts

To mount an NFS share automatically at boot, add an entry to `/etc/fstab`:

```txt
server:/remote/path   /mnt/nfs   nfs   defaults   0   0
```

See [Mounts](01_mounts.md) for the fields of this file.

### Viewing NFS Mounts

To see active NFS mounts:

```bash
mount -t nfs
```

Or use `df` to see usage:

```bash
df -hT | grep nfs
```

### Exporting Directories (Server Side)

On the NFS server, edit `/etc/exports` to specify which directories to share:

```txt
/srv/nfs    192.168.1.0/24(rw,sync,no_subtree_check)
```

The options mean: `rw` allows read and write, `sync` replies to requests only after changes are committed to stable storage, and `no_subtree_check` disables subtree checking. Then re-export the shares (`-r` re-exports all directories, `-a` exports or unexports all), and make sure the server is running:

```bash
sudo exportfs -ra
sudo systemctl enable --now nfs-server   # the unit is nfs-kernel-server on Debian/Ubuntu
```

Use `sudo exportfs -v` to list what is currently exported.

## Examples (e.g.,)

_Nothing here yet._

## References

- [nfs(5)](https://man7.org/linux/man-pages/man5/nfs.5.html)
- [exports(5)](https://man7.org/linux/man-pages/man5/exports.5.html)
- [exportfs(8)](https://man7.org/linux/man-pages/man8/exportfs.8.html)
- [mount(8)](https://man7.org/linux/man-pages/man8/mount.8.html)
