"""كتالوج الوسائط التعليمية المرخصة وتنزيلها محليًا للعمل دون اتصال."""
from pathlib import Path
from urllib.request import Request, urlopen
from app.config import MEDIA_DIR

LICENSED_MEDIA = [
    {
        "id":"ar_alphabet_001","language":"ar","level":1,"age_group":"6–7","kind":"video",
        "title":"الحروف العربية — درس الأبجدية",
        "filename":"ar_alphabet_001.webm",
        "url":"https://upload.wikimedia.org/wikipedia/commons/3/34/The_Arabic_Alphabet-0Isyy_ZvZR8.webm",
        "source_page":"https://commons.wikimedia.org/wiki/File:The_Arabic_Alphabet-0Isyy_ZvZR8.webm",
        "license":"CC BY 3.0","attribution":"Waikato Islamic School of Education",
        "animated":False,"teaches":True
    },
    {
        "id":"en_parrot_001","language":"en","level":1,"age_group":"4–7","kind":"video",
        "title":"The Parrot — English for children",
        "filename":"en_parrot_001.webm",
        "url":"https://upload.wikimedia.org/wikipedia/commons/b/b6/The_Parrot_-_Toyor_Baby_English.webm",
        "source_page":"https://commons.wikimedia.org/wiki/File:The_Parrot_-_Toyor_Baby_English.webm",
        "license":"CC BY 3.0","attribution":"Toyor Baby English",
        "animated":True,"teaches":True
    },
    {
        "id":"en_cartoons_001","language":"en","level":0,"age_group":"4–10","kind":"video",
        "title":"Learn English with Cartoons — study tips",
        "filename":"en_cartoons_001.webm",
        "url":"https://upload.wikimedia.org/wikipedia/commons/d/d0/Learn_English_with_Cartoons%21_%F0%9F%8E%AC.webm",
        "source_page":"https://commons.wikimedia.org/wiki/File:Learn_English_with_Cartoons!_%F0%9F%8E%AC.webm",
        "license":"CC0 1.0","attribution":"Ms Animo",
        "animated":True,"teaches":True
    }
]

def catalog():
    root=Path(MEDIA_DIR)/"licensed"
    return [{**item,"local_path":str(root/item["filename"]),"downloaded":(root/item["filename"]).exists()} for item in LICENSED_MEDIA]

def get_item(item_id):
    return next((x for x in LICENSED_MEDIA if x["id"]==item_id),None)

def download_item(item_id, timeout=60):
    item=get_item(item_id)
    if not item: raise KeyError(item_id)
    root=Path(MEDIA_DIR)/"licensed"; root.mkdir(parents=True,exist_ok=True)
    target=root/item["filename"]
    if target.exists() and target.stat().st_size>0: return target
    req=Request(item["url"],headers={"User-Agent":"Lughati-Educational-App/1.0"})
    with urlopen(req,timeout=timeout) as response, target.open("wb") as out:
        while True:
            chunk=response.read(1024*1024)
            if not chunk: break
            out.write(chunk)
    if target.stat().st_size==0:
        target.unlink(missing_ok=True)
        raise IOError("تم تنزيل ملف فارغ")
    return target

def local_path(item_id):
    item=get_item(item_id)
    if not item: return None
    return Path(MEDIA_DIR)/"licensed"/item["filename"]
