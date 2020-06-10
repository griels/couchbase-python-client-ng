import logging
import warnings
import pathlib
import traceback
import os
from cbuild_config import couchbase_core
from enum import IntEnum
import json
import sys


curdir = pathlib.Path(__file__).parent

lcb_min_version_baseline = (3, 0, 1)


def get_lcb_min_version():
    result = lcb_min_version_baseline
    try:
        # check the version listed in README.rst isn't greater than lcb_min_version
        # bump it up to the specified version if it is
        import docutils.parsers.rst
        import docutils.utils
        import docutils.frontend

        parser = docutils.parsers.rst.Parser()

        with open(str(curdir.joinpath("README.rst"))) as README:
            settings = docutils.frontend.OptionParser().get_default_values()
            settings.update(
                dict(tab_width=4, report_level=1, pep_references=False, rfc_references=False, syntax_highlight=False),
                docutils.frontend.OptionParser())
            document = docutils.utils.new_document(README.name, settings=settings)

            parser.parse(README.read(), document)
            readme_min_version = tuple(
                map(int, document.substitution_defs.get("libcouchbase_version").astext().split('.')))
            result = max(result, readme_min_version)
            logging.info("min version is {}".format(result))
    except Exception as e:
        warnings.warn("problem: {}".format(traceback.format_exc()))
    return result


lcb_min_version = get_lcb_min_version()

build_dir = curdir.joinpath('build')


class SSL_MinVer(IntEnum):
    dev = 0
    beta_1 = 0x1
    beta_2 = 0x2
    beta_3 = 0x3
    beta_4 = 0x4
    beta_5 = 0x5
    beta_6 = 0x6
    beta_7 = 0x7
    beta_8 = 0x8
    beta_9 = 0x9
    beta_10 = 0xa
    beta_11 = 0xb
    beta_12 = 0xc
    beta_13 = 0xd
    beta_14 = 0xe
    release = 0xf


import ssl

ssl_letter = bytes.decode(bytes((str.encode('a', 'utf-8')[0] + ssl.OPENSSL_VERSION_INFO[-2] - 1,)), 'utf-8')
ssl_major = "{}{}".format(".".join(map(str, ssl.OPENSSL_VERSION_INFO[:-2])), ssl_letter)
ssl_root_dir_pattern = os.getenv("OPENSSL_ROOT_DIR",
                                 str(curdir.joinpath('..', 'install', 'openssl-{}-cb1').absolute()))
ssl_root_dir = ssl_root_dir_pattern.format(ssl_major)

ssl_info = dict(major=ssl_major,
                minor=SSL_MinVer(ssl.OPENSSL_VERSION_INFO[-1]).name.replace('_', ' '),
                original=ssl.OPENSSL_VERSION,
                ssl_root_dir=ssl_root_dir,
                python_version=sys.version_info,
                raw_version_info=".".join(map(str,ssl.OPENSSL_VERSION_INFO[:-2])))


def __main__():
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
    with open(str(build_dir.joinpath("lcb_min_version.h")), "w+") as LCB_MIN_VERSION:
        LCB_MIN_VERSION.write('\n'.join(
            ["#define LCB_MIN_VERSION 0x{}".format(''.join(map(lambda x: "{0:02d}".format(x), lcb_min_version))),
             '#define LCB_MIN_VERSION_TEXT "{}"'.format('.'.join(map(str, lcb_min_version))),
             '#define PYCBC_PACKAGE_NAME "{}"'.format(couchbase_core)]))
    with open("openssl_version.json", "w+") as OUTPUT:
        json.dump(ssl_info, OUTPUT)


if __name__ == "__main__":
    __main__()
