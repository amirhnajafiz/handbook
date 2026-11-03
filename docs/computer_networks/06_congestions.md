# Congestion Control

## Quick Description (QD)

Congestion control refers to techniques and mechanisms used to prevent network congestion and to recover from it when it occurs. Effective congestion control ensures efficient use of network resources and maintains good performance for all users.

### Why Congestion Control Is Needed

Without congestion control, excessive data transmission can overwhelm network devices, leading to packet loss, high latency, and reduced throughput. Congestion control helps maintain network stability and fairness.

### Common Congestion Control Algorithms

#### TCP Congestion Control

[TCP](04_tcp.md) uses several algorithms to detect and respond to congestion (RFC 5681):

- **Slow Start:** Begins transmission with a small congestion window and increases it exponentially until the first loss or threshold is reached.
- **Congestion Avoidance:** Increases the congestion window linearly to probe for available bandwidth.
- **Fast Retransmit and Fast Recovery:** Three duplicate ACKs trigger a retransmission without waiting for a timeout, and the congestion window is halved instead of reset, so the sender does not return to slow start.

#### Active Queue Management (AQM)

Routers and switches can use AQM techniques to manage congestion:

- **Random Early Detection (RED):** Proactively drops packets, with a probability that grows with the average queue length, before buffers are full to signal senders to slow down.
- **Explicit Congestion Notification (ECN):** Routers mark packets (instead of dropping them) to indicate congestion, and the receiver echoes the mark back to the sender (RFC 3168).

#### Traffic Shaping and Policing

- **Leaky Bucket and Token Bucket:** Limit the rate (and burstiness) at which packets enter the network, smoothing out bursts.

#### Quality of Service (QoS)

- **Prioritization:** Assigns higher priority to critical traffic, ensuring important data is delivered even during congestion.

### Modern Congestion Control Algorithms

- **CUBIC:** Default in Linux, optimized for high-speed, high-latency networks. The window grows as a cubic function of time since the last loss (RFC 9438).
- **BBR (Bottleneck Bandwidth and Round-trip propagation time):** Not loss-based; it models the bottleneck bandwidth and minimum RTT to maximize throughput and minimize queueing.
- **DCTCP:** ECN-based variant for datacenters, see [Datacenters](09_datacenters.md).

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

On Linux, check and change the congestion control algorithm:

```bash
sysctl net.ipv4.tcp_congestion_control
sysctl net.ipv4.tcp_available_congestion_control
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
```

## Examples (e.g.,)

_Nothing here yet._

## References

- [TCP Congestion Control (RFC 5681)](https://datatracker.ietf.org/doc/html/rfc5681)
- [Active Queue Management (RFC 7567)](https://datatracker.ietf.org/doc/html/rfc7567)
- [Explicit Congestion Notification (RFC 3168)](https://datatracker.ietf.org/doc/html/rfc3168)
- [CUBIC for Fast and Long-Distance Networks (RFC 9438)](https://datatracker.ietf.org/doc/html/rfc9438)
- [BBR Congestion Control (IETF draft)](https://datatracker.ietf.org/doc/html/draft-cardwell-iccrg-bbr-congestion-control)
