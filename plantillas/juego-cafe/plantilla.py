"""Juego Café · plantilla firma de la familia Juego.

Café de barrio con humor. Firma: marca gigante en letra burbuja sobre la foto, mosaico de
paneles café y crema con fotos y texto encima (uno en curva), "lo más pedido" con tarjetas
escalonadas, carta con precios y un texto que gira alrededor de un producto.

Campos propios en sitio.json:
  "mosaico": [{"texto": "...", "color": "cafe|crema"} | {"src": "foto.jpg", "titulo": "...", "precio": "...", "curva": "texto en arco"}]
  "carta": [{"titulo": "bebidas", "items": [{"n": "capuchino", "p": "$9.000"}]}], "carta_imagen": "local.jpg"
  "tienda": {"titulo": "...", "texto": "...", "precio": "...", "imagen": "...", "cta": {...}}
"""
from generar_v3 import Gen3, e, ea


def curva(txt, i):
    return (f'<svg class="curva" viewBox="0 0 500 220" aria-hidden="true"><defs><path id="cv{i}" d="M10 170 Q250 10 490 140"/></defs>'
            f'<text><textPath href="#cv{i}">{e(txt)}</textPath></text></svg>')


class Plantilla(Gen3):

    def nav(self):
        return (f'<nav class="nav" id="nav"><div class="nav-in"><a href="#top" class="marca">{e(self.m.get("nombre", "")).lower()}</a>'
                f'<a href="{ea(self.cta_href())}" class="bola"{self.ext(self.cta_href())} aria-label="{e(self.d.get("nav_cta") or self.t["contacto"])}">'
                '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5h14a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-8l-4.5 3.5V17H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/></svg></a></div></nav>\n')

    def portada(self):
        h = self.d.get("hero", {})
        img = self.foto(h.get("imagen"), h.get("alt", ""), "ph", 2400).replace(' loading="lazy"', ' fetchpriority="high"')
        lineas = "".join(f"<span>{e(x).lower()}</span>" for x in h.get("info", []))
        return (f'<header class="portada" id="top">{img}<div class="velo"></div><div class="portada-in">'
                f'<h1 class="burbuja" data-fit>{e(h.get("nombre_grande") or self.m.get("nombre", "")).lower()}</h1>'
                + (f'<p class="frase rv">{e(h["texto"]).lower()}</p>' if h.get("texto") else "")
                + f'<div class="info">{lineas}</div></div></header>\n')

    def mosaico(self):
        tiles = self.d.get("mosaico") or []
        if not tiles: return ""
        out = []
        for i, t in enumerate(tiles):
            if t.get("src"):
                cap = ""
                if t.get("curva"): cap += curva(t["curva"].lower(), i)
                if t.get("titulo"): cap += f'<p class="sobre-f">' + (f'<small>{e(t["eti"]).lower()}</small>' if t.get("eti") else "") + f'{e(t["titulo"]).lower()}' + (f'<b>{e(t["precio"]).lower()}</b>' if t.get("precio") else "") + "</p>"
                out.append(f'<figure class="tile foto rv">{self.foto(t["src"], t.get("alt", ""), "", 1400)}{cap}</figure>')
            else:
                cls = "crema" if t.get("color") == "crema" else "cafe"
                big = " grande" if t.get("grande") else ""
                cta = f'<a class="pill" href="{ea(t["cta"].get("href") or self.cta_href())}"{self.ext(t["cta"].get("href") or self.cta_href())}>{e(t["cta"]["texto"]).lower()}</a>' if t.get("cta") else ""
                out.append(f'<div class="tile {cls}{big} rv">' + (f'<h2>{e(t["titulo"]).lower()}</h2>' if t.get("titulo") else "")
                           + (f'<p>{e(t["texto"]).lower()}</p>' if t.get("texto") else "") + cta + (f'<small class="pie-t">{"<br>".join(e(x).lower() for x in t.get("pie", []))}</small>' if t.get("pie") else "") + "</div>")
        return f'<section class="mosaico" id="sobre">{"".join(out)}</section>\n'

    def pedidos(self):
        s = self.d.get("servicios")
        if not s: return ""
        cards = "".join(f'<article class="pedido {"crema" if i % 2 == 0 else "cafe"} rv" style="--i:{i}"><h3>{e(it.get("titulo", "")).lower()}</h3>'
                        + (f'<small>{e(it["tipo"]).lower()}</small>' if it.get("tipo") else "") + f'<p>{e(it.get("texto", "")).lower()}</p>'
                        + f'<a class="pill" href="{ea(self.cta_href())}"{self.ext(self.cta_href())}>{e(it.get("cta", "pedir" if self.lang == "es" else "order now")).lower()}</a></article>'
                        for i, it in enumerate(s.get("items", [])))
        return (f'<section class="pedidos" id="servicios"><h2 class="gigante" data-fit>{e(" ".join(s.get("titulo") or ["lo más pedido"])).lower()}</h2>'
                f'<div class="wrap esc">{cards}</div></section>\n')

    def carta(self):
        cs = self.d.get("carta") or []
        if not cs: return ""
        bloques = []
        for i, c in enumerate(cs):
            filas = "".join(f'<li><span>{e(x.get("n")).lower()}</span><i></i><b>{e(x.get("p"))}</b></li>' for x in c.get("items", []))
            bloques.append(f'<div class="menu {"crema" if i % 2 == 0 else "cafe"} rv"><h3>{e(c.get("titulo", "")).lower()}</h3><ul>{filas}</ul></div>')
        # sin foto del local no se pone un panel vacío; el relleno solo existe para cuadrar la grilla de 2 columnas
        celdas = ([f'<figure class="tile foto">{self.foto(self.d["carta_imagen"], "", "", 1400)}</figure>'] if self.d.get("carta_imagen") else []) + bloques
        if len(celdas) % 2: celdas.append('<div class="tile cafe relleno" aria-hidden="true"></div>')
        return f'<section class="carta mosaico" id="paquetes">{"".join(celdas)}</section>\n'

    def tienda(self):
        t = self.d.get("tienda")
        if not t: return ""
        palabra = (t.get("giro") or "tienda · ").lower()
        return (f'<section class="tienda"><div class="giro" aria-hidden="true"><span>{e(palabra * 8)}</span></div><div class="producto rv">'
                + (f'<div class="pr-f">{self.foto(t["imagen"], t.get("titulo", ""), "", 900)}</div>' if t.get("imagen") else "")
                + f'<h3>{e(t.get("titulo", "")).lower()}</h3><p>{e(t.get("texto", "")).lower()}</p><div class="pr-pie"><b>{e(t.get("precio", ""))}</b>'
                + f'<a class="pill oscuro" href="{ea((t.get("cta") or {}).get("href") or self.cta_href())}"{self.ext((t.get("cta") or {}).get("href") or self.cta_href())}>{e((t.get("cta") or {}).get("texto", "comprar")).lower()}</a></div></div></section>\n')

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        det = "".join(f'<details><summary>{e(x.get("p")).lower()}<span aria-hidden="true">+</span></summary><p>{e(x.get("r")).lower()}</p></details>' for x in items)
        return f'<section class="faq mosaico" id="faq"><div class="tile crema"><h2>{e(" ".join(self.t["faq_t"])).lower()}</h2></div><div class="tile cafe acc">{det}</div></section>\n'

    def contacto(self):
        datos = self.contacto_items(); form = self.formulario()
        if not datos and not form: return ""
        lista = "".join(f'<a href="{ea(h)}"{self.ext(h)}><small>{e(k).lower()}</small>{e(v).lower()}</a>' for k, v, h in datos)
        co = self.d.get("contacto_seccion", {})
        ancha = "" if form else " ancha"
        return (f'<section class="contacto mosaico" id="contacto"><div class="tile crema{ancha}"><h2>{e(" ".join(co.get("titulo") or ["ven a vernos"])).lower()}</h2>'
                + (f'<p>{e(co["bajada"]).lower()}</p>' if co.get("bajada") else "") + f'<div class="datos">{lista}</div></div>'
                + (f'<div class="tile cafe">{form}</div>' if form else "") + '</section>\n')

    def secciones(self):
        return [self.portada(), self.mosaico(), self.pedidos(), self.carta(), self.tienda(), self.faq(), self.contacto()]

    def footer(self, desde=""):
        from datetime import date
        c = self.c; redes = []
        if c.get("instagram"): redes.append(f'<a href="https://instagram.com/{ea(c["instagram"].lstrip("@"))}" target="_blank" rel="noopener">instagram</a>')
        for k, lab in (("tiktok", "tiktok"), ("youtube", "youtube")):
            if c.get(k): redes.append(f'<a href="{ea(c[k])}" target="_blank" rel="noopener">{lab}</a>')
        return (f'<footer class="pie"><a href="{desde or "#top"}" class="burbuja pie-m">{e(self.m.get("nombre", "")).lower()}</a><div class="pie-fila"><div class="redes">{"".join(redes)}</div>'
                f'<div class="leg">{self.enlaces_legales(desde)}</div><span>© {date.today().year} {e(self.m.get("nombre", "")).lower()}</span></div></footer>\n')
