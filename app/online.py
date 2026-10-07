import json
from pathlib import Path
from urllib.request import Request,urlopen

def internet_available(url="https://www.google.com",timeout=4):
    try:
        with urlopen(Request(url,method="HEAD"),timeout=timeout): return True
    except Exception: return False

def fetch_manifest(url,timeout=8):
    with urlopen(url,timeout=timeout) as r: return json.loads(r.read().decode("utf-8"))

def download_resumable(url,destination,chunk_size=1024*256):
    destination=Path(destination); destination.parent.mkdir(parents=True,exist_ok=True)
    existing=destination.stat().st_size if destination.exists() else 0
    headers={"Range":f"bytes={existing}-"} if existing else {}
    with urlopen(Request(url,headers=headers),timeout=30) as r, destination.open("ab" if existing else "wb") as f:
        while True:
            chunk=r.read(chunk_size)
            if not chunk: break
            f.write(chunk)
    return destination