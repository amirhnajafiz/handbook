# Pods

## Quick Description (QD)

`Pods` are the smallest deployable units of computing that you can create and manage in Kubernetes.

A Pod (as in a pod of whales or pea pod) is a group of one or more containers, with shared storage and network resources, and a specification for how to run the containers.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

Get all pods:

```sh
kubectl get pods
```

Deploy a pod:

```sh
kubectl apply -f pod.yaml
```

Show logs of a pod:

```sh
kubectl logs nginx
```

Describe a pod:

```sh
kubectl describe pod nginx
```

## Examples (e.g.,)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
```

## References

- [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
