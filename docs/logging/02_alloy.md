# Grafana Alloy

## Quick Description (QD)

Alloy is a flexible, high-performance, vendor-neutral distribution of the OpenTelemetry Collector. It's fully compatible with the most popular open-source observability standards, such as OpenTelemetry and Prometheus. Alloy focuses on ease of use and the ability to adapt to the needs of power users.

### Features

Some of the key features of Alloy include:

- Custom components: you can use Alloy to create and share custom components. Custom components combine a pipeline of existing components into a single, easy-to-understand component that's just a few lines long. You can use pre-built custom components from the community, ones packaged by Grafana, or create your own.
- Reusable components: you can use the output of a component as the input for multiple other components.
- Chained components: you can chain components together to form a pipeline.
- Single task per component: the scope of each component is limited to one specific task.
- GitOps compatibility: Alloy uses frameworks to pull configurations from Git, S3, HTTP endpoints, and just about any other source.
- Clustering support: Alloy has native clustering support. Clustering helps distribute the workload and ensures you have high availability. You can quickly create horizontally scalable deployments with minimal resource and operational overhead.
- Security: Alloy helps you manage authentication credentials and connect to HashiCorp Vaults or Kubernetes clusters to retrieve secrets.
- Debugging utilities: Alloy provides troubleshooting support and an embedded user interface to help you identify and resolve configuration problems.

<img src="docs/logging/images/flow-diagram-small-alloy.png" width="600" />

#### Collect

Alloy uses components to collect telemetry data from applications, databases, and OpenTelemetry collectors. Alloy supports collection using multiple ecosystems, including OpenTelemetry and Prometheus.

Telemetry data can be either pushed to Alloy, or Alloy can pull it from your data sources.

#### Transform

Alloy processes data and transforms it for sending. You can use transformations to inject extra metadata into telemetry or filter out unwanted data.

#### Write

Alloy sends data to OpenTelemetry-compatible databases or collectors, the Grafana stack, or Grafana Cloud. Alloy can also write alerting rules in compatible databases.

## Installation

_Nothing here yet._

## Useful Tips/Commands (UToC)

_Nothing here yet._

## Examples (e.g.,)

_Nothing here yet._

## References

- [Grafana Alloy documentation](https://grafana.com/docs/alloy/latest/)
- [Collect logs in Kubernetes with Grafana Alloy](https://grafana.com/docs/alloy/latest/collect/logs-in-kubernetes/)
