# Environment Variables

## Quick Description (QD)

Environment variables are a set of key-value pairs that can be set inside a Pod's container as local env variables.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

Check the variables inside the container:

```sh
kubectl exec envar-demo -- printenv DEMO_GREETING
```

Values can also come from a ConfigMap or a Secret, see [ConfigMap](11_configmap.md) and [Secrets](12_secrets.md).

## Examples (e.g.,)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: envar-demo
  labels:
    purpose: demonstrate-envars
spec:
  containers:
  - name: envar-demo-container
    image: gcr.io/google-samples/node-hello:1.0
    env:
    - name: DEMO_GREETING
      value: "Hello from the environment"
    - name: DEMO_FAREWELL
      value: "Such a sweet sorrow"
```

## References

- [Define Environment Variables for a Container](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)
