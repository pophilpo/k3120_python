import hashlib
import operator
import os
import pathlib
import struct
import typing as tp
import binascii
from collections import namedtuple

from pyvcs.objects import hash_object
from unittest import TestCase
TestCase.maxDiff = None


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:

        ctime_s = self.ctime_s
        ctime_n = self.ctime_n
        mtime_s = self.mtime_s
        mtime_n = self.mtime_n
        dev = self.dev
        ino = self.ino
        mode = self.mode
        uid = self.uid
        gid = self.gid
        size = self.size
        sha1 = self.sha1
        flags = self.flags
        name = self.name
        values = struct.pack("!10i", ctime_s, ctime_n, mtime_s, mtime_n, dev,
                             ino, mode, uid, gid, size)
        values += struct.pack("20s", sha1)
        values += struct.pack("!h", flags)
        values += struct.pack(f"{len(name)+3}s", name.encode())
        return(values)

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        """
        k = struct.unpack("!10i", data[0:40])
        s = data[40:60]
        p = struct.unpack("!h", data[60:62])
        p = p[0]
        l = str(len(data) - 65)
        l = l + "s"
        t = struct.unpack(l, data[62:len(data)-3])
        t = t[0]
        t = t.decode()
        return GitIndexEntry(
            ctime_s = k[0],
            ctime_n = k[1],
            mtime_s = k[2],
            mtime_n = k[3],
            dev = k[4],
            ino = k[5],
            mode = k[6],
            uid = k[7],
            gid = k[8],
            size = k[9],
            sha1 = s,
            flags = p,
            name = t        
        )
        """
        (
            ctime_s,
            ctime_n,
            mtime_s,
            mtime_n,
            dev,
            ino,
            mode,
            uid,
            gid,
            size,
            sha1,
            flags,
        ) = struct.unpack(">10i20sh", data[:62])
        data = data[62:]
        last_byte = data.find(b"\x00\x00\x00")
        name = data[:last_byte].decode()
        return GitIndexEntry(
            ctime_s, ctime_n, mtime_s, mtime_n, dev, ino, mode, uid, gid, size, sha1, flags, name
        )


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    if not pathlib.Path(gitdir/"index").exists():
        return []
    else:
        gitdir = pathlib.Path(gitdir/"index")
        with gitdir.open("rb") as f:
            a = f.read()
            f.close()
        mas = []
        arr = str(a).split("\\")
        # print(str(a).split("\0"))
        tr = 0
        for i in range(len(arr)):
            if tr < struct.unpack("!i", a[8:12])[0]:
                if ("." in arr[i]) and (len(arr[i]) > 5):
                    mas.append(arr[i][3:])
                    tr += 1
            else:
                break
        if len(mas) == 0:
            return []
        else:
            d = 0
            i = 12
            mas_2 = []
            k = 0
            while k < len(mas):
                d = i + 62 + len(mas[k]) + 3
                l = a[i:d]
                l_1 = GitIndexEntry.unpack(l)
                mas_2.append(l_1)
                i += 62 + len(mas[k]) + 3
                k += 1
            return mas_2


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    values = b'DIRC\x00\x00\x00\x02'
    values += struct.pack("!i", len(entries))
    for i in range(len(entries)):
        values += GitIndexEntry.pack(entries[i])
    hash_object = hashlib.sha1(values)
    hex_dig = hash_object.hexdigest()
    h = binascii.unhexlify(hex_dig)
    values += h
    if not pathlib.Path(gitdir/"index").exists():
        pathlib.Path(gitdir/"index").touch()
    with pathlib.Path(gitdir/"index").open("wb") as f:
        f.write(values)
        f.close()


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    if not pathlib.Path(gitdir/"index").exists():
        return []
    else:
        if details == False:
            gitdir = pathlib.Path(gitdir/"index")
            with gitdir.open("rb") as f:
                a = f.read()
                f.close()
            mas = []
            arr = str(a).split("\\")
            # print(str(a).split("\0"))
            for i in range(len(arr)-13):
                if ("." in arr[i]) and len(arr[i]) > 3:
                    mas.append(arr[i][3:])
            string = "\n".join(mas)
            print(string)
            # print(string)
            if len(mas) == 0:
                return []
        if details == True:
            gitdir = pathlib.Path(gitdir/"index")
            with gitdir.open("rb") as f:
                a = f.read()
                f.close()
            mas = []
            arr = str(a).split("\\")
            # print(str(a).split("\0"))
            for i in range(len(arr)):
                if ("." in arr[i]) and (len(arr[i]) > 3):
                    mas.append(arr[i][3:])
            # print(string)
            if len(mas) == 0:
                return []
            d = 0
            i = 12
            mas_2 = []
            k = 0
            lenght = len(mas)
            while k < len(mas):
                d = i + 62 + len(mas[k]) + 3
                l = a[i:d]
                l_1 = GitIndexEntry.unpack(l)
                mas_2.append(l_1)
                i += 62 + len(mas[k]) + 3
                k += 1
            for i in mas_2:
                print(str(oct(i.mode)[2:]) + " " +
                      str(i.sha1.hex()) + " " + "0" + "\t" + i.name)
            return mas_2


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    paths.sort()
    mas = []
    ct = 0
    for i in range(len(paths)):
        with paths[i].open("r") as f:
            a = f.read().encode()
            f.close()
        path = hash_object(a, "blob", True)
        sha = binascii.unhexlify(path)
        arr = os.stat(paths[i])
        if len(str(paths[i]).replace("\\", "/")) > 7:
            ct = 7
        else:
            ct = len(str(paths[i]).replace("\\", "/"))
        en = GitIndexEntry(
            ctime_s=arr[9],
            ctime_n=0,
            mtime_s=arr[8],
            mtime_n=0,
            dev=arr[2],
            ino=arr[1],
            mode=arr[0],
            uid=arr[4],
            gid=arr[5],
            size=arr[6],
            sha1=sha,
            flags=ct,
            name=str(paths[i]).replace("\\", "/")
        )
        mas.append(en)
    write_index(gitdir, mas)
