#!/usr/bin/env python
import logging
import os
import couchbase_version

from cbuild_config import get_ext_options, couchbase_core, build_type
from cmodule import gen_distutils_build
from cmake_build import gen_cmake_build

try:
    if os.environ.get('PYCBC_NO_DISTRIBUTE'):
        raise ImportError()

    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

import os
import itertools
import pathlib
curdir = pathlib.Path(__file__).parent
from cbuild_config import BUILD_CFG, couchbase_core
from lcb_version import get_lcb_min_version

lcb_min_version = get_lcb_min_version()

if not os.path.exists("build"):
    os.mkdir("build")

with open(curdir.joinpath("build/lcb_min_version.h"), "w+") as LCB_MIN_VERSION:
    LCB_MIN_VERSION.write('\n'.join(
        ["#define LCB_MIN_VERSION 0x{}".format(''.join(map(lambda x: "{0:02d}".format(x), lcb_min_version))),
         '#define LCB_MIN_VERSION_TEXT "{}"'.format('.'.join(map(str, lcb_min_version))),
         '#define PYCBC_PACKAGE_NAME "{}"'.format(couchbase_core)]))

try:
    couchbase_version.gen_version()
except couchbase_version.CantInvokeGit:
    pass

pkgversion = couchbase_version.get_version()


def handle_build_type_and_gen_deps():
    cmake_build = build_type in ['CMAKE', 'CMAKE_HYBRID']
    print("Build type: {}, cmake:{}".format(build_type, cmake_build))
    general_requires = open(curdir.joinpath('requirements.txt')).readlines()
    extoptions, pkgdata=get_ext_options()

    if cmake_build:
        e_mods, extra_requires, cmdclass = gen_cmake_build(extoptions, pkgdata)
        general_requires += extra_requires
    else:
        print("Legacy build")
        e_mods, cmdclass = gen_distutils_build(extoptions, pkgdata)

    setup_kw = {'ext_modules': e_mods}
    logging.error(setup_kw)

    setup_kw['setup_requires'] = general_requires
    setup_kw['install_requires'] = general_requires
    setup_kw['cmdclass'] = cmdclass
    setup_kw['package_data'] = pkgdata
    setup_kw['eager_resources'] = list(itertools.chain.from_iterable(pkgdata.values()))
    return setup_kw


setup_kw = handle_build_type_and_gen_deps()

def traverse_packages(branch, prefixes=None):
    prefixes = prefixes or []
    if isinstance(branch, list):
        return list(traverse_packages(entry, prefixes) for entry in branch)
    elif isinstance(branch, dict):
        result=[]
        for key, value in branch.items():
            result+=[traverse_packages(key, prefixes)]+traverse_packages(value, prefixes+[key])
        return result
    return '.'.join(prefixes+[branch])

packages=traverse_packages(BUILD_CFG['packages'])

setup(
    name='couchbase',
    version=pkgversion,
    url="https://github.com/couchbase/couchbase-python-client",
    author="Couchbase, Inc.",
    author_email="PythonPackage@couchbase.com",
    license="Apache License 2.0",
    description="Python Client for Couchbase",
    long_description=open(curdir.joinpath("README.rst"), "r").read(),
    long_description_content_type='text/x-rst',
    keywords=["couchbase", "nosql", "pycouchbase", "libcouchbase"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"],
    python_requires=">=3.5",
    packages=list(packages),
    tests_require=['utilspie','nose', 'testresources>=0.2.7', 'basictracer==2.2.0'],
    test_suite='couchbase_tests.test_sync',
    **setup_kw
)
