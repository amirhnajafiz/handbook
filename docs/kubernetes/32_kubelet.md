# Kubelet

## Quick Description (QD)

The **Kubelet** is the primary node agent that runs on every node in a Kubernetes cluster. It is responsible for managing the lifecycle of pods and containers, ensuring that the containers described in PodSpecs are running and healthy.

### Responsibilities

- Registers the node with the Kubernetes cluster.
- Watches the API server for PodSpecs assigned to the node.
- Starts, stops, and monitors containers using a container runtime (e.g., containerd or CRI-O; Docker Engine needs the `cri-dockerd` adapter).
- Reports node and pod status back to the API server.
- Runs container probes and restarts failed containers according to the pod's `restartPolicy`.
- Manages pod volumes and secrets.

### How It Works

1. **Node registration:** On startup, the kubelet registers the node with the API server.
2. **Pod management:** Watches for new or updated PodSpecs assigned to the node.
3. **Container lifecycle:** Uses the container runtime to create, start, stop, and delete containers.
4. **Status reporting:** Continuously reports node and pod status to the API server.
5. **Health monitoring:** Runs liveness, readiness, and startup probes for containers (see [Probes](16_probes.md)).

### Key Features

- Integrates with various container runtimes via the Container Runtime Interface (CRI).
- Mounts pod volumes, secrets, and config maps, and runs static pods from a local manifest directory.
- Handles node-level resource management and reporting.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### Troubleshooting

Check if the kubelet is running:

```bash
sudo systemctl status kubelet
```

Look at recent logs:

```bash
sudo journalctl -u kubelet -xe --no-pager
```

Restart the kubelet:

```bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

### Remember these files

| File purpose                               | Typical locations                                               |
| ------------------------------------------ | --------------------------------------------------------------- |
| **Kubelet main config** (YAML)             | `/var/lib/kubelet/config.yaml` (kubeadm)                        |
| **Kubelet kubeconfig (for API server)**    | `/etc/kubernetes/kubelet.conf`                                  |
| **Bootstrap kubeconfig** (TLS bootstrap)   | `/etc/kubernetes/bootstrap-kubelet.conf`                        |
| **Environment overrides**                  | `/var/lib/kubelet/kubeadm-flags.env` (kubeadm)                  |
|                                            | `/etc/default/kubelet` *(Debian/Ubuntu)*                        |
|                                            | `/etc/sysconfig/kubelet` *(RHEL/CentOS)*                        |
| **Static pod manifests**                   | `/etc/kubernetes/manifests/`                                    |
| **Runtime state** (pods, plugins, volumes) | `/var/lib/kubelet/`                                             |
| **Service**                                | `/usr/lib/systemd/system/kubelet.service`                       |
|                                            | `/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf`     |

## Examples (e.g.,)

### Example kubelet configuration

The kubelet is configured with a configuration file (the recommended way) or command-line flags; many flags are deprecated in favor of the file. Below is an example of a kubelet configuration file (`kubelet-config.yaml`):

```yaml
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
address: 0.0.0.0
port: 10250
readOnlyPort: 0
authentication:
  anonymous:
    enabled: false
  webhook:
    enabled: true
authorization:
  mode: Webhook
clusterDomain: cluster.local
clusterDNS:
  - 10.96.0.10
failSwapOn: true
cgroupDriver: systemd
```

To start the kubelet with a configuration file:

```shell
kubelet --config=/etc/kubernetes/kubelet-config.yaml --kubeconfig=/etc/kubernetes/kubelet.conf
```

## References

- [Kubelet Reference](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)
- [Set Kubelet Parameters Via A Configuration File](https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/)
- [Kubelet Configuration (v1beta1)](https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/)
- [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/)
