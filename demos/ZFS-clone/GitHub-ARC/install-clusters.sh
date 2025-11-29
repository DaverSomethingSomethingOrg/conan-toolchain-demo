#!/bin/bash

export KUBECONFIG=/home/dave/.kube/config

CONFIG_DIR="/home/dave/projects/GitHub-ARC"

#INSTALLATION_NAME="github-arc-runner-set"
INSTALLATION_NAME="linux-x86-64"
#NAMESPACE="github-arc-runners"
NAMESPACE="devcontainer"

# Set up our Internal CA Certificate chain ConfigMap
kubectl apply \
  --filename "${CONFIG_DIR}/certConfigMap.yaml" \
  --namespace "${NAMESPACE}"

# Set up our container hooks for ZFS volume mounting
kubectl apply \
  --filename "${CONFIG_DIR}/hookExtensionConfigMap.yaml" \
  --namespace "${NAMESPACE}"

#github-arc-container-hooks

helm install "${INSTALLATION_NAME}" \
    -f "${CONFIG_DIR}/clusters/values.yaml" \
    --namespace "${NAMESPACE}" \
    --create-namespace \
    oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set

