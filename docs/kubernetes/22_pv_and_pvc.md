# PV and PVC

## Quick Description (QD)

A PersistentVolume (PV) is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using StorageClasses. It is a resource in the cluster just like a node is a cluster resource.

PVs are volume plugins like Volumes, but have a lifecycle independent of any individual Pod that uses the PV. This API object captures the details of the implementation of the storage, be that NFS, iSCSI, or a cloud-provider-specific storage system.

A PersistentVolumeClaim (PVC) is a request for storage by a user. It is similar to a Pod. Pods consume node resources and PVCs consume PV resources. Pods can request specific levels of resources (CPU and memory). Claims can request specific size and access modes (e.g., they can be mounted ReadWriteOnce, ReadOnlyMany, or ReadWriteMany).

PVs are resources in the cluster. PVCs are requests for those resources and also act as claim checks to the resource. While PersistentVolumeClaims allow a user to consume abstract storage resources, it is common that users need PersistentVolumes with varying properties, such as performance, for different problems. Cluster administrators need to be able to offer a variety of PersistentVolumes that differ in more ways than size and access modes, without exposing users to the details of how those volumes are implemented. For these needs, there is the StorageClass resource.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

```sh
kubectl get pv,pvc,storageclass
kubectl describe pvc myclaim
```

- A PV is cluster-scoped, a PVC is namespaced and a PVC binds to exactly one PV.
- The PV `persistentVolumeReclaimPolicy` decides what happens when the claim is deleted: `Retain` (keep the data, manual cleanup), `Delete` (delete the volume, the default for dynamically provisioned PVs). `Recycle` is deprecated; use dynamic provisioning instead.
- Setting `storageClassName: ""` on a PVC disables dynamic provisioning and binds it only to PVs without a class.

## Examples (e.g.,)

A statically provisioned PV (a `hostPath` volume is only for single-node testing), a PVC that requests it, and a Pod that mounts the claim:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/data
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: task-pod
spec:
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: myclaim
  containers:
    - name: app
      image: nginx
      volumeMounts:
        - name: data
          mountPath: /usr/share/nginx/html
```

A StorageClass describes how volumes are dynamically provisioned. A PVC that omits `storageClassName` uses the cluster's default StorageClass, and a PVC can also pick specific PVs with `spec.selector` (label selector).

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: example-vol-default
provisioner: vendor-name.example/magicstorage
parameters:
  type: fast
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
```

## References

- [K8S PV and PVC](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
