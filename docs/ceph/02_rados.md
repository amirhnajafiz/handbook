# Rados

**Rados** is a utility for interacting with a Ceph object storage cluster (RADOS), part of the Ceph distributed storage system.

## Gateway

An object storage interface built on top of `librados`. Ceph Object Gateway provides a RESTful gateway between applications and Ceph storage clusters.

Ceph Object Storage supports two interfaces:

- **S3-compatible**: Provides object storage functionality with an interface that is compatible with a large subset of the Amazon S3 RESTful API.
- **Swift-compatible**: Provides object storage functionality with an interface that is compatible with a large subset of the OpenStack Swift API.

Ceph Object Storage uses the Ceph Object Gateway daemon (radosgw), an HTTP server designed to interact with a Ceph Storage Cluster.

The Ceph Object Gateway provides interfaces that are compatible with both Amazon S3 and OpenStack Swift, and it has its own user management. Ceph Object Gateway can use a single Ceph Storage cluster to store data from Ceph File System and from Ceph Block device clients.

The S3 API and the Swift API share a common namespace, which means that it is possible to write data to a Ceph Storage Cluster with one API and then retrieve that data with the other API.
