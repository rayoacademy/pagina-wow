"""Juego Stickers · plantilla firma de la familia Juego.

Portafolio juguetón con guiños de Figma. Firma: regla de lienzo, nombre en caja de selección
con manijas, notas adhesivas giradas, cursores con etiqueta, polaroids, servicios como fichas
de colores, proyectos en carpetas con pestaña y un comentario de Figma en el contacto.

Campos propios: hero.notas [{"t","color"}], hero.cursores [{"t","color"}], sobre.imagenes [{src,pie}], sobre.avatar
"""
from generar_v3 import Gen3, e, ea

COLORES = ["amarillo", "verde", "rosa", "azul", "naranja"]
ICONOS = ['<path d="M4 4h7v7H4zM13 13h7v7h-7zM13 4l7 7M20 4l-7 7"/>', '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>',
          '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>', '<path d="M5 5h5v5H5zM14 5h5v5h-5zM5 14h5v5H5zM14 14h5v5h-5z"/>']
FLOR = ('<svg class="flor" viewBox="0 0 200 200" aria-hidden="true"><path d="M100 30c22 0 36 22 30 42 20-6 42 8 42 30s-22 36-42 30c6 20-8 38-30 38s-36-18-30-38c-20 6-42-8-42-30s22-36 42-30c-6-20 8-42 30-42Z" fill="#2fbf7a" stroke="#1c7a4c" stroke-width="2"/>'
        '<rect x="80" y="88" width="10" height="30" rx="5" transform="rotate(20 85 103)" fill="#1a1a1a"/><rect x="104" y="84" width="10" height="30" rx="5" transform="rotate(20 109 99)" fill="#1a1a1a"/></svg>')
FL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
FLECHAS = '<span class="ff" aria-hidden="true">»</span>'


def sel(contenido, cls=""):
    """caja de selección con manijas"""
    return f'<span class="sel {cls}">{contenido}<i class="h1"></i><i class="h2"></i><i class="h3"></i><i class="h4"></i></span>'


class Plantilla(Gen3):

    def menu(self):
        return [x for x in super().menu() if x[0] != "#testimonios"]

    def nav(self):
        links = "".join(f'<a href="{h}">{e(t).upper()}</a>' for h, t in self.menu()[:5])
        regla = "".join(f"<span>{n}</span>" for n in range(0, 2600, 200))
        return (f'<nav class="nav" id="nav"><div class="barra"><a href="#top" class="marca on">⌂ {"INICIO" if self.lang == "es" else "HOME"}</a>{links}'
                f'<a href="#contacto" class="cta">♥ {e(self.d.get("nav_cta") or self.t["contacto"]).upper()}</a></div><div class="regla" aria-hidden="true">{regla}</div></nav>\n')

    def portada(self):
        h = self.d.get("hero", {})
        notas = "".join(f'<span class="nota {n.get("color", COLORES[i % 5])} n{i}">{e(n["t"])}</span>' for i, n in enumerate(h.get("notas", [])[:2]))
        curs = "".join(f'<span class="cursor {c.get("color", COLORES[(i + 2) % 5])} c{i}">{e(c["t"]).upper()}<i></i></span>' for i, c in enumerate(h.get("cursores", [])[:2]))
        av = self.img((self.d.get("sobre") or {}).get("avatar"), 200)
        burbujas = (f'<img class="burbuja b1" src="{av}" alt=""/><img class="burbuja b2" src="{av}" alt=""/>' if av else "")
        estado = f'<p class="estado"><i></i>{e(h["etiqueta"]).upper()}</p>' if h.get("etiqueta") else ""
        return (f'<header class="portada" id="top"><p class="hora mono" id="hora"></p><div class="lienzo"><p class="mano">{e(h.get("saludo", "me llamo" if self.lang == "es" else "my name is"))}</p>'
                f'{notas}<h1>{sel(e(h.get("nombre_grande") or self.m.get("nombre", "")).upper())}</h1>{estado}{curs}{burbujas}'
                f'<a class="btn negro" href="{ea(self.cta_href())}"{self.ext(self.cta_href())}>{FLECHAS}{e((h.get("cta") or {}).get("texto") or self.t["contacto"]).upper()}</a></div>'
                '<svg class="raya" viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 110C400 10 1000 0 1440 70" fill="none" stroke="#1a1a1a" stroke-width="1.2"/></svg></header>\n')

    def sobre(self):
        s = self.d.get("sobre")
        if not s: return ""
        pols = "".join(f'<figure class="pol p{i} rv">{self.foto(f.get("src"), f.get("pie", ""), "", 700)}<figcaption>{e(f.get("pie", ""))}</figcaption></figure>' for i, f in enumerate(s.get("imagenes", [])[:2]))
        fichas = ""
        for i, it in enumerate((self.d.get("servicios") or {}).get("items", [])):
            col = it.get("color", COLORES[(i + (i // 2)) % 5])
            ico = f'<span class="ico {COLORES[(i + 3) % 5]}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{ICONOS[i % 4]}</svg></span>'
            fichas += f'<span class="ficha {col}">{e(it.get("titulo"))}</span>{ico}'
        return (f'<section class="sobre" id="sobre"><p class="mano rv">{e(s.get("etiqueta", "sobre mí" if self.lang == "es" else "about me!"))}</p>'
                f'<h2 class="rv">{sel(e(" ".join(s.get("titulo") or ["qué hago"])), "chica")}</h2>'
                + (f'<p class="baj rv">{e(s["bajada"])}</p>' if s.get("bajada") else "") + f'{pols}<div class="fichas rv" id="servicios">{fichas}</div></section>\n')

    def proyectos(self):
        g = self.d.get("galeria"); fotos = self.fotos_galeria()
        if not fotos: return ""
        gd = g if isinstance(g, dict) else {}
        es = self.lang == "es"
        colores = ["azul", "negro", "amarillo", "rosa"]
        cards = []
        for i, f in enumerate(fotos):
            tags = "".join(f'<span class="tag">{e(t).upper()}</span>' for t in f.get("servicios", []))
            pos = ("izq", "centro", "der", "derecha")[i % 4]
            cards.append(f'<article class="carpeta {colores[i % 4]} rv"><span class="pest {pos}">▮ {"PROYECTO" if es else "PROJECT"} {i + 1:02d}</span><div class="ca-in"><div class="ca-t">'
                         + (f'<p class="mono fecha"><i></i>{e(f["etiqueta"]).upper()}</p>' if f.get("etiqueta") else "") + f'<h3>{e(f.get("titulo", ""))}</h3><p>{e(f.get("texto", ""))}</p>'
                         + f'<a class="mono lnk" href="{ea(f.get("href", "#contacto"))}"{self.ext(f.get("href", ""))}>{"VER PROYECTO" if es else "VIEW PROJECT"} ↗</a><div class="tags">{tags}</div></div>'
                         f'<div class="ca-f">{sel(self.foto(f.get("src"), f.get("alt", ""), "", 1400), "img")}<span class="mono archivo">▣ IMAGEN.JPG</span></div></div></article>')
        return (f'<section class="proyectos" id="galeria"><p class="mano rv">{e(gd.get("etiqueta", "mira mi trabajo" if es else "explore my work!"))}</p>'
                f'<h2 class="pixel rv">{"<br>".join(e(x).upper() for x in (gd.get("titulo") or ["Proyectos"]))}</h2>'
                + (f'<p class="nota amarillo suelta rv">{e(gd["bajada"])}</p>' if gd.get("bajada") else "") + f'<div class="wrap carpetas">{"".join(cards)}</div></section>\n')

    def testimonios(self):
        return ""  # los testimonios aparecen como comentario en el contacto

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        det = "".join(f'<details><summary>{e(x.get("p"))}<span aria-hidden="true">+</span></summary><p>{e(x.get("r"))}</p></details>' for x in items)
        return f'<section class="faq" id="faq"><div class="wrap angosto"><h2 class="pixel">{"<br>".join(e(x).upper() for x in self.t["faq_t"])}</h2><div class="acc">{det}</div></div></section>\n'

    def contacto(self):
        c = self.d.get("cierre") or {}; es = self.lang == "es"
        q = ((self.d.get("testimonios") or {}).get("items") or [None])[0]
        av = self.img((q or {}).get("foto") or (self.d.get("sobre") or {}).get("avatar"), 200)
        coment = (f'<div class="comentario rv"><small>{"Comentario" if es else "Comment"}</small><div class="co-fila">' + (f'<img src="{av}" alt=""/>' if av else "")
                  + f'<div><b>{e(q.get("nombre", ""))}</b><p>{e(q.get("texto", ""))}</p><span class="reac">⚡ 1</span></div></div></div>') if q else ""
        form = self.formulario(); datos = self.contacto_items()
        lista = "".join(f'<a href="{ea(h)}"{self.ext(h)}><small>{e(k).upper()}</small>{e(v)}</a>' for k, v, h in datos)
        return (f'<section class="contacto" id="contacto"><div class="wrap"><div class="hablemos">{FLOR}<div><h2 class="pixel rv">{"<br>".join(e(x).upper() for x in (c.get("titulo") or (["Hablemos"] if es else ["Let’s talk"])))}</h2>'
                + (f'<p class="rv">{e(c["texto"])}</p>' if c.get("texto") else "") + f'</div></div><div class="panel rv">{coment}'
                f'<a class="boton-pixel" href="{ea(self.cta_href())}"{self.ext(self.cta_href())}><i aria-hidden="true">»</i>{e((c.get("cta") or {}).get("texto") or self.t["contacto"]).upper()}<i aria-hidden="true">»</i></a></div>'
                + (f'<div class="ct-datos">{lista}</div>' if lista else "") + (f'<div class="ct-form">{form}</div>' if form else "") + "</div></section>\n")

    def secciones(self):
        return [self.portada(), self.sobre(), self.proyectos(), self.faq(), self.contacto()]

    def footer(self, desde=""):
        from datetime import date
        regla = "".join(f"<span>{n}</span>" for n in range(0, 2600, 200))
        return (f'<footer class="pie"><div class="regla" aria-hidden="true">{regla}</div><div class="pie-fila mono"><span>© {date.today().year} {e(self.m.get("nombre", "")).upper()}</span>'
                f'<div class="leg">{self.enlaces_legales(desde)}</div></div></footer>\n')
