import abc
import base64
import logging
import warnings
import pathlib
import traceback
import os
from abc import abstractmethod
from enum import IntEnum
import json
import sys
import ssl
import platform
import posixpath
from enum import Enum
import argparse

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


class DownloadableRepo(object):
    def __init__(self,
                 repository_name,  # type: str
                 gh_client=None  # type: github.Github
                 ):

        import github
        gh_client = gh_client or github.Github(login_or_token=os.getenv("PYCBC_GH_TOKEN_ENCRYPTED"))
        self._ghrepo = gh_client.get_repo(repository_name)

    def get_sha_for_tag(self,  # type: github.Repository
                        tag  # type: str
                        ):
        """
        Returns a commit PyGithub object for the specified repository and tag.
        """
        branches = self._ghrepo.get_branches()
        matched_branches = [match for match in branches if match.name == tag]
        if matched_branches:
            return matched_branches[0].commit.sha

        y = next(iter({x for x in self._ghrepo.get_tags() if x.name == tag}), None)
        return y.commit.sha if y else None

    def download_directory(self, sha, server_path, dest):
        """
        Download all contents at server_path with commit tag sha in
        the repository.
        """
        from github.GithubException import GithubException
        contents = self._ghrepo.get_dir_contents(server_path, ref=sha)

        for content in contents:
            print("Processing %s" % content.path)
            if content.type == 'dir':
                self.download_directory(sha, content.path)
            else:
                try:
                    path = content.path
                    file_content = self._ghrepo.get_contents(path, ref=sha)
                    with open(content.name, "wb") as file_out:
                        file_out.write(file_content.decoded_content)
                except (GithubException, IOError) as exc:
                    logging.error('Error processing %s: %s', content.path, exc)


class AbstractOpenSSL(abc.ABC):
    def get_headers(self, dest=os.path.abspath(os.path.curdir)):
        self.get_arch_content(dest, ('include',))

    @abstractmethod
    def get_arch_content(self, dest, rel_path):
        pass


class Windows(object):
    class Machine(Enum):
        x86_64 = 'amd64'
        x86_32 = 'win32'
        aarch_be = 'arm64'
        aarch = 'arm64'
        armv8b = 'arm64'
        armv8l = 'arm64'
        AMD64 = 'amd64'
        WIN32 = 'win32'

    class OpenSSL(AbstractOpenSSL):
        def __init__(self,
                     arch  # type: Windows.Machine
                     ):
            self.arch = arch
            self.repo = DownloadableRepo('python/cpython-bin-deps')
            self.sha = self.repo.get_sha_for_tag("openssl-bin-{}".format(ssl_major))

        def get_arch_content(self, dest, rel_path):
            if self.sha:
                self.repo.download_directory(self.sha, posixpath.join(self.arch.value(), *rel_path), dest)

    @classmethod
    def get_arch(cls):
        return cls.Machine[platform.machine()]

    @classmethod
    def get_openssl(cls):
        return Windows.OpenSSL(cls.get_arch())


def get_system():
    if platform.system().lower().startswith('win'):
        return Windows
    return None


def get_openssl():
    system = get_system()
    return system().get_openssl() if system else None


def gen_config(temp_build_dir=os.path.curdir, couchbase_core='couchbase_core'):
    build_dir = curdir.joinpath('build')

    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
    with open(str(build_dir.joinpath("lcb_min_version.h")), "w+") as LCB_MIN_VERSION:
        LCB_MIN_VERSION.write('\n'.join(
            ["#define LCB_MIN_VERSION 0x{}".format(''.join(map(lambda x: "{0:02d}".format(x), lcb_min_version))),
             '#define LCB_MIN_VERSION_TEXT "{}"'.format('.'.join(map(str, lcb_min_version))),
             '#define PYCBC_PACKAGE_NAME "{}"'.format(couchbase_core)]))
    with open("openssl_version.json", "w+") as OUTPUT:
        json.dump(ssl_info, OUTPUT)

    openssl = get_openssl()
    if openssl:
        openssl.get_headers(temp_build_dir)


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('temp_build_dir', type=str)
    parser.parse_args()
    gen_config(parser.parse_args().temp_build_dir)
