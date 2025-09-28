# Librados

Librados is a C++ library that provides direct access to the RADOS (Reliable Autonomic Distributed Object Store) layer of Ceph. It allows applications to interact with Ceph storage clusters without going through the CephFS or RADOS Gateway layers.

## Key Features

- **Direct Object Storage Access**: Read, write, and manage objects directly in the Ceph cluster.
- **High Performance**: Bypasses file and block interfaces for lower latency.
- **Scalable**: Designed to work efficiently with large-scale distributed systems.
- **Multi-language Support**: Bindings available for C, C++, Python, Java, and more.

## Basic Usage

To use Librados, link your application with the `librados` library and include the appropriate headers. Below is a simple example in C++:

```cpp
#include <rados/librados.hpp>

int main() {
    librados::Rados cluster;
    cluster.init("admin"); // Use the 'admin' user
    cluster.conf_read_file("/etc/ceph/ceph.conf");
    cluster.connect();

    librados::IoCtx io_ctx;
    cluster.ioctx_create("data", io_ctx);

    std::string obj_name = "hello_object";
    std::string content = "Hello, Ceph!";
    io_ctx.write_full(obj_name, librados::bufferlist::static_from_mem(content.c_str(), content.size()));

    io_ctx.close();
    cluster.shutdown();
    return 0;
}
```

## When to Use Librados?

- Building custom storage solutions that require direct object access.
- Integrating Ceph with applications that need fine-grained control over data placement and retrieval.
- Developing high-performance services that leverage Ceph's scalability.

## References

- [Ceph Documentation: Librados](https://docs.ceph.com/en/latest/rados/api/librados/)
- [Librados API Reference](https://docs.ceph.com/en/latest/rados/api/librados/)
