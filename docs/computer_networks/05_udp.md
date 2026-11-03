# UDP

## Quick Description (QD)

The User Datagram Protocol (UDP) is a core protocol of the Internet Protocol Suite. Unlike [TCP](04_tcp.md), UDP provides a connectionless, lightweight method for sending datagrams without guaranteeing delivery, order, or error checking.

### Key Features

- **Connectionless:** No connection is established before data transfer.
- **Unreliable Delivery:** Packets may be lost, duplicated, or arrive out of order.
- **No Flow or Congestion Control:** UDP does not manage data rate or retransmissions, so applications that need this must implement it themselves (as QUIC does, see [HTTP](03_http.md)).
- **Low Overhead:** Minimal protocol mechanism and a fixed 8-byte header, making it fast and efficient.
- **Supports Broadcast and Multicast:** Since there is no connection, it can send to multiple recipients (TCP is strictly point-to-point).

### UDP Header Fields

- **Source Port / Destination Port:** Identify sending and receiving applications.
- **Length:** Length of the UDP header and data.
- **Checksum:** Error-checking for the header and data (optional in IPv4, required in IPv6).

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

Use cases:

- Streaming media (audio/video)
- Online gaming
- DNS queries (see [DNS](01_dns.md); large responses fall back to TCP)
- Voice over IP (VoIP)
- Simple query-response protocols

## References

- [RFC 8085: UDP Usage Guidelines](https://datatracker.ietf.org/doc/html/rfc8085)
- [UDP in RFC 768](https://datatracker.ietf.org/doc/html/rfc768)
- [Computer Networking: A Top-Down Approach (Kurose & Ross)](https://www.pearson.com/en-us/subject-catalog/p/computer-networking-a-top-down-approach/P200000003481/9780136681557)
