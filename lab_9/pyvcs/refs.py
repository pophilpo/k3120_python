import pathlib
import typing as tp

def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    gitdr = pathlib.Path(gitdir)
    new_gitdr = pathlib.Path(gitdr/ref)
    pathlib.Path(new_gitdr).touch()
    with open(new_gitdr, "w") as f:
        f.write(new_value)
        f.close()

def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    gitdr = pathlib.Path(gitdir).absolute()
    pathlib.Path(gitdr/name).touch()
    file = pathlib.Path(gitdr/name)
    with open(file, "w") as f:
        f.write(f"ref: {ref}")
        f.close()

def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:    
    gitdir = pathlib.Path(gitdir)
    if refname=="HEAD":
        #gitdr = pathlib.Path(gitdir).absolute()
        path =  pathlib.Path(gitdir, refname)
        with open(path, "r") as f:
            f.seek(5)
            rd = f.read()[:-1]
            f.close()
        path_master = pathlib.Path(gitdir, rd)
        with open(path_master, "r") as f_new:
            wf = f_new.read()
            f_new.close()
        return(wf)
    elif refname == "refs/heads/master":
        path_master = pathlib.Path(gitdir, refname).absolute()
        with open(path_master, "r") as f_new:
            wf = f_new.read()
            f_new.close()
        return(wf)


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    paths = sorted(pathlib.Path(gitdir).glob('**/master'))
    if len(paths) == 0:
        return None
    else:
        with open(paths[0], "r") as f_new:
            wf = f_new.read()
            return(wf) 



def is_detached(gitdir: pathlib.Path) -> bool:
    if not pathlib.Path.exists(gitdir/"HEAD"):
        return False
    with pathlib.Path(gitdir, "HEAD").open("r") as f:
        data = f.read()
        f.close()
    if type(data) == str and len(data) == 40 and data[:5] != "ref: ":
        return True
    return False

        

def get_ref(gitdir: pathlib.Path) -> str:
    with pathlib.Path(gitdir,"HEAD").open("r") as f:
        ref = f.read()
        f.close()
    if ref[:5] == "ref: ":
        ref = ref[5:-1]
    return ref
