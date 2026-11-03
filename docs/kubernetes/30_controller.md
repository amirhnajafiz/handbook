# Kube Controller Manager

## Quick Description (QD)

The **Kube Controller Manager** runs controller processes that regulate the state of the Kubernetes cluster. A controller is a control loop that watches the state of the cluster through the API server and makes or requests changes as needed to move the current state toward the desired state.

Controllers are responsible for responding to cluster events, ensuring resources match their specifications, and handling failures or changes automatically. All core controllers are packaged and run together as a single process: the Kube Controller Manager.

### Responsibilities

- Monitors the cluster state via the API server.
- Ensures the desired state of resources matches the actual state.
- Handles failures, scaling, and replication.
- Automates routine tasks (e.g., creating pods, managing endpoints).

### Common Controllers

- **Node Controller:** Monitors node health and responds when nodes go down.
- **ReplicaSet Controller:** Ensures the specified number of pod replicas are running (the [ReplicaSet](05_replica_set.md) and [Replication Controller](04_replica_controller.md) pages cover this).
- **Deployment Controller:** Manages deployments and rolling updates.
- **Job and CronJob Controllers:** Run pods to completion for one-off and scheduled tasks.
- **EndpointSlice Controller:** Populates EndpointSlice objects for services (see [Endpoints](25_endpoints.md)).
- **Namespace Controller:** Deletes the objects inside a namespace when it is deleted.
- **ServiceAccount Controller:** Creates default service accounts for new namespaces.

Controllers that depend on a cloud provider (such as the service load balancer controller) run in the separate cloud-controller-manager.

### How It Works

Each controller watches the cluster state through the API server. When it detects a difference between the desired and actual state, it takes action to reconcile them. For example, if a node stops reporting, the Node Controller marks it as `Unknown`/`NotReady` and taints it, and pods that do not tolerate the taint are evicted so that their controllers create replacements on other nodes. The Controller Manager does not place pods; that is the job of the [Scheduler](31_scheduler.md).

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

On a kubeadm cluster the controller manager runs as a static pod in `kube-system`:

```shell
kubectl -n kube-system get pods -l component=kube-controller-manager
kubectl -n kube-system logs -l component=kube-controller-manager
```

Controller manager runs leader election, so only one replica is active. Check the current leader:

```shell
kubectl -n kube-system get lease kube-controller-manager
```

## Examples (e.g.,)

_Nothing here yet._

## References

- [Controllers](https://kubernetes.io/docs/concepts/architecture/controller/)
- [Kubernetes Components: kube-controller-manager](https://kubernetes.io/docs/concepts/overview/components/#kube-controller-manager)
- [kube-controller-manager Reference](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/)
- [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/)
