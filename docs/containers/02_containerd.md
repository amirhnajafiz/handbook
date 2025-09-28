# Container-d

**Container-d** is an industry-standard container runtime that manages the complete container lifecycle on a host system. It is designed to be embedded into a larger system, such as Docker or Kubernetes, and provides core container management capabilities.

## Key Concepts

- **Container Runtime:** The low-level software responsible for running containers.
- **Snapshotter:** Manages the filesystem snapshots used by containers.
- **Namespaces:** Isolate resources and workloads within containerd.
- **CRI (Container Runtime Interface):** Allows Kubernetes to interact with containerd.

## Useful containerd Commands

- **Check containerd version**

```sh
containerd --version
```

- **List running containers**

```sh
ctr -n <namespace> containers list
```

- **List all images**

```sh
ctr -n <namespace> images list
```

- **Pull an image**

```sh
ctr -n <namespace> images pull <image-name>
```

- **Run a container**

```sh
ctr -n <namespace> run -t <image-name> <container-id>
```

- **Start a container**

```sh
ctr -n <namespace> tasks start <container-id>
```

- **Stop a container**

```sh
ctr -n <namespace> tasks kill <container-id>
```

- **Remove a container**

```sh
ctr -n <namespace> containers delete <container-id>
```

- **Remove an image**

```sh
ctr -n <namespace> images remove <image-name>
```

- **View container logs**

```sh
ctr -n <namespace> tasks logs <container-id>
```

## Namespaces

Container-d uses namespaces to isolate groups of containers and images. The default namespace is usually `default`, but you can specify others.

## Configuration

containerd is configured using the `config.toml` file.

### Main Configuration File

- `/etc/containerd/config.toml`

### Generate Default Config

To generate a default configuration file:

```sh
containerd config default > /etc/containerd/config.toml
```

### Example `config.toml`

```toml
[plugins."io.containerd.grpc.v1.cri".containerd]
  snapshotter = "overlayfs"

[plugins."io.containerd.grpc.v1.cri".registry]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
    [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
      endpoint = ["https://mirror.gcr.io"]
```

### Common Configuration Options

- `snapshotter`: Filesystem snapshotter to use (e.g., `overlayfs`).
- `registry.mirrors`: Configure registry mirrors for pulling images.
- `plugins`: Plugin-specific configuration, such as CRI for Kubernetes integration.

### Reloading containerd Configuration

After editing `config.toml`, restart containerd:

```sh
sudo systemctl restart containerd
```
