#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y cmake
yum list installed
yum install -y python36-devel
LCB_VER_NUM=3.0.0
LCB_VER=libcouchbase-3.0.0_centos7_x86_64
curl -O https://packages.couchbase.com/clients/c/${LCB_VER}.tar
tar xf ${LCB_VER}.tar
cd ${LCB_VER}
yum install -y libcouchbase3{-tools,-libevent,}-3.0.0*.rpm libcouchbase-devel-*.rpm

ls -alr .

echo `ls -alr /io`
pushd .

# Compile wheels
PY_BASE="/opt/python"
PY_VALID=".*3[5-9].*"
#export CFLAGS="-static-libstdc++ ${CFLAGS}"
for VERSION_PATH in ${PY_BASE}/*/; do
    VERSION=`basename ${VERSION_PATH}`
    PYBIN="${VERSION_PATH}bin"
    echo "Testing ${VERSION}"
    if [[ ${VERSION} =~ $PY_VALID ]]
    then
      echo "${VERSION} matches ${PY_VALID}"
      if [ -d "${PYBIN}" ]
      then
        echo "Building for ${VERSION} at ${PYBIN}"
        ${PYBIN}/pip wheel /io/ -w /io/wheelhouse/${VERSION}

        # Bundle external shared libraries into the wheels
        for whl in /io/wheelhouse/*.whl; do
            auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse/${VERSION}
        done

        # Install packages and test
        cd /io/

        "${PYBIN}/pip" install -r /io/dev_requirements.txt
        "${PYBIN}/pip" install couchbase --no-index -f /io/wheelhouse/${VERSION}
        "${PYBIN}/nosetests" couchbase.tests -v

      else
        echo "${PYBIN} does not exist"
      fi
    else
      echo "${VERSION} does not match ${PY_VALID}"
    fi
done

echo `ls /io/wheelhouse`
echo `ls /wheelhouse`
echo `ls wheelhouse`
