#!/bin/bash

######################################################################
# postCreate.sh
#
# Copyright © 2025 David L. Armstrong
#
# This script installs Docker-CE and GitHub gh client and the ACT
# extension for running and testing GitHub Actions workflows locally
#

. /etc/os-release

case "${ID}" in
    ubuntu | debian)
        # Official `python` image is Debian based.
        export DEBIAN_FRONTEND=noninteractive
        apt-get install --no-install-recommends -y \
            gh
# TODO            docker-ce \
        gh extension install nektos/gh-act
        ;;
    almalinux)
        # For RH* support we use AlmaLinux
        ;;

    # Otherwise assume the container image comes fully loaded I guess
esac

# Common stuff
