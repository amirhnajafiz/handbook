# Consistency

## Quick Description (QD)

Consistency in distributed systems refers to the guarantee about the visibility and ordering of updates to a data item. It defines how and when changes made by one node become visible to others, and how systems handle concurrent operations.

### Consistency Models

- **Strong consistency:** Every read receives the most recent write or an error, as if there was a single copy of the data. Example: linearizability, where every operation appears to take effect atomically at some point between its invocation and its response.
- **Sequential consistency:** The result of execution is as if all operations were executed in some sequential order, and the operations of each individual process appear in this sequence in the order issued. Unlike linearizability, this order does not have to respect real time.
- **Causal consistency:** Writes that are causally related (one may have influenced the other) must be seen by all processes in the same order. Concurrent writes may be seen in a different order on different nodes.
- **Eventual consistency:** If no new updates are made, eventually all replicas converge and all accesses return the last updated value. There is no bound on how long this takes, and until then reads may return stale data.
- **Read-your-writes consistency:** After a process writes a value, it will always see that value in subsequent reads.
- **Monotonic read consistency:** Once a process has seen a particular value, it will never see an earlier value in subsequent reads.
- **Monotonic write consistency:** Writes by a process are applied in the order issued.
- **Session consistency:** Guarantees consistency for a single session, often combining read-your-writes and monotonic reads.

### Trade-offs

- The CAP theorem says that when a network partition happens, a system must choose between consistency (linearizability) and availability. Even without partitions, stronger models cost latency (the PACELC trade-off).
- Stronger consistency models provide more predictable behavior but can reduce system availability and performance.
- Weaker consistency models improve performance and availability but may expose stale or out-of-order data.

### Use Cases

- **Strong consistency:** Banking systems, distributed locking, critical configuration management.
- **Eventual consistency:** Social media feeds, DNS, caching systems.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

_Nothing here yet._

## References

- [Jepsen: Consistency Models](https://jepsen.io/consistency)
- [Jepsen: Linearizability](https://jepsen.io/consistency/models/linearizable)
- [Jepsen: Sequential Consistency](https://jepsen.io/consistency/models/sequential)
- [Jepsen: Causal Consistency](https://jepsen.io/consistency/models/causal)
- [Jepsen: Read Your Writes](https://jepsen.io/consistency/models/read-your-writes)
- [Jepsen: Monotonic Reads](https://jepsen.io/consistency/models/monotonic-reads)
- [Jepsen: Monotonic Writes](https://jepsen.io/consistency/models/monotonic-writes)
- [Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services (Gilbert and Lynch)](https://www.comp.nus.edu.sg/~gilbert/pubs/BrewersConjecture-SigAct.pdf)
- [Eventually Consistent (Werner Vogels)](https://www.allthingsdistributed.com/2008/12/eventually_consistent.html)
- [Strong consistency models (Kyle Kingsbury)](https://aphyr.com/posts/313-strong-consistency-models)
- [Consistency Models (Wikipedia)](https://en.wikipedia.org/wiki/Consistency_model)
- [Designing Data-Intensive Applications (Martin Kleppmann)](https://dataintensive.net/)
