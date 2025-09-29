#!/bin/sh

# Initialize toplevel ZFS Pool for all Conan Cache operations
zpool destroy zpool-conancache
zpool create zpool-conancache /dev/nvme0n1p7

# We do NOT want to be tracking access time here
zfs set atime=off zpool-conancache
