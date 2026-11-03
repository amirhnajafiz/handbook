# eBPF

## Quick Description (QD)

**eBPF (Extended Berkeley Packet Filter)** is a powerful and flexible technology that allows the execution of custom bytecode within the Linux kernel. Originally designed for packet filtering, eBPF has evolved into a general-purpose infrastructure for running sandboxed programs in kernel space.

These programs can be attached to various hooks, such as network events, system calls, and tracepoints, enabling developers to extend kernel functionality without modifying the kernel source code. This capability makes eBPF a versatile tool for performance monitoring, security enforcement, and network traffic analysis.

### Overview

<div align="center">
    <img src="docs/tracing/images/ebpf.png" width="500" />
</div>

### BCC

**BCC (BPF Compiler Collection)** is a set of tools and libraries for creating, loading, and managing eBPF programs. It provides Python, Lua, and C++ front ends, making it easier to write eBPF programs for tracing, monitoring, and debugging Linux systems.

## Installation

```sh
sudo apt install linux-headers-$(uname -r)
sudo apt install clang llvm
sudo apt install libbpf-dev libbpfcc-dev
sudo apt install build-essential git make gcc libelf-dev libzstd-dev
```

### Installing BCC

To install BCC on Ubuntu, run:

```sh
sudo apt install bpfcc-tools python3-bpfcc libbpfcc-dev bpftrace
```

## Useful Tips/Commands (UToC)

### Test Your eBPF Installation

To verify your eBPF setup, you can run a simple `bpftrace` (installed by the `bpftrace` package) one-liner that traces system calls. For example, to trace every time a process calls the `execve` syscall:

```sh
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_execve { printf("%s\n", comm); }'
```

If your installation is correct, you should see process names printed as they execute new programs. Press `Ctrl+C` to stop tracing.

Alternatively, you can check the installed version of `bpftrace`:

```sh
bpftrace --version
```

### Test Your BCC Installation

You can test BCC by running one of its example tools, such as `execsnoop`, which traces new process executions:

```sh
sudo execsnoop-bpfcc
```

On Ubuntu/Debian the BCC tools are installed with a `-bpfcc` suffix (on other distributions the tool is usually just `execsnoop`). If BCC is installed correctly, you should see a list of executed commands in real time.

## Examples (e.g.,)

_Nothing here yet._

## References

- [How to write and run an eBPF program on Linux](https://www.srodi.com/posts/how-to-write-and-run-an-ebpf-program-on-linux/)
- [What is eBPF? (ebpf.io)](https://ebpf.io/what-is-ebpf/)
- [BPF Documentation (Linux kernel)](https://docs.kernel.org/bpf/index.html)
- [BCC repository](https://github.com/iovisor/bcc)
- [bpftrace repository](https://github.com/bpftrace/bpftrace)
- [Introduction to eBPF (Ubuntu Server documentation)](https://documentation.ubuntu.com/server/explanation/intro-to/ebpf/)
