# Service Mesh

## Quick Description (QD)

The use of Kubernetes to run workloads has become the standard in most organizations. While this has many advantages, it also introduces some challenges, especially around managing communication between services.

Kubernetes abstracts away much of the underlying network, making it difficult to troubleshoot problems and ensure that services are communicating reliably and securely.

**Service mesh** technologies offer a robust and effective solution to these challenges. By placing a proxy next to each workload (the classic sidecar approach; Istio also offers a sidecar-less ambient mode), a service mesh provides a centralized way of managing service-to-service communication. This approach brings a wide range of features such as:

- **Traffic management** (load balancing, traffic splitting, retries, timeouts)
- **Observability** (metrics, tracing, logging)
- **Security** (mutual TLS, policy enforcement, access control)
- **Resilience** (circuit breaking, fault injection)
- **Service discovery** and more

Two of the leading service meshes for Kubernetes are **Istio** and **Linkerd**. Both are graduated projects in the Cloud Native Computing Foundation (CNCF).

Other service mesh tools include:

- **Consul** (by HashiCorp)
- **Kuma** (by Kong)
- **Network Service Mesh** (NSM)
- **Traefik Mesh**
- **Open Service Mesh** (OSM, by Microsoft; the project is archived)
- **AWS App Mesh** (not open source; AWS ended support on September 30, 2026)

These platforms offer a variety of features to help improve the reliability, performance, and security of microservices-based applications.

<div align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1260/format:webp/1*dE01Th9iyq3VQUni9bC2_A.png" width="500" />
</div>

### Service Mesh Architecture

A typical service mesh consists of two main planes:

- **Data plane:** Consists of lightweight proxies (sidecars) deployed alongside each application instance. These proxies intercept and manage all network traffic between services.
- **Control plane:** Manages and configures the proxies to enforce policies and collect telemetry. The control plane provides APIs for operators to define routing, security, and observability rules.

### Key Features of a Service Mesh

- **Automatic mTLS:** Encrypts traffic between services by default.
- **Traffic shaping:** Canary releases, A/B testing, and blue-green deployments.
- **Observability:** Distributed tracing, metrics, and logging for all service-to-service traffic.
- **Policy enforcement:** Fine-grained access control and rate limiting.
- **Resilience:** Retries, timeouts, circuit breakers, and fault injection.

### When to Use a Service Mesh

- You have many microservices and need consistent, centralized management of traffic, security, and observability.
- You require advanced deployment strategies (canary, blue-green, etc.).
- You need to enforce security policies (mTLS, RBAC) between services.
- You want deep visibility into service-to-service communication.

### When Not to Use a Service Mesh

- Your application is simple or monolithic.
- You have only a few services and do not need advanced traffic management or security features.
- You want to minimize operational complexity and resource overhead.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

### Istio Control Plane Components

The Istio control plane consists of the following components:

- **Istiod:** The single control plane component in Istio. It manages configuration, service discovery, and certificate issuance, and pushes configuration to the Envoy proxies.

Historically these were separate components (Pilot for service discovery and traffic management, Galley for configuration validation, and Citadel for certificates), but since Istio 1.5 all of them are merged into `istiod`.

## References

- [Istio Documentation](https://istio.io/latest/docs/)
- [Istio Architecture](https://istio.io/latest/docs/ops/deployment/architecture/)
- [Linkerd Documentation](https://linkerd.io/docs/)
- [Consul Service Mesh](https://developer.hashicorp.com/consul/docs/connect)
- [Kuma Service Mesh](https://kuma.io/)
- [Network Service Mesh](https://networkservicemesh.io/)
- [Open Service Mesh](https://openservicemesh.io/)
- [CNCF Projects](https://www.cncf.io/projects/)
