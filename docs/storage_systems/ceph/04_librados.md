# Librados

## Quick Description (QD)

Librados is a library that provides direct access to the RADOS (Reliable Autonomic Distributed Object Store) layer of Ceph (see [RADOS](02_rados.md)). It allows applications to interact with Ceph storage clusters without going through the CephFS, RBD, or Object Gateway layers.

### Key Features

- **Direct object storage access**: Read, write, and manage objects directly in the Ceph cluster.
- **Fewer layers**: Bypasses the file and block interfaces, so there is less overhead between the application and the cluster.
- **Scalable**: Designed to work efficiently with large-scale distributed systems.
- **Multi-language support**: Native APIs are available for C and C++, and there are bindings for Python, Java, PHP, and more.

### When to Use Librados

- Building custom storage solutions that require direct object access.
- Integrating Ceph with applications that need fine-grained control over data placement and retrieval.
- Developing high-performance services that leverage Ceph's scalability.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

- Link your application with `librados` and include `<rados/librados.hpp>` (C++) or `<rados/librados.h>` (C). On Debian/Ubuntu the headers come from `librados-dev`; on RHEL-like systems from `librados-devel`.
- The client needs a `ceph.conf` and a keyring for the user it connects as.
- Create the pool before running the example, for example `ceph osd pool create data`.
- Check the result with the `rados` CLI: `rados -p data ls` and `rados -p data get hello_object -`.

## Examples (e.g.,)

### Basic Usage

Below is a simple example in C++ that writes one object (error handling is reduced to a minimum):

```cpp
#include <rados/librados.hpp>
#include <iostream>
#include <string>

int main() {
    librados::Rados cluster;
    int ret = cluster.init("admin"); // connect as client.admin
    if (ret < 0) { std::cerr << "init failed: " << ret << std::endl; return 1; }

    cluster.conf_read_file("/etc/ceph/ceph.conf");
    ret = cluster.connect();
    if (ret < 0) { std::cerr << "connect failed: " << ret << std::endl; return 1; }

    librados::IoCtx io_ctx;
    ret = cluster.ioctx_create("data", io_ctx); // pool "data" must exist
    if (ret < 0) { std::cerr << "ioctx_create failed: " << ret << std::endl; cluster.shutdown(); return 1; }

    librados::bufferlist bl;
    bl.append("Hello, Ceph!");
    ret = io_ctx.write_full("hello_object", bl);
    if (ret < 0) { std::cerr << "write_full failed: " << ret << std::endl; }

    io_ctx.close();
    cluster.shutdown();
    return ret < 0 ? 1 : 0;
}
```

Build it with:

```sh
g++ -o hello hello.cc -lrados
```

## References

- [Ceph Documentation: Librados (C/C++)](https://docs.ceph.com/en/latest/rados/api/librados/)
- [Ceph Documentation: Introduction to librados](https://docs.ceph.com/en/latest/rados/api/librados-intro/)
- [RADOS: A Scalable, Reliable Storage Service for Petabyte-scale Storage Clusters (Weil et al.)](https://ceph.com/assets/pdfs/weil-rados-pdsw07.pdf)
