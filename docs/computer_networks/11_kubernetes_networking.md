# Kubernetes Networking

## Quick Description (QD)

Kubernetes (sometimes referred to as K8s) is an open-source platform, originally designed by Google, for automating the deployment, scaling, and operation of containerized applications across a cluster of machines.

Kubernetes networking allows Kubernetes components to communicate with each other and with other applications. It is built on a flat network model: every Pod gets its own IP address, and Pods can reach all other Pods on all nodes directly, without NAT and without mapping container ports to host ports. This lets machines be shared between applications without dynamically allocating ports. Kubernetes itself only defines this model; it is implemented by a network plugin (see CNI below).

### How Networking Works in Kubernetes

There are four networking problems: container-to-container communication, Pod-to-Pod communication, Pod-to-Service communication, and external-to-Service communication.

- **Container-to-container:** Containers in the same Pod share one network namespace, so they share the Pod's IP address and port space, and talk to each other over `localhost`. Two containers in one Pod therefore cannot listen on the same port.
- **Pod-to-Pod:** Containers in different Pods are in different network namespaces, so `localhost` does not reach them. A Pod reaches another Pod using its Pod IP (usually through a Service instead, since Pod IPs change when Pods are recreated). Pod traffic is not NAT-ed, whether the Pods are on the same node or not. What the Pods are allowed to talk to is restricted by NetworkPolicies, which are enforced by the network plugin (if it supports them).
- **Pod-to-Service:** A Service gives a set of Pods a stable virtual IP and DNS name, and `kube-proxy` (or the network plugin) load-balances connections to the Pods behind it.
- **External-to-Service:** See the Service types below.

For the container-level building blocks (network namespaces, veth pairs, bridges, overlays), see [Container Networking](10_container_networking.md).

One of the challenges of Kubernetes networking is how internal (east-west) traffic and external (north-south) traffic interact. There are a few different ways of getting external traffic into a Kubernetes cluster:

- **ClusterIP:** The default Service type, reachable only from inside the cluster. It can be reached from outside for debugging or internal dashboards through a proxy (e.g., `kubectl proxy` or `kubectl port-forward`).
- **NodePort:** Opens the same port on every node, and traffic to that port is forwarded to the Service. Useful for demos or as a building block for load balancers.
- **LoadBalancer:** The standard way to expose a Service to the internet on a cloud provider. The provider provisions an external load balancer that forwards traffic to the Service, and each Service gets its own load balancer IP.
- **Ingress:** Not a Service type, but an API object (served by an ingress controller) that routes HTTP(S) traffic to Services based on host and path. It is useful if you want to use the same IP address to expose multiple services. The newer Gateway API is its successor.

### CNI

The Container Network Interface (CNI) is a specification for plugins that configure a container's network interface when it is created and clean it up when it is deleted. The container runtime calls the CNI plugin to set up the Pod's network namespace, assign an IP address, and wire it to the cluster network. Kubernetes does not ship a default CNI plugin: you need to install one (older versions had a basic built-in plugin called kubenet, which was removed in Kubernetes 1.24). Plugins differ in features such as NetworkPolicy support, encryption, and routing modes (overlay vs. direct routing).

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

```bash
kubectl get pods -o wide                      # Pod IPs and the nodes they run on
kubectl get svc,endpoints                     # Service ClusterIPs and the Pod IPs behind them
kubectl exec <pod> -- ip addr                 # the Pod's network namespace
kubectl get networkpolicy -A                  # NetworkPolicies in the cluster
```

## Examples (e.g.,)

Common CNI plugins:

- **Flannel:** Simple overlay network (VXLAN by default); no NetworkPolicy support.
- **Calico:** Routed (BGP) or overlay networking with NetworkPolicy enforcement.
- **Cilium:** eBPF-based networking, policy, and observability (see [eBPF](../tracing/01_ebpf.md)).
- **Weave Net:** Overlay network with NetworkPolicy support (the project is no longer maintained).

## References

- [Cluster Networking (Kubernetes docs)](https://kubernetes.io/docs/concepts/cluster-administration/networking/)
- [Services, Load Balancing, and Networking (Kubernetes docs)](https://kubernetes.io/docs/concepts/services-networking/)
- [Service (Kubernetes docs)](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Ingress (Kubernetes docs)](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Network Policies (Kubernetes docs)](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Network Plugins (Kubernetes docs)](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
- [Pods (Kubernetes docs)](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Container Network Interface (CNI) specification](https://github.com/containernetworking/cni/blob/main/SPEC.md)
