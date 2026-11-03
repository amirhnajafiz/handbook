# Blue-Green Deployment

<div class="dedication">
I want to dedicate this page to Elizabeth Hargrave (Wingspan creator)!
</div>

---

## Quick Description (QD)

**Blue-Green Deployment** is a deployment pattern that reduces downtime and risk by running two identical production environments, called **blue** and **green**. At any given time, only one environment (blue or green) is live and serving production traffic.

<img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/0*Tp58tyzgHLBSA_xp.png" width="500" />

### How It Works

1. **Blue environment:** The current production environment serving all user traffic.
2. **Green environment:** The new version of the application is deployed here. It is kept isolated from users until it is fully tested and ready.
3. **Switch over:** Once the green environment passes all tests, traffic is switched from blue to green, typically by updating a Kubernetes Service selector or changing DNS records.
4. **Rollback:** If issues are detected, you can quickly revert traffic back to the blue environment.

### Benefits

- **Near-zero downtime:** Users experience little to no interruption during deployment.
- **Easy rollback:** Quickly revert to the previous version if problems occur.
- **Safe testing:** The new version can be tested in a production-identical environment before going live.

### When to Use Blue-Green Deployment

- When you need zero-downtime deployments.
- When rollback speed is critical.
- For stateless applications or those with minimal data migration needs.

### When to Consider Alternatives

- For stateful applications with complex data requirements.
- When database schema changes are involved.
- When gradual rollout and monitoring are preferred (consider canary or rolling updates).

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

### Considerations in Kubernetes

1. **Storage:** If your application requires persistent storage, ensure both blue and green deployments use the same PersistentVolume (PV) or PersistentVolumeClaim (PVC). Otherwise, you may risk data loss or inconsistency during the switch.
2. **DNS and Service switching:**
   - If using a custom domain, update DNS records to point to the new environment.
   - In Kubernetes, you can update the `selector` field of a Service to point to the new deployment (green), instantly switching traffic.
3. **Testing:** Before switching traffic, thoroughly test the green deployment, for example through a separate Service or port-forward. Canary deployments are a different strategy for gradually shifting traffic.
4. **Resources:** Both environments run at the same time during the switch, so the cluster needs capacity for roughly double the replicas.
5. **Database migrations and stateful applications:** see [When to Consider Alternatives](#when-to-consider-alternatives). Schema changes must stay compatible with both versions during the switch.

## Examples (e.g.,)

### Blue-Green Deployment in Kubernetes

#### 1. Deploy Blue and Green Environments

```yaml
# blue-deployment.yaml (save the two Deployments in separate files)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: myapp
        image: myapp:1.0
---
# green-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: myapp
        image: myapp:2.0
```

#### 2. Service Definition

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
    version: blue   # Change to 'green' to switch traffic
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

#### 3. Switch Traffic

Apply the manifests (`kubectl apply -f blue-deployment.yaml -f green-deployment.yaml -f service.yaml`) and check that the green pods are ready (`kubectl get pods -l version=green`). To switch from blue to green, update the Service selector:

```shell
kubectl patch service myapp-service -p '{"spec":{"selector":{"app":"myapp","version":"green"}}}'
```

#### 4. Rollback

If issues are found, revert the selector back to blue:

```shell
kubectl patch service myapp-service -p '{"spec":{"selector":{"app":"myapp","version":"blue"}}}'
```

## References

- [BlueGreenDeployment (Martin Fowler)](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Zero-downtime Deployment in Kubernetes with Jenkins](https://kubernetes.io/blog/2018/04/30/zero-downtime-deployment-kubernetes-jenkins/)
- [Kubernetes Service Documentation](https://kubernetes.io/docs/concepts/services-networking/service/)
