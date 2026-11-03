# Kubeadm

## Quick Description (QD)

**Kubeadm** is a tool provided by Kubernetes to simplify the process of creating, configuring, and managing Kubernetes clusters. It automates the tasks required to bootstrap a minimum viable, secure, and production-ready cluster.

### Key Features

- Initializes and configures Kubernetes control plane components.
- Joins worker nodes to the cluster.
- Handles certificate generation and management.
- Supports cluster upgrades and configuration changes.
- Provides configuration files for repeatable, declarative cluster setups.

## Installation

Install a container runtime (e.g., containerd or CRI-O; see [Container runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)), then install `kubeadm`, `kubelet`, and `kubectl` on all nodes. The legacy `apt.kubernetes.io` / `packages.cloud.google.com` repositories are deprecated and frozen; packages are now published at `pkgs.k8s.io`, with a separate repository per minor version. Set `KUBE_MINOR` to the minor version you want (e.g., `v1.37`):

```shell
KUBE_MINOR=v1.37   # change to the minor version you want to install

sudo apt-get update
# apt-transport-https may be a dummy package; if so, you can skip it
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
# on releases older than Debian 12 / Ubuntu 22.04: sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/${KUBE_MINOR}/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/${KUBE_MINOR}/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
sudo systemctl enable --now kubelet
```

To move to another minor version, change the version in the repository URL (see [Changing the Kubernetes package repository](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/change-package-repository/)).

> By default the kubelet fails to start when swap is on, so turn swap off: `sudo swapoff -a && sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab`

## Useful Tips/Commands (UToC)

Check cluster status:

```shell
kubectl get nodes
kubectl get pods -A
```

View the cluster configuration that kubeadm stored (`kubeadm config view` was removed):

```shell
kubectl -n kube-system get cm kubeadm-config -o yaml
```

Print the default configuration kubeadm would use:

```shell
kubeadm config print init-defaults
```

Generate a new join token:

```shell
kubeadm token create --print-join-command
```

Bootstrap tokens expire after 24 hours by default.

### Upgrade Cluster

On the first control plane node, upgrade the `kubeadm` package first, then:

```shell
sudo kubeadm upgrade plan
sudo kubeadm upgrade apply v1.37.2
```

On other control plane nodes and on workers, run `sudo kubeadm upgrade node`, after draining the node (see [Node Upgrade](34_node_upgrade.md)), then upgrade `kubelet`/`kubectl` and restart the kubelet. The version above is an example; use one shown by `kubeadm upgrade plan`.

### Reset Cluster

This reverts changes made by `kubeadm init` or `join` on the node. It does not clean up CNI configuration, iptables/IPVS rules, or your kubeconfig, so do those by hand.

```shell
sudo kubeadm reset
```

## Examples (e.g.,)

### Typical Workflow

#### 1. Initialize the Control Plane

You can use default settings or provide a configuration file for custom setups.

Default initialization:

```shell
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

Using a configuration file. Create a file named `kubeadm-config.yaml`:

```yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: "192.168.1.100"
  bindPort: 6443
---
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
kubernetesVersion: "1.34.1"
networking:
  podSubnet: "10.244.0.0/16"
  serviceSubnet: "10.96.0.0/12"
apiServer:
  extraArgs:
    - name: authorization-mode
      value: Node,RBAC
controllerManager: {}
scheduler: {}
---
apiVersion: kubeadm.k8s.io/v1beta4
kind: KubeletConfiguration
cgroupDriver: systemd
```

Initialize with:

```shell
sudo kubeadm init --config=kubeadm-config.yaml
```

#### 2. Set Up kubectl Access

```shell
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

#### 3. Install a Pod Network Add-on

Example with Flannel (its default pod CIDR is `10.244.0.0/16`, matching the one used above; any other CNI plugin works too, but nodes stay `NotReady` until one is installed):

```shell
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```

#### 4. Join Worker Nodes

On each worker node, run the join command output by `kubeadm init`, e.g.:

```shell
sudo kubeadm join <control-plane-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

### Example HA-Ready Configuration File

A stable `controlPlaneEndpoint` (a DNS name or load balancer in front of all control plane nodes) is needed to add more control plane nodes later:

```yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
kubernetesVersion: "1.34.1"
controlPlaneEndpoint: "k8s.example.com:6443"
networking:
  podSubnet: "10.244.0.0/16"
  serviceSubnet: "10.96.0.0/12"
apiServer:
  extraArgs:
    - name: v
      value: "2"
controllerManager: {}
scheduler: {}
```

## References

- [Bootstrapping clusters with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/)
- [Installing kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
- [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- [kubeadm init](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/)
- [kubeadm reset](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-reset/)
- [kubeadm Configuration Reference (v1beta4)](https://kubernetes.io/docs/reference/config-api/kubeadm-config.v1beta4/)
- [Upgrading kubeadm clusters](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)
- [Flannel](https://github.com/flannel-io/flannel)
