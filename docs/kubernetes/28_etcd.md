# etcd

## Quick Description (QD)

etcd is a distributed, reliable key-value store that is simple, secure, and fast. It is designed for fast reads and writes, and provides strong consistency using the Raft consensus algorithm.

### Features

- Distributed and highly available
- Strong consistency and reliability
- Secure communication with TLS
- Watch support for real-time updates
- Snapshots and backup/restore capabilities

### etcd in Kubernetes

etcd is the primary data store for Kubernetes. It stores all cluster state and configuration, including:

- Nodes, Pods, and Deployments
- ConfigMaps and Secrets
- ServiceAccounts, Roles, and RoleBindings
- PersistentVolumeClaims and StorageClasses
- All API objects and their state

Every change to the Kubernetes cluster is recorded in etcd, making it critical for cluster reliability and disaster recovery.

### Deployment

A typical etcd deployment in production is a cluster of 3, 5, or 7 members (an odd number, since a majority, or quorum, must be alive: 3 members tolerate 1 failure, 5 tolerate 2). Each member communicates with others using secure peer URLs. Note that Secrets are stored in etcd unencrypted by default, so enable [encryption at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/).

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### Running etcd

etcd listens on port `2379` for client requests and `2380` for peer communication. You can run the `etcd` server and interact with it using the `etcdctl` command-line tool.

```sh
etcdctl put key1 value1
etcdctl get key1
etcdctl get --prefix /registry/pods --keys-only
etcdctl watch key1
etcdctl del key1
```

Check the health and members of a cluster (add the TLS flags below when TLS is enabled):

```sh
etcdctl endpoint health --cluster
etcdctl member list -w table
```

### Talking to a TLS-secured etcd

On a kubeadm cluster, etcd runs as a static Pod and its certificates are in `/etc/kubernetes/pki/etcd/`:

```sh
etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  member list
```

### Backup and restore

Regular backups are essential for disaster recovery. `etcdctl snapshot save` talks to a running member (so it needs the endpoint and TLS flags above), while restoring works on the snapshot file only and is done with `etcdutl` (the `etcdctl snapshot restore` form is deprecated since etcd 3.5).

```sh
# Backup
etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save backup.db

# Check the snapshot
etcdutl snapshot status backup.db -w table

# Restore into a new data directory
etcdutl snapshot restore backup.db --data-dir /var/lib/etcd-restored
```

After a restore, point the etcd member (for kubeadm, the `hostPath` of the static Pod manifest) at the new data directory.

### Security best practices

- Always enable TLS for client and peer communication.
- Restrict access to etcd endpoints (anyone with access can read all cluster Secrets).
- Regularly back up etcd data.
- Monitor etcd health and cluster status.

## Examples (e.g.,)

### Example `etcd.service` configuration

A systemd unit for one member of a two-member cluster (as in Kubernetes The Hard Way). Use an odd number of members in production. `INTERNAL_IP`, `CONTROLLER0_IP` and `CONTROLLER1_IP` are shell variables to be replaced with real addresses when generating the file.

```ini
[Unit]
Description=etcd
Documentation=https://github.com/etcd-io/etcd

[Service]
Type=notify
ExecStart=/usr/local/bin/etcd \
  --name controller-0 \
  --cert-file=/etc/etcd/etcd-server.crt \
  --key-file=/etc/etcd/etcd-server.key \
  --peer-cert-file=/etc/etcd/etcd-server.crt \
  --peer-key-file=/etc/etcd/etcd-server.key \
  --trusted-ca-file=/etc/etcd/ca.crt \
  --peer-trusted-ca-file=/etc/etcd/ca.crt \
  --peer-client-cert-auth \
  --client-cert-auth \
  --initial-advertise-peer-urls https://${INTERNAL_IP}:2380 \
  --listen-peer-urls https://${INTERNAL_IP}:2380 \
  --listen-client-urls https://${INTERNAL_IP}:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://${INTERNAL_IP}:2379 \
  --initial-cluster-token etcd-cluster-0 \
  --initial-cluster controller-0=https://${CONTROLLER0_IP}:2380,controller-1=https://${CONTROLLER1_IP}:2380 \
  --initial-cluster-state new \
  --data-dir=/var/lib/etcd
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## References

- [etcd documentation](https://etcd.io/docs/)
- [etcd disaster recovery](https://etcd.io/docs/v3.5/op-guide/recovery/)
- [etcd security model](https://etcd.io/docs/v3.5/op-guide/security/)
- [etcd clustering guide](https://etcd.io/docs/v3.5/op-guide/clustering/)
- [Kubernetes etcd cluster administration](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)
- [etcd Operator](https://github.com/etcd-io/etcd-operator)
