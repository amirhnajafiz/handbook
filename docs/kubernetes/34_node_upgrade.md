# Node Upgrade

## Quick Description (QD)

Upgrading or maintaining nodes can cause problems when replicas are running on different nodes. If a node goes down or gets terminated, pods that are managed by a controller are replaced on other nodes. By default, pods tolerate an unreachable or not-ready node for 300 seconds (5 minutes) before they are evicted. For node maintenance, check the replicas and pods running on the node first.

The best solution is to drain the node. Draining cordons the node (so it is unschedulable) and evicts its pods, and the controllers recreate them on other nodes. Pods that are not managed by a controller are not recreated. Once maintenance is done, uncordon the node to make it schedulable again. Draining respects PodDisruptionBudgets.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

Drain a node:

```sh
kubectl drain node-1 --ignore-daemonsets --delete-emptydir-data
```

`--ignore-daemonsets` is needed because DaemonSet pods cannot be evicted, and `--delete-emptydir-data` allows evicting pods that use `emptyDir` volumes (their data is lost).

Bring a drained node back:

```sh
kubectl uncordon node-1
```

Cordoning a node does not move its existing pods, but the node becomes unschedulable:

```sh
kubectl cordon node-1
```

## Examples (e.g.,)

For a kubeadm cluster, upgrade nodes one at a time: drain, upgrade (see [Kubeadm](39_kubeadm.md)), then uncordon.

## References

- [Safely Drain a Node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)
- [kubectl drain](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_drain/)
- [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/)
- [Upgrading kubeadm clusters](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)
