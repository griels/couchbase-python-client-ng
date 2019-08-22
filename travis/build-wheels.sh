#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y cmake
ls -alr .
echo `ls -alr /io`

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" wheel /io/ -w /io/wheelhouse/
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
