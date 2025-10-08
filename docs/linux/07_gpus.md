# GPUs

To use GPUs on your machines, you first need to install NVIDIA drivers on any computer (host) that has a GPU card. These drivers let your operating system recognize and communicate with the GPU hardware. 

You can install the drivers with these commands:

```bash
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt-get update
sudo apt install nvidia-driver-<version> # e.g., 550
```

After installing the driver, your system will be able to use the GPU for processing tasks. To verify the installation, run:

```bash
nvidia-smi
```

The output shows the data of your GPU cards (reboot the system if you don't see any).

## NVIDIA Container Toolkit

Applications run inside containers using a container runtime like Docker or containerd. Therefore, you need to install additional toolkits to allow containers to access and use GPUs. 

The NVIDIA Container Toolkit connects the GPU driver with the containers and allows programs inside the container to use the GPU through CUDA (a platform for GPU computing).

Install it using the following commands:

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && \
  curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
```

After installing the NVIDIA Container Toolkit, configure the container runtime (e.g., `containerd`) to use the NVIDIA runtime by default. Edit `/etc/containerd/config.toml` and add or update the following section:

```toml
[plugins."io.containerd.grpc.v1.cri".containerd]
  default_runtime_name = "nvidia"
```

Restart containerd for changes to take effect:

```bash
sudo systemctl restart containerd
```

## NVIDIA Device Plugin (For Kubernetes)

Now that everything is installed on your nodes, enable Kubernetes to recognize and manage GPU resources using a device plugin. This plugin helps Kubernetes detect and schedule GPU resources correctly and runs as a DaemonSet on each GPU-enabled node.

Deploy the official NVIDIA device plugin with:

```bash
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.0/nvidia-device-plugin.yml
```

This command starts the plugin on each GPU-enabled node in your cluster.

## DCGM Exporter (For Kubernetes)

As the final step of the configuration process, we need to install the **DCGM Exporter**. In the following sections, we will explain how this exporter works in more detail. For now, our focus is simply on deploying it in the cluster.

```bash
helm repo add gpu-helm-charts https://nvidia.github.io/dcgm-exporter/helm-charts
helm repo update
helm install --generate-name gpu-helm-charts/dcgm-exporter
```

## GPU Usage Lifecycle

Now we will discuss the GPU usage lifecycle in a Kubernetes cluster. This includes what happens when a GPU is requested, which components are involved, and how the system manages GPU allocation and usage from start to finish.

The **NVIDIA Device Plugin** connects to the **kubelet** (the main Kubernetes agent running on each node) using a gRPC socket at:

```
/var/lib/kubelet/device-plugins/
```

Once connected, the plugin tells kubelet which GPU devices are available by advertising them with a resource name like `nvidia.com/gpu`. It also monitors GPU health to ensure they are functioning correctly.

When a pod requests a GPU, it includes a section like this in its YAML:

```yaml
resources:
  requests:
    nvidia.com/gpu: 1
```

The **Kubernetes scheduler** then selects a node with at least one available GPU. If GPU resources are not requested, the **DCGM Exporter** will not report any allocation metrics.

Before the pod starts, the kubelet on the selected node calls the `Allocate()` method of the NVIDIA device plugin. This method is part of the Device Plugin API and performs several key setup tasks:

1. **Mounts device files** such as:

   * `/dev/nvidia0`
   * `/dev/nvidiactl`
   * `/dev/nvidia-uvm`

2. **Provides GPU libraries and binaries** like:

   * `libcuda.so`
   * `libnvidia-ml.so`
   * Other driver-specific files under `/usr/lib/x86_64-linux-gnu/`

These are made available in the container's environment using volume mounts and environment variables such as `LD_LIBRARY_PATH`. This ensures that containers can run GPU-accelerated workloads via CUDA as if running directly on the host.

Without this step, the container cannot detect or use the GPU, even if one is physically present on the node.

## GPU Isolation

Inside the container, only the GPU(s) explicitly assigned to it are visible. Even if the node has multiple GPUs, the container will interact only with the GPU(s) allocated to it. All others are hidden from view.

This isolation is enforced by:

* The **device plugin**
* The **container runtime**

Kubernetes ensures **exclusive GPU access**, assigning each GPU to only one pod at a time. When a pod requests a GPU using `resources.requests["nvidia.com/gpu"] = 1`, the scheduler chooses a suitable node, and the kubelet/device plugin combo assigns the GPU securely.

This isolation is essential to:

* Prevent resource contention
* Ensure reliable performance
* Avoid issues from shared GPU access across workloads

## Useful Commands for Debugging

Getting more GPU details:

```bash
nvidia-smi -q
```

Getting details of PCIe link:

```bash
sudo lspci -vvv -s 0000:60:00.0 | grep "LnkCap"
```

Mapping GT/s to PCIe Generations:

| PCIe Generation | Signaling rate | Typical name | Encoding  | Effective data rate per lane | Approx. total for ×16 slot |
| --------------- | -------------- | ------------ | --------- | ---------------------------- | -------------------------- |
| Gen1            | 2.5 GT/s       | PCIe 1.0     | 8b/10b    | ~0.25 GB/s                   | ~4 GB/s                    |
| Gen2            | 5.0 GT/s       | PCIe 2.0     | 8b/10b    | ~0.5 GB/s                    | ~8 GB/s                    |
| **Gen3**        | **8.0 GT/s**   | **PCIe 3.0** | 128b/130b | **~0.985 GB/s**              | **~15.75 GB/s**            |
| Gen4            | 16 GT/s        | PCIe 4.0     | 128b/130b | ~1.97 GB/s                   | ~31.5 GB/s                 |
| Gen5            | 32 GT/s        | PCIe 5.0     | 128b/130b | ~3.94 GB/s                   | ~63 GB/s                   |

## GPU Cores

- **CUDA Cores**: The term for Nvidia's GPU cores, which also encompasses their parallel programming platform for efficient use. Best at Logic, control flow, non-matrix tasks. Example usages: Simulations, analytics, batch jobs.
- **Ray Tracing Cores**: Specialized units dedicated to rendering realistic light and shadow effects by calculating ray interactions with virtual objects, enhancing graphical fidelity. They are removed from newer GPU cards like A100 or H100.
- **Tensor Cores**: Specialized cores in some NVIDIA GPUs that accelerate matrix operations, significantly speeding up deep learning and AI workloads by using mixed-precision computing. Best at Matrix math, neural network ops. Example usages: Model training, inference, AI workloads.

A CUDA core can do whatever a Tensor core does. However, Tensor cores are faster in matrix multiplication. They are built to do a 4x4 matrix multiplication in fewer clocks than CUDA cores. Therefore, in deep learning tasks (e.g., vLLM inference) Tensor cores would be useful to decrease the computational overhead.
