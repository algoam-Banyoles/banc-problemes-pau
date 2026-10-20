"""Eines per extreure problemes dels PDFs de selectivitat.

Ús:
  python -I tools/pdftools.py text PDF [PAGINA]          text amb coordenades de cada bloc (punts PDF)
  python -I tools/pdftools.py render PDF PAGINA OUT.png   pàgina sencera (zoom 1.5) per mirar-la
  python -I tools/pdftools.py figs PDF PAGINA             caixes d'imatges i dibuixos vectorials de la pàgina
  python -I tools/pdftools.py crop PDF PAGINA x0 y0 x1 y1 OUT.png   retall en punts PDF (zoom 2.5)
  python -I tools/pdftools.py lines PDF PAGINA [x0 y0 x1 y1]      segments/corbes vectorials (per mesurar dibuixos)

Les pàgines es numeren des d'1. Les coordenades són en punts PDF (A4 = 595 x 842), origen a dalt a l'esquerra.
"""
import sys
import fitz
fitz.TOOLS.mupdf_display_errors(False)


def page_of(path, n):
    doc = fitz.open(path)
    return doc, doc[int(n) - 1]


def cmd_text(path, n=None):
    doc = fitz.open(path)
    pages = [int(n)] if n else range(1, doc.page_count + 1)
    for p in pages:
        page = doc[p - 1]
        print(f"===== pàgina {p}  ({page.rect.width:.0f}x{page.rect.height:.0f})")
        for b in page.get_text("blocks"):
            x0, y0, x1, y1, txt = b[:5]
            txt = " ".join(txt.split())
            if txt:
                print(f"[{x0:5.0f} {y0:5.0f} {x1:5.0f} {y1:5.0f}] {txt}")


def cmd_render(path, n, out, zoom=1.5):
    _, page = page_of(path, n)
    page.get_pixmap(matrix=fitz.Matrix(float(zoom), float(zoom))).save(out)
    print(out)


def merge_rects(rects, gap=12):
    rects = [fitz.Rect(r) for r in rects]
    changed = True
    while changed:
        changed = False
        out = []
        for r in rects:
            for o in out:
                g = fitz.Rect(o.x0 - gap, o.y0 - gap, o.x1 + gap, o.y1 + gap)
                if g.intersects(r):
                    o |= r
                    changed = True
                    break
            else:
                out.append(fitz.Rect(r))
        rects = out
    return rects


def cmd_figs(path, n):
    _, page = page_of(path, n)
    rects = []
    for info in page.get_image_info():
        rects.append(fitz.Rect(info["bbox"]))
    for d in page.get_drawings():
        r = d["rect"]
        # ignora línies de punts/separadors molt fins que ocupen tota l'amplada
        if r.width > page.rect.width * 0.8 and r.height < 3:
            continue
        rects.append(r)
    for r in sorted(merge_rects(rects), key=lambda r: (r.y0, r.x0)):
        if r.width > 15 and r.height > 15:
            print(f"[{r.x0:5.0f} {r.y0:5.0f} {r.x1:5.0f} {r.y1:5.0f}]  {r.width:.0f}x{r.height:.0f}")


def cmd_lines(path, n, x0=0, y0=0, x1=9999, y1=9999):
    """Segments, arcs (com a corbes Bézier) i rectangles vectorials dins d'una zona, en punts PDF (1 pt = 0,3528 mm)."""
    _, page = page_of(path, n)
    zone = fitz.Rect(float(x0), float(y0), float(x1), float(y1))
    for d in page.get_drawings():
        if not d["rect"].intersects(zone):
            continue
        for it in d["items"]:
            kind, pts = it[0], it[1:]
            coords = []
            for q in pts:
                if isinstance(q, fitz.Point):
                    coords.append(f"({q.x:.1f},{q.y:.1f})")
                elif isinstance(q, fitz.Rect):
                    coords.append(f"[{q.x0:.1f},{q.y0:.1f},{q.x1:.1f},{q.y1:.1f}]")
            name = {"l": "segment", "c": "corba", "re": "rect", "qu": "quad"}.get(kind, kind)
            print(name, " ".join(coords), f"gruix={d.get('width') or 0:.2f}")


def cmd_crop(path, n, x0, y0, x1, y1, out):
    _, page = page_of(path, n)
    clip = fitz.Rect(float(x0), float(y0), float(x1), float(y1))
    page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=clip).save(out)
    print(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cmd, *args = sys.argv[1:]
    {"text": cmd_text, "render": cmd_render, "figs": cmd_figs, "crop": cmd_crop, "lines": cmd_lines}[cmd](*args)
