# Endpoints and EndpointSlices

## Quick Description (QD)

In the Kubernetes API, an Endpoints object (the resource kind is plural) defines a list of network endpoints, typically referenced by a Service to define which Pods the traffic can be sent to. The EndpointSlice API is the recommended replacement for Endpoints, which has been deprecated since Kubernetes v1.33.

The Kubernetes EndpointSlice API provides a way to track network endpoints within a Kubernetes cluster. EndpointSlices offer a more scalable and extensible alternative to Endpoints. An EndpointSlice contains references to a set of network endpoints. The control plane automatically creates EndpointSlices for any Kubernetes Service that has a selector specified. These EndpointSlices include references to all the Pods that match the Service selector.

EndpointSlices group network endpoints together by unique combinations of protocol, port number, and Service name. The name of an EndpointSlice object must be a valid DNS subdomain name.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

```sh
kubectl get endpointslices
kubectl get endpointslices -l kubernetes.io/service-name=example -o yaml
```

- Each EndpointSlice holds at most 100 endpoints by default; larger Services are split across several slices.
- For a Service without a selector, you create the EndpointSlice yourself and link it with the `kubernetes.io/service-name` label (see [Service](19_service.md)).
- Only endpoints whose `ready` condition is true receive traffic; readiness comes from the Pod's [readiness probe](16_probes.md).

## Examples (e.g.,)

An EndpointSlice belonging to the Service `example` (through the `kubernetes.io/service-name` label), as you would write one for a Service without a selector:

```yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: example-abc
  labels:
    kubernetes.io/service-name: example
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 80
endpoints:
  - addresses:
      - "10.1.2.3"
    conditions:
      ready: true
    hostname: pod-1
    nodeName: node-1
    zone: us-west2-a
```

## References

- [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/)
- [Endpoints API reference](https://kubernetes.io/docs/reference/kubernetes-api/service-resources/endpoints-v1/)
- [K8S Service](https://kubernetes.io/docs/concepts/services-networking/service/)
