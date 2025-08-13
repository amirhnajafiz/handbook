# Architecture

Ceph uniquely delivers object, block, and file storage in one unified system. Ceph is highly reliable, easy to manage, and free. Ceph delivers extraordinary scalability–thousands of clients accessing petabytes to exabytes of data. A Ceph Node leverages commodity hardware and intelligent daemons, and a Ceph Storage Cluster accommodates large numbers of nodes, which communicate with each other to replicate and redistribute data dynamically.

![stack](cephfs/images/stack.webp)

## Storing data

The Ceph Storage Cluster receives data from Ceph Clients--whether it comes through a Ceph Block Device, Ceph Object Storage, the Ceph File System, or a custom implementation that you create by using librados. The data received by the Ceph Storage Cluster is stored as RADOS objects. Each object is stored on an Object Storage Device (this is also called an “OSD”). Ceph OSDs control read, write, and replication operations on storage drives. The default BlueStore back end stores objects in a monolithic, database-like fashion.

![osd](cephfs/images/osd.webp)

Ceph OSD Daemons store data as objects in a flat namespace. This means that objects are not stored in a hierarchy of directories. An object has an identifier, binary data, and metadata consisting of name/value pairs. Ceph Clients determine the semantics of the object data. For example, CephFS uses metadata to store file attributes such as the file owner, the created date, and the last modified date.

![metadata](cephfs/images/meta.webp)
