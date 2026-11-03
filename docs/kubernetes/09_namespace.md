# Namespaces

## Quick Description (QD)

In Kubernetes, `namespaces` provide a mechanism for isolating groups of resources within a single cluster. Names of resources need to be unique within a namespace, but not across namespaces.

Namespace-based scoping is applicable only for namespaced objects (for example, Deployments and Services) and not for cluster-wide objects (for example, StorageClass, Nodes, and PersistentVolumes).

The initial namespaces are:

- default
- kube-node-lease
- kube-system
- kube-public

### DNS

Kubernetes creates DNS records for Services and Pods. You can contact Services with consistent DNS names instead of IP addresses.

Services defined in the cluster are assigned DNS names. By default, a client Pod's DNS search list includes the Pod's own namespace and the cluster's default domain.

DNS queries may be expanded using the Pod's `/etc/resolv.conf`. Kubelet configures this file for each Pod. For example, a query for just `data` may be expanded to `data.test.svc.cluster.local`. The values of the search option are used to expand queries.

### Resource quota

When several users or teams share a cluster with a fixed number of nodes, there is a concern that one team could use more than its fair share of resources. `Resource quotas` are a tool for administrators to address this concern.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### Namespace commands

```sh
kubectl run nginx --image=nginx --namespace=<insert-namespace-name-here>
kubectl get pods --namespace=<insert-namespace-name-here>
```

```sh
kubectl config set-context --current --namespace=<insert-namespace-name-here>
kubectl config view --minify | grep namespace:
```

```sh
kubectl create -f namespace-dev.yml
```

```sh
kubectl create namespace dev
```

```sh
kubectl get pods --all-namespaces   # or -A
```

```sh
kubectl get pods --namespace=kube-system
```

```sh
kubectl get pods -n=dev
```

### DNS commands

A Service is reachable at `<service-name>.<namespace>.svc.<cluster-domain>`:

```text
db-service.dev.svc.cluster.local
```

### Resource quota commands

```sh
kubectl create -f compute-quota.yml
```

```sh
kubectl get quota --namespace=myspace
```

## Examples (e.g.,)

### Pod in a namespace

```yaml
apiVersion: v1
kind: Pod

metadata:
    name: myapp-pod
    namespace: dev
# ... rest of the Pod spec
```

### Resource quota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
    name: pods-medium
spec:
    hard:
      cpu: "10"
      memory: 20Gi
      pods: "10"
    scopeSelector:
      matchExpressions:
      - operator : In
        scopeName: PriorityClass
        values: ["medium"]
```

## References

- [Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
- [K8S DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
- [Configure Memory and CPU Quotas for a Namespace](https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)
