# Conan and ZFS and Kubernetes CI (Oh my!) - Demo

Read the article here:

- https://daversomethingsomethingorg.github.io/ConanToolchain/latest/ConanK8sARCDemo/

## GitHub ARC Controller Configuration

### [`controller/values.yaml`](./controller/values.yaml)

Typical GitHub ARC Controller Helm chart `values.yaml` with no
special configuration options.

### Controller Maintenance scripts

- [`install-controller.sh`](./install-controller.sh)
- [`upgrade-controller.sh`](./upgrade-controller.sh)

## GitHub ARC Cluster RunnerScaleSet Configuration

### [`clusters/values.yaml`](./clusters/values.yaml)

Helm chart `values.yaml` file to configure our GitHub ARC RunnerScaleSet
Fairly standard configuration for `containerMode: kubernetes` operation
with a container hook template extension specified.

### [`hookExtensionConfigMap.yaml`](./hookExtensionConfigMap.yaml)

Manifest for a Kubernetes ConfigMap intended for mounting by our Runner
containers in order to extend the spec for the Workflow $job container
deployed by our Runner container.

### [`certConfigMap.yaml`](./certConfigMap.yaml)

Manifest for a Kubernetes ConfigMap intended for mounting by our Runner
containers in order to recognize the certificates of our internal services.

Reference:

- [GitHub ARC Tutorials - Custom TLS certificates](https://docs.github.com/en/actions/tutorials/use-actions-runner-controller/deploy-runner-scale-sets#custom-tls-certificates)

### RunnerScaleSet Maintenance scripts

- [`install-clusters.sh`](./install-clusters.sh)
- [`upgrade-clusters.sh`](./upgrade-clusters.sh)
- [`uninstall-clusters.sh`](./uninstall-clusters.sh)
