# Kubernetes

<div class="dedication">
I want to dedicate this page to Myself!
</div>

---

Kubernetes automates operational tasks of container management and includes built-in commands for deploying applications, rolling out changes to your applications, scaling your applications up and down to fit changing needs, monitoring your applications, and more—making it easier to manage applications. Kubernetes is written in `Go`.

The most useful feature of Kubernetes is that it can deploy your applications on more than one physical node. It has a scheduler that manages your deployments on nodes.

Where you run Kubernetes is up to you. This can be on bare metal servers, virtual machines (VMs), public cloud providers, private clouds, and hybrid cloud environments. One of Kubernetes' key advantages is it works on many different kinds of infrastructure.

Kubernetes has a control plane (formerly called the master) on which the main components run. Other nodes are worker nodes that communicate with the control plane through the `kubelet`.

The main Kubernetes components are listed below:

- Kube API server (control plane): connects all of the components together
- Kube Scheduler (control plane): sets up pods on nodes
- Kube Controller Manager (control plane): contains all controllers that perform system logic
- etcd (control plane): a key-value database
- Kubelet (worker): manages pods on each node
- Kube Proxy (worker): manages each node's network interface
- Container runtime (worker): containerd, CRI-O, and others that implement the CRI
- Persistent storage: volumes that outlive pods
- Container registry: stores and lets you distribute container images (an external service)

<div align="center">
    <img src="https://www.redhat.com/rhdc/managed-files/kubernetes_diagram-v3-770x717_0_0_v2_0.svg" width="500" />
</div>
