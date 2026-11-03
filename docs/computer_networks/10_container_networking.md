# Container Networking

## Quick Description (QD)

Containers are a form of operating system virtualization: they share the host kernel, unlike VMs, which virtualize hardware and each run their own kernel. Containers are usually short-lived, so a host runs many more of them than VMs, which requires many more addresses.

To create isolation, a container relies on two Linux kernel features: namespaces and cgroups. For networking, the important one is the **network namespace**: each container gets its own interfaces, IP addresses, routing table, and firewall rules, separate from the host. Control groups (cgroups) are then used to limit resources like CPU and memory. A container network is therefore a way of connecting these network namespaces to each other and to the outside, usually with virtual ethernet (`veth`) pairs, bridges, and NAT (see [Switching](08_switching.md) and [IP](07_ip.md)).

For how Pods and Services build on this, see [Kubernetes Networking](11_kubernetes_networking.md).

### Types

These are the common container network modes (the names follow Docker). They differ in how containers get IP addresses and whether NAT is needed to reach the outside.

- **None:** The container receives a network stack; however, it lacks an external connection. This mode is useful for testing containers, staging a container for a later network connection, and assigning to containers not requiring external communications.
- **Bridge:** Containers are attached to a virtual bridge on the host and get private IPs, so they can talk to each other on the same host. Outbound traffic is NAT-ed, and inbound traffic from outside requires publishing ports (`-p`). Bridge is the default network for Docker containers.
- **Host:** This configuration allows a created container to share the host's network namespace, granting the container access to all the host's network interfaces. The least complex of the external networking configurations, this type is prone to port conflicts due to the shared use of the networking interfaces.
- **Underlay (macvlan/ipvlan):** Containers get addresses directly on the host's physical network, which removes the need for port mapping and NAT and makes them more efficient than bridges.
- **Overlay:** Overlays encapsulate container traffic in tunnels (e.g., VXLAN) between hosts, allowing containers to act like they are on the same network when they are hosted on different hosts.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

```bash
docker network ls                      # list networks (bridge, host, none by default)
docker network inspect bridge          # subnet, gateway, attached containers
docker run --rm --network none alpine ip addr      # only a loopback interface
docker run --rm --network host alpine ip addr      # same interfaces as the host
ip link show type veth                 # host side of the container veth pairs
```

## Examples (e.g.,)

_Nothing here yet._

## References

- [Docker: Networking overview](https://docs.docker.com/engine/network/)
- [Docker: Network drivers](https://docs.docker.com/engine/network/drivers/)
- [Docker: Macvlan network driver](https://docs.docker.com/engine/network/drivers/macvlan/)
- [network_namespaces(7), Linux manual page](https://man7.org/linux/man-pages/man7/network_namespaces.7.html)
- [Container Network Interface (CNI) specification](https://github.com/containernetworking/cni/blob/main/SPEC.md)
