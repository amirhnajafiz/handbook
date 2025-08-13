# Cephadm

Cephadm is the official tool for deploying and managing Ceph clusters. It uses containers to simplify installation, upgrades, and maintenance.

## Key Features

- **Containerized deployment:** Runs Ceph daemons in containers for consistency and portability.
- **Automated orchestration:** Handles service placement, scaling, and upgrades.
- **Minimal host dependencies:** Only requires Python 3 and podman/docker.

## Basic Workflow

1. **Bootstrap the cluster:** Initializes the first Ceph monitor and manager.
2. **Add hosts:** Register additional nodes to the cluster.
3. **Deploy services:** Use Ceph orchestrator commands to add OSDs, MDS, RGW, etc.
4. **Manage and upgrade:** Perform rolling upgrades and monitor cluster health.

## Example: Bootstrapping

```sh
cephadm bootstrap --mon-ip <MONITOR_IP>
```

## Example: Adding Hosts

```sh
ceph orch host add <HOSTNAME> <HOST_IP>
```

## Example: Deploying OSDs

```sh
ceph orch daemon add osd <HOSTNAME>:<DEVICE_PATH>
```

## Example: Installing Cephadm

To install Cephadm on your initial host:

```sh
curl --silent --remote-name https://raw.githubusercontent.com/ceph/ceph/reef/src/cephadm/cephadm
chmod +x cephadm
sudo mv cephadm /usr/local/bin/
```

You may also need to install `podman` or `docker` and `python3`:

```sh
sudo dnf install -y podman python3  # On RHEL/CentOS/Fedora
sudo apt install -y podman python3  # On Ubuntu/Debian
```

## References

- [Cephadm Documentation](https://docs.ceph.com/en/latest/cephadm/)
- [Ceph Orchestrator CLI](https://docs.ceph.com/en/latest/cephadm/cli/)
