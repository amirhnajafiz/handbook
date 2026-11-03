# Network policies

## Quick Description (QD)

If you want to control traffic flow at the IP address or port level (OSI layer 3 or 4), then you might consider using Kubernetes NetworkPolicies for particular applications in your cluster.

NetworkPolicies are an application-centric construct that allows you to specify how a Pod is allowed to communicate with various network "entities" over the network. NetworkPolicies apply to a connection with a Pod on one or both ends, and are not relevant to other connections.

NetworkPolicies are enforced by the network plugin (CNI), so creating one has no effect if your plugin does not support them. Pods are non-isolated (all traffic allowed) until a policy selects them; once selected, only the traffic the policies allow is permitted.

The entities that a Pod can communicate with are identified through a combination of the following three identifiers:

- Other Pods that are allowed (exception: a Pod cannot block access to itself)
- Namespaces that are allowed
- IP blocks (exception: traffic to and from the node where a Pod is running is always allowed, regardless of the IP address of the Pod or the node)

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

This policy isolates Pods labeled `role=db` in the `default` namespace. It allows ingress on TCP 6379 from the given IP range (minus the excluded subnet), from Pods in namespaces labeled `project=myproject`, and from Pods labeled `role=frontend`; egress is only allowed to `10.0.0.0/24` on TCP 5978.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - ipBlock:
            cidr: 172.17.0.0/16
            except:
              - 172.17.1.0/24
        - namespaceSelector:
            matchLabels:
              project: myproject
        - podSelector:
            matchLabels:
              role: frontend
      ports:
        - protocol: TCP
          port: 6379
  egress:
    - to:
        - ipBlock:
            cidr: 10.0.0.0/24
      ports:
        - protocol: TCP
          port: 5978
```

## References

- [K8S network policy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
