# eBPF FlameGraph

Clone FlameGraph repository:

```sh
git clone https://github.com/brendangregg/FlameGraph.git
```

## Convert traces to FG output

```sh
# Save bpftrace output
sudo bpftrace ext4.bt > out.txt

# Convert to folded format
./stackcollapse-bpftrace.pl out.txt > out.folded

# Generate SVG flamegraph
./flamegraph.pl out.folded > flamegraph.svg
```

### folded

```sh
cat out.txt \
  | sed -e 's/^@\[/STACK:/' -e 's/\]:/ /' \
  | awk '
    /^STACK:/ {
      # Replace commas and spaces after the tag
      gsub(/^STACK:/, "")
      gsub(/,/, "")
      gsub(/^[ \t]+/, "")
      stack=$0
      count=""
    }
    /^[ \t]/ {
      # Stack line continuation
      gsub(/^[ \t]+/, "")
      stack=stack ";" $0
    }
    /^[^ \t]/ && $NF ~ /^[0-9]+$/ {
      # Last line with count
      count=$NF
      print stack, count
    }
  ' > out.folded
```

output:

```txt
write:ext4_file_write_iter;ext4_file_write_iter+1;vfs_iter_write+188;lo_write_simple.isra.0+294;do_req_filebacked+387;loop_process_work+185;loop_workfn+29;process_one_work+388;worker_thread+774;kthread+242;ret_from_fork+71;ret_from_fork_asm+27 12492
```

## References

- [https://github.com/brendangregg/FlameGraph](https://github.com/brendangregg/FlameGraph)
