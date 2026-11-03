# Cephadm

## Quick Description (QD)

Cephadm is the official tool for deploying and managing Ceph clusters. It uses containers to simplify installation, upgrades, and maintenance.

### Key Features

- **Containerized deployment:** Runs Ceph daemons in containers for consistency and portability.
- **Automated orchestration:** Handles service placement, scaling, and upgrades.
- **Minimal host dependencies:** Requires Python 3, systemd, LVM2, time synchronization, and Podman or Docker.

### Basic Workflow

1. **Bootstrap the cluster:** Initializes the first Ceph monitor and manager.
2. **Add hosts:** Register additional nodes to the cluster.
3. **Deploy services:** Use Ceph orchestrator commands to add OSDs, MDS, RGW, and so on.
4. **Manage and upgrade:** Perform rolling upgrades and monitor cluster health.

## Installation

Cephadm needs Python 3, systemd, a container runtime (Podman or Docker), time synchronization (for example chrony), and LVM2. You can install it from your distribution's packages, or download the standalone script. Set `CEPH_RELEASE` to the Ceph release you want (for example `tentacle` or `squid`) and use the matching distribution directory (`el9` below):

```sh
CEPH_RELEASE=tentacle   # or another release name, e.g. squid
curl --silent --remote-name --location https://download.ceph.com/rpm-${CEPH_RELEASE}/el9/noarch/cephadm
chmod +x cephadm
sudo mv cephadm /usr/local/bin/
```

Install the prerequisites if they are missing:

```sh
sudo dnf install -y podman python3 lvm2 chrony  # On RHEL/CentOS/Fedora
sudo apt install -y podman python3 lvm2 chrony  # On Ubuntu/Debian
```

## Useful Tips/Commands (UToC)

- Install the `ceph` CLI on the host with `cephadm install ceph-common`, or run it inside a container with `cephadm shell`.
- `ceph orch ps` lists the running daemons, `ceph orch ls` lists the services, and `ceph orch device ls` lists the devices that can be used for OSDs.
- `ceph orch host ls` shows the hosts that are managed by the orchestrator.

## Examples (e.g.,)

### Bootstrapping

```sh
cephadm bootstrap --mon-ip <MONITOR_IP>
```

### Adding Hosts

Copy the cluster's SSH key to the new host first (`ssh-copy-id -f -i /etc/ceph/ceph.pub root@<HOSTNAME>`), then:

```sh
ceph orch host add <HOSTNAME> <HOST_IP>
```

### Deploying OSDs

Either create an OSD on one specific device:

```sh
ceph orch daemon add osd <HOSTNAME>:<DEVICE_PATH>
```

or let the orchestrator consume every available (empty, unpartitioned) device:

```sh
ceph orch apply osd --all-available-devices
```

## References

- [Cephadm Documentation](https://docs.ceph.com/en/latest/cephadm/)
- [Cephadm: Installing a New Cluster](https://docs.ceph.com/en/latest/cephadm/install/)
- [Cephadm: Host Management](https://docs.ceph.com/en/latest/cephadm/host-management/)
- [Cephadm: OSD Service](https://docs.ceph.com/en/latest/cephadm/services/osd/)
