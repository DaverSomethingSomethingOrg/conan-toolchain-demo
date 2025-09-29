#!/bin/sh

conan profile detect
conan config install https://github.com/DaverSomethingSomethingOrg/conan-system-packaging.git

conan remote add -t local-recipes-index conan-local-recipes "${CONTAINER_WORKSPACE_ROOT}/conan-center-index"
conan remote update conan-local-recipes --index 0

# Enable conan-local-repo to download from our Nexus Artifact Management
#conan remote add conan-local-repo https://nexus.homelab/repository/conan-homelab
#conan remote update conan-local-repo --index 0

set -e

conan install --build=missing \
              --options="*:install_prefix=${INSTALL_PREFIX}" \
              --conf:all="tools.system.package_manager:mode=install" \
              "${COMPONENT_SUBDIR}"
#              --options:all="*:install_prefix=${INSTALL_PREFIX}" \

# conan install --deployer-folder="${COMPONENT_SUBDIR}/deb_deploy" \
#                 --deployer=deb_deployer \
#                 --options="*:install_prefix=${INSTALL_PREFIX}" \
#                 "${COMPONENT_SUBDIR}"
