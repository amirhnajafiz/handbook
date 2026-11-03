# ReplicaSet

## Quick Description (QD)

A `ReplicaSet`'s purpose is to maintain a stable set of replica Pods running at any given time. As such, it is often used to guarantee the availability of a specified number of identical Pods.

A `Deployment` is a higher-level concept that manages ReplicaSets and provides declarative updates to Pods along with a lot of other useful features.

A `ReplicaSet` is not limited to owning Pods specified by its template. It can acquire other Pods in the manner specified in their metadata.

### HPA

A `ReplicaSet` can also be a target for `Horizontal Pod Autoscalers` (HPA). That is, a `ReplicaSet` can be auto-scaled by an `HPA`.

### How HPA scales a ReplicaSet

Based on the collected resource usage, the HPA calculates the desired number of replicas, then updates the replica count of its target (here, the ReplicaSet). The ReplicaSet controller then creates or deletes Pods to match it. See [Scale](07_scale.md) for the algorithm.

### HPA vs VPA

The HPA changes the number of Pods to handle the workload and spikes in traffic. The VPA (Vertical Pod Autoscaler, a separate add-on), on the other hand, adjusts the CPU and memory requests and limits of the pods based on their actual resource usage.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### ReplicaSet commands

```sh
kubectl create -f replicaset-definition.yml
```

```sh
kubectl get rs
```

### HPA commands

```sh
kubectl autoscale rs frontend --max=10 --min=3 --cpu-percent=50
```

## Examples (e.g.,)

### ReplicaSet

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
  labels:
    app: guestbook
    tier: frontend
spec:
  # modify replicas according to your case
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: php-redis
        image: gcr.io/google_samples/gb-frontend:v3
```

### HPA

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: frontend-scaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: ReplicaSet
    name: frontend
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 50
```

## References

- [K8S replicaset](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
