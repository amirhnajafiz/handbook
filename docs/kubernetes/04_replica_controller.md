# Replica Controller

## Quick Description (QD)

A `ReplicationController` ensures that a specified number of pod replicas are running at any one time. In other words, a `ReplicationController` makes sure that a pod or a homogeneous set of pods is always up and available.

### Usage patterns

- Rescheduling
- Scaling
- Rolling updates
- Multiple release tracks
- Using ReplicationControllers with Services

### Alternatives

A [Deployment](08_deployment.md) that configures a [ReplicaSet](05_replica_set.md) is now the recommended way to set up replication.

- ReplicaSet
- Deployment
- Bare Pods
- Job
- DaemonSet

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

```sh
kubectl create -f rc-definition.yml
```

```sh
kubectl get replicationcontroller/nginx
kubectl get rc
```

## Examples (e.g.,)

```yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    app: nginx
  template:
    metadata:
      name: nginx
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
```

## References

- [K8S RC](https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/)
