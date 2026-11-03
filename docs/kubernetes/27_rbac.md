# RBAC

## Quick Description (QD)

Role-based access control (RBAC) is a method of regulating access to computer or network resources based on the roles of individual users within your organization.

RBAC authorization uses the `rbac.authorization.k8s.io` API group to drive authorization decisions, allowing you to dynamically configure policies through the Kubernetes API.

The RBAC API declares four kinds of Kubernetes object:

- Role
- ClusterRole
- RoleBinding
- ClusterRoleBinding

An RBAC Role or ClusterRole contains rules that represent a set of permissions. Permissions are purely additive (there are no "deny" rules).

A Role always sets permissions within a particular namespace; when you create a Role, you have to specify the namespace it belongs in.

ClusterRole, by contrast, is a non-namespaced resource. The resources have different names (Role and ClusterRole) because a Kubernetes object always has to be either namespaced or not namespaced; it can't be both.

ClusterRoles have several uses. You can use a ClusterRole to:

- Define permissions on namespaced resources and be granted access within individual namespaces
- Define permissions on namespaced resources and be granted access across all namespaces
- Define permissions on cluster-scoped resources

### Role bindings

A role binding grants the permissions defined in a role to a user or set of users. It holds a list of subjects (users, groups, or service accounts) and a reference to the role being granted. A RoleBinding grants permissions within a specific namespace, whereas a ClusterRoleBinding grants that access cluster-wide.

A RoleBinding may reference any Role in the same namespace. Alternatively, a RoleBinding can reference a ClusterRole and bind that ClusterRole to the namespace of the RoleBinding.

If you want to bind a ClusterRole to all the namespaces in your cluster, you use a ClusterRoleBinding.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

Check what a user can do, and create the same objects imperatively:

```sh
kubectl auth can-i list pods --namespace default --as jane
kubectl create role pod-reader --verb=get,list,watch --resource=pods -n default
kubectl create rolebinding read-pods --role=pod-reader --user=jane -n default
```

- RBAC is additive: if no rule allows an action, it is denied.
- You cannot change the `roleRef` of an existing binding; delete and recreate it.
- A user cannot create or edit a Role unless they already hold the permissions it grants (privilege escalation prevention).

## Examples (e.g.,)

A Role that allows reading Pods in the `default` namespace:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
# This role binding allows "jane" to read pods in the "default" namespace.
# You need to already have a Role named "pod-reader" in that namespace.
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
# You can specify more than one "subject"
- kind: User
  name: jane # "name" is case sensitive
  apiGroup: rbac.authorization.k8s.io
roleRef:
  # "roleRef" specifies the binding to a Role / ClusterRole
  kind: Role # this must be Role or ClusterRole
  name: pod-reader # this must match the name of the Role or ClusterRole you wish to bind to
  apiGroup: rbac.authorization.k8s.io
```

## References

- [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Authorization Overview](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)
