#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y cmake
ls -alr .
echo `ls -alr /io`

PY_VERSIONS=(3.5, 3.6, 3.7, 3.8)
# Compile wheels
for VERSION in PY_VERSIONS; do
    PYBIN="${/opt/python/${VERSION}/bin}"
    echo "Building for ${VERSION}"
    result=`"${PYBIN}/pip" wheel /io/ -w /io/wheelhouse/`
done

# Bundle external shared libraries into the wheels
#for whl in wheelhouse/*.whl; do
#    auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse/
#done

# Install packages and test

#for PYBIN in /opt/python/*/bin/; do
#    "${PYBIN}/pip" install -r /io/dev_requirements.txt
#    "${PYBIN}/pip" install . --no-index -f /io/wheelhouse
#    (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
#done

echo `ls /io/wheelhouse`
echo `ls /wheelhouse`
echo `ls wheelhouse`
