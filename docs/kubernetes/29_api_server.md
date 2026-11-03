# Kube API Server

## Quick Description (QD)

The **Kube API Server** is the central management component of a Kubernetes cluster. All communication, whether from users, automation, or internal cluster components, passes through the API server.

### Responsibilities

- Serves as the front end for the Kubernetes control plane.
- Handles all REST operations for creating, reading, updating, and deleting (CRUD) Kubernetes resources.
- Authenticates and authorizes API requests.
- Validates and processes resource definitions.
- Persists cluster state to etcd.
- Exposes a watch mechanism, so components such as the scheduler, controllers, and kubelets are notified of changes in cluster state (the API server is the only component that talks to [etcd](28_etcd.md) directly).

### How It Works

1. **Receives requests:** All `kubectl` commands and API calls are sent to the API server.
2. **Authentication and authorization:** Verifies the identity and permissions of the requester.
3. **Admission and validation:** Runs mutating and validating admission controllers, then checks the request against the Kubernetes API schema.
4. **Persistence:** Updates or retrieves data from etcd, the cluster's backing store.
5. **Notification:** Streams change events to clients that watch resources (e.g., scheduler, controllers, kubelets).

### Key Features

- RESTful API interface over HTTPS (JSON, with Protobuf also supported).
- Extensible via Custom Resource Definitions (CRDs) and API aggregation.
- Supports admission controllers for policy enforcement.
- Secure communication via TLS.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

Check the health of the API server:

```shell
kubectl get --raw='/readyz?verbose'
kubectl get --raw='/livez?verbose'
```

List the resource types served by the API server:

```shell
kubectl api-resources
kubectl api-versions
```

See the HTTP requests `kubectl` sends (higher verbosity prints more detail):

```shell
kubectl get pods -v=8
```

## Examples (e.g.,)

```shell
kubectl get pods
```

This command sends a request to the API server, which authenticates the user, retrieves the list of pods from etcd, and returns the result.

## References

- [Kubernetes Components: kube-apiserver](https://kubernetes.io/docs/concepts/overview/components/#kube-apiserver)
- [kube-apiserver Reference](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/)
- [Controlling Access to the Kubernetes API](https://kubernetes.io/docs/concepts/security/controlling-access/)
- [API Access Control](https://kubernetes.io/docs/reference/access-authn-authz/)
