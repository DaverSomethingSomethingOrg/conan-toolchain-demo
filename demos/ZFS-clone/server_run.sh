#!/bin/sh

######################################################################
# Setup and Initialization
#
# Make sure the zpool already exists first!
#
# In this example we have pre-allocated a ZFS pool named
# `zpool-conancache` mounted as `/zpool-conancache`. (see `init.sh`)
#

# Input Args
BUILD_ID=$1
BUILD_BREAKER=$2

if [ -z "${BUILD_BREAKER}" ]; then
    echo "Usage: $0 <build id> <build status>" 1>&2
    exit 1
fi

# Toplevel Configuration
PROJECT="gcc12-toolchain"
BRANCH="main"
JOB_HOST="hephaestus"
REPO_NAME="conan-toolchain-demo"
ZPOOL_NAME="zpool-conancache"
SAVE_BROKEN_BUILDS=1

# Project-specific structure
SERVER_WORKSPACE_ROOT="/home/dave/projects/ConanCache/${REPO_NAME}"
CONTAINER_WORKSPACE_ROOT="/workspaces/${REPO_NAME}"
WORKSPACE_SUBDIR="demos/gcc-toolchain/phase3"
#INSTALL_PREFIX="/opt/${PROJECT}"
INSTALL_PREFIX="/opt/toolchain"

# ZFS layout / structure
PROJECT_DATASET="${ZPOOL_NAME}/${PROJECT}"
BRANCH_DATASET="${PROJECT_DATASET}/${BRANCH}"

BUILD_CLONE="${BRANCH_DATASET}_${JOB_HOST}-${BUILD_ID}"
BUILD_SNAPSHOT="${BRANCH_DATASET}@${JOB_HOST}-pre${BUILD_ID}"

CONTAINER_CONAN_HOME="/CONAN_HOME"
CONAN_BUILD_SCRIPT="conan_build.sh"

set -x

# If our build clone already exists something is wrong..
#TODO allow re-run?  New JobID?
CLONE_FOUND=$(sudo zfs list -o name |grep "^${BUILD_CLONE}\$")
if [ $? -eq 0 ]; then
    echo "ERROR: Build clone already exists.  Cannot proceed!" 1>&2
    exit 1
fi

# Create our ZFS branch dataset if it doesn't already exist
BRANCH_DATASET_FOUND=$(sudo zfs list -o name |grep "^${BRANCH_DATASET}\$")
if [ $? -eq 1 ]; then
    # Use '-p' to create branch dataset if it doesn't exist as well
    sudo zfs create -p "${BRANCH_DATASET}"
fi

# Create a new clone for our build's use - potentially concurrent!
sudo zfs snapshot "${BUILD_SNAPSHOT}"
sudo zfs clone "${BUILD_SNAPSHOT}" "${BUILD_CLONE}"

# Run the build
DOCKER_IMAGE="nexus.homelab/conan-docker-build-ubuntu:x86_64-latest"
docker run -it --rm \
    --volume="/${BUILD_CLONE}:${CONTAINER_CONAN_HOME}" \
    --volume="${SERVER_WORKSPACE_ROOT}:${CONTAINER_WORKSPACE_ROOT}" \
    --env="CONAN_HOME=${CONTAINER_CONAN_HOME}" \
    --env="INSTALL_PREFIX=${INSTALL_PREFIX}" \
    --env="CONTAINER_WORKSPACE_ROOT=${CONTAINER_WORKSPACE_ROOT}" \
    --env="COMPONENT_SUBDIR=${CONTAINER_WORKSPACE_ROOT}/${WORKSPACE_SUBDIR}" \
    "${DOCKER_IMAGE}" \
    "${CONTAINER_WORKSPACE_ROOT}/${CONAN_BUILD_SCRIPT}"

# Detect build failures
retval=$?

# For this demo we can mark the build broken regardless
if [ ${BUILD_BREAKER} -ne 0 ]; then
    retval=${BUILD_BREAKER}
fi

set -x

if [ ${retval} -eq 0 ]; then
    # Build succeeded - Promote build clone to branch@latest
    echo "SUCCESS! Updating snapshot"

    # Promote our successful build and rename it to replace our previous
    sudo zfs promote "${BUILD_CLONE}"
    sudo zfs rename "${BRANCH_DATASET}" "${BRANCH_DATASET}-legacy"
    sudo zfs rename "${BUILD_CLONE}" "${BRANCH_DATASET}"

    # Finally, clean up the legacy dataset/snapshot
    sudo zfs destroy "${BRANCH_DATASET}-legacy"
    sudo zfs destroy "${BUILD_SNAPSHOT}"
else
    # Build failed - rollback to previous state using "latest" snapshot
    echo "FAILURE!"

    # If not configured to save broken builds, destroy the broken clone
    # and snapshot
    if [ ${SAVE_BROKEN_BUILDS} -eq 0 ]; then
        # No rollback needed, just destroy our "temporary" clone&snapshot without promoting them
        sudo zfs destroy "${BUILD_CLONE}"
        sudo zfs destroy "${BUILD_SNAPSHOT}"
    fi
fi
