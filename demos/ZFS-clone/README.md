# Optimizing C/C++ Build Performance using Conan and OpenZFS - Demo

This demo provides a few simple scripts to demonstrate use of OpenZFS
dataset clones to optimize Conan build performance and storage space
usage.  OpenZFS also enables sharing of a single conan cache across
multiple concurrent users without any race condition concerns from
sharing a Conan cache that is not concurrent-safe.

- https://github.com/conan-io/conan/issues/15840

## [`init.sh`](./init.sh)

Nothing special here, just (re)initializing our ZFS pool on our HomeLab
server's NVMe SSD for this demo.  Turning off `atime` is important for
maximum performance!

```bash
❯ sudo ./init.sh
❯ zfs list -r -o name,used,avail,refer
NAME               USED  AVAIL  REFER
zpool-conancache   114K   189G    24K
❯ zfs list -t snapshot -o name,used,refer
no datasets available
❯
```

## [`conan_build.sh`](./conan_build.sh)

Convenience script for setting up our Conan build environment and running
the toolchain build.  It configures our profile, remotes and executes
`conan install --build=missing [...]`

```bash
❯ DOCKER_IMAGE="nexus.homelab/conan-docker-build-ubuntu:x86_64-latest"
❯ docker run -it --rm \
    --volume="/${BUILD_CLONE}:${CONTAINER_CONAN_HOME}" \
    --volume="${SERVER_WORKSPACE_ROOT}:${CONTAINER_WORKSPACE_ROOT}" \
    --env="CONAN_HOME=${CONTAINER_CONAN_HOME}" \
    --env="INSTALL_PREFIX=${INSTALL_PREFIX}" \
    --env="CONTAINER_WORKSPACE_ROOT=${CONTAINER_WORKSPACE_ROOT}" \
    --env="COMPONENT_SUBDIR=${CONTAINER_WORKSPACE_ROOT}/${WORKSPACE_SUBDIR}" \
    "${DOCKER_IMAGE}" \
    "${CONTAINER_WORKSPACE_ROOT}/conan_build.sh"
```

## [`server_run.sh`](./server_run.sh)

This is the main script we use to run the demo after `init.sh`.  It does
the following:

- Defines and builds the basic ZFS dataset structure within the ZFS pool.
- Creates a new ZFS snapshot and clone for our build's exclusive use.
- Starts up our `conan-docker-build` container prepared with a good Conan
  and GCC toolchain installation.
- Promotes a successful build to represent the preferred branch cache.
- Offers an option to save a broken build's clone and snapshot in place
  for troubleshooting.  Destroys the broken build's cache clone otherwise.

```bash
❯ time ./server_run.sh 13 0 2>&1 | tee ../../../server_run.sh.log
```
