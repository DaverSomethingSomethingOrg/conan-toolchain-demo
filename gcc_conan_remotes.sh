#!/bin/bash

CONAN_CENTER_PROXY=""
CONAN_LOCAL_RECIPES="components/gcc-toolchain-recipes"
CONAN_LOCAL_REPO="https://nexus.homelab/repository/conan-homelab"

if [ -n "${CONAN_CENTER_PROXY}" ]; then
  conan remote disable conancenter
  conan remote add conan-center-proxy "${CONAN_CENTER_PROXY=}"
  conan remote update conan-center-proxy --index 0
fi

if [ -n "${CONAN_LOCAL_RECIPES}" ]; then
  conan remote remove conan-local-recipes >/dev/null 2>&1 || /bin/true
  conan remote add -t local-recipes-index conan-local-recipes "${CONAN_LOCAL_RECIPES}"
  conan remote update conan-local-recipes --index 0
fi

if [ -n "${CONAN_LOCAL_REPO}" ]; then
  conan remote remove conan-local-repo >/dev/null 2>&1 || /bin/true
  conan remote add conan-local-repo "${CONAN_LOCAL_REPO}"
  conan remote update conan-local-repo --index 0
fi

conan remote list
