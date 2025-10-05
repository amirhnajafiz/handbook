# eBPF

**eBPF (Extended Berkeley Packet Filter)** is a powerful and flexible technology that allows for the execution of custom bytecode within the Linux kernel. Originally designed for packet filtering, eBPF has evolved into a general-purpose infrastructure for running sandboxed programs in the kernel space.

These programs can be attached to various hooks, such as network events, system calls, and tracepoints, enabling developers to extend kernel functionality without modifying the kernel source code. This capability makes eBPF a versatile tool for performance monitoring, security enforcement, and network traffic analysis.

## Overview

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

## Test Your eBPF Installation

To verify your eBPF setup, you can run a simple bpftrace one-liner that traces system calls. For example, to trace every time a process calls the `execve` syscall:

```sh
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_execve { printf("%s\n", comm); }'
```

If your installation is correct, you should see process names printed as they execute new programs. Press `Ctrl+C` to stop tracing.

Alternatively, you can check the installed version of bpftrace:

```sh
bpftrace --version
```

## BCC

**BCC (BPF Compiler Collection)** is a set of tools and libraries for creating, loading, and managing eBPF programs. It provides Python and Lua bindings, making it easier to write eBPF programs for tracing, monitoring, and debugging Linux systems.

### Installation

To install BCC on Ubuntu, run:

```sh
sudo apt install bpfcc-tools python3-bpfcc libbpfcc-dev
```

### Test Your BCC Installation

You can test BCC by running one of its example tools, such as `execsnoop`, which traces new process executions:

```sh
sudo execsnoop
```

If BCC is installed correctly, you should see a list of executed commands in real time.

## References

- [https://www.srodi.com/posts/how-to-write-and-run-an-ebpf-program-on-linux/](https://www.srodi.com/posts/how-to-write-and-run-an-ebpf-program-on-linux/)
- [https://documentation.ubuntu.com/server/explanation/intro-to/ebpf/](https://documentation.ubuntu.com/server/explanation/intro-to/ebpf/)
