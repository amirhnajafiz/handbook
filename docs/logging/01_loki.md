# Grafana Loki

Loki is a horizontally scalable, highly available, multi-tenant log aggregation system inspired by Prometheus. It is designed to be very cost effective and easy to operate. It does not index the contents of the logs, but rather a set of labels for each log stream.

![loki](logging/images/loki-diagram.png)

To collect logs and view your log data generally involves the following steps:

1. Install Loki on Kubernetes in simple scalable mode, using the recommended Helm chart. Supply the Helm chart with your object storage authentication details.
    - Storage options
    - Configuration reference
2. Deploy Grafana Alloy to collect logs from your applications.
    - On Kubernetes, deploy Grafana Alloy using the Helm chart. Configure Grafana Alloy to scrape logs from your Kubernetes cluster, and add your Loki endpoint details. Refer to the following section for an example Grafana Alloy configuration file.
    - Add labels to your logs following our best practices. Most Loki users start by adding labels that describe where the logs are coming from such as region, cluster, or environment.
3. Deploy Grafana or Grafana Cloud and configure a Loki data source.
4. Select the Explore feature in the Grafana main menu. To view logs in Explore:
    - Pick a time range.
    - Choose the Loki data source.
    - Use LogQL in the query editor, use the Builder view to explore your labels, or select from sample pre-configured queries using the Kick start your query button.

## Methods of deployment

The Loki chart supports three methods of deployment:

- Monolithic: The simplest mode of operation is the monolithic deployment mode. You enable monolithic mode by setting the `-target=all` command line parameter. This mode runs all of Loki’s microservice components inside a single process as a single binary or Docker image.
- Simple Scalable: The simple scalable deployment is the default configuration installed by the Loki Helm Chart. This deployment mode is the easiest way to deploy Loki at scale. It strikes a balance between deploying in monolithic mode or deploying each component as a separate microservice. Simple scalable deployment is also referred to as SSD. Loki’s simple scalable deployment mode separates execution paths into read, write, and backend targets. These targets can be scaled independently, letting you customize your Loki deployment to meet your business needs for log ingestion and log query so that your infrastructure costs better match how you use Loki.
- Microservice: The microservices deployment mode runs components of Loki as distinct processes. The microservices deployment is also referred to as a Distributed deployment. Each process is invoked specifying its target. 

## Architecture

Grafana Loki has a microservices-based architecture and is designed to run as a horizontally scalable, distributed system. The system has multiple components that can run separately and in parallel. The Grafana Loki design compiles the code for all components into a single binary or Docker image. The -target command-line flag controls which component(s) that binary will behave as.

To get started easily, run Grafana Loki in “single binary” mode with all components running simultaneously in one process, or in “simple scalable deployment” mode, which groups components into read, write, and backend parts.

Grafana Loki is designed to easily redeploy a cluster under a different mode as your needs change, with no configuration changes or minimal configuration changes.

![loki-components](logging/images/loki_architecture_components.svg)

## References

- [https://grafana.com/docs/loki/latest/get-started/architecture/](https://grafana.com/docs/loki/latest/get-started/architecture/)
- [https://grafana.com/docs/loki/latest/setup/install/helm/concepts/](https://grafana.com/docs/loki/latest/setup/install/helm/concepts/)
- [https://github.com/grafana/helm-charts](https://github.com/grafana/helm-charts)
