#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y cmake
ls -alr .
echo `ls -alr /io`

# Compile wheels
PY_BASE="/opt/python"
PY_VALID="3\.[5-9]\..*"
for VERSION in $(ls -d ${PY_BASE}/*/); do echo ${i%%/}; done
    PYBIN="${PY_BASE}/${VERSION}/bin"
    echo "Testing ${VERSION}"
    valid=`${VERSION} =~ ${PY_VALID}`
    if [ ${valid} ]; then
      if [ -f "${PYBIN}" ]; then
        echo "Building for ${VERSION} at ${PYBIN}"
        result=`"${PYBIN}/pip" wheel /io/ -w /io/wheelhouse/`
      fi
    fi
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
