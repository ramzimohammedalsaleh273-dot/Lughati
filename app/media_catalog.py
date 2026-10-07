"""فهرس الوسائط المحلية."""
from pathlib import Path
def catalog(root):
    root=Path(root); out=[]
    for kind,folder,ext in (("image","images","*.svg"),("audio","audio","*.wav"),("video","video","*.mp4")):
        for p in sorted((root/folder).glob(ext)):
            lang,level=p.stem.split("_"); out.append({"language":lang,"level":int(level),"kind":kind,"path":str(p),"offline_ready":p.exists()})
    return out
