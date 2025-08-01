# Ceph

Ceph is a clustered and distributed storage manager. If that’s too cryptic, then just think of Ceph as a computer program that stores data and uses a network to make sure that there is a backup copy of the data.

## Components

Ceph offers several “storage interfaces”, which is another way of saying “ways of storing data”. These storage interfaces include: - CephFS (a file system) - RBD (block devices) - RADOS (an object store). Deep down, though, all three of these are really RADOS object stores. CephFS and RBD are just presenting themselves as file systems and block devices.

Ceph is a clustered and distributed storage manager that offers data redundancy. Let’s explain all of the terms in it:

* **Storage Manager**: Ceph is a storage manager. This means that Ceph is software that helps storage resources store data. Storage resources come in several forms: hard disk drives (HDD), solid-state drives (SSD), magnetic tape, floppy disks, punched tape, Hollerith-style punch cards, and magnetic drum memory are all forms of storage resources.

* **Clustered storage manager**: Ceph is a clustered storage manager. That means that the storage manager installed not just on a single machine but on several machines that work together as a system.

* **Distributed storage manager**: Ceph is a clustered and distributed storage manager. That means that the data that is stored and the infrastructure that supports it is spread across multiple machines and is not centralized in a single machine.

* **Data Redundancy**: Having a second copy of your data somewhere.

### Ceph Monitor

The Ceph Monitor is one of the daemons essential to the functioning of a Ceph cluster. Monitors know the location of all the data in the Ceph cluster. Monitors maintain maps of the cluster state, and those maps make it possible for Ceph daemons to work together. These maps include the monitor map, the OSD map, the MDS map, and the CRUSH map. Three monitors are required to reach quorum. Quorum is a state that is necessary for a Ceph cluster to work properly. Quorum means that a majority of the monitors are in the “up” state.

### Manager

The manager balances the data in the Ceph cluster, distributing load evenly so that no part of the cluster gets overloaded. The manager is one of the daemons essential to the functioning of the Ceph cluster. Managers keep track of runtime metrics, system utilization, CPU performance, disk load, and they host the Ceph dashboard web GUI.

### Object Storage Daemons

Object Storage Daemons (OSDs) store objects. An OSD is a process that runs on a storage server. The OSD is responsible for managing a single unit of storage, which is usually a single disk.

### Pools

A pool is an abstraction that can be designated as either “replicated” or “erasure coded”. In Ceph, the method of data protection is set at the pool level. Ceph offers and supports two types of data protection: replication and erasure coding. Objects are stored in pools. A storage pool is a collection of storage volumes. A storage volume is the basic unit of storage, such as allocated space on a disk or a single tape cartridge. The server uses the storage volumes to store backed-up, archived, or space-managed files.

#### Placement Groups

Placement groups are a part of pools.

### Metadata Server

A metadata server (MDS) is necessary for the proper functioning of CephFS.

> A Ceph Object Store consists of a Ceph Storage Cluster and a Ceph Object Gateway (RGW).
