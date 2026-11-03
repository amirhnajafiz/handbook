# Overview and Administration

## Quick Description (QD)

General Parallel File System (GPFS), now known as IBM Spectrum Scale, is a high-performance clustered file system developed by IBM. It is designed to provide fast, reliable, and scalable access to data across multiple servers.

GPFS is commonly used in environments that require large-scale data management, such as high-performance computing (HPC), big data analytics, and enterprise storage solutions. Its features include data replication, high availability, and support for both POSIX and non-POSIX workloads.

### Key Components

GPFS consists of several key components:

- **Cluster nodes:** Servers that participate in the GPFS cluster, each running GPFS software.
- **NSD (Network Shared Disk) servers:** Nodes that provide access to storage devices over the network.
- **Disks:** Physical or logical storage devices managed by GPFS.
- **File system manager:** Coordinates file system operations and metadata management.
- **Quorum nodes:** Nodes responsible for maintaining cluster consistency and availability.
- **GPFS daemons:** Background processes that handle file system operations, health monitoring, and communication between nodes.

These components work together to deliver high availability, scalability, and performance for clustered storage environments.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### System Health

Check the health of the cluster:

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

Create a cluster from the nodes listed in a NodesList file (`-r` and `-R` set the remote shell and copy commands, and `-C` the cluster name; CCR is the default configuration repository):

```sh
mmcrcluster -N NodesList -r /usr/bin/ssh -R /usr/bin/scp -C cluster1.spectrum
```

View the configuration:

```sh
mmlscluster
```

An example of a NodesList file (each line is `NodeName:designations`, where designations are dash-separated, e.g., `quorum-manager`):

```text
node1:quorum
node2
node3
node4:quorum-manager
node5:quorum-manager
```

Start the GPFS daemons on all nodes by using the following command from one of the nodes (use `-N NodesList` to start only the nodes in a file):

```sh
mmstartup -a
```

You can use the `mmgetstate -N NodesList` command to verify that the GPFS software is running on these nodes.

### Filesets

List the attributes of all file systems:

```sh
mmlsfs all
```

List the filesets of a specific device (`-L` adds IDs, inode space and creation time):

```sh
mmlsfileset [device] -L
```

Create a fileset:

```sh
mmcrfileset [device] [name] --inode-space new
```

Link the fileset to a path:

```sh
mmlinkfileset [device] [name] -J [path]
```

### Quota

Set a fileset quota (limits are `soft:hard`; blocks accept K, M, G or T):

```sh
mmsetquota device:name --block 16G:32G --files 10K:11K
```

Check the quota:

```sh
mmlsquota -j [name] [device]
```

### Export Services

Export a GPFS file system using NFS:

```sh
mmnfs export add <path> --client "<client>(Access_Type=RW)"
```

List current NFS exports:

```sh
mmnfs export list
```

Remove an NFS export (this does not delete the data):

```sh
mmnfs export remove <path>
```

Enable the NFS service on the protocol (CES) nodes:

```sh
mmces service enable NFS
```

Check the state of the CES services:

```sh
mmces service list
```

Mount the exported path on a client:

```sh
mount -t nfs <server-ip>:/path /local-path/
```

## Examples (e.g.,)

_Nothing here yet._

## References

- [mmcrcluster command (IBM Storage Scale)](https://www.ibm.com/docs/en/storage-scale/6.0.1?topic=reference-mmcrcluster-command)
- [mmlsfileset command](https://www.ibm.com/docs/en/storage-scale/6.0.1?topic=reference-mmlsfileset-command)
- [mmsetquota command](https://www.ibm.com/docs/en/storage-scale/6.0.1?topic=reference-mmsetquota-command)
- [mmlsquota command](https://www.ibm.com/docs/en/storage-scale/6.0.1?topic=reference-mmlsquota-command)
- [mmnfs command](https://www.ibm.com/docs/en/storage-scale/6.0.1?topic=reference-mmnfs-command)
- [mmhealth command](https://www.ibm.com/docs/en/storage-scale/6.0.1?topic=reference-mmhealth-command)
- [mmstartup command](https://www.ibm.com/docs/en/storage-scale/6.0.1?topic=reference-mmstartup-command)
