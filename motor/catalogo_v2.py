#!/usr/bin/env python3
"""pagina-wow · catálogo de los 42 diseños (v2: cada página sale con legal, seguridad y SEO).

Uso:
  python3 catalogo_v2.py ruta/sitio.json carpeta_salida
  (luego capturar portadas con miniaturas.sh y volver a correr con --solo-indice)

Genera carpeta_salida/<id-variante>/ (página completa) y carpeta_salida/index.html (catálogo).
Las miniaturas se buscan en carpeta_salida/_mini/<id>.jpg.
"""
import os, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_v2 import Gen2 as Gen
from generar import VARIANTES

NOMBRES = {"noche": "Noche", "calma": "Calma", "cartel": "Cartel", "plano": "Plano", "pulso": "Pulso", "juego": "Juego", "clinica": "Clínica"}
DESC = {"noche": "Editorial oscuro, foto dramática, premium.", "calma": "Claro y cálido, serif con itálica, cercano.",
        "cartel": "Tu nombre gigante, carácter de marca personal.", "plano": "Blanco técnico, retícula, mucho aire.",
        "pulso": "Color y gradiente, energía.", "juego": "Maximalista, bordes gruesos, divertido.", "clinica": "Confianza, limpio, sereno."}

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    solo = "--solo-indice" in sys.argv
    src, out = args[0], args[1]
    os.makedirs(out, exist_ok=True)
    if not solo:
        for vid in VARIANTES:
            Gen(src, os.path.join(out, vid), sobre={"variante": vid, "familia": None, "estructura": None}).build()
    fams = {}
    for v in VARIANTES.values(): fams.setdefault(v["familia"], []).append(v)
    secs = []
    for f, vs in fams.items():
        cards = []
        for v in vs:
            mini = f"_mini/{v['id']}.jpg"
            img = f'<img src="{mini}" alt="Portada {html.escape(v["nombre"])}" loading="lazy"/>' if os.path.exists(os.path.join(out, mini)) else '<div class="sin"></div>'
            cards.append(f'<a class="c" href="{v["id"]}/" target="_blank" rel="noopener"><div class="th">{img}</div>'
                         f'<div class="i"><b>{html.escape(v["nombre"])}</b><span>{html.escape(v["estructura"])} · {html.escape(v.get("servicios",""))}</span>'
                         f'<p>{html.escape(v.get("para",""))}</p></div></a>')
        secs.append(f'<section id="{f}"><div class="fh"><h2>{NOMBRES[f]}</h2><p>{DESC[f]}</p></div><div class="g">{"".join(cards)}</div></section>')
    nav = "".join(f'<a href="#{f}">{NOMBRES[f]}</a>' for f in fams)
    doc = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Catálogo de diseños</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f4f3ef;--ink:#121212;--mut:#6b6b66;--line:rgba(0,0,0,.09);--card:#fff;}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0d0d0d;--ink:#f2f2ef;--mut:#8e8e89;--line:rgba(255,255,255,.1);--card:#161616;}}}}
:root[data-theme="dark"]{{--bg:#0d0d0d;--ink:#f2f2ef;--mut:#8e8e89;--line:rgba(255,255,255,.1);--card:#161616;}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}.w{{max-width:1320px;margin:0 auto;padding:0 clamp(16px,3vw,32px)}}
header{{padding:72px 0 28px}}h1{{font-family:'Inter Tight';font-weight:500;font-size:clamp(2.4rem,6vw,4.6rem);letter-spacing:-.04em;line-height:1}}
h1 span{{color:var(--mut);display:block}}header p{{color:var(--mut);max-width:40rem;margin-top:18px}}
nav{{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 85%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}}
nav .w{{display:flex;gap:22px;overflow-x:auto;padding-top:14px;padding-bottom:14px;font-size:.9rem;color:var(--mut);scrollbar-width:none}}nav a:hover{{color:var(--ink)}}
section{{padding:44px 0 8px}}.fh{{display:flex;align-items:baseline;gap:16px;margin-bottom:18px;flex-wrap:wrap}}.fh h2{{font-family:'Inter Tight';font-weight:500;font-size:2rem;letter-spacing:-.03em}}.fh p{{color:var(--mut)}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}@media(max-width:980px){{.g{{grid-template-columns:repeat(2,1fr)}}}}@media(max-width:600px){{.g{{grid-template-columns:1fr}}}}
.c{{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;transition:.3s}}.c:hover{{transform:translateY(-3px);box-shadow:0 18px 40px -20px rgba(0,0,0,.35)}}
.th{{aspect-ratio:16/10;overflow:hidden;background:#ddd}}.th img{{width:100%;height:100%;object-fit:cover;object-position:top}}.sin{{width:100%;height:100%}}
.i{{padding:14px 16px 16px}}.i b{{font-family:'Inter Tight';font-weight:500;font-size:1.1rem;letter-spacing:-.02em}}.i span{{display:block;font-size:.75rem;color:var(--mut);margin:2px 0 6px;text-transform:uppercase;letter-spacing:.06em}}.i p{{font-size:.88rem;color:var(--mut)}}
footer{{padding:56px 0;color:var(--mut);font-size:.85rem}}
</style></head><body>
<header class="w"><h1>42 diseños<span>para tu página web</span></h1><p>Siete familias de estilo, seis variantes cada una. Toca cualquiera para ver la página completa con contenido de ejemplo.</p></header>
<nav><div class="w">{nav}</div></nav><main class="w">{"".join(secs)}</main><footer class="w">pagina-wow · {len(VARIANTES)} diseños</footer></body></html>"""
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(doc)
    print("catálogo:", os.path.join(out, "index.html"), len(VARIANTES), "diseños")

if __name__ == "__main__":
    main()
