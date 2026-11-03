# Multi-container pods

## Quick Description (QD)

Containers in a Pod run on a "logical host": they use the same network namespace (same IP address and port space), the same IPC namespace and, optionally, shared volumes. Therefore, these containers can communicate efficiently, ensuring data locality. Also, Pods allow managing several tightly coupled application containers as a single unit.

The primary purpose of a multi-container Pod is to support co-located, co-managed helper processes for a main program. There are some general patterns of using helper processes in Pods:

- Sidecar containers
- Proxies, bridges, and adapters
- Ambassador pattern

Containers in a Pod can also communicate with each other using standard inter-process communication such as SystemV semaphores or POSIX shared memory. Since they share the network namespace, they reach each other via `localhost` (so two containers in the same Pod cannot listen on the same port).

Since Kubernetes 1.29 (stable in 1.33), sidecars can also be declared as init containers with `restartPolicy: Always`. These start before the main containers, keep running next to them, and are shut down after them (see [Sidecar containers](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)).

### Why use it?

- Efficient collaboration: Containers work closely together, which is ideal for applications with interconnected components.
- Streamlined management: The Pod is the unit of scheduling, so all containers in it are placed on the same Node and are created and deleted together. Note that each container is still restarted independently according to the Pod's `restartPolicy`.
- Shared resources: Containers share the Pod's network and can share volumes. CPU and memory are still requested and limited per container; the Pod's effective request is the sum of its containers' requests.
- Effective communication: Containers in the same Pod exchange data over `localhost`, shared volumes or IPC, without crossing the network.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

Two containers sharing an `emptyDir` volume: the second writes the date into `index.html`, the first (nginx) serves it.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mc1
spec:
  volumes:
  - name: html
    emptyDir: {}
  containers:
  - name: 1st
    image: nginx
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
  - name: 2nd
    image: debian
    volumeMounts:
    - name: html
      mountPath: /html
    command: ["/bin/sh", "-c"]
    args:
      - while true; do
          date >> /html/index.html;
          sleep 1;
        done
```

## References

- [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Communicate between containers in the same Pod using a shared volume](https://kubernetes.io/docs/tasks/access-application-cluster/communicate-containers-same-pod-shared-volume/)
- [Sidecar containers](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)
