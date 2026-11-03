# Raft

## Quick Description (QD)

**Raft** is a consensus algorithm designed to manage a replicated log in distributed systems. It is widely used because it is easier to understand than other consensus algorithms like Paxos, while being equivalent to (multi-)Paxos in fault tolerance and performance. It assumes crash failures (nodes can stop and restart), not Byzantine ones.

### Key Concepts

- **Leader election:** One node is elected as the leader, which handles all client requests that modify the log.
- **Log replication:** The leader appends client requests to its log and replicates them to follower nodes.
- **Safety:** Raft ensures that committed entries are durable and consistent across the cluster, even in the presence of failures.
- **Term:** Time in Raft is divided into terms, numbered with consecutive integers. Each term begins with an election, and there is at most one leader per term. Terms act as a logical clock and are used to detect obsolete information: a node that sees a higher term updates its own, and a leader or candidate with an outdated term steps down.

### Raft Roles

- **Leader:** Handles all client interactions and log replication.
- **Follower:** Passive nodes that respond to requests from leaders and candidates.
- **Candidate:** A follower becomes a candidate when it starts an election to become the leader.

### Leader Election Process

1. Each node starts as a follower.
2. The leader sends periodic heartbeats (empty AppendEntries RPCs). If a follower does not hear from a leader within its election timeout (randomized, to avoid split votes), it increments its term, becomes a candidate, votes for itself, and sends RequestVote RPCs to the other nodes.
3. A node votes for at most one candidate per term, and only if the candidate's log is at least as up-to-date as its own.
4. If a candidate receives votes from a majority, it becomes the leader. If it hears from a leader with a term at least as large as its own, it goes back to being a follower. If nobody wins (split vote), a new election starts after another timeout.

### Log Replication

- The leader receives commands from clients and appends them to its log.
- The leader sends AppendEntries RPCs to followers to replicate the log entries.
- Once a log entry is safely replicated on a majority of nodes, the leader considers it committed and applies it to its state machine. Followers learn the commit index from later AppendEntries RPCs.
- A leader only commits entries from its own term by counting replicas. Entries from earlier terms are committed indirectly when a later entry of the current term is committed.

### Safety and Fault Tolerance

- Raft can tolerate up to ⌊(N-1)/2⌋ crash failures in a cluster of N nodes (for example, 2 failures out of 5).
- Committed entries are never lost: any new leader is guaranteed to have all committed entries, because a candidate needs the votes of a majority and that majority overlaps with the one that stored the entry.
- Progress needs a majority of nodes to be up and able to communicate.

### Use Cases

- Distributed databases
- Key-value stores
- Configuration management systems

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

_Nothing here yet._

## References

- [In Search of an Understandable Consensus Algorithm (Raft Paper)](https://raft.github.io/raft.pdf)
- [The Raft Consensus Algorithm Website](https://raft.github.io/)
- [Consensus: Bridging Theory and Practice (Diego Ongaro's PhD thesis)](https://web.stanford.edu/~ouster/cgi-bin/papers/OngaroPhD.pdf)
