# FlameGraph

## Quick Description (QD)

A FlameGraph is a visualization of profiled stack traces, invented by Brendan Gregg. Each box is a function, the width of a box is proportional to how often it appeared in the sampled stacks (so wide boxes are where the time goes), the y-axis is the stack depth, and the x-axis is sorted alphabetically (it is **not** time). It works with any data that can be turned into folded stacks: CPU, off-CPU, memory, or I/O profiling.

## Installation

Clone the FlameGraph repository:

```sh
git clone https://github.com/brendangregg/FlameGraph.git
```

## Useful Tips/Commands (UToC)

### Convert Traces to FlameGraph Output

```sh
# Save bpftrace output
sudo bpftrace ext4.bt > out.txt

# Convert to folded format
./stackcollapse-bpftrace.pl out.txt > out.folded

# Generate SVG flamegraph
./flamegraph.pl out.folded > flamegraph.svg
```

### Profile CPU with perf

```sh
sudo perf record -F 99 -a -g -- sleep 30
sudo perf script | ./stackcollapse-perf.pl | ./flamegraph.pl > cpu.svg
```

Each `stackcollapse-*.pl` script in the repository converts the output of a different profiler (perf, bpftrace, DTrace, ...) to the folded format, so there is no need to write the conversion by hand.

## Examples (e.g.,)

Example of a folded stack line (frames separated by `;`, then a space and the sample count):

```txt
write:ext4_file_write_iter;ext4_file_write_iter+1;vfs_iter_write+188;lo_write_simple.isra.0+294;do_req_filebacked+387;loop_process_work+185;loop_workfn+29;process_one_work+388;worker_thread+774;kthread+242;ret_from_fork+71;ret_from_fork_asm+27 12492
```

## References

- [FlameGraph repository](https://github.com/brendangregg/FlameGraph)
- [Flame Graphs (Brendan Gregg)](https://www.brendangregg.com/flamegraphs.html)
