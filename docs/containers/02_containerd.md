# containerd

## Quick Description (QD)

**containerd** is an industry-standard container runtime that manages the complete container lifecycle on a host system. It is designed to be embedded into a larger system, such as Docker or Kubernetes, and provides core container management capabilities.

### Key Concepts

- **Container runtime:** The low-level software responsible for running containers.
- **Snapshotter:** Manages the filesystem snapshots used by containers.
- **Namespaces:** Isolate resources and workloads within containerd.
- **CRI (Container Runtime Interface):** Allows Kubernetes to interact with containerd.

### Namespaces

containerd uses namespaces to isolate groups of containers and images. The `ctr` default namespace is `default`, but you can specify others with `-n`. Docker uses `moby` and Kubernetes (CRI) uses `k8s.io`, so use `-n k8s.io` to see Kubernetes containers and images.

## Installation

containerd is usually installed as a dependency of Docker or Kubernetes. To install it on its own, see the official getting started guide (packages are available from the Docker apt repository, or as release binaries). Then enable the service:

```sh
sudo systemctl enable --now containerd
```

## Useful Tips/Commands (UToC)

### Useful containerd Commands

Check the containerd version:

```sh
containerd --version
```

List containers (to see which ones are actually running, use `tasks list`):

```sh
ctr -n <namespace> containers list
ctr -n <namespace> tasks list
```

List all images:

```sh
ctr -n <namespace> images list
```

Pull an image (`ctr` needs the fully qualified name, e.g., `docker.io/library/nginx:latest`):

```sh
ctr -n <namespace> images pull <image-name>
```

Run a container (creates it and starts its task; add `-d` to detach):

```sh
ctr -n <namespace> run -t --rm <image-name> <container-id>
```

Create a container without starting it, then start its task:

```sh
ctr -n <namespace> containers create <image-name> <container-id>
ctr -n <namespace> tasks start <container-id>
```

Stop a container (sends SIGTERM by default; use `--signal SIGKILL` to force):

```sh
ctr -n <namespace> tasks kill <container-id>
```

Remove a container (stop its task first with `tasks delete <container-id>` if it is still present):

```sh
ctr -n <namespace> containers delete <container-id>
```

Remove an image:

```sh
ctr -n <namespace> images remove <image-name>
```

### Configuration

containerd is configured using the `config.toml` file.

#### Main Configuration File

- `/etc/containerd/config.toml`

#### Generate the Default Config

To generate a default configuration file:

```sh
containerd config default | sudo tee /etc/containerd/config.toml
```

#### Common Configuration Options

- `snapshotter`: Filesystem snapshotter to use (e.g., `overlayfs`), set inside the CRI plugin section.
- Registry mirrors: configure per-registry `hosts.toml` files and set `config_path` in the CRI registry section (the old `registry.mirrors` table is deprecated).
- `plugins`: Plugin-specific configuration, such as CRI for Kubernetes integration.
- `SystemdCgroup = true` under the `runc` runtime options is required when the kubelet uses the systemd cgroup driver.

#### Reloading containerd Configuration

After editing `config.toml`, restart containerd:

```sh
sudo systemctl restart containerd
```

## Examples (e.g.,)

### Example `config.toml`

```toml
[plugins."io.containerd.grpc.v1.cri".containerd]
  snapshotter = "overlayfs"

[plugins."io.containerd.grpc.v1.cri".registry]
  config_path = "/etc/containerd/certs.d"
```

Then define the mirror for Docker Hub in `/etc/containerd/certs.d/docker.io/hosts.toml`:

```toml
server = "https://registry-1.docker.io"

[host."https://mirror.gcr.io"]
  capabilities = ["pull", "resolve"]
```

## References

- [containerd documentation](https://containerd.io/docs/)
- [Getting started with containerd](https://github.com/containerd/containerd/blob/main/docs/getting-started.md)
- [containerd CRI plugin configuration](https://github.com/containerd/containerd/blob/main/docs/cri/config.md)
- [Registry host namespace (hosts.toml)](https://github.com/containerd/containerd/blob/main/docs/hosts.md)
