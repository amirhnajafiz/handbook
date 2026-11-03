# Paxos

## Quick Description (QD)

**Paxos** is a family of protocols for solving consensus in a network of unreliable processors (nodes). It is designed to ensure that a group of nodes can agree on a single value, even if some nodes or network messages fail.

### Key Concepts

- **Consensus:** The process of agreeing on a single value among distributed nodes.
- **Proposer:** Suggests values to be agreed upon.
- **Acceptor:** Votes on proposed values.
- **Learner:** Learns the chosen value after consensus is reached.
- **Quorum:** A majority of acceptors whose agreement is required. Any two majorities overlap in at least one acceptor, which is what makes Paxos safe. With 2f + 1 acceptors, Paxos tolerates f crash failures.

### Paxos Phases

1. **Prepare phase:**
    - A proposer selects a unique proposal number n and sends a prepare request to a majority of acceptors.
    - If n is higher than any prepare request the acceptor has already answered, it responds with a promise not to accept proposals numbered lower than n, and includes the highest-numbered proposal it has already accepted (if any).

2. **Accept phase:**
    - After receiving promises from a majority, the proposer sends an accept request with number n. The value must be the value of the highest-numbered proposal reported in the promises; if none was reported, the proposer is free to choose its own value.
    - An acceptor accepts the proposal unless it has already promised to a higher-numbered one.

3. **Learn phase:**
    - Once a value is accepted by a majority, it is chosen.
    - Learners are informed of the chosen value.

### Safety and Fault Tolerance

- Paxos guarantees safety (only a value that was proposed can be chosen, and only one value is chosen) even with crashes, message loss, duplication, and reordering. It does not assume synchrony.
- Liveness is not guaranteed in general: by the FLP result no asynchronous consensus protocol can guarantee it, and with two competing proposers the prepare/accept rounds can keep preempting each other forever. In practice a single distinguished proposer (leader) is elected, and progress then needs a majority of acceptors that can communicate.
- Basic Paxos decides one value. Multi-Paxos runs many instances to build a replicated log, which is what [Raft](01_raft.md) does with a stronger leader.

### Use Cases

- Distributed databases
- Distributed locks
- Replicated state machines

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

_Nothing here yet._

## References

- [Paxos Made Simple (Leslie Lamport)](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)
- [The Part-Time Parliament (Original Paxos Paper)](https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf)
- [Time, Clocks, and the Ordering of Events in a Distributed System (Leslie Lamport)](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)
