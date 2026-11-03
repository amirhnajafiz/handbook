# Ingress

## Quick Description (QD)

Ingress exposes HTTP and HTTPS routes from outside the cluster to Services within the cluster. Traffic routing is controlled by rules defined on the Ingress resource.

<img src="https://kubernetes.io/docs/images/ingress.svg" width="500" />

An Ingress may be configured to give Services externally reachable URLs, load balance traffic, terminate SSL/TLS, and offer name-based virtual hosting. An Ingress controller is responsible for fulfilling the Ingress, usually with a load balancer, though it may also configure your edge router or additional frontends to help handle the traffic.

### Ingress controller

In order for the Ingress resource to work, the cluster must have an Ingress controller running. Unlike other types of controllers, which run as part of the `kube-controller-manager` binary, Ingress controllers are not started automatically with a cluster. The `ingressClassName` field of an Ingress selects which controller (through an `IngressClass`) handles it.

Note that the Ingress API is frozen: the Kubernetes project recommends the newer Gateway API for new work.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

```sh
kubectl get ingressclass
kubectl get ingress
kubectl describe ingress minimal-ingress
```

## Examples (e.g.,)

Routes requests for `/testpath` to port 80 of the Service `test`. The annotation is specific to the NGINX Ingress controller:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx-example
  rules:
  - http:
      paths:
      - path: /testpath
        pathType: Prefix
        backend:
          service:
            name: test
            port:
              number: 80
```

## References

- [K8S Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/)
- [Ingress controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
