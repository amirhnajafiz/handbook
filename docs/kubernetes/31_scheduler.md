# Kube Scheduler

## Quick Description (QD)

The **Kube Scheduler** is a core component of the Kubernetes control plane responsible for assigning newly created pods to nodes in the cluster. It ensures that workloads are placed on nodes that meet their resource and scheduling requirements.

### Responsibilities

- Watches for unscheduled pods via the API server.
- Selects an appropriate node for each pod based on resource requirements, constraints, and policies.
- Considers factors such as CPU, memory, affinity/anti-affinity rules, taints and tolerations, and custom scheduling policies.
- Spreads load across the cluster according to its scoring plugins.

### How It Works

1. **Pod creation:** When a new pod is created without a node assignment, it is detected by the scheduler.
2. **Filtering:** The scheduler filters out nodes that do not meet the pod's requirements (e.g., insufficient resources, untolerated taints, node selectors).
3. **Scoring:** Remaining nodes are scored based on criteria like resource availability, affinity rules, and custom priorities.
4. **Binding:** The scheduler selects the highest-scoring node and tells the API server to bind the pod to it (by setting `spec.nodeName`). The [kubelet](32_kubelet.md) on that node then starts the pod.

### Custom Schedulers

Kubernetes supports running multiple schedulers. A pod picks its scheduler with `spec.schedulerName` (the default is `default-scheduler`).

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

Find out why a pod is `Pending` (the events show messages such as `FailedScheduling`):

```shell
kubectl describe pod <pod-name>
```

See which node each pod was scheduled on:

```shell
kubectl get pods -o wide
```

On a kubeadm cluster the scheduler runs as a static pod:

```shell
kubectl -n kube-system get pods -l component=kube-scheduler
```

## Examples (e.g.,)

### Example Scheduling Criteria

- **Resource requests:** Ensures the node has enough unreserved CPU and memory (limits are not used for placement).
- **Node selectors and affinity:** Schedules pods based on labels or affinity/anti-affinity rules.
- **Taints and tolerations:** Prevents pods from being scheduled on unsuitable nodes.
- **Pod topology spread constraints:** Distributes pods for high availability.

## References

- [Kubernetes Scheduler](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/)
- [Scheduling, Preemption and Eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/)
- [kube-scheduler Reference](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/)
