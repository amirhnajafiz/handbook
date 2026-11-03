# PBFT

## Quick Description (QD)

**Practical Byzantine Fault Tolerance (PBFT)** is a state machine replication algorithm (Castro and Liskov, 1999) designed to work in asynchronous distributed systems where nodes may fail or act maliciously (Byzantine faults). It was the first Byzantine fault tolerant algorithm efficient enough to be used in practice. PBFT ensures that a distributed system can reach agreement even if some nodes behave arbitrarily.

### Key Concepts

- **Byzantine fault:** A failure where nodes may act arbitrarily, including malicious behavior or sending conflicting information.
- **Replica:** Each node in the system is called a replica.
- **Primary:** The leader node that coordinates the consensus process.
- **View:** A period during which a particular primary is responsible for coordinating consensus.
- **Quorum:** PBFT requires at least 3f + 1 replicas to tolerate up to f Byzantine faults. Decisions need a quorum of 2f + 1 replicas, so any two quorums intersect in at least one non-faulty replica.

### PBFT Phases

1. **Pre-prepare:**
    - The client sends a request to the primary. The primary assigns it a sequence number and multicasts a pre-prepare message to all backups.

2. **Prepare:**
    - A backup that accepts the pre-prepare (same view, valid sequence number, no conflicting one) multicasts a prepare message to all replicas.
    - A replica is "prepared" once it has the pre-prepare and 2f matching prepare messages from different replicas.

3. **Commit:**
    - A prepared replica multicasts a commit message.
    - When a replica has 2f + 1 matching commit messages (including its own), the request is committed-local: it executes the request (after all lower sequence numbers) and replies directly to the client.
    - The client accepts a result after receiving f + 1 matching replies from different replicas.

4. **View change:**
    - If the primary is faulty or too slow, backups time out and move to the next view with a new primary (replica `v mod n`).

### Safety and Fault Tolerance

- PBFT can tolerate up to f faulty nodes in a system of 3f + 1 replicas.
- Safety (the replicated service is linearizable) holds in an asynchronous network, with no timing assumptions, as long as at most f replicas are faulty.
- Liveness relies on weak synchrony: message delay must not grow faster than time indefinitely. Otherwise, by the FLP result, progress can not be guaranteed.
- The three-phase message pattern costs O(n²) messages per request, which limits the number of replicas.

### Use Cases

- Permissioned blockchains
- Distributed databases
- Financial systems requiring high integrity

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

_Nothing here yet._

## References

- [Practical Byzantine Fault Tolerance (Castro and Liskov, OSDI 1999)](https://www.usenix.org/conference/osdi-99/practical-byzantine-fault-tolerance)
- [Practical Byzantine Fault Tolerance (paper, HTML version)](https://www.usenix.org/publications/library/proceedings/osdi99/full_papers/castro/castro_html/castro.html)
- [The Byzantine Generals Problem (Lamport, Shostak, Pease)](https://lamport.azurewebsites.net/pubs/byz.pdf)
