# RADOS

## Quick Description (QD)

**RADOS** (Reliable Autonomic Distributed Object Store) is the object store at the core of Ceph. CephFS, RBD, and the Object Gateway are all built on top of it (see [Components](01_components.md)). Applications can talk to it directly through [librados](04_librados.md), and the `rados` command-line utility is used to interact with a RADOS cluster.

### Gateway

The Ceph Object Gateway is an object storage interface built on top of `librados`. It provides a RESTful gateway between applications and Ceph storage clusters.

Ceph Object Storage supports two interfaces:

- **S3-compatible**: Provides object storage functionality with an interface that is compatible with a large subset of the Amazon S3 RESTful API.
- **Swift-compatible**: Provides object storage functionality with an interface that is compatible with a large subset of the OpenStack Swift API.

Ceph Object Storage uses the Ceph Object Gateway daemon (`radosgw`), an HTTP server designed to interact with a Ceph Storage Cluster. The gateway has its own user management, and it can use the same Ceph Storage Cluster that stores data from Ceph File System and Ceph Block Device clients.

The S3 API and the Swift API share a common namespace, which means that it is possible to write data to a Ceph Storage Cluster with one API and then retrieve that data with the other API.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

_Nothing here yet._

## References

- [RADOS: A Scalable, Reliable Storage Service for Petabyte-scale Storage Clusters (Weil et al.)](https://ceph.com/assets/pdfs/weil-rados-pdsw07.pdf)
- [Ceph Documentation: RADOS](https://docs.ceph.com/en/latest/rados/)
- [Ceph Documentation: rados man page](https://docs.ceph.com/en/latest/man/8/rados/)
- [Ceph Documentation: Object Gateway](https://docs.ceph.com/en/latest/radosgw/)
