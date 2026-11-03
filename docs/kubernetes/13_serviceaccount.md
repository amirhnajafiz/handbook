# Service Accounts

## Quick Description (QD)

A service account provides an identity for processes that run in a Pod, and maps to a ServiceAccount object. When you authenticate to the API server, you identify yourself as a particular user.

Kubernetes recognizes the concept of a user (for humans). However, Kubernetes itself does not have a User API. Pods authenticate as a particular ServiceAccount (for example, `default`). There is always at least one ServiceAccount in each namespace.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

```sh
kubectl create serviceaccount build-robot
kubectl get serviceaccounts
kubectl create token build-robot
```

## Examples (e.g.,)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  serviceAccountName: build-robot
  automountServiceAccountToken: false
```

## References

- [Service Accounts](https://kubernetes.io/docs/concepts/security/service-accounts/)
- [K8S Service Account](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)
- [K8S Authorization](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)
