import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    if fmt == "blob":
        content = data.decode()
        header = f"{fmt} {len(content)}\0"
        store = header + content
        hash_object = hashlib.sha1(store.encode())
        hex_dig = hash_object.hexdigest()
    if fmt == "tree" or fmt == "commit":
        header = f"{fmt} {len(data)}\0"
        store = header.encode() + data
        hash_object = hashlib.sha1(store)
        hex_dig = hash_object.hexdigest()
    if write == True:
        path = repo_find()
        paths = pathlib.Path(path, "objects")
        if fmt == "tree":
            content = data
            header = f"{fmt} {len(content)}\0"
            store = header.encode() + content
            hash_object = hashlib.sha1(store)
        else:
            content = data.decode()
            header = f"{fmt} {len(content)}\0"
            store = header + content
            hash_object = hashlib.sha1(store.encode())
        hex_dig = hash_object.hexdigest()
        start = hex_dig[0:2]
        continues = hex_dig[2:]
        if not os.path.exists(pathlib.Path(paths / start)):
            os.mkdir(pathlib.Path(paths / start))
        if not os.path.exists(pathlib.Path(paths / start / continues)):
            pathlib.Path(paths / start / continues).touch()
        lib = pathlib.Path(paths / start / continues)
        with lib.open(mode="wb") as f:
            if fmt == "blob" or fmt == "commit":
                a = zlib.compress(store.encode(), -1)
            if fmt == "tree":
                a = zlib.compress(store, 1)
            f.write(a)
            f.close()
    return hex_dig


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if len(obj_name) not in range(4, 41):
        raise AssertionError(f"Not a valid object name {obj_name}")
    obj_dir = gitdir / "objects"
    if not os.path.isdir(obj_dir / obj_name[0:2]):
        raise AssertionError(f"Not a valid object name {obj_name}")
    curr_dir = obj_dir / obj_name[0:2]
    ending = obj_name[2:]
    n = len(ending)
    result = []
    for f in os.listdir(curr_dir):
        if os.path.isfile(curr_dir / f) and f == ending or f[0:n] == ending:
            result.append(obj_name[0:2] + f)
    if len(result) == 0:
        raise AssertionError(f"Not a valid object name {obj_name}")
    return result


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    return resolve_object(obj_name, gitdir)[0]


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = find_object(sha, gitdir)
    with pathlib.Path(gitdir/"objects"/path[0:2]/path[2:]).open("rb") as f:
        obj_data = zlib.decompress(f.read())
        f.close()
    index, content = obj_data.find(b" "), obj_data.find(b"\x00")
    content = obj_data[content+1:]
    fmt = obj_data[:index].decode()
    return fmt, content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    arr = []
    while len(data) > 0:
        fmt = data[:6].decode()
        data = data[6:]
        if fmt == "100644":
            data = data[1:]
            ind = data.find(b"\x00")
            arr.append((100644, data[:ind].decode(), data[ind+1:ind+21].hex()))
            data = data[ind+21:]
        else:
            ind = data.find(b"\x00")
            arr.append((40000, data[:ind].decode(), data[ind+1:ind+21].hex()))
            data = data[ind+21:]
    return arr


def cat_file(obj_name: str, pretty: bool = True) -> None:
    path = repo_find()
    paths = pathlib.Path(path, "objects", obj_name[0:2], obj_name[2:])
    with paths.open(mode="rb") as f:
        a = f.read()
        f.close()
    zl = zlib.decompress(a)
    string = str(zl)
    if string[2] == "b":
        print(zl[8:].decode())
    if string[2] == "t":
        c = 9
        k = 0
        k2 = 0
        arr = []
        while c < len(zl):
            s = ""
            if zl[c] == 52:
                s += "0" + zl[c:c+6].decode()
                c += 6
                s += "tree "
            else:
                s += zl[c:c+7].decode()
                c += 7
                s += "blob "
            k = c
            while zl[k:k+1] != b'\x00':
                k += 1
            s += zl[k+1:k+21].hex()
            s += "\t"
            s += zl[c:k].decode()
            c = k + 21
            arr.append(s)
        print("\n".join(arr))
    if string[2] == "c":
        k = 0
        arr = []
        c = 11
        arr.append(zl[c:56].decode())
        c = 56 + 1
        k = c
        # print(zl[110:111])
        while zl[k:k+1] != b"\n":
            k += 1
        arr.append(zl[c:k].decode())
        k = k + 1
        c = k
        while zl[k:k+1] != b"\n":
            k += 1
        arr.append(zl[c:k].decode())
        arr.append('')
        k = k + 2
        c = k
        while zl[k:k+1] != b"\n":
            k += 1
        arr.append(zl[c:k].decode())
        print('\n'.join(arr))


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    fmt, content = read_object(tree_sha, gitdir)
    objects = read_tree(content)
    arr = []
    for i in objects:
        if i[0] == 100644:
            arr.append((i[1], i[2]))
        else:
            sub_objects = find_tree_files(i[2], gitdir)
            for j in sub_objects:
                arr.append((i[1] + "/" + j[0], j[1]))
    return arr


def commit_parse(raw: bytes, start: int = 0, dct=None):
    pass
