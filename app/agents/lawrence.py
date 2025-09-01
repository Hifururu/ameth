from app.core.textutil import normalize

CATEGORY_RULES = [
    (["mcdonald","mc","burger","pizza","kfc","pollo","comida","almuerzo","desayuno","once","sushi","tottus","lider","jumbo","santa isabel"], "comida"),
    (["metro","bip","bus","micro","uber","cabify","peaje","benzina","bencina","petroleo"], "transporte"),
    (["farmacia","salud","doctor","dentista","isapre","fonasa","medicamento","paracetamol"], "salud"),
    (["luz","agua","internet","arriendo","gas","cuenta","electricidad","hogar","enchufe","cable"], "hogar"),
    (["kanji","libro","jlpt","aprender japones","sensei","haru","curso japones"], "estudios"),
    (["netflix","spotify","twitch","cine","juego","videojuego","steam"], "entretenimiento"),
]
DEFAULT_CATEGORIA = "otros"

def auto_categoria(concepto: str) -> str:
    base = normalize(concepto)
    for keywords, cat in CATEGORY_RULES:
        for k in keywords:
            if k in base:
                return cat
    return DEFAULT_CATEGORIA
