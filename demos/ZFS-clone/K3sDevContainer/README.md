# Optimizing the Inner Loop with Conan and ZFS in Remote DevContainers - Demo

Inspired by:
- Botha, Dr. Charl P., vxlabs (2021).

  ["Using Kubernetes for development containers"](https://vxlabs.com/2021/11/21/using-kubernetes-for-development-containers)

Read the article on the demo here:

- https://daversomethingsomethingorg.github.io/ConanToolchain/latest/ConanK8sDevContainerDemo/

## [`devContainer-pod.yaml`](./devContainer-pod.yaml)

Kubernetes YAML manifests for provisioning a single DevContainer Pod with
our source repo cloned from GitHub and our OpenEBS ZFS Conan Cache
mounted.  Ready for VS Code to attach to remotely.

## [`upgrade-devContainer.sh`](./upgrade-devContainer.sh)

Simple shell script to deploy our DevContainer Pod in our Kubernetes
cluster.
