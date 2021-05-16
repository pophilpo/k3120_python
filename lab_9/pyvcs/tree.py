import os
import pathlib
import stat
import time
import typing as tp
import hashlib
import binascii

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    sh_f = b""
    for i in range(len(index)):
        string = ""
        sha = index[i].sha1
        mode = str(oct(index[i].mode)[2:])
        name = index[i].name
        n = name.split("/")
        name = n[len(n)-1]
        string += mode + " " + name + "\0"
        string = string.encode()
        string += sha
        hasho = hash_object(string, "tree")
        hasho = bytes.fromhex(hasho)
        if len(n) == 1:
            sh_f += string
            with open(name, "r") as f:
                rd = f.read()
                rd = rd.encode()
                f.close()
                hash_object(rd, "blob", False)
        if len(n) > 1:
            zl = ""
            for i in range(1, len(n)-1):
                zl_2 = ""
                name = str(n[len(n)-2-i])
                mode = "40000"
                zl_2 += mode + " " + name + "\0"
                zl_2 = zl_2.encode()
                zl_2 += hasho
                hasho = hash_object(zl_2, "tree")
                hasho = binascii.unhexlify(hasho)
            name = str(n[0])
            mode = "40000"
            zl += mode + " " + name + "\0"
            zl = zl.encode()
            zl += hasho
            hash_object(string, "tree", True)
            sh_f += zl
    return hash_object(sh_f, "tree", True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    commenttime = str(int(time.mktime(time.localtime()))) + \
        " " + str(time.strftime("%z", time.gmtime()))
    string = "tree "
    string += tree
    string += "\nauthor "
    string += author
    string += " "
    string += commenttime
    string += "\ncommitter "
    string += author
    string += " "
    string += commenttime
    string += "\n\n"
    string += message
    string += "\n"
    return hash_object(string.encode(), "commit", True)
