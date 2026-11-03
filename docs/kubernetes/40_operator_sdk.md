# Operator SDK

## Quick Description (QD)

The **Operator SDK** is a framework for building Kubernetes Operators. It provides tools, libraries, and code generation to help you develop, test, package, and deploy Operators using Go, Ansible, or Helm. Under the hood, the Go plugin is built on [Kubebuilder](https://book.kubebuilder.io/) and controller-runtime.

### Key Concepts

- **Operator:** A controller that manages a custom resource and automates application lifecycle tasks.
- **Custom Resource Definition (CRD):** Extends the Kubernetes API with new resource types.
- **Controller:** Watches for changes to resources and reconciles the actual state to the desired state.

### Common Kubernetes Objects Used

- **CustomResourceDefinition (CRD):** Defines new resource types.
- **Deployment:** Runs the Operator controller.
- **ServiceAccount, Role, RoleBinding:** RBAC for Operator permissions.
- **ClusterServiceVersion (CSV):** OLM metadata for Operator versioning.
- **Subscription:** Tells OLM to install or upgrade an Operator.
- **InstallPlan:** OLM's plan for installing or upgrading Operators.

### Bundles and Catalogs

A **bundle** is a packaging format for Operators. It contains manifests for the Operator, CRDs, RBAC, and metadata.

A **catalog** is a collection of Operator bundles, used by OLM to manage Operator installation and upgrades.

### ClusterServiceVersions (CSVs)

A **ClusterServiceVersion (CSV)** is a YAML manifest used by OLM to describe an Operator, its version, permissions, install strategy, and owned CRDs. OLM uses CSVs to manage Operator installation, upgrades, and lifecycle.

### Upgrade Workflow

1. **Update the catalog:** Build and push a new bundle and update your catalog image with the new bundle version.
2. **OLM detects the new version:** OLM watches the catalog for new CSVs. When a new version is available, OLM creates a new InstallPlan.
3. **InstallPlan execution:** The InstallPlan creates or updates resources (Deployments, CRDs, RBAC, etc.) as defined in the new CSV.
4. **CSV status:** The new CSV transitions through phases: `Pending` → `InstallReady` → `Installing` → `Succeeded`.
5. **Operator pod update:** The Operator Deployment is updated, and new pods are rolled out.

### Events and Workflow

- **Subscription** triggers OLM to check the catalog for updates.
- **InstallPlan** is created for new CSVs.
- **CSV** is installed and transitions through phases.
- **Deployment** for the Operator is updated.
- **Pods** are rolled out for the new Operator version.

## Installation

```shell
brew install operator-sdk
```

Or see the [Operator SDK installation guide](https://sdk.operatorframework.io/docs/installation/) for release binaries. The `opm` tool used below comes from the [operator-registry](https://github.com/operator-framework/operator-registry) project.

## Useful Tips/Commands (UToC)

### Useful Commands

```shell
operator-sdk init ...
operator-sdk create api ...
operator-sdk olm install               # install OLM into the cluster
operator-sdk run bundle <bundle-image> # install a bundle through OLM
operator-sdk cleanup <operator-name>   # remove what run bundle installed
operator-sdk bundle validate ./bundle
kubectl get crd
```

### Useful kubectl Commands

List CSVs in a namespace:

```shell
kubectl get csv -n <namespace>
```

Describe a CSV (see status, conditions, errors):

```shell
kubectl describe csv <csv-name> -n <namespace>
```

List InstallPlans:

```shell
kubectl get installplan -n <namespace>
```

Describe an InstallPlan:

```shell
kubectl describe installplan <installplan-name> -n <namespace>
```

List Subscriptions (controls the upgrade channel):

```shell
kubectl get subscription -n <namespace>
```

Describe a Subscription:

```shell
kubectl describe subscription <subscription-name> -n <namespace>
```

### Debugging and Troubleshooting

- **Check CSV status:** Look for errors or failed phases in the CSV.
- **Check the InstallPlan:** Ensure all steps completed successfully.
- **Check Operator pod logs:**

  ```shell
  kubectl get pods -n <namespace> -l name=<operator-name>
  kubectl logs <pod-name> -n <namespace>
  ```

- **Check OLM pods:** OLM runs in the `olm` namespace.

  ```shell
  kubectl get pods -n olm
  kubectl logs <olm-pod> -n olm
  ```

- **Check events:**

  ```shell
  kubectl get events -n <namespace>
  ```

### Typical Pods to Check

- **Operator pod:** The main pod running your Operator logic.
- **OLM pods:** `olm-operator`, `catalog-operator`, `operator-lifecycle-manager`, etc. in the `olm` namespace.
- **Catalog source pod:** If using a custom catalog, check the pod serving your catalog image.

## Examples (e.g.,)

### Initialize a New Operator Project

```shell
operator-sdk init --domain=example.com --repo=github.com/example/memcached-operator
```

- `--domain`: The API group domain (e.g., `cache.example.com`).
- `--repo`: The Go module path for your project.

### Create an API and Controller

```shell
operator-sdk create api --group=cache --version=v1 --kind=Memcached --resource --controller
```

- This generates CRD manifests, API types, and a controller scaffold.

### Implement Reconcile Logic

Edit the generated controller code (in `internal/controller/` in recent scaffolds, `controllers/` in older ones) to define how your Operator manages resources.

### Build and Run Locally

```shell
make install   # Install CRDs into the cluster
make run       # Run the operator locally (uses your kubeconfig)
```

### Deploy to Cluster

Build and push your Operator image:

```shell
make docker-build docker-push IMG=<your-registry>/memcached-operator:tag
```

Deploy to the cluster:

```shell
make deploy IMG=<your-registry>/memcached-operator:tag
```

### Operator Lifecycle Manager (OLM), Bundles, and Catalogs

Generate a bundle:

```shell
make bundle
```

Validate the bundle:

```shell
operator-sdk bundle validate ./bundle
```

Build a catalog image. `opm index add` is deprecated in favor of file-based catalogs (`opm render` / `opm generate dockerfile`), but still works with older OLM versions:

```shell
opm index add --bundles <bundle-image> --tag <catalog-image>
```

Push the catalog image to a registry.

To deploy with OLM:

- Install OLM in your cluster (`operator-sdk olm install`, or see the [OLM getting started guide](https://olm.operatorframework.io/docs/getting-started/)).
- Deploy your Operator from a catalog using OLM.

## References

- [Operator SDK Documentation](https://sdk.operatorframework.io/docs/)
- [OLM Documentation](https://olm.operatorframework.io/docs/)
- [Operator SDK Go Tutorial](https://sdk.operatorframework.io/docs/building-operators/golang/tutorial/)
- [Kubebuilder Book](https://book.kubebuilder.io/)
- [OperatorHub.io](https://operatorhub.io/)
