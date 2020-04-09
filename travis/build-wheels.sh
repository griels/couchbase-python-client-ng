#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y cmake
yum list installed
yum install -y python36-devel

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
PY_VALID=".*3[6].*"
#export CFLAGS="-static-libstdc++ ${CFLAGS}"
cd ${PY_BASE}
for VERSION in */; do
    PYBIN="${VERSION}bin"
    echo "Testing ${VERSION}"
    if [[ ${VERSION} =~ $PY_VALID ]]
    then
      echo "${VERSION} matches ${PY_VALID}"
      if [ -d "${PYBIN}" ]
      then
        echo "Building for ${VERSION} at ${PYBIN}"
        ${PYBIN}/pip wheel /io/ -w /io/wheelhouse/
      else
        echo "${PYBIN} does not exist"
      fi
    else
      echo "${VERSION} does not match ${PY_VALID}"
    fi
done

popd

# Bundle external shared libraries into the wheels
for whl in /io/wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse/
done

# Install packages and test

#for PYBIN in /opt/python/*/bin/; do
#    "${PYBIN}/pip" install -r /io/dev_requirements.txt
#    "${PYBIN}/pip" install . --no-index -f /io/wheelhouse
#    (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
#done

echo `ls /io/wheelhouse`
echo `ls /wheelhouse`
echo `ls wheelhouse`
