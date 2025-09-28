# Ceph File-system

CephFS is a POSIX-compliant file system built on top of Ceph’s distributed object store (RADOS). It is designed for high performance, scalability, and availability, supporting use cases like shared directories, HPC scratch space, and distributed workflows.

Key features include:

* **Separation of data and metadata:** File metadata is stored in a dedicated RADOS pool and managed by a scalable cluster of Metadata Servers (MDS), while clients access file data directly from RADOS.
* **Scalable architecture:** Clients bypass intermediaries and interact directly with RADOS, allowing performance to scale with the underlying object store.
* **Efficient metadata handling:** Metadata updates are journaled in RADOS by MDSes without relying on local storage, enabling fast, coordinated access and modifications across clients.

![cephfs-architecture](images/cephfs-architecture.svg)
