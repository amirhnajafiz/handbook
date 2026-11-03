# Scale

## Quick Description (QD)

Scaling sets a new size for a Deployment, ReplicaSet, ReplicationController, or StatefulSet. Scaling out a Deployment will ensure new Pods are created and scheduled to Nodes with available resources. Scaling will increase the number of Pods to the new desired state.

Running multiple instances of an application will require a way to distribute the traffic to all of them. Services have an integrated load balancer that will distribute network traffic to all Pods of an exposed Deployment. Services continuously track the running Pods using EndpointSlices (Endpoints), to ensure the traffic is sent only to available Pods.

### HPA

In Kubernetes, a `HorizontalPodAutoscaler` automatically updates a workload resource (such as a Deployment or StatefulSet), with the aim of automatically scaling the workload to match demand.

Horizontal scaling means that the response to increased load is to deploy more Pods. This is different from vertical scaling, which for Kubernetes would mean assigning more resources (for example, memory or CPU) to the Pods that are already running for the workload. Horizontal pod autoscaling does not apply to objects that can't be scaled (for example, a DaemonSet).

Kubernetes implements horizontal pod autoscaling as a control loop that runs intermittently (it is not a continuous process). The interval is set by the `--horizontal-pod-autoscaler-sync-period` parameter to the kube-controller-manager (and the default interval is 15 seconds).

Once during each period, the controller manager queries the resource utilization against the metrics specified in each HorizontalPodAutoscaler definition. The controller manager finds the target resource defined by the `scaleTargetRef`, then selects the pods based on the target resource's `.spec.selector` labels, and obtains the metrics from either the resource metrics API (for per-pod resource metrics), or the custom metrics API (for all other metrics).

#### Algorithm

```text
desiredReplicas = ceil[currentReplicas * ( currentMetricValue / desiredMetricValue )]
```

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

Replace the object:

```sh
kubectl replace -f replicaset-definition.yml
```

Change the object by its file:

```sh
kubectl scale --replicas=6 -f replicaset-definition.yml
```

Change the object in the cluster:

```sh
kubectl scale --replicas=6 replicaset myapp-replicaset
```

## Examples (e.g.,)

_Nothing here yet._

## References

- [K8S Scaling](https://kubernetes.io/docs/tutorials/kubernetes-basics/scale/scale-intro/)
- [kubectl scale](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_scale/)
- [K8S HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
