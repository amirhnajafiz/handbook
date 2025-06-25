# GPFS

## System Health

Check health of cluster:

```sh
mmhealth cluster show
```

Node health:

```sh
mmhealth node show <service>
```

Node logs and events:

```sh
mmhealth node eventlog
```

## Cluster

Create a cluster:

```sh
mmcrcluster
```

View configuration:

```sh
mmlscluster
```

Add NodesList:

```sh
/mmcrcluster -N NodesList --ccr-enable -r /usr/bin/ssh -R /usr/bin/scp -C cluster1.spectrum
```

An example of NodesList file:

```
node1:quorum
node2
node3
node4:quorum-manager
node5:quorum-manager
```

Start the GPFS daemons and the cluster by using the following command from one of the nodes:

```sh
mmstartup -N NodesList
```

You can use the `mmgetstate -N NodesList` command to verify that the GPFS software is running on these nodes.
