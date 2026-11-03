# Hardware and OS

## Quick Description (QD)

Minimum hardware per daemon (small test clusters; production needs more, and you should benchmark):

- **CPU:** Choose for IOPS per core. OSDs need at least 1 thread (3 recommended) per HDD OSD and 4 (6 recommended) per NVMe OSD. MONs and MDSs need at least 2 cores, and for an MDS clock speed matters more than core count.
- **Memory:** At least 4 GiB per OSD (the default `osd_memory_target`), at least 5 GB per MON, and at least 8 GiB per MDS.
- **Storage:** One drive per OSD, and a separate drive for the OS. HDD OSDs benefit from putting their BlueStore WAL+DB on a shared SSD; SSD OSDs keep WAL+DB on the device. Put MON databases, CephFS metadata, and RGW index pools on enterprise SSDs.
- **Network:** 1 Gb/s minimum, but 10 Gb/s or more is recommended (25 Gb/s or more for substantial workloads). Faster links also shorten recovery time.

### Supported Operating Systems

Ceph is primarily developed for Linux. Which distributions are tested depends on the Ceph release, so check the OS recommendations page for the release you deploy (at the time of writing, recent releases are tested on CentOS Stream 9, Rocky Linux, and Ubuntu 22.04/24.04 LTS). The monitors, OSDs, and gateways run in containers when you use [cephadm](06_cephadm.md), so the host mostly needs a supported container runtime.

- **Kernel:** Only kernel clients (RBD and CephFS) depend on the host kernel version. For RBD, 5.3 or newer (or Enterprise Linux 8.2) is recommended, and 4.19 is the oldest that is practical. Use a stable or long-term maintenance kernel series.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

- Use enterprise-class drives with power loss protection for production clusters.
- Ensure all nodes have synchronized clocks (for example, via chrony or NTP). Monitors raise a clock skew warning when clocks drift apart.
- Bond links across two switches, and keep BMC (out-of-band) traffic on a separate network. A separate cluster (replication) network is optional and can be configured as described in the network configuration reference.
- Regularly update the OS and Ceph packages for security and stability.

## Examples (e.g.,)

_Nothing here yet._

## References

- [Ceph Documentation: Hardware Recommendations](https://docs.ceph.com/en/latest/start/hardware-recommendations/)
- [Ceph Documentation: Minimum Hardware per Daemon](https://docs.ceph.com/en/latest/start/minimum-hardware/)
- [Ceph Documentation: Network Sizing](https://docs.ceph.com/en/latest/start/hardware-networks/)
- [Ceph Documentation: OS Recommendations](https://docs.ceph.com/en/latest/start/os-recommendations/)
