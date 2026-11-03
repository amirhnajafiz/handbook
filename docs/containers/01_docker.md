# Docker

## Quick Description (QD)

**Docker** is a popular platform for developing, shipping, and running applications inside containers. It simplifies application deployment by packaging code and dependencies together. The Docker Engine is a client-server application: the `docker` CLI talks to the `dockerd` daemon, which uses [containerd](02_containerd.md) (and `runc`) to actually run containers.

### Key Concepts

- **Image:** A read-only template with instructions for creating a container.
- **Container:** A runnable instance of an image.
- **Dockerfile:** A text file with instructions to build a Docker image.
- **Docker Hub:** A cloud-based registry for sharing Docker images.

## Installation

Follow the official guide for your platform (Docker Engine for Linux, or Docker Desktop for macOS and Windows). On a Linux host, the quickest way to verify the install is:

```sh
sudo docker run hello-world
```

## Useful Tips/Commands (UToC)

### Useful Docker Commands

Check the Docker version:

```sh
docker --version
```

List running containers:

```sh
docker ps
```

List all containers:

```sh
docker ps -a
```

List images:

```sh
docker images
```

Pull an image:

```sh
docker pull <image-name>
```

Build an image from a Dockerfile:

```sh
docker build -t <image-name> .
```

Run a container:

```sh
docker run -it --name <container-name> <image-name>
```

Add `-d` to run in the background (detached), `-p <host-port>:<container-port>` to publish a port, and `--rm` to remove the container when it exits.

Stop a container:

```sh
docker stop <container-name>
```

Start a stopped container:

```sh
docker start <container-name>
```

Remove a container:

```sh
docker rm <container-name>
```

Remove an image:

```sh
docker rmi <image-name>
```

View container logs:

```sh
docker logs <container-name>
```

Execute a command in a running container:

```sh
docker exec -it <container-name> /bin/bash
```

### Networking Commands

List networks:

```sh
docker network ls
```

Create a network:

```sh
docker network create <network-name>
```

Connect a container to a network:

```sh
docker network connect <network-name> <container-name>
```

Disconnect a container from a network:

```sh
docker network disconnect <network-name> <container-name>
```

### Volume Commands

List volumes:

```sh
docker volume ls
```

Create a volume:

```sh
docker volume create <volume-name>
```

Use a volume with a container:

```sh
docker run -v <volume-name>:/path/in/container <image-name>
```

Remove a volume:

```sh
docker volume rm <volume-name>
```

### Docker Configuration

Docker can be configured using the `daemon.json` file, command-line flags, and environment variables.

#### Main Configuration File

- Linux: `/etc/docker/daemon.json` (the file does not exist by default; create it)
- Docker Desktop: edit the daemon configuration from Settings > Docker Engine. (Docker Desktop's own settings file is `settings-store.json` in `~/Library/Group Containers/group.com.docker/` on macOS, and is a different file.)

#### Common Configuration Options

- `data-root`: Directory where Docker stores images, containers, and volumes.
- `log-level`: Logging level (`debug`, `info`, `warn`, `error`, `fatal`).
- `storage-driver`: Storage driver (e.g., `overlay2`, the default on modern Linux).
- `insecure-registries`: List of registries Docker should treat as insecure.
- `registry-mirrors`: List of registry mirrors to use for image pulls (Docker Hub only).

#### Reloading Docker Configuration

After changing `daemon.json`, restart Docker:

```sh
sudo systemctl restart docker
```

Or, for Docker Desktop, restart the application.

## Examples (e.g.,)

### Example `daemon.json`

```json
{
  "data-root": "/var/lib/docker",
  "log-level": "info",
  "storage-driver": "overlay2",
  "insecure-registries": ["myregistry.local:5000"],
  "registry-mirrors": ["https://mirror.gcr.io"]
}
```

## References

- [Docker overview](https://docs.docker.com/get-started/docker-overview/)
- [Install Docker Engine](https://docs.docker.com/engine/install/)
- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Docker daemon configuration](https://docs.docker.com/engine/daemon/)
- [dockerd reference](https://docs.docker.com/reference/cli/dockerd/)
