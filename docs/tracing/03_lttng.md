# LTTng

The Linux Trace Toolkit next generation is an open source software toolkit which you can use to trace the Linux kernel, user applications, and user libraries at the same time.

LTTng traces using several mechanisms:

- **Kernel and User-space Tracepoints**: The primary mechanism for LTTng tracing is tracepoints. These are static instrumentation points in both kernel and user-space code that can be “activated” by tracers like LTTng, resulting in minimal runtime overhead when disabled, and efficient data collection when enabled. LTTng-UST provides a user-space API for defining and using tracepoints in applications, using macros like TRACEPOINT_EVENT().
- **Kprobes and Kretprobes**: LTTng supports dynamic instrumentation via kprobes (and kretprobes), which allows the toolkit to tap into arbitrary kernel instructions and function entry/exit points. This enables tracing even if explicit tracepoints aren’t present.
- **Function Tracing**: LTTng can hook into function tracer mechanisms to record function calls within the kernel.
- **CPU Performance Monitoring Unit (PMU) Counters**: It can also trace using hardware performance counters for fine-grained, low-level performance analysis.

While eBPF focuses on using tracepoints and kprobes for dynamic instrumentation, LTTng supports both these mechanisms and more, with an emphasis on pre-defined tracepoints for zero overhead when disabled, extensive trace coverage, and support for dynamic probes for flexibility.

## Installation

Install the tools:

```bash
sudo apt update
sudo apt install lttng-tools lttng-modules-dkms babeltrace2
```

> babeltrace2 is used to convert the binary trace files into readable text for counting.

### Check the session daemon

Check to see if the session daemon is running:

```bash
ps aux | grep lttng-sessiond
```

If not, start it manually:

```bash
sudo lttng-sessiond --daemonize
sudo systemctl enable --now lttng-sessiond
```

For reset, remove it:

```bash
sudo rm -rf /var/run/lttng
sudo lttng-sessiond --daemonize
```

### Create a session

Session daemons are act as user level applications to collect the results of kernel tracing:

```bash
sudo lttng create mysession -o /tmp/lttng-traces
```

### Find available tracepoints

E.g. if you want ext4-specific tracepoints, first verify they exist on your kernel:

```bash
# Option A: use lttng to list kernel tracepoints and filter
lttng list -k | grep '^ *ext4' -A5

# Option B: check ftrace tracepoint filesystem
ls /sys/kernel/debug/tracing/events/ext4  # shows ext4:... tracepoint names
```

#### Enable kernel tracepoints

The tracepoints are managed via the debugfs filesystem, which is usually mounted at /sys/kernel/debug. The tracepoints for various subsystems (including ext4) are found under:

```txt
/sys/kernel/debug/tracing/events/
```

You can enable all ext4 tracepoints by running:

```bash
echo 1 | sudo tee /sys/kernel/debug/tracing/events/ext4/enable
```

#### View traces

View the traces, to see the trace data:

```bash
cat /sys/kernel/debug/tracing/trace
```

Or, watch live events with:

```bash
cat /sys/kernel/debug/tracing/trace_pipe
```

### Enable recordings

To enable all kernel syscalls (every syscall entry/exit):

```bash
sudo lttng enable-event --kernel --syscall --all
```

To enable specific syscall names (example: open/read/write/close):

```bash
sudo lttng enable-event --kernel --syscall open,read,write,close
```

To enable ext4 tracepoints (example: ext4_write_begin and ext4_free_inode):

```bash
sudo lttng enable-event --kernel --tracepoint ext4:ext4_write_begin,ext4:ext4_free_inode
```

To enable probs:

```bash
sudo lttng enable-event --kernel --probe=ext4_xattr_get ext_attr
```

### Start & Stop

```bash
sudo lttng start
# ... run workload that will hit ext4 / syscalls ...
sudo lttng stop
sudo lttng destroy
```

### Overview

```bash
babeltrace2 /tmp/lttng-traces/mysession-* | grep 'ext4:ext4_write_begin' | wc -l
```

```bash
babeltrace2 /tmp/lttng-traces/mysession-* \
  | awk '/sys_enter_/ { gsub(/.*sys_enter_/, "", $0); name=$1; counts[name]++ } 
         END { for (n in counts) print counts[n], n }' \
  | sort -rn
```

## Tips

- If the trace is large, enable only the events you need (syscalls of interest or only ext4 tracepoints). 
LTTng
- Use lttng list -k to inspect what’s available before enabling. 
- If your goal is per-process syscall counts, combine lttng track --kernel --pid=PID with babeltrace2 + grep/awk to attribute events. 
- If ext4 tracepoints are missing, check kernel config (TRACEPOINTS) or kernel version; some distros / kernels may not expose all FS tracepoints. You can also use the generic syscall trace (which will capture VFS/syscall activity even if ext4 tracepoints are absent).

## E.g.

Example end-to-end (count write syscalls and ext4 write begin):

```bash
# create
sudo lttng create countsession -o /tmp/lttng-traces

# enable: kernel write syscall + ext4 write begin tracepoint
sudo lttng enable-event --kernel --syscall write
sudo lttng enable-event --kernel --tracepoint ext4:ext4_write_begin

# add pid context (optional)
sudo lttng add-context --kernel -t pid -t procname

# start
sudo lttng start

# run workload that writes to ext4 files here...

# stop
sudo lttng stop

# count
babeltrace2 /tmp/lttng-traces/countsession-* | tee /tmp/trace.txt
grep 'sys_enter_write' /tmp/trace.txt | wc -l         # number of write syscalls
grep 'ext4:ext4_write_begin' /tmp/trace.txt | wc -l   # number of ext4 write begin tracepoints
```

## Context

When tracing with LTTng using kprobes, the default payload for kprobe events is empty, meaning it does not automatically capture detailed information like input parameters, function location, or other contextual data. However, LTTng provides options and mechanisms to export more detailed information during tracing:

- Location option: When enabling a kprobe event, LTTng supports a --location option to specify the exact probe location in the kernel code. This can be an address or function offset, which helps precisely identify where the probe is placed.
- Custom tracepoints and user-space instrumentation: For richer event payloads such as input parameters and more detailed context, LTTng encourages using static tracepoints or user-space tracepoints, where the event payload and context fields can be defined to include these details explicitly.
- Context fields: LTTng allows attaching additional context fields to a tracing session or channels. This can include CPU id, process id, thread id, timestamps, and source code information, which helps provide more insight into where and when an event occurred.
- Function and user-space tracepoints: These can be defined to capture function parameters and other runtime data explicitly, in contrast to kprobes which are more generic and have limited payload.
- Dynamic instrumentation limitations: Kprobes alone do not capture input parameters or the function call stack by default. To capture input function parameters, either kernel static tracepoints need to be defined with the payload, or additional instrumentation techniques like eBPF can be used in combination with tracing tools.

## References

- [https://lttng.org/docs/v2.13/](https://lttng.org/docs/v2.13/)
