# Headless service

## Quick Description (QD)

A headless Service is a Service that does not allocate a cluster IP address and does no load balancing or proxying. It is created by explicitly setting `spec.clusterIP` to `None` (with `spec.type` being `ClusterIP`). Instead, DNS exposes the IP addresses of the Pods behind the Service, so clients connect directly to the Pods.

Headless Services are assigned DNS A and/or AAAA records, with a name of the form `my-svc.my-namespace.svc.cluster-domain.example`. Unlike normal Services, this name resolves to the set of IPs of all of the Pods selected by the Service, and the client chooses which one to use. SRV records are also created for all the named ports of the Service's endpoints.

How DNS is configured depends on whether the Service has a selector:

- With a selector, the endpoint controller creates EndpointSlices, and DNS returns A/AAAA records pointing directly at the Pods.
- Without a selector, no EndpointSlices are created automatically, and DNS only returns A/AAAA records for the ready endpoints of EndpointSlices that you create yourself with the same name as the Service (see [Endpoints](25_endpoints.md)).

### Why stateful workloads need it

Stateful workloads often have to reach a specific Pod directly (for example, during database writes) or need Pod-to-Pod communication, without load balancing. A [StatefulSet](23_stateful_set.md) gives Pods fixed, ordered names (`$statefulsetname-$ordinal`, e.g., `mongo-0`, `mongo-1`, `mongo-2`) and, together with a headless Service named in `serviceName`, each Pod gets a stable DNS name such as `mongo-0.mongo.my-namespace.svc.cluster.local`.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

Check what DNS returns for a headless Service from inside the cluster:

```sh
kubectl run -it --rm dns-test --image=busybox:1.28 --restart=Never -- nslookup foo
```

## Examples (e.g.,)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: foo
spec:
  clusterIP: None
  selector:
    key1: val1
    key2: val2
  ports:
    - port: 8080
      protocol: TCP
  type: ClusterIP
```

## References

- [K8S Service: headless Services](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- [StatefulSet: stable network ID](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#stable-network-id)
