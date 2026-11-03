# Kube Proxy

## Quick Description (QD)

**Kube Proxy** is a network component that runs on every node in a Kubernetes cluster. It maintains network rules on nodes, enabling communication to your services and pods from inside or outside the cluster.

Every pod can access another pod by using an internal virtual network. Traffic is forwarded to backend applications based on service definitions. A Kubernetes Service is an abstraction that defines a logical set of pods and a policy by which to access them.

Kube Proxy watches the API server for new or updated services and EndpointSlices (see [Endpoints](25_endpoints.md)), and creates or updates rules to direct traffic accordingly. It uses operating system packet filtering (like `iptables`, `ipvs`, or `nftables`) to handle traffic routing.

### Responsibilities

- Watches for new or updated services and EndpointSlices via the API server.
- Maintains network rules on each node to route traffic to the correct backend pods.
- Supports different proxy modes for handling traffic (iptables, ipvs, nftables).
- Enables load balancing for service traffic.

### How It Works

1. **Service creation:** When a Service is created, kube-proxy sets up rules to capture traffic to the Service's cluster IP.
2. **Endpoint updates:** As pods are added or removed, kube-proxy updates the rules to ensure traffic is routed only to ready pods.
3. **Traffic forwarding:** Incoming traffic to a Service is load balanced and forwarded to one of the backend pods.

### Key Features

- Supports TCP, UDP, and SCTP protocols.
- Spreads connections across backends (the iptables mode picks a backend at random; ipvs supports several scheduling algorithms).
- Handles `ClusterIP`, `NodePort`, and (together with the cloud provider's load balancer) `LoadBalancer` traffic.
- Automatically updates rules as services and endpoints change.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### Proxy modes

Kube Proxy supports several modes for handling network traffic:

- **iptables (default on Linux):** Uses Linux `iptables` rules to direct traffic to backend pods. Efficient and widely used.
- **ipvs:** Uses Linux IP Virtual Server (IPVS) for load balancing. Scales better than iptables in clusters with a very large number of services.
- **nftables:** Uses `nftables` rules, the successor to iptables in the kernel.

The old `userspace` mode has been removed. The upstream docs recommend setting the mode explicitly, because the default may change in a future release.

You can specify the proxy mode with the `--proxy-mode` flag (or the `mode` field in the config file):

```shell
kube-proxy --proxy-mode=ipvs
```

## Examples (e.g.,)

### Example Kube Proxy configuration

A typical `kube-proxy` configuration file (`kube-proxy-config.yaml`):

```yaml
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "ipvs"
clusterCIDR: "10.244.0.0/16"
metricsBindAddress: "0.0.0.0:10249"
hostnameOverride: ""
clientConnection:
  kubeconfig: "/var/lib/kube-proxy/kubeconfig"
```

To start kube-proxy with a configuration file:

```shell
kube-proxy --config=/etc/kubernetes/kube-proxy-config.yaml
```

## References

- [Virtual IPs and Service Proxies](https://kubernetes.io/docs/reference/networking/virtual-ips/)
- [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- [kube-proxy Reference](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/)
- [kube-proxy Configuration (v1alpha1)](https://kubernetes.io/docs/reference/config-api/kube-proxy-config.v1alpha1/)
