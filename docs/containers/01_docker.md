# Docker

**Docker** is a popular platform for developing, shipping, and running applications inside containers. It simplifies application deployment by packaging code and dependencies together.

## Key Concepts

- **Image:** A read-only template with instructions for creating a container.
- **Container:** A runnable instance of an image.
- **Dockerfile:** A text file with instructions to build a Docker image.
- **Docker Hub:** A cloud-based registry for sharing Docker images.

## Useful Docker Commands

- **Check Docker version**

```sh
docker --version
```

- **List running containers**

```sh
docker ps
```

- **List all containers**

```sh
docker ps -a
```

- **List images**

```sh
docker images
```

- **Pull an image**

```sh
docker pull <image-name>
```

- **Build an image from a Dockerfile**

```sh
docker build -t <image-name> .
```

- **Run a container**

```sh
docker run -it --name <container-name> <image-name>
```

- **Stop a container**

```sh
docker stop <container-name>
```

- **Remove a container**

```sh
docker rm <container-name>
```

- **Remove an image**

```sh
docker rmi <image-name>
```

- **View container logs**

```sh
docker logs <container-name>
```

- **Execute a command in a running container**

```sh
docker exec -it <container-name> /bin/bash
```

### Networking Commands

- **List networks**

```sh
docker network ls
```

- **Create a network**

```sh
docker network create <network-name>
```

- **Connect a container to a network**

```sh
docker network connect <network-name> <container-name>
```

- **Disconnect a container from a network**

```sh
docker network disconnect <network-name> <container-name>
```

## Volumes Commands

- **List volumes**

```sh
docker volume ls
```

- **Create a volume**

```sh
docker volume create <volume-name>
```

- **Use a volume with a container**

```sh
docker run -v <volume-name>:/path/in/container <image-name>
```

- **Remove a volume**

```sh
docker volume rm <volume-name>
```

## Docker Configuration

Docker can be configured using the `daemon.json` file, command-line flags, and environment variables.

### Main Configuration File

- Linux: `/etc/docker/daemon.json`  
- macOS: `~/Library/Group Containers/group.com.docker/settings.json` (for Docker Desktop)

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

### Common Configuration Options

- `data-root`: Directory where Docker stores images, containers, and volumes.
- `log-level`: Logging level (`debug`, `info`, `warn`, `error`, `fatal`).
- `storage-driver`: Filesystem driver (e.g., `overlay2`, `aufs`).
- `insecure-registries`: List of registries Docker should treat as insecure.
- `registry-mirrors`: List of registry mirrors to use for image pulls.

### Reloading Docker Configuration

After changing `daemon.json`, restart Docker:

```sh
sudo systemctl restart docker
```

Or, for Docker Desktop, restart the application.
