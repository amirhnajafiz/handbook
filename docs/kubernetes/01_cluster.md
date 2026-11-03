# Cluster

## Quick Description (QD)

Kubernetes can be installed in various ways. Kubernetes runs your workload by placing containers into Pods to run on Nodes.

A node may be a virtual or physical machine, depending on the cluster. Each node is managed by the control plane and contains the services necessary to run Pods. The components on a node include the kubelet, a container runtime, and the kube-proxy.

## Installation

To run a local Kubernetes cluster on your system, you can use the following tools. See [Install Kind](02_install_kind.md) for a step-by-step kind setup.

### minikube

`minikube` is local Kubernetes, focusing on making it easy to learn and develop for Kubernetes.

### kind

`kind` is a tool for running local Kubernetes clusters using Docker container nodes. `kind` was primarily designed for testing Kubernetes itself, but may be used for local development or CI.

### k3s

`k3s` is a lightweight, certified Kubernetes distribution designed for production workloads in unattended, resource-constrained, remote locations or inside IoT appliances.

## Useful Tips/Commands (UToC)

### Context

Kubernetes cluster information is located in the `~/.kube/config` file. A Kubernetes context is a group of access parameters that define which cluster you are interacting with, which user you are using, and which namespace you are working in.

Change the context:

```sh
kubectl config use-context my-cluster
```

View the configs:

```sh
kubectl config view
```

## Examples (e.g.,)

The `~/.kube/config` file looks like this:

```yaml
apiVersion: v1

clusters:
- cluster:
    server: https://<api-server-address>:6443
  name: my-cluster
contexts:
- context:
    cluster: my-cluster
    namespace: default
    user: my-user
  name: my-cluster

current-context: my-cluster

kind: Config
preferences: {}
users:
- name: my-user
  user:
    token: <redacted-token>
```

## References

- [minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kind](https://kind.sigs.k8s.io/)
- [k3s](https://k3s.io/)
- [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/)
- [K8S configure access](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)
