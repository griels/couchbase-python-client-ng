from typing import *
from couchbase_core import subdocument as SD
from .options import OptionBlockTimeOut
from couchbase_core.subdocument import array_addunique, array_append, array_insert, array_prepend, insert, remove, replace, upsert, counter, Spec


SDType = type(SD)


# noinspection PyPep8Naming
def GetSpec():
    # type: () -> SDType
    return SD


LookupInSpec = Iterable[Spec]
MutateInSpec = Iterable[Spec]


# noinspection PyPep8Naming
def MutateSpec():
    # type: () -> SDType
    return SD


def exists(
        path,  # type: str
        xattr=False  # type: bool
):
    # type: (...) -> Spec
    """
    Checks for the existence of a field given a path.

    :param str path: path to the element
    :param xattr: operation is done on an Extended Attribute.
    :return: Spec
    """
    return SD.exists(path,xattr=xattr)


def get(path,  # type: str
        xattr=False  # type: bool
        ):
    # type: (...) -> Spec
    """
    Fetches an element's value given a path.

    :param str path: String path - path to the element
    :param bool xattr: operation is done on an Extended Attribute.
    :return: Spec
    """
    return SD.get(path,xattr=xattr)


def count(path,  # type: str
                  xattr=False  # type; bool
                  ):
    # type: (...) -> Spec
    """
    Gets the count of a list or dictionary element given a path

    :param path: String path - path to the element
    :param bool xattr: operation is done on an Extended Attribute.
    :return: Spec
    """
    return SD.get_count(path)


def get_full():
    # type: (...) -> Spec
    """
    Fetches the entire document.

    :return: Spec
    """
    return SD._gen_3spec(SD.LCB_SDCMD_GET_FULLDOC, "")


def with_expiry():
    # type: (...) -> Spec
    """
    Fetches the expiry from the xattrs of the doc

    :return: Spec
    """
    return SD.get('$document.exptime', xattr=True)


def gen_projection_spec(project, with_exp=False):
    def generate(path):
        if path is None:
            return with_expiry()
        if path:
            return SD.get(path)
        return get_full()

    # empty string = with_expiry
    # None = get_full
    if not project:
        project = [""]
    if with_exp:
        project = [None] + project
    return map(generate, project)


class MutateInOptions(OptionBlockTimeOut):
    def __init__(self, *args, **kwargs):
        super(MutateInOptions, self).__init__(*args, **kwargs)

