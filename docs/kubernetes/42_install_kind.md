# Install Kind

Download and install Docker and [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation).

Here is the YAML configuration file for a 3-node kind cluster with default CNI disabled.
Save this locally to your workstation as kind-config.yaml with the contents:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
networking:
  disableDefaultCNI: true
```

Now create a new kind cluster using this configuration:

```sh
kind create cluster --config=kind-config.yaml
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.31.0) 🖼
 ✓ Preparing nodes 📦 📦 📦
 ✓ Writing configuration 📜
 ✓ Starting control-plane 🕹️
 ✓ Installing StorageClass 💾
 ✓ Joining worker nodes 🚜
Set kubectl context to "kind-kind"
You can now use your cluster with: 

kubectl cluster-info --context kind-kind 

Have a nice day! 👋
```

Kind will create the cluster and will configure an associated kubectl context. Confirm your new kind cluster is the default kubectl context:

```sh
kubectl config current-context
```

Note: Because you have created the cluster without a default CNI, the Kubernetes nodes are in a NotReady state:

```sh
kubectl get nodes
NAME                STATUS    ROLES          AGE    VERSION
kind-control-plane  NotReady  control-plane  8m30s   v1.31.0
kind-worker         NotReady  <none>         8m17s   v1.31.0
kind-worker2        NotReady  <none>         8m17s   v1.31.0
```
