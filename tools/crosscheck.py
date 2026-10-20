"""Comprova que l'enunciat de cada problema surt realment al PDF del seu examen (detecta exàmens barrejats).

Ús: python -I tools/crosscheck.py data/tecno/*.json
"""
import json
import re
import sys
import unicodedata

import fitz

fitz.TOOLS.mupdf_display_errors(False)


def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return s.replace("ŀ", "l").replace("·", "")


def words(text):
    text = re.sub(r"\$\$.*?\$\$|\$[^$]*\$", " ", text, flags=re.S)
    return {w for w in re.findall(r"[a-z]{7,}", norm(text))}


sys.stdout.reconfigure(encoding="utf-8")
bad = 0
for f in sys.argv[1:]:
    d = json.load(open(f, encoding="utf-8"))
    pdf = norm(" ".join(p.get_text() for p in fitz.open(d["examen"]["pdf_examen"])))
    pdf = re.sub(r"-\s*\n\s*", "", pdf)
    for p in d["problemes"]:
        ws = words(p["enunciat"] + " " + " ".join(a.get("enunciat", "") for a in p.get("apartats") or []))
        if len(ws) < 4:
            continue
        hit = sum(w in pdf for w in ws) / len(ws)
        if hit < 0.7:
            bad += 1
            print(f"⚠ {p['id']}: només {hit:.0%} de {len(ws)} paraules surten al PDF")
print("cap problema sospitós" if not bad else f"{bad} problemes sospitosos")
