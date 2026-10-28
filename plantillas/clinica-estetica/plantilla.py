"""Clínica Estética · plantilla firma de la familia Clínica.

Clínica cálida y confiable. Firma: portada en tarjeta redondeada con tratamientos en arco,
frase en serif con íconos entre palabras, fotos flotando, tratamientos en filas con ícono,
profesional con nombre en vidrio, mosaico de por qué elegirnos y calificación sobre una foto.

Campos propios: sobre.iconos (palabras tras las que va un ícono), bento {imagen, cifras, texto}, proceso.imagen, testimonios.imagen
"""
import math
from generar_v3 import Gen3, e, ea

ICONOS = ['<path d="M12 3v18M3 12h18M5.6 5.6l12.8 12.8M18.4 5.6 5.6 18.4"/><circle cx="12" cy="12" r="3.5"/>',
          '<path d="M8 3c0 4-3 5-3 9a7 7 0 0 0 14 0c0-4-3-5-3-9"/><path d="M9 14c1 1.5 5 1.5 6 0"/>',
          '<rect x="3" y="8" width="18" height="10" rx="2"/><path d="M7 8V5h10v3M7 13h2M11 13h2M15 13h2"/>',
          '<circle cx="12" cy="9" r="5"/><path d="M5 21c1-4 4-6 7-6s6 2 7 6"/>',
          '<path d="M12 21s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 5.5-7 10-7 10Z"/>']
HOJA = '<svg class="ic-in" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20C4 10 10 4 20 4c0 10-6 16-16 16Z" fill="#7a9a5e"/><path d="M4 20 14 10" stroke="#fff" stroke-width="1.4"/></svg>'
GOTA = '<svg class="ic-in" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C8 8 5 11 5 15a7 7 0 0 0 14 0c0-4-3-7-7-13Z" fill="#9a5b3c"/></svg>'
CHECK = '<svg class="ck" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="9" fill="none" stroke="currentColor" stroke-opacity=".45"/><path d="m6 10.2 2.6 2.6L14 7.4" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'


def t2(t):
    if isinstance(t, str): t = [x.strip() for x in t.split("|")]
    return "<br>".join(e(x) for x in t if x)


class Plantilla(Gen3):

    def chip(self, x):
        return f'<span class="chip"><i></i>{e(x).upper()}</span>' if x else ""

    def btn(self, b, cls="btn cafe"):
        if not b: return ""
        if isinstance(b, str): b = {"texto": b}
        href = b.get("href") or self.cta_href()
        return f'<a href="{ea(href)}" class="{cls}"{self.ext(href)}><i class="pt"></i>{e(b["texto"])}</a>'

    def nav(self):
        links = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in self.menu()[:5])
        return (f'<nav class="nav" id="nav"><div class="nav-in"><a href="#top" class="marca">{e(self.m.get("nombre"))}</a><div class="links">{links}</div>'
                f'{self.btn({"texto": self.d.get("nav_cta") or self.t["contacto"]}, "btn cafe pq")}</div></nav>\n')

    def portada(self):
        h = self.d.get("hero", {})
        arco = h.get("arco") or [x.get("titulo") for x in (self.d.get("servicios") or {}).get("items", [])][:6]
        n = len(arco); marcas = ""
        for i, x in enumerate(arco):
            ang = -60 + (120 * i / max(1, n - 1))  # de -60° a 60°
            rad = math.radians(ang)
            left = 50 + 38 * math.sin(rad); top = 100 - 46 * math.cos(rad)
            marcas += f'<span class="pto-arco" style="left:{left:.1f}%;top:{top:.1f}%;--r:{ang:.0f}deg"><i></i><b>{e(x)}</b></span>'
        img = self.foto(h.get("imagen"), h.get("alt", ""), "ph", 2400).replace(' loading="lazy"', ' fetchpriority="high"')
        return (f'<header class="portada" id="top"><div class="tarjeta">{img}<div class="velo"></div><div class="pt-in"><h1 class="rv">{t2(h.get("titulo") or [self.m.get("nombre", "")])}</h1>'
                + (f'<p class="rv d1">{e(h["texto"])}</p>' if h.get("texto") else "") + f'</div><div class="arco" aria-hidden="true">{marcas}</div>'
                f'<a class="muesca" href="#servicios">{e(h.get("muesca", "Ver tratamientos" if self.lang == "es" else "Explore our treatments"))}</a></div></header>\n')

    def frase(self):
        s = self.d.get("sobre")
        if not s: return ""
        txt = e(s.get("bajada", ""))
        for i, palabra in enumerate(s.get("iconos", [])):
            txt = txt.replace(e(palabra), e(palabra) + (GOTA if i % 2 == 0 else HOJA), 1)
        datos = (self.d.get("hero") or {}).get("datos") or []
        nota = (f'<p class="nota-r"><b>{e(datos[0].get("n"))}</b><span>★★★★★<small>{e(datos[0].get("t"))}</small></span></p>' if datos else "")
        fotos = self.fotos_galeria()[:4]
        flot = "".join(f'<figure class="flt f{i} rv d{i % 3}">{self.foto(f.get("src"), f.get("alt", ""), "", 800)}</figure>' for i, f in enumerate(fotos))
        return (f'<section class="frase" id="sobre"><div class="wrap"><div class="centro">{self.chip(s.get("etiqueta", ""))}<p class="grande rv">{txt}</p>{nota}</div>'
                + (f'<div class="flotantes">{flot}</div>' if flot else "") + "</div></section>\n")

    def tratamientos(self):
        s = self.d.get("servicios")
        if not s: return ""
        filas = "".join(f'<details class="tr rv"><summary><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3">{ICONOS[i % len(ICONOS)]}</svg></span>'
                        f'<h3>{e(it.get("titulo"))}</h3><div class="tr-d"><p>{e(it.get("texto", ""))}</p><span class="ver">{"Ver detalle" if self.lang == "es" else "View detail"}</span></div><span class="mas" aria-hidden="true">+</span></summary>'
                        f'<div class="tr-in">' + "".join(f'<p>{e(x)}</p>' for x in it.get("detalle", [])) + (f'<p class="pr">{e(it["precio"])}</p>' if it.get("precio") else "") + "</div></details>"
                        for i, it in enumerate(s.get("items", [])))
        return (f'<section class="tratamientos" id="servicios"><div class="wrap"><div class="cab">{self.chip(s.get("etiqueta", self.t["menu"]["servicios"]))}<h2 class="rv">{t2(s.get("titulo", ""))}</h2></div>'
                f'<div class="trs">{filas}</div></div></section>\n')

    def profesional(self):
        s = self.d.get("sobre") or {}
        f = s.get("firma") or {}
        if not s.get("imagen"): return ""
        puntos = "".join(f'<li>{CHECK}{e(x)}</li>' for x in s.get("puntos", []))
        ps = "".join(f'<p>{e(p)}</p>' for p in s.get("texto", []))
        return (f'<section class="profesional"><div class="wrap"><div class="caja"><figure class="pr-f rv">{self.foto(s["imagen"], s.get("alt", ""), "", 1200)}'
                f'<figcaption class="vidrio"><b>{e(f.get("nombre", ""))}</b><small>{e(f.get("rol", ""))}</small></figcaption></figure>'
                f'<div class="pr-t rv d1">{self.chip(s.get("etiqueta2", ""))}<h2>{t2(s.get("titulo", ""))}</h2>{ps}' + (f'<ul>{puntos}</ul>' if puntos else "")
                + f'{self.btn(s.get("cta") or {"texto": self.d.get("nav_cta") or self.t["contacto"]})}</div></div></div></section>\n')

    def bento(self):
        b = self.d.get("bento")
        if not b: return ""
        cif = b.get("cifras", [])
        def stat(c, cls=""): return f'<div class="bt stat {cls} rv"><b>{e(c.get("n"))}</b><small>{e(c.get("t"))}</small>' + (f'<span class="marca-agua" aria-hidden="true">{e(c["fondo"])}</span>' if c.get("fondo") else "") + "</div>"
        avs = "".join(f'<img src="{self.img(x["foto"], 200)}" alt=""/>' for x in (self.d.get("testimonios") or {}).get("items", []) if x.get("foto"))
        celdas = [f'<div class="bt foto alta rv">{self.foto(b.get("imagen"), b.get("alt", ""), "", 1000)}<p class="vidrio">{e(b.get("pie", ""))}</p></div>']
        if b.get("texto"): celdas.append(f'<div class="bt txt rv"><p>{e(b["texto"])}</p></div>')
        if cif: celdas.append(stat(cif[0], "alta2"))
        celdas.append(f'<div class="bt avs rv"><div class="fila-av">{avs}</div><p>{e(b.get("texto2", ""))}</p></div>')
        if len(cif) > 1: celdas.append(stat(cif[1]))
        if b.get("cta"): celdas.append(f'<div class="bt cta rv"><h3>{e(b["cta"].get("titulo", ""))}</h3><p>{e(b["cta"].get("bajada", ""))}</p>{self.btn(b["cta"])}</div>')
        return (f'<section class="bento-s"><div class="wrap"><div class="cab">{self.chip(b.get("etiqueta", ""))}<h2 class="rv">{t2(b.get("titulo", ""))}</h2></div>'
                f'<div class="bento">{"".join(celdas)}</div></div></section>\n')

    def ciencia(self):
        p = self.d.get("proceso")
        if not p: return ""
        li = "".join(f'<li>{CHECK}{e(x.get("titulo"))}</li>' for x in p.get("items", []))
        foto = (f'<figure class="ci-f rv d1">{self.foto(p["imagen"], p.get("alt", ""), "", 1400)}<figcaption class="vidrio">{e(p.get("pie", ""))}</figcaption></figure>' if p.get("imagen") else "")
        return (f'<section class="ciencia" id="proceso"><div class="wrap ci-grid"><div class="rv">{self.chip(p.get("etiqueta", ""))}<h2>{t2(p.get("titulo", ""))}</h2>'
                + (f'<p>{e(p["bajada"])}</p>' if p.get("bajada") else "") + f'<ul>{li}</ul></div>{foto}</div></section>\n')

    def testimonios(self):
        t = self.d.get("testimonios")
        if not t: return ""
        cards = "".join(f'<figure class="tq rv d{i % 2}"><b class="est">★★★★★</b><blockquote>{e(x.get("texto"))}</blockquote><figcaption>'
                        + (f'<img src="{self.img(x["foto"], 200)}" alt=""/>' if x.get("foto") else "") + f'<span>{e(x.get("nombre"))}<small>{e(x.get("rol", ""))}</small></span></figcaption></figure>'
                        for i, x in enumerate(t.get("items", [])[:2]))
        datos = (self.d.get("hero") or {}).get("datos") or [{}]
        foto = (f'<figure class="tq-f rv">{self.foto(t["imagen"], "", "", 900)}<figcaption class="vidrio"><b>{e(datos[0].get("n", ""))}</b><span>★★★★★</span><small>{e(t.get("pie", "calificación" if self.lang == "es" else "client rating"))}</small></figcaption></figure>' if t.get("imagen") else "")
        return (f'<section class="testimonios" id="testimonios"><div class="wrap tq-grid"><div><h2 class="rv">{t2(t.get("titulo") or [self.t["menu"]["testimonios"]])}</h2><div class="tqs">{cards}</div></div>{foto}</div></section>\n')

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        det = "".join(f'<details><summary>{e(x.get("p"))}<span aria-hidden="true">+</span></summary><p>{e(x.get("r"))}</p></details>' for x in items)
        return f'<section class="faq" id="faq"><div class="wrap angosto"><div class="cab">{self.chip(self.t["menu"]["faq"])}<h2 class="rv">{t2(self.t["faq_t"])}</h2></div><div class="acc">{det}</div></div></section>\n'

    def cierre(self):
        c = self.d.get("cierre") or {}
        form = self.formulario(); datos = self.contacto_items()
        lista = "".join(f'<a href="{ea(h)}"{self.ext(h)}><small>{e(k)}</small>{e(v)}</a>' for k, v, h in datos)
        foto = self.foto(c.get("imagen"), "", "", 2200) if c.get("imagen") else ""
        return (f'<section class="cierre" id="contacto"><div class="wrap"><div class="ci-banda">{foto}<div class="ci-txt"><h2 class="rv">{t2(c.get("titulo") or [self.t["contacto"]])}</h2>'
                + (f'<p class="rv">{e(c["texto"])}</p>' if c.get("texto") else "") + f'{self.btn(c.get("cta") or {"texto": self.t["contacto"]})}</div></div>'
                + f'<div class="ct-grid"><div class="datos">{lista}</div><div>{form}</div></div></div></section>\n')

    def secciones(self):
        return [self.portada(), self.frase(), self.tratamientos(), self.profesional(), self.bento(), self.ciencia(), self.testimonios(), self.faq(), self.cierre()]

    def footer(self, desde=""):
        from datetime import date
        nav = "".join(f'<a href="{desde}{h}">{e(t)}</a>' for h, t in self.menu())
        return (f'<footer class="pie"><div class="wrap pie-in"><a href="{desde or "#top"}" class="marca">{e(self.m.get("nombre"))}</a><div class="pie-nav">{nav}</div>'
                f'<div class="pie-base"><span>© {date.today().year} {e(self.m.get("nombre"))}</span><div class="leg">{self.enlaces_legales(desde)}</div></div></div></footer>\n')
