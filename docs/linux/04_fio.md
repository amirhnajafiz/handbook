# fio

## Quick Description (QD)

fio (Flexible I/O Tester) is a powerful, open-source tool used for benchmarking and stress testing disk I/O performance on Linux and other UNIX-like operating systems, as well as Windows. It allows users to simulate various I/O workloads and measure key performance metrics like throughput, IOPS (I/O operations per second), and latency.

## Installation

Before installing, ensure your system's package lists are up to date.

```bash
sudo apt update
```

Execute the following command to install fio.

```bash
sudo apt install -y fio
```

After the installation completes, you can verify it by checking the fio version.

```bash
fio --version
```

## Useful Tips/Commands (UToC)

- Run fio against a file on the filesystem you want to test, not against a raw device. Tests that write to a raw device (`--filename=/dev/sdX`) destroy the data on it.
- `--direct=1` bypasses the page cache, so you measure the disk and not RAM.
- Use `--output-format=json` to get machine-readable results.

## Examples (e.g.,)

### Random Read/Write Test

```bash
fio --name=randrw --filename=/mnt/test/fio.dat --size=1G \
    --rw=randrw --rwmixread=70 --bs=4k \
    --ioengine=libaio --iodepth=16 --direct=1 \
    --runtime=60 --time_based --group_reporting
```

- `--name`: the job name (it also starts a new job on the command line).
- `--filename`: the file (or device) the job reads and writes.
- `--size`: how much data the job covers.
- `--rw=randrw`: random mixed reads and writes; `--rwmixread=70` makes 70% of them reads.
- `--bs=4k`: the block size of each I/O.
- `--ioengine=libaio`: asynchronous I/O on Linux, and `--iodepth=16` keeps up to 16 I/Os in flight.
- `--direct=1`: non-buffered I/O (`O_DIRECT`).
- `--runtime=60 --time_based`: run for 60 seconds, looping over the file if needed.
- `--group_reporting`: report one aggregate result instead of one per job.

In the output, look at `IOPS`, `BW` (bandwidth), and the completion latency (`clat`) percentiles.

## References

- [fio on GitHub](https://github.com/axboe/fio)
- [fio documentation](https://fio.readthedocs.io/en/latest/fio_doc.html)
