import unicodedata

def normalize(txt: str) -> str:
    if not isinstance(txt, str):
        txt = str(txt or "")
    txt = txt.lower().strip()
    txt = unicodedata.normalize("NFD", txt)
    txt = "".join(c for c in txt if unicodedata.category(c) != "Mn")
    return txt
