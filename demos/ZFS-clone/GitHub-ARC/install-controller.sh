#!/bin/bash

export KUBECONFIG=/home/dave/.kube/config

CONFIG_DIR="/home/dave/projects/GitHub-ARC"
#WORKING_DIR="/export/disk0/services/GitHub-ARC"

# https://github.com/actions/actions-runner-controller/tree/master/charts/gha-runner-scale-set-controller
#
NAMESPACE="github-arc-systems"
helm install github-arc \
    -f "${CONFIG_DIR}/controller/values.yaml" \
    --namespace "${NAMESPACE}" \
    --create-namespace \
    oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller

