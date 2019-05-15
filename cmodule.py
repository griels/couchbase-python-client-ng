from setuptools import Extension
import platform
import warnings

def gen_cmodule(extoptions):
    if platform.python_implementation() != 'PyPy':
        print("sources are {}".format(extoptions['sources']))
        module = Extension('couchbase._libcouchbase', **extoptions)
    else:
        warnings.warn('The C extension libary does not work on PyPy. '
                      'You should install the couchbase_ffi module. Installation of this '
                      'module will continue but will be unusable without couchbase_ffi')
        module = None
    return extoptions, module


