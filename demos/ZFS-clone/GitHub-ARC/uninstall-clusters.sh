#!/bin/bash

export KUBECONFIG=/home/dave/.kube/config

CONFIG_DIR="/home/dave/projects/GitHub-ARC"

#INSTALLATION_NAME="github-arc-runner-set"
INSTALLATION_NAME="linux-x86-64"
#NAMESPACE="github-arc-runners"
NAMESPACE="devcontainer"

helm uninstall "${INSTALLATION_NAME}" \
    --namespace "${NAMESPACE}"

# --kubeconfig string
