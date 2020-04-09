#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y cmake
ls -alr .
echo `ls -alr /io`

# Compile wheels
PY_BASE="/opt/python"
PY_VALID=".*3[5-9].*"
cd ${PY_BASE}
for VERSION in */; do
    PYBIN="${VERSION}bin"
    echo "Testing ${VERSION}"
    if [[ ${VERSION} =~ $PY_VALID ]]
    then
      echo "${VERSION} matches ${PY_VALID}"
      if [ -f "${PYBIN}" ]
      then
        echo "Building for ${VERSION} at ${PYBIN}"
        result=`"${PYBIN}/pip" wheel /io/ -w /io/wheelhouse/`
      else
        echo "${PYBIN} does not exist"
      fi
    else
      echo "${VERSION} does not match ${PY_VALID}"
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
