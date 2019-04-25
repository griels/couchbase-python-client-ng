from setuptools import Extension
import platform
import warnings
import re

from cbuild_config import get_all_sources


def get_sources(extoptions):
    all_sources = get_all_sources()
    SOURCEMODS = list(filter(re.compile(r'^.*\.c$').match, all_sources))
    SOURCEMODS_CPP = list(filter(re.compile(r'^.*\.(cpp|cxx|cc)$').match, all_sources))
    extoptions['sources'] = list(map(str, SOURCEMODS+SOURCEMODS_CPP))
    return extoptions


def gen_cmodule(extoptions):
    get_sources(extoptions)
    if platform.python_implementation() != 'PyPy':
        print("sources are {}".format(extoptions['sources']))
        module = Extension('couchbase._libcouchbase', **extoptions)
    else:
        warnings.warn('The C extension libary does not work on PyPy. '
                      'You should install the couchbase_ffi module. Installation of this '
                      'module will continue but will be unusable without couchbase_ffi')
        module = None
    return extoptions, module


