# Service

## Quick Description (QD)

In Kubernetes, a Service is a method for exposing a network application that is running as one or more Pods in your cluster.

The Service API, part of Kubernetes, is an abstraction to help you expose groups of Pods over a network. Each Service object defines a logical set of endpoints (usually these endpoints are Pods) along with a policy about how to make those Pods accessible.

### Service without selectors

Services most commonly abstract access to Kubernetes Pods thanks to the selector, but when used with a corresponding set of EndpointSlice objects and without a selector, the Service can abstract other kinds of backends, including ones that run outside the cluster.

### Service types

#### ClusterIP

Exposes the Service on a cluster-internal IP. Choosing this value makes the Service only reachable from within the cluster. This is the default that is used if you don't explicitly specify a type for a Service. You can expose the Service to the public internet using an Ingress or a Gateway.

#### NodePort

Exposes the Service on each Node's IP at a static port (the NodePort). To make the node port available, Kubernetes sets up a cluster IP address, the same as if you had requested a Service of type `ClusterIP`.

#### LoadBalancer

Exposes the Service externally using an external load balancer. Kubernetes does not directly offer a load balancing component; you must provide one, or you can integrate your Kubernetes cluster with a cloud provider.

#### ExternalName

Maps the Service to the contents of the `externalName` field (for example, to the hostname `api.foo.bar.example`). The mapping configures your cluster's DNS server to return a CNAME record with that external hostname value. No proxying of any kind is set up.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

Expose a Deployment as a Service and list the Service with its endpoints:

```sh
kubectl expose deployment <name> --port=80 --target-port=9376
kubectl get service,endpointslices
```

For Services without a selector see [Endpoints](25_endpoints.md), and for Services without a cluster IP see [Headless service](24_headless_service.md).

## Examples (e.g.,)

This Service sends traffic arriving on port 80 to port 9376 of the Pods labeled `app.kubernetes.io/name: MyApp`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

## References

- [K8S Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Connecting Applications with Services](https://kubernetes.io/docs/tutorials/services/connect-applications-service/)
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
