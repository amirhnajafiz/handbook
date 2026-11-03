# LTTng

## Quick Description (QD)

The Linux Trace Toolkit next generation (LTTng) is an open-source software toolkit that you can use to trace the Linux kernel, user applications, and user libraries at the same time.

LTTng traces using several mechanisms:

- **Kernel and User-Space Tracepoints:** The primary mechanism for LTTng tracing is tracepoints. These are static instrumentation points in both kernel and user-space code that can be "activated" by tracers like LTTng, resulting in minimal runtime overhead when disabled and efficient data collection when enabled. LTTng-UST provides a user-space API for defining and using tracepoints in applications, using macros like `TRACEPOINT_EVENT()`.
- **Kprobes and Kretprobes:** LTTng supports dynamic instrumentation via kprobes (and kretprobes), which allows the toolkit to tap into arbitrary kernel instructions and function entry/exit points. This enables tracing even if explicit tracepoints are not present.
- **Function Tracing:** LTTng can hook into function tracer mechanisms to record function calls within the kernel.
- **CPU Performance Monitoring Unit (PMU) Counters:** It can also trace using hardware performance counters for fine-grained, low-level performance analysis.

Like [eBPF](01_ebpf.md), LTTng can use tracepoints and kprobes. The difference is that LTTng is a pure tracer: it records events into ring buffers at low overhead for offline analysis, instead of running custom programs in the kernel.

### Context

When tracing with LTTng using kprobes, the default payload for kprobe events is empty, meaning it does not automatically capture detailed information like input parameters, function location, or other contextual data. However, LTTng provides options and mechanisms to export more detailed information during tracing:

- **Probe location:** When enabling a kprobe event with `--probe`, the argument is the location: a symbol (optionally with an offset, `SYMBOL+OFFSET`) or an address. The same applies to `--function` for kretprobes.
- **Custom tracepoints and user-space instrumentation:** For richer event payloads such as input parameters and more detailed context, LTTng encourages using static tracepoints or user-space tracepoints, where the event payload and context fields can be defined to include these details explicitly.
- **Context fields:** LTTng allows attaching additional context fields to a tracing session or channels. This can include CPU ID, process ID, thread ID, timestamps, and source code information, which helps provide more insight into where and when an event occurred.
- **Function and user-space tracepoints:** These can be defined to capture function parameters and other runtime data explicitly, in contrast to kprobes, which are more generic and have limited payload.
- **Dynamic instrumentation limitations:** Kprobes alone do not capture input parameters or the function call stack by default. To capture input function parameters, either kernel static tracepoints need to be defined with the payload, or additional instrumentation techniques like eBPF can be used in combination with tracing tools.

## Installation

Install the tools:

```bash
sudo apt-add-repository ppa:lttng/stable-2.15
sudo apt-get update
sudo apt install lttng-tools liblttng-ust-dev lttng-modules-dkms babeltrace2
```

> `babeltrace2` is used to convert the binary trace files into readable text for counting.

### Check the Session Daemon

Check whether the session daemon is running:

```bash
ps aux | grep lttng-sessiond
```

If not, start it manually:

```bash
sudo lttng-sessiond --daemonize
sudo systemctl enable --now lttng-sessiond
```

To reset it, stop the daemon, remove its runtime directory, and start it again:

```bash
sudo pkill lttng-sessiond
sudo rm -rf /var/run/lttng
sudo lttng-sessiond --daemonize
```

## Useful Tips/Commands (UToC)

### Create a Session

A tracing session groups the event rules and the recorded data. The session daemon (`lttng-sessiond`) manages the sessions, and the traces are written to the given output directory:

```bash
sudo lttng create mysession -o /tmp/lttng-traces
```

### Find Available Tracepoints

For example, if you want ext4-specific tracepoints, first verify they exist on your kernel:

```bash
# Option A: use lttng to list kernel tracepoints and filter
lttng list -k | grep '^ *ext4' -A5

# Option B: check the ftrace events directory (see the Tracing index)
ls /sys/kernel/debug/tracing/events/ext4
```

### Enable Recordings

To enable all kernel syscalls (every syscall entry/exit):

```bash
sudo lttng enable-event --kernel --syscall --all
```

To enable specific syscall names (example: openat/read/write/close; on modern kernels `open` is mostly replaced by `openat`):

```bash
sudo lttng enable-event --kernel --syscall openat,read,write,close
```

Syscall events are recorded as `syscall_entry_<name>` and `syscall_exit_<name>`.

To enable ext4 tracepoints (example: `ext4_write_begin` and `ext4_free_inode`; use the names shown by `lttng list --kernel`):

```bash
sudo lttng enable-event --kernel --tracepoint ext4_write_begin,ext4_free_inode
```

To enable a kprobe on a function (the last argument is the name you give to the event):

```bash
sudo lttng enable-event --kernel --probe ext4_xattr_get ext4_xattr_get_probe
```

### Start and Stop

```bash
sudo lttng start
# ... run workload that will hit ext4 / syscalls ...
sudo lttng stop
sudo lttng destroy
```

### Overview

```bash
babeltrace2 /tmp/lttng-traces/mysession-* | grep 'ext4_write_begin' | wc -l
```

```bash
babeltrace2 /tmp/lttng-traces/mysession-* \
  | awk 'match($0, /syscall_entry_[a-z0-9_]+/) { counts[substr($0, RSTART + 14, RLENGTH - 14)]++ }
         END { for (n in counts) print counts[n], n }' \
  | sort -rn
```

### Tips

- If the trace is large, enable only the events you need (syscalls of interest or only ext4 tracepoints).
- Use `lttng list -k` to inspect what is available before enabling.
- If your goal is per-process syscall counts, combine `lttng track --kernel --pid=PID` with `babeltrace2` + `grep`/`awk` to attribute events.
- If ext4 tracepoints are missing, check the kernel config (`CONFIG_TRACEPOINTS`) or kernel version; some distros and kernels may not expose all filesystem tracepoints. You can also use the generic syscall trace, which captures VFS/syscall activity even if ext4 tracepoints are absent.

## Examples (e.g.,)

End-to-end example (count write syscalls and ext4 write begin events):

```bash
# create
sudo lttng create countsession -o /tmp/lttng-traces

# enable: kernel write syscall + ext4 write begin tracepoint
sudo lttng enable-event --kernel --syscall write
sudo lttng enable-event --kernel --tracepoint ext4_write_begin

# add pid context (optional)
sudo lttng add-context --kernel -t pid -t procname

# start
sudo lttng start

# run workload that writes to ext4 files here...

# stop
sudo lttng stop

# count
babeltrace2 /tmp/lttng-traces/countsession-* | tee /tmp/trace.txt
grep 'syscall_entry_write' /tmp/trace.txt | wc -l        # number of write syscalls
grep 'ext4_write_begin' /tmp/trace.txt | wc -l   # number of ext4 write begin tracepoints
```

## References

- [LTTng documentation (v2.13)](https://lttng.org/docs/v2.13/)
- [lttng-enable-event(1) manual page (v2.13)](https://lttng.org/man/1/lttng-enable-event/v2.13/)
- [Kernel tracing with ftrace (Linux kernel documentation)](https://www.kernel.org/doc/html/latest/trace/ftrace.html)
