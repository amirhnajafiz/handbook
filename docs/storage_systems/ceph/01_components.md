# Components

## Quick Description (QD)

Ceph offers several storage interfaces, which is another way of saying ways of storing data. These storage interfaces include:

- CephFS (a file system)
- RBD (block devices)
- RADOS (an object store)

Deep down, though, all three of these are really RADOS object stores. CephFS and RBD are just presenting themselves as file systems and block devices.

<div align="center">
    <img src="docs/storage_systems/ceph/images/architecture.svg" width="500" />
</div>

### Data Redundancy

Ceph is a clustered and distributed storage manager that offers data redundancy. Let's explain all of the terms in it:

- **Storage manager**: Ceph is a storage manager. This means that Ceph is software that helps storage resources store data. Storage resources come in several forms: hard disk drives (HDD), solid-state drives (SSD), magnetic tape, floppy disks, punched tape, Hollerith-style punch cards, and magnetic drum memory are all forms of storage resources.
- **Clustered storage manager**: Ceph is a clustered storage manager. That means that the storage manager is installed not just on a single machine but on several machines that work together as a system.
- **Distributed storage manager**: Ceph is a clustered and distributed storage manager. That means that the data that is stored and the infrastructure that supports it are spread across multiple machines and are not centralized in a single machine.
- **Data redundancy**: Having a second copy of your data somewhere.

### Ceph Monitor

The Ceph Monitor (`ceph-mon`) is one of the daemons essential to the functioning of a Ceph cluster. Monitors maintain the maps of the cluster state (the monitor map, the OSD map, the MDS map, the manager map, and the CRUSH map) and handle authentication between daemons and clients. Those maps make it possible for Ceph daemons to work together. Monitors do not keep a table of where every object lives: clients get the cluster maps from a monitor and calculate the location of data themselves using CRUSH (see [Architecture](03_architecture.md)).

Monitors must reach quorum, which means that a majority of them must be up and able to talk to each other, otherwise the cluster stops. That is why a production cluster runs at least three monitors (a single one is enough for a test cluster).

### Manager

The Ceph Manager (`ceph-mgr`) is another daemon essential to the functioning of the cluster. Managers keep track of runtime metrics and the current state of the cluster (storage utilization, performance metrics, system load), and they host modules such as the Ceph dashboard web GUI, the orchestrator, and the balancer. At least two managers are recommended for high availability.

### Object Storage Daemons

Object Storage Daemons (OSDs) store objects. An OSD is a process that runs on a storage server and manages a single unit of storage, usually a single disk. OSDs also handle replication, recovery, rebalancing, and heartbeats with their peers, and they report to the monitors.

### Data Pools

Objects are stored in logical partitions called pools. A pool is an abstraction that can be designated as either "replicated" or "erasure coded". In Ceph, the method of data protection (replication or erasure coding) is set at the pool level.

### Placement Groups

Ceph hashes each object name into a placement group (PG), and then CRUSH calculates which OSDs store that PG. Placement groups are a part of pools: a pool is divided into PGs, and the PGs are what get mapped onto OSDs.

### Metadata Server

A metadata server (MDS, `ceph-mds`) stores the metadata of CephFS, such as directory listings and file attributes. It is needed only for CephFS (not for RBD or RGW). Plan for at least one active MDS per file system plus a standby.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

_Nothing here yet._

## References

- [Ceph Documentation: The Parts of a Ceph Cluster](https://docs.ceph.com/en/latest/start/ceph-cluster-components/)
- [Ceph Documentation: Architecture](https://docs.ceph.com/en/latest/architecture/)
- [Ceph Documentation: Pools](https://docs.ceph.com/en/latest/rados/operations/pools/)
- [Ceph Documentation: Placement Groups](https://docs.ceph.com/en/latest/rados/operations/placement-groups/)
