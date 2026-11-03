# Tracing

<div class="dedication">
I want to dedicate this page to all computer engineers!
</div>

---

Tracing tools can help developers, end users, or admins to track their programs for debugging, monitoring, or security. These tools may add overhead to the system, which impacts performance.

This section covers:

- eBPF
- _bpftrace_ (coming soon)
- FlameGraph
- LTTng
- _ptrace_ (coming soon)
- _strace_ (coming soon)

## Viewing Tracepoints in Linux

To list the available tracepoints in a Linux system, you can explore the `/sys/kernel/debug/tracing/events/` directory. Each subdirectory represents a tracepoint category.

```bash
ls /sys/kernel/debug/tracing/events/
```

To see all tracepoints and their details, use:

```bash
sudo cat /sys/kernel/debug/tracing/available_events
```

This shows which tracepoints are available for tracing with tools like `perf`, `bpftrace`, or `ftrace`.
