# eBPF

**eBPF (Extended Berkeley Packet Filter)** is a powerful and flexible technology that allows for the execution of custom bytecode within the Linux kernel. Originally designed for packet filtering, eBPF has evolved into a general-purpose infrastructure for running sandboxed programs in the kernel space.

These programs can be attached to various hooks, such as network events, system calls, and tracepoints, enabling developers to extend kernel functionality without modifying the kernel source code. This capability makes eBPF a versatile tool for performance monitoring, security enforcement, and network traffic analysis.

<div align="center">
    <img src="docs/tracing/images/ebpf.png" width="500" />
</div>

## Installation

```sh
sudo apt install linux-headers-$(uname -r)
sudo apt install clang llvm
sudo apt install libbpf-dev libbpfcc-dev
sudo apt install build-essential git make gcc libelf-dev libzstd-dev
```

## References

- [https://www.srodi.com/posts/how-to-write-and-run-an-ebpf-program-on-linux/](https://www.srodi.com/posts/how-to-write-and-run-an-ebpf-program-on-linux/)
- [https://documentation.ubuntu.com/server/explanation/intro-to/ebpf/](https://documentation.ubuntu.com/server/explanation/intro-to/ebpf/)
