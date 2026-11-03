# Architecture

## Quick Description (QD)

Ceph uniquely delivers object, block, and file storage in one unified system. Ceph is highly reliable, easy to manage, and free. Ceph delivers extraordinary scalability: thousands of clients accessing petabytes to exabytes of data.

A Ceph Node leverages commodity hardware and intelligent daemons, and a Ceph Storage Cluster accommodates large numbers of nodes, which communicate with each other to replicate and redistribute data dynamically.

<div align="center">
    <img src="docs/storage_systems/ceph/images/stack.webp" width="400" />
</div>

### Storing Data

The Ceph Storage Cluster receives data from Ceph Clients, whether it comes through a Ceph Block Device, Ceph Object Storage, the Ceph File System, or a custom implementation that you create by using `librados`.

The data received by the Ceph Storage Cluster is stored as RADOS objects. Each object is stored on an Object Storage Daemon (also called an "OSD").

Ceph OSDs control read, write, and replication operations on storage drives. The default BlueStore back end stores objects directly on the raw block device, and uses an embedded RocksDB database for metadata.

<div align="center">
    <img src="docs/storage_systems/ceph/images/osd.webp" width="400" />
</div>

Ceph OSD Daemons store data as objects in a flat namespace. This means that objects are not stored in a hierarchy of directories. An object has an identifier, binary data, and metadata consisting of name/value pairs.

### Finding Data

There is no central lookup table. A client gets the cluster maps from a monitor, hashes the object name to a placement group, and uses the CRUSH algorithm to calculate which OSDs store that PG, so it talks to the OSDs directly. Pools and PGs are described in [Components](01_components.md).

### Object Semantics

Ceph Clients determine the semantics of the object data. For example, CephFS uses metadata to store file attributes such as the file owner, the created date, and the last modified date.

<div align="center">
    <img src="docs/storage_systems/ceph/images/meta.webp" width="400" />
</div>

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

_Nothing here yet._

## References

- [Ceph Documentation: Architecture](https://docs.ceph.com/en/latest/architecture/)
- [Ceph Documentation: CRUSH Maps](https://docs.ceph.com/en/latest/rados/operations/crush-map/)
- [CRUSH: Controlled, Scalable, Decentralized Placement of Replicated Data (Weil et al.)](https://ceph.com/assets/pdfs/weil-crush-sc06.pdf)
