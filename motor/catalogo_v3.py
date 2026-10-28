#!/usr/bin/env python3
"""pagina-wow · catálogo de las plantillas firma (v3).

Uso:
  python3 catalogo_v3.py carpeta_salida                   con el ejemplo y las fotos de muestra de cada plantilla
  python3 catalogo_v3.py carpeta_pruebas carpeta_salida   con un sitio.json propio por plantilla (si falta, usa el ejemplo)

Genera cada página en carpeta_salida/<id>/ y un index.html con tarjeta, para quién sirve y firma de cada una.
La miniatura sale de plantillas/<id>/portada.jpg.
"""
import os, sys, json, html, shutil, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_v3 import generador, PLANT
from nueva import preparar

FAMILIAS = ["calma", "noche", "cartel", "plano", "pulso", "juego", "clinica"]
NOMBRES = {"calma": "Calma", "noche": "Noche", "cartel": "Cartel", "plano": "Plano", "pulso": "Pulso", "juego": "Juego", "clinica": "Clínica"}


def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    src, out = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else (None, sys.argv[1])
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="pw-catalogo-")
    fichas = []
    for pid in sorted(os.listdir(PLANT)):
        fp = os.path.join(PLANT, pid, "ficha.json")
        if not os.path.exists(fp): continue
        f = json.load(open(fp, encoding="utf-8")); fichas.append(f)
        sj = os.path.join(src, pid, "sitio.json") if src else ""
        if not os.path.exists(sj):
            sj = preparar(pid, os.path.join(tmp, pid))
            d = json.load(open(sj, encoding="utf-8")); d.pop("_muestras", None); d["_catalogo"] = True  # en el catálogo las muestras son lo esperado
            json.dump(d, open(sj, "w", encoding="utf-8"), ensure_ascii=False)
        generador(sj, os.path.join(out, pid)).build()
        mini = os.path.join(PLANT, pid, "portada.jpg")
        if os.path.exists(mini):
            os.makedirs(os.path.join(out, "_mini"), exist_ok=True)
            shutil.copy2(mini, os.path.join(out, "_mini", pid + ".jpg"))
    shutil.rmtree(tmp, ignore_errors=True)
    secs = []
    for fam in FAMILIAS:
        cards = []
        for f in [x for x in fichas if x["familia"] == fam]:
            mini = f"_mini/{f['id']}.jpg"
            img = f'<img src="{mini}" alt="Portada {html.escape(f["nombre"])}" loading="lazy"/>' if os.path.exists(os.path.join(out, mini)) else '<div class="sin"></div>'
            firma = "".join(f"<li>{html.escape(x)}</li>" for x in f.get("firma", [])[:4])
            cards.append(f'<a class="c" href="{f["id"]}/" target="_blank" rel="noopener"><div class="th">{img}</div><div class="i"><b>{html.escape(f["nombre"])}</b>'
                         f'<span>{html.escape(f.get("se_siente", ""))}</span><p>Para: {html.escape(f.get("para", ""))}</p><ul>{firma}</ul></div></a>')
        if cards: secs.append(f'<section id="{fam}"><h2>{NOMBRES[fam]}</h2><div class="g">{"".join(cards)}</div></section>')
    nav = "".join(f'<a href="#{f}">{NOMBRES[f]}</a>' for f in FAMILIAS)
    doc = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Plantillas firma</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f4f3ef;--ink:#121212;--mut:#6b6b66;--line:rgba(0,0,0,.09);--card:#fff;}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0d0d0d;--ink:#f2f2ef;--mut:#8e8e89;--line:rgba(255,255,255,.1);--card:#161616;}}}}
:root[data-theme="dark"]{{--bg:#0d0d0d;--ink:#f2f2ef;--mut:#8e8e89;--line:rgba(255,255,255,.1);--card:#161616;}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}.w{{max-width:1320px;margin:0 auto;padding:0 clamp(16px,3vw,32px)}}
header{{padding:72px 0 28px}}h1{{font-family:'Inter Tight';font-weight:500;font-size:clamp(2.4rem,6vw,4.6rem);letter-spacing:-.04em;line-height:1}}
h1 span{{color:var(--mut);display:block}}header p{{color:var(--mut);max-width:42rem;margin-top:18px}}
nav{{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 85%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}}
nav .w{{display:flex;gap:22px;overflow-x:auto;padding-top:14px;padding-bottom:14px;font-size:.9rem;color:var(--mut)}}nav a:hover{{color:var(--ink)}}
section{{padding:44px 0 8px}}h2{{font-family:'Inter Tight';font-weight:500;font-size:2rem;letter-spacing:-.03em;margin-bottom:18px}}
.g{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}}@media(max-width:760px){{.g{{grid-template-columns:1fr}}}}
.c{{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;transition:.3s}}.c:hover{{transform:translateY(-3px);box-shadow:0 18px 40px -20px rgba(0,0,0,.35)}}
.th{{aspect-ratio:16/10;overflow:hidden;background:#ddd}}.th img{{width:100%;height:100%;object-fit:cover;object-position:top}}.sin{{width:100%;height:100%}}
.i{{padding:16px 18px 18px}}.i b{{font-family:'Inter Tight';font-weight:500;font-size:1.25rem;letter-spacing:-.02em}}.i span{{display:block;font-size:.86rem;color:var(--mut);margin:4px 0 8px}}
.i p{{font-size:.82rem;color:var(--mut);margin-bottom:8px}}.i ul{{font-size:.8rem;color:var(--mut);padding-left:1.1rem;display:grid;gap:2px}}
footer{{padding:56px 0;color:var(--mut);font-size:.85rem}}
</style></head><body>
<header class="w"><h1>{len(fichas)} plantillas firma<span>para tu página web</span></h1><p>Siete familias, dos plantillas cada una. Cada plantilla tiene su propia composición, sus secciones y su movimiento. Toca una para ver la página completa con contenido de ejemplo.</p></header>
<nav><div class="w">{nav}</div></nav><main class="w">{"".join(secs)}</main><footer class="w">pagina-wow · plantillas firma</footer></body></html>"""
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(doc)
    print("catálogo:", os.path.join(out, "index.html"), len(fichas), "plantillas")


if __name__ == "__main__":
    main()
