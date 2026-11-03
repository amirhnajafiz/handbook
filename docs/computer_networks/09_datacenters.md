# Datacenters

## Quick Description (QD)

Datacenters are specialized facilities that house large numbers of servers, storage systems, and networking equipment to support cloud computing, enterprise IT, and large-scale web services. Datacenter networking focuses on providing high bandwidth, low latency, scalability, and reliability to interconnect thousands of servers efficiently.

### Key Concepts in Datacenter Networking

- **High Bandwidth and Low Latency:** Datacenter networks are designed to handle massive amounts of data with minimal delay.
- **Scalability:** Networks must support rapid growth in the number of servers and virtual machines.
- **Redundancy and Reliability:** Multiple paths and failover mechanisms ensure continuous operation.
- **East-West Traffic:** Most traffic is between servers within the datacenter (east-west), not just in and out (north-south).

### Datacenter Network Topologies

- **Three-Tier Architecture:** Traditional model with Core, Aggregation, and Access layers.
- **Fat-Tree (Clos) Topology:** Built from identical commodity switches, it provides high bisection bandwidth and multiple equal-cost paths between servers, enabling scalability and fault tolerance.
- **Leaf-Spine Architecture:** Modern design with two layers. Leaf switches connect to servers, and spine switches interconnect all leaf switches, reducing bottlenecks.

### Datacenter TCP (DCTCP)

- **DCTCP** is a TCP variant optimized for datacenter environments.
- Uses Explicit Congestion Notification (ECN) marks to provide fine-grained feedback about congestion: the sender reduces its window in proportion to the fraction of marked packets, instead of halving it (see [Congestion Control](06_congestions.md)).
- Reduces queue buildup and latency, improving throughput for long flows without hurting short ones.
- Developed at Microsoft Research and available in Windows Server and Linux.

### PortLand

- **PortLand** is a scalable, fault-tolerant Layer 2 datacenter network fabric.
- Uses hierarchical, location-aware pseudo MAC (PMAC) addresses to simplify forwarding and support VM migration.
- Employs a logically centralized fabric manager that answers ARP requests and tracks the topology.
- Designed to work with fat-tree topologies and support large-scale datacenter deployments.

### Software-Defined Networking (SDN) in Datacenters

- **SDN** separates the control plane from the data plane, enabling centralized management and programmability of the network.
- Controllers (e.g., ONOS, OpenDaylight) manage network devices and policies, talking to switches through southbound protocols such as OpenFlow.
- Enables rapid deployment of new services, automated network management, and fine-grained traffic engineering.
- Facilitates network virtualization and multi-tenancy.

### Other Datacenter Networking Technologies

- **VXLAN (Virtual Extensible LAN):** Overlays Layer 2 networks over Layer 3 infrastructure, enabling scalable network virtualization.
- **RDMA (Remote Direct Memory Access):** Enables high-throughput, low-latency networking for storage and compute clusters.
- **TRILL/SPB:** Protocols for scalable Layer 2 multipath forwarding.
- **BGP in the datacenter:** Many large datacenters run eBGP on Clos fabrics (RFC 7938) instead of Layer 2 fabrics.
- **Network Function Virtualization (NFV):** Virtualizes network services (firewalls, load balancers) to run on commodity hardware.

### Challenges in Datacenter Networking

- **Congestion Control:** Managing incast and outcast congestion, especially for bursty workloads.
- **Load Balancing:** Distributing traffic evenly across multiple paths and servers.
- **Fault Tolerance:** Rapid detection and recovery from failures.
- **Security:** Isolating tenants, preventing attacks, and ensuring compliance.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

_Nothing here yet._

## References

- [RFC 8257: Data Center TCP (DCTCP): TCP Congestion Control for Data Centers](https://datatracker.ietf.org/doc/html/rfc8257)
- [Data Center TCP (DCTCP), Microsoft Research](https://www.microsoft.com/en-us/research/publication/data-center-tcp-dctcp/)
- [PortLand: A Scalable Fault-Tolerant Layer 2 Data Center Network Fabric](https://cseweb.ucsd.edu/~vahdat/papers/portland-sigcomm09.pdf)
- [A Scalable, Commodity Data Center Network Architecture (Al-Fares et al.)](https://cseweb.ucsd.edu/~vahdat/papers/sigcomm08.pdf)
- [RFC 7348: Virtual eXtensible Local Area Network (VXLAN)](https://datatracker.ietf.org/doc/html/rfc7348)
- [RFC 7938: Use of BGP for Routing in Large-Scale Data Centers](https://datatracker.ietf.org/doc/html/rfc7938)
- [Software-Defined Networking (Open Networking Foundation)](https://opennetworking.org/sdn-definition/)
