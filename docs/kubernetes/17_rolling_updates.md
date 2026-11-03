# Rolling updates

## Quick Description (QD)

Rolling updates allow a Deployment's update to take place with zero downtime by incrementally replacing Pod instances with new ones. The new Pods will be scheduled on Nodes with available resources.

Rolling updates allow the following actions:

- Promote an application from one environment to another (via container image updates)
- Roll back to previous versions
- Continuous integration and continuous delivery of applications with zero downtime

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

Update the image of a Deployment (this triggers a rolling update):

```sh
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=<new-image>
```

Watch the rollout, check its history, and roll back:

```sh
kubectl rollout status deployments/kubernetes-bootcamp
kubectl rollout history deployments/kubernetes-bootcamp
kubectl rollout undo deployments/kubernetes-bootcamp
```

## Examples (e.g.,)

The speed of a rolling update is controlled by the Deployment's strategy. Here at most one extra Pod is created and no Pod is allowed to be unavailable:

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

The rollout only moves on when new Pods become ready, so define a [readiness probe](16_probes.md) for zero downtime.

## References

- [Performing a Rolling Update](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)
- [Deployments: rolling update strategy](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment)
