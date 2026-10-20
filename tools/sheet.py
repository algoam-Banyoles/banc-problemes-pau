"""Full de contactes de les figures d'un examen, per revisar retalls d'un cop d'ull.

Ús: python -I tools/sheet.py img/dibuix/2023-J OUT.png
"""
import os
import sys

import fitz

folder, out = sys.argv[1], sys.argv[2]
files = sorted(f for f in os.listdir(folder) if f.endswith(".png"))
cols = 4
rows = max(1, -(-len(files) // cols))
W, cw, ch = 1600, 400, 420
doc = fitz.open()
page = doc.new_page(width=W, height=rows * ch)
for i, name in enumerate(files):
    x, y = (i % cols) * cw, (i // cols) * ch
    page.insert_text((x + 6, y + 16), name, fontsize=13)
    page.insert_image(fitz.Rect(x + 6, y + 22, x + cw - 6, y + ch - 6), filename=os.path.join(folder, name))
page.get_pixmap().save(out)
print(out, len(files), "figures")
