import logging
import warnings
from setuptools.command.build_ext import build_ext
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
lcb_min_version_baseline = (2, 9, 0)

import re
import sys

from sphinx.cmd.build import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())

def get_lcb_min_version():
    result = lcb_min_version_baseline
    try:
        # check the version listed in README.rst isn't greater than lcb_min_version
        # bump it up to the specified version if it is
        import docutils.parsers.rst
        import docutils.utils
        import docutils.frontend

        parser = docutils.parsers.rst.Parser()

        with open(os.path.join(dir_path, "README.rst")) as README:
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
        warnings.warn("problem: {}".format(e))
    return result