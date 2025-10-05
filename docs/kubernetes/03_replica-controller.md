# Replica Controller

A ```ReplicationController``` ensures that a specified number of pod replicas are running at any one time.

In other words, a ```ReplicationController``` makes sure that a pod or a homogeneous set of pods is always up and available.

## e.g.,

```yml
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

### Usage patterns

- Rescheduling
- Scaling
- Rolling updates
- Multiple release tracks
- Using ReplicationControllers with Services

### Alternatives

- ReplicaSet
- Deployment
- Bare Pods
- Job
- DaemonSet

## Commands

```shell
kubectl create -f rc-definition.yml
```

```shell
kubectl get replicationcontroller/rc
```

## References

- [K8S RC](https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/)
