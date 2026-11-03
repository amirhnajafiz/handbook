# Readiness and liveness probes

## Quick Description (QD)

The kubelet uses probes to know the state of a container. There are three kinds:

- Liveness probes tell the kubelet when to restart a container. For example, they can catch a deadlock, where an application is running but unable to make progress. Restarting a container in such a state can help to make the application more available despite bugs.
- Readiness probes tell the kubelet when a container is ready to accept traffic. A Pod is considered ready when all of its containers are ready. One use of this signal is to control which Pods are used as backends for Services. When a Pod is not ready, it is removed from the Service's endpoints (see [Endpoints](25_endpoints.md)).
- Startup probes tell the kubelet when the application inside the container has started. While a startup probe is configured and has not yet succeeded, the liveness and readiness probes are disabled. This is useful for slow-starting containers, so the liveness probe does not kill them before they are up.

A failed readiness probe does not restart the container; it only marks the Pod as not ready. A failed liveness or startup probe makes the kubelet kill the container, which is then subject to the Pod's `restartPolicy`.

### Probe mechanisms

Each probe uses one of these: `exec` (run a command; exit code 0 is success), `httpGet` (status code from 200 to 399 is success), `tcpSocket` (the port is open), or `grpc`.

### Common fields

- `initialDelaySeconds`: seconds to wait after the container starts before probing (default 0).
- `periodSeconds`: how often to probe (default 10).
- `timeoutSeconds`: probe timeout (default 1).
- `failureThreshold`: consecutive failures before the probe is considered failed (default 3).
- `successThreshold`: consecutive successes to be considered successful again (default 1; must be 1 for liveness and startup probes).

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

- With a startup probe, the application has up to `failureThreshold * periodSeconds` to start.
- Check probe failures in the Pod events:

```sh
kubectl describe pod <pod-name>
```

## Examples (e.g.,)

Liveness probe with a command. The file is removed after 30 seconds, so the probe fails and the container is restarted:

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    test: liveness
  name: liveness-exec
spec:
  containers:
  - name: liveness
    image: registry.k8s.io/busybox
    args:
    - /bin/sh
    - -c
    - touch /tmp/healthy; sleep 30; rm -f /tmp/healthy; sleep 600
    livenessProbe:
      exec:
        command:
        - cat
        - /tmp/healthy
      initialDelaySeconds: 5
      periodSeconds: 5
```

Readiness, liveness and startup probes over HTTP on the same container. The startup probe gives the application up to 300 seconds (30 x 10) to start:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: probes-http
spec:
  containers:
  - name: app
    image: registry.k8s.io/e2e-test-images/agnhost:2.40
    args: ["liveness"]
    ports:
    - name: liveness-port
      containerPort: 8080
    startupProbe:
      httpGet:
        path: /healthz
        port: liveness-port
      failureThreshold: 30
      periodSeconds: 10
    livenessProbe:
      httpGet:
        path: /healthz
        port: liveness-port
      periodSeconds: 10
    readinessProbe:
      tcpSocket:
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 10
```

## References

- [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
