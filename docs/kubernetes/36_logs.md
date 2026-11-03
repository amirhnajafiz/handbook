# Centralized Logs in Kubernetes

## Quick Description (QD)

Kubernetes does not ship a built-in storage for logs: container logs live on the node and are lost when the pod is evicted or the node goes away (`kubectl logs` only reads them from the node). Centralized logging in Kubernetes involves deploying a [DaemonSet](26_daemonset.md) for a logging agent that collects logs from all pods and nodes, then forwards them to one or more log storage backends. This approach enables you to aggregate, search, and analyze logs from across your entire cluster in a single place.

### How It Works

1. **Log collection:** A logging agent (e.g., Fluent Bit, Filebeat) runs as a DaemonSet on each node, collecting logs from containers and system components.
2. **Log forwarding:** The agent forwards logs to a central log processor or directly to a storage backend (e.g., Elasticsearch, Graylog).
3. **Storage and analysis:** Logs are indexed and stored in a backend (Elasticsearch, Graylog, Loki, etc.), where they can be searched, visualized, and analyzed.

### Popular Centralized Logging Solutions

- **ELK Stack (Elasticsearch, Logstash, Kibana):** The most well-known solution. Logstash collects and processes logs, Elasticsearch stores them, and Kibana provides dashboards and search.

  *Note:* Logstash can be resource-intensive. Alternatives like Filebeat, Fluentd, and Fluent Bit are often used as lighter log shippers.

- **Graylog:** An open-source log management platform with real-time search, alerting, and dashboards. It stores logs in OpenSearch (or Elasticsearch, depending on the version) and keeps its metadata in MongoDB. It can receive logs in the GELF format used in the example below.
- **Fluentd and Fluent Bit:** Both are log collectors and forwarders. Fluent Bit is a lightweight, high-performance alternative to Fluentd, suitable for resource-constrained environments. Fluentd offers more plugins and flexibility, while Fluent Bit is easier to deploy and maintain.

### Other Notable Solutions

- **Loki (Grafana):** Indexes only labels instead of the full log text, which keeps storage cheap, and integrates with Grafana dashboards.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

### Fluent Bit and Graylog

- **Fluent Bit** collects logs from all pods and forwards them to Graylog.
- **Graylog** provides a web UI for searching, alerting, and dashboarding.

#### Fluent Bit DaemonSet Example

The agent needs a configuration that tails the container log files and sends them to Graylog. It is mounted from a ConfigMap (`/fluent-bit/etc/fluent-bit.conf` is where the official image reads its config):

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: logging
data:
  fluent-bit.conf: |
    [INPUT]
        Name    tail
        Tag     kube.*
        Path    /var/log/containers/*.log
        multiline.parser docker, cri

    [OUTPUT]
        Name                    gelf
        Match                   kube.*
        Host                    ${GRAYLOG_HOST}
        Port                    ${GRAYLOG_PORT}
        Mode                    tcp
        Gelf_Short_Message_Key  log
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluent-bit
  namespace: logging
spec:
  selector:
    matchLabels:
      k8s-app: fluent-bit
  template:
    metadata:
      labels:
        k8s-app: fluent-bit
    spec:
      containers:
      - name: fluent-bit
        image: fluent/fluent-bit:<version>
        env:
        - name: GRAYLOG_HOST
          value: "graylog.logging.svc.cluster.local"
        - name: GRAYLOG_PORT
          value: "12201"
        volumeMounts:
        - name: config
          mountPath: /fluent-bit/etc/fluent-bit.conf
          subPath: fluent-bit.conf
        - name: varlog
          mountPath: /var/log
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: fluent-bit-config
      - name: varlog
        hostPath:
          path: /var/log
```

Replace `<version>` with a pinned Fluent Bit release instead of `latest`. The files in `/var/log/containers` are symlinks into `/var/log/pods`, so mounting `/var/log` covers containerd and CRI-O. With the legacy Docker runtime you also have to mount `/var/lib/docker/containers`. For metadata such as pod and namespace names, add the Fluent Bit `kubernetes` filter (this also needs a ServiceAccount with read access to pods). The Graylog side needs a GELF TCP input listening on the chosen port.

## References

- [Logging Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
- [Fluent Bit Documentation](https://docs.fluentbit.io/)
- [Fluent Bit GELF Output](https://docs.fluentbit.io/manual/pipeline/outputs/gelf)
- [Graylog Documentation](https://docs.graylog.org/)
- [Grafana Loki Documentation](https://grafana.com/docs/loki/latest/)
