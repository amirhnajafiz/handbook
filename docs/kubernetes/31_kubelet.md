# Kubelet

The **Kubelet** is the primary node agent that runs on every node in a Kubernetes cluster. It is responsible for managing the lifecycle of pods and containers, ensuring that the containers described in PodSpecs are running and healthy.

## Responsibilities

- Registers the node with the Kubernetes cluster.
- Watches the API server for PodSpecs assigned to the node.
- Starts, stops, and monitors containers using a container runtime (e.g., containerd, Docker, CRI-O).
- Reports node and pod status back to the API server.
- Performs health checks and restarts failed containers as needed.
- Manages pod volumes and secrets.

## How It Works

1. **Node Registration:** On startup, the kubelet registers the node with the API server.
2. **Pod Management:** Watches for new or updated PodSpecs assigned to the node.
3. **Container Lifecycle:** Uses the container runtime to create, start, stop, and delete containers.
4. **Status Reporting:** Continuously reports node and pod status to the API server.
5. **Health Monitoring:** Performs liveness and readiness checks for containers.

## Example Kubelet Configuration

Kubelet can be configured via command-line flags, a configuration file, or environment variables. Below is an example of a kubelet configuration file (`kubelet-config.yaml`):

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
failSwapOn: false
cgroupDriver: systemd
runtimeRequestTimeout: "15m"
```

To start kubelet with a configuration file:

```shell
kubelet --config=/etc/kubernetes/kubelet-config.yaml --kubeconfig=/etc/kubernetes/kubelet.conf
```

## Key Features

- Integrates with various container runtimes via the Container Runtime Interface (CRI).
- Supports liveness and readiness probes for containers.
- Manages pod volumes, secrets, and config maps.
- Handles node-level resource management and reporting.

## Troubleshooting

Check if the Kubelet is running:

```bash
sudo systemctl status kubelet
```

Look at recent logs:

```bash
sudo journalctl -u kubelet -xe --no-pager
```

Restart kubelet:

```bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

### Remember these files

| File purpose                               | Typical locations                                               |
| ------------------------------------------ | --------------------------------------------------------------- |
| **Kubelet main config** (YAML)             | `/var/lib/kubelet/config.yaml`                                  |
|                                            | `/etc/kubernetes/kubelet.conf` *(sometimes same as kubeconfig)* |
| **Bootstrap kubeconfig**                   | `/etc/kubernetes/bootstrap-kubelet.conf`                        |
| **Kubelet kubeconfig (for API server)**    | `/etc/kubernetes/kubelet.conf`                                  |
| **Environment overrides**                  | `/var/lib/kubelet/kubeadm-flags.env`                            |
|                                            | `/etc/sysconfig/kubelet` *(RHEL/CentOS)*                        |
|                                            | `/etc/default/kubelet` *(Debian/Ubuntu)*                        |
| **Static pod manifests**                   | `/etc/kubernetes/manifests/`                                    |
| **Runtime state** (various files, volumes) | `/var/lib/kubelet/` *(plugins, pods, device-plugins, volumes)*  |
| **Service**                                | `/etc/systemd/system/kubelet.service`                           |
|                                            | `/usr/lib/systemd/system/kubelet.service`                       |


## Further Reading

- [Kubelet Documentation](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)
- [Kubelet Configuration](https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/)
