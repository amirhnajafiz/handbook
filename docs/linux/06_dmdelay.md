# DM Delay

## Quick Description (QD)

The device mapper `delay` target creates a block device that delays reads and writes. It is useful for simulating slow disks.

The table line passed to `dmsetup` has the form `<start> <length> delay <device> <offset> <delay_ms>`, optionally followed by `<write_device> <write_offset> <write_delay_ms>` to give writes their own device and delay. Start and length are in 512-byte sectors, and delays are in milliseconds.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

Here are some other useful commands:

```sh
# list the device mapper devices
ls /dev/mapper/
# remove a device
sudo dmsetup remove delayed_loop
# show the table of all devices
sudo dmsetup table
# get information of a device
sudo dmsetup info delayed_loop
# suspend a device
sudo dmsetup suspend delayed_loop
# resume a device
sudo dmsetup resume delayed_loop
# change an existing device (keep the same length), here to 2s on both reads and writes
echo "0 $(sudo blockdev --getsz /dev/sdX) delay /dev/sdX 0 2000" | sudo dmsetup reload delayed_loop
sudo dmsetup resume delayed_loop
# drop the OS page cache if the delay is not noticeable (reads served from cache are not delayed)
sync; echo 3 | sudo tee /proc/sys/vm/drop_caches
```

`reload` loads a new table into the inactive slot, and `resume` swaps it in.

## Examples (e.g.,)

Assume that your device is `/dev/sdX`.

First, get the size in sectors.

```sh
$ sudo blockdev --getsz /dev/sdX
# 4096
```

Create a delayed device (1s on both read and write), using that size as the length.

```sh
# <start> <length> delay <dev> <offset> <read_delay_ms> <write_dev> <write_offset> <write_delay_ms>
echo "0 4096 delay /dev/sdX 0 1000 /dev/sdX 0 1000" | sudo dmsetup create delayed_loop
```

Get your mapped device from `/dev/mapper/delayed_loop`.

```sh
sudo mkdir -p /mnt/delayed_loop
sudo mount /dev/mapper/delayed_loop /mnt/delayed_loop
```

Unmount it before removing the device with `dmsetup remove`.

## References

- [dm-delay (kernel documentation)](https://docs.kernel.org/admin-guide/device-mapper/delay.html)
- [dmsetup(8)](https://man7.org/linux/man-pages/man8/dmsetup.8.html)
- [blockdev(8)](https://man7.org/linux/man-pages/man8/blockdev.8.html)
- [/proc/sys/vm (proc_sys_vm(5))](https://man7.org/linux/man-pages/man5/proc_sys_vm.5.html)
