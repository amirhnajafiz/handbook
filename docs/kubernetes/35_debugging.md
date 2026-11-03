# Debugging Pods in Kubernetes

## Quick Description (QD)

Debugging is a critical skill for maintaining healthy Kubernetes clusters. Kubernetes provides several tools and techniques to help you diagnose and resolve issues with your pods and containers.

### Using `kubectl debug`

The Kubernetes-native answer to debugging running containers is to use `kubectl debug`. This command adds an ephemeral container to a running pod, allowing you to troubleshoot issues interactively even when the application image has no shell or tools.

- The debug container can use any image you choose.
- It shares the pod's network namespace and volumes it mounts; with `--target=<container>` it also shares that container's process namespace (if the runtime supports it), so you can see its processes.
- Ephemeral containers cannot be removed or restarted once added; they go away when the pod is deleted.

It can also copy a pod for debugging (`--copy-to`) or start a privileged pod on a node (`kubectl debug node/<node-name>`).

### Common Debugging Scenarios

- **Network issues:** Use tools like `curl`, `wget`, or `nslookup` inside the debug container.
- **File system inspection:** With `--target`, look at the target container's root through `/proc/<pid>/root`; or use `--copy-to` to start a copy of the pod with different volumes or image.
- **Process inspection:** Use `ps`, `top`, or `htop` to view running processes.
- **Environment variables:** Check with `env` or `printenv`.
- **Resource limits:** Inspect with `ulimit` and check `/sys/fs/cgroup` for cgroup limits.

### Debugging Images

For advanced debugging, use images with extra troubleshooting tools (e.g., `nicolaka/netshoot`, `busybox`, or `alpine`).

- `nicolaka/netshoot` includes networking tools like `dig`, `tcpdump`, `iftop`, and more.
- `busybox` and `alpine` are lightweight and useful for basic inspection.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### Other Useful Commands

- `kubectl describe pod <pod-name>`: Shows detailed information about the pod, including events.
- `kubectl logs <pod-name> [-c container-name]`: Views logs for a specific container.
- `kubectl exec -it <pod-name> -- /bin/sh`: Gets a shell inside a running container.
- `kubectl get events --sort-by=.metadata.creationTimestamp`: Views recent events for troubleshooting.

### Best Practices

- Always use minimal and trusted images for debugging.
- Delete debug pods and copies (`--copy-to`) after use, since ephemeral containers stay until the pod is deleted.
- Use RBAC to restrict who can run debug containers.
- Document common troubleshooting steps for your team.

## Examples (e.g.,)

### Standalone Debug Pod

Spin up a throwaway pod for network debugging. `nicolaka/netshoot` is a popular image containing a comprehensive set of network troubleshooting tools.

```sh
kubectl run debugging-pod \
  --rm -i --tty \
  --image nicolaka/netshoot \
  --restart=Never \
  -- sh
```

### Debug Command

Attach an ephemeral container named `debug-container` to the pod `postpod`, targeting its container `postcont`:

```shell
kubectl debug -it postpod \
  --container=debug-container \
  --image=alpine \
  --target=postcont
```

### Debug with a Troubleshooting Image

```shell
kubectl debug -it <pod-name> --image=nicolaka/netshoot --target=<container-name>
```

Debug a copy of a crashing pod with a shell instead of its entrypoint:

```shell
kubectl debug <pod-name> -it --copy-to=<pod-name>-debug --container=<container-name> -- sh
```

## References

- [Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)
- [Netshoot image](https://github.com/nicolaka/netshoot)
