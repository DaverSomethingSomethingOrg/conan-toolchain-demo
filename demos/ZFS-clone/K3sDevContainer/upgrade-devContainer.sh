#!/bin/bash

export KUBECONFIG=/home/dave/.kube/config

CONFIG_DIR="/home/dave/projects/K3sDevContainer"

#NAMESPACE="github-arc-runners"
NAMESPACE="devcontainer"

kubectl delete pod \
    --namespace "${NAMESPACE}" \
    devcontainer-pod

kubectl apply \
    --namespace "${NAMESPACE}" \
    -f "${CONFIG_DIR}/devContainer-pod.yaml"
