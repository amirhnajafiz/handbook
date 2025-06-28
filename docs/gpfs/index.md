# GPFS

General Parallel File System (GPFS), now known as IBM Spectrum Scale, is a high-performance clustered file system developed by IBM. It is designed to provide fast, reliable, and scalable access to data across multiple servers. GPFS is commonly used in environments that require large-scale data management, such as high-performance computing (HPC), big data analytics, and enterprise storage solutions. Its features include data replication, high availability, and support for both POSIX and non-POSIX workloads.

## Components

GPFS consists of several key components:

- **Cluster Nodes**: Servers that participate in the GPFS cluster, each running GPFS software.
- **NSD (Network Shared Disk) Servers**: Nodes that provide access to storage devices over the network.
- **Disks**: Physical or logical storage devices managed by GPFS.
- **File System Manager**: Coordinates file system operations and metadata management.
- **Quorum Nodes**: Nodes responsible for maintaining cluster consistency and availability.
- **GPFS Daemons**: Background processes that handle file system operations, health monitoring, and communication between nodes.

These components work together to deliver high availability, scalability, and performance for clustered storage environments.

## Commands

### System Health

Check health of cluster:

```sh
mmhealth cluster show
```

Node health:

```sh
mmhealth node show <service>
```

Node logs and events:

```sh
mmhealth node eventlog
```

### Cluster

Create a cluster:

```sh
mmcrcluster
```

View configuration:

```sh
mmlscluster
```

Add NodesList:

```sh
/mmcrcluster -N NodesList --ccr-enable -r /usr/bin/ssh -R /usr/bin/scp -C cluster1.spectrum
```

An example of NodesList file:

```
node1:quorum
node2
node3
node4:quorum-manager
node5:quorum-manager
```

Start the GPFS daemons and the cluster by using the following command from one of the nodes:

```sh
mmstartup -N NodesList
```

You can use the `mmgetstate -N NodesList` command to verify that the GPFS software is running on these nodes.

### Export services

Export a GPFS file system using NFS:

```sh
mmnfs export add <filesystem> -p <path> -c <client>
```

List current NFS exports:

```sh
mmnfs export list
```

Remove an NFS export:

```sh
mmnfs export delete <filesystem> -p <path>
```

To enable NFS service on a node:

```sh
mmnfs enable
```

Check NFS service status:

```sh
mmnfs service list
```
