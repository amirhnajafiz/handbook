# Switching

## Quick Description (QD)

Switching refers to the process of forwarding data packets between devices within a network. It primarily operates at the Data Link Layer (Layer 2) and, in some cases, at the Network Layer (Layer 3) of the OSI model. Switching enables efficient communication within local area networks (LANs) and forms the backbone of modern Ethernet networks.

### Key Concepts

- **MAC Address:** A unique hardware address assigned to each network interface card (NIC), used for identification at the Data Link Layer.
- **Switch:** A Layer 2 device that forwards frames based on MAC addresses. Switches learn the MAC addresses of devices on each port and use this information to forward traffic only to the intended recipient (a modern switch is essentially a multi-port bridge).
- **Bridge:** An older Layer 2 device that connects and filters traffic between two or more network segments, reducing collisions by splitting a network into separate collision domains. A bridge still forwards broadcasts, so it does not split broadcast domains.
- **Hub:** A basic Layer 1 device that simply repeats incoming signals to all ports. Hubs do not filter or forward traffic intelligently and are largely obsolete.
- **ARP (Address Resolution Protocol):** A protocol used to map IP addresses (Layer 3) to MAC addresses (Layer 2) so that devices can communicate within a local network.

### Types of Switching

- **Circuit Switching:** Establishes a dedicated communication path between devices for the duration of the session (used in traditional telephone networks).
- **Packet Switching:** Data is broken into packets and each packet may take a different path to the destination (see [IP](07_ip.md)) (used in most computer networks, including the Internet).
- **Message Switching:** Entire messages are routed from source to destination, stored temporarily at intermediate devices (rarely used in modern networks).

### How Switches Work

1. **Learning:** The switch records the source MAC address and the port it arrived on in its MAC address table.
2. **Forwarding:** When a frame arrives, the switch checks the destination MAC address:
   - If known, it forwards the frame only to the correct port.
   - If unknown, it floods the frame to all ports except the source.
3. **Filtering:** Switches prevent unnecessary traffic by only sending frames to the intended recipient. Broadcast frames are still flooded to all ports in the VLAN.

### VLANs (Virtual LANs)

- Switches can segment a physical network into multiple logical networks (VLANs, IEEE 802.1Q), each being its own broadcast domain. Traffic between VLANs must go through a router (or a Layer 3 switch).

### Common Devices

- **Switch:** Layer 2, forwards frames based on MAC addresses.
- **Bridge:** Layer 2, connects network segments.
- **Hub:** Layer 1, repeats signals to all ports.
- **Router:** Layer 3, forwards packets based on IP addresses.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

- `arp -a` or `ip neigh`: View the ARP table (shows IP-to-MAC mappings).
- `ip link` or `ifconfig`: Show network interfaces and MAC addresses.
- `bridge fdb show`: Show the forwarding (MAC) table of a Linux bridge.
- `show mac address-table` (on Cisco switches): Display learned MAC addresses and associated ports.

## Examples (e.g.,)

_Nothing here yet._

## References

- [RFC 826: An Ethernet Address Resolution Protocol](https://datatracker.ietf.org/doc/html/rfc826)
- [Computer Networking: A Top-Down Approach (Kurose & Ross)](https://www.pearson.com/en-us/subject-catalog/p/computer-networking-a-top-down-approach/P200000003481/9780136681557)
