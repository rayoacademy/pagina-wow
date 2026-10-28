"""Pulso Energía · plantilla firma de la familia Pulso.

Fitness con energía. Firma: portada en duotono rosa a azul con titular apilado, equipo en mazo
de tarjetas con palabra gigante detrás, cifras con degradado, programas en tarjetas con foto que
sobresale, foto de artículo, pasos en tarjetas pastel y testimonios con palabra gigante de fondo.
"""
from generar_v3 import Gen3, e, ea

FL = '<i class="cir" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2.2"/></svg></i>'
IZQ = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5 8 12l7 7" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
DER = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 7 7-7 7" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
CHECK = '<svg class="ck" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="9" fill="currentColor" opacity=".16"/><path d="m6 10.3 2.6 2.6L14 7.5" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'


def t2(t):
    if isinstance(t, str): t = [x.strip() for x in t.split("|")]
    a = e(t[0]) if t else ""
    b = e(t[1]) if len(t) > 1 and t[1] else ""
    return a + (f' <span class="rosa">{b}</span>' if b else "")


class Plantilla(Gen3):

    def btn(self, b, cls="btn blanco"):
        if not b: return ""
        if isinstance(b, str): b = {"texto": b}
        href = b.get("href") or self.cta_href()
        return f'<a href="{ea(href)}" class="{cls}"{self.ext(href)}>{e(b["texto"])}{FL}</a>'

    def nav(self):
        links = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in self.menu()[:5])
        return (f'<nav class="nav" id="nav"><div class="nav-in"><a href="#top" class="marca">{e(self.m.get("nombre"))}</a><div class="links">{links}</div>'
                f'<a href="{ea(self.cta_href())}" class="btn rosa pq"{self.ext(self.cta_href())}>{e(self.d.get("nav_cta") or self.t["contacto"])}</a></div></nav>\n')

    def portada(self):
        h = self.d.get("hero", {})
        tit = h.get("titulo") or [self.m.get("nombre", "")]
        if isinstance(tit, str): tit = [tit]
        foco = f' style="object-position:50% {int(h["foco"])}%"' if h.get("foco") is not None else ""
        img = self.foto(h.get("imagen"), h.get("alt", ""), "ph", 2400).replace("<img ", f"<img{foco} ", 1).replace(' loading="lazy"', ' fetchpriority="high"')
        return (f'<header class="portada" id="top">{img}<div class="duo"></div><div class="wrap portada-in"><div>'
                + (f'<p class="eti rv">★ {e(h["etiqueta"])}</p>' if h.get("etiqueta") else "")
                + f'<h1 class="rv d1">{"".join(f"<span>{e(x)}</span>" for x in tit)}</h1></div><div class="lado rv d2">'
                + (f'<p>{e(h["texto"])}</p>' if h.get("texto") else "") + f'{self.btn(h.get("cta"))}</div></div></header>\n')

    def equipo(self):
        eq = self.d.get("equipo")
        if not eq: return ""
        items = eq.get("items", [])
        cartas = "".join(f'<figure class="carta"><div class="ca-f">{self.foto(x.get("foto"), x.get("nombre", ""), "", 900)}</div><figcaption><b>{e(x.get("nombre"))}</b><small>{e(x.get("rol", ""))}</small></figcaption></figure>' for x in items)
        nav = f'<button type="button" class="fl-b iz" data-mazo="-1" aria-label="Anterior">{IZQ}</button><button type="button" class="fl-b de" data-mazo="1" aria-label="Siguiente">{DER}</button>' if len(items) > 1 else ""
        palabra = eq.get("palabra") or ["Conoce", "al equipo"]
        cif = "".join(f'<div class="rv d{i % 3}"><b>{e(c.get("n"))}</b><small>{e(c.get("t"))}</small></div>' for i, c in enumerate(eq.get("cifras", [])))
        return (f'<section class="equipo" id="equipo"><div class="wrap"><div class="escena"><p class="fondo" aria-hidden="true">{"<br>".join(e(x) for x in palabra)}</p>'
                f'<div class="mazo">{cartas}</div>{nav}</div>' + (f'<div class="cifras">{cif}</div>' if cif else "") + "</div></section>\n")

    def programas(self):
        s = self.d.get("servicios")
        if not s: return ""
        cards = []
        for i, it in enumerate(s.get("items", [])):
            li = "".join(f"<li>{CHECK}{e(x)}</li>" for x in it.get("incluye", []))
            cards.append(f'<article class="prog{" inv" if i % 2 else ""} rv"><div class="pr-f">{self.foto(it.get("imagen"), it.get("titulo", ""), "", 800)}</div>'
                         f'<div class="pr-t"><h3>{e(it.get("titulo"))}</h3><p>{e(it.get("texto", ""))}</p>' + (f'<ul>{li}</ul>' if li else "")
                         + (f'<span class="precio">{e(it["precio"])}</span>' if it.get("precio") else "") + "</div></article>")
        return (f'<section class="programas" id="servicios"><div class="wrap angosto"><h2 class="rv">{t2(s.get("titulo") or [self.t["menu"]["servicios"]])}</h2>'
                + (f'<p class="baj rv">{e(s["bajada"])}</p>' if s.get("bajada") else "") + f'<div class="progs">{"".join(cards)}</div>'
                f'<div class="centro rv">{self.btn({"texto": self.d.get("nav_cta") or self.t["contacto"]}, "btn rosa")}</div></div></section>\n')

    def articulo(self):
        p = self.d.get("pausa")
        if not p or not p.get("imagen"): return ""
        return (f'<section class="articulo">{self.foto(p["imagen"], p.get("alt", ""), "", 2400)}<div class="velo"></div><div class="wrap ar-in">'
                + (f'<small class="rv">{e(p["etiqueta"])}</small>' if p.get("etiqueta") else "") + f'<h2 class="rv d1">{e(p.get("titulo", ""))}</h2>'
                + (f'<p class="rv d2">{e(p["texto"])}</p>' if p.get("texto") else "")
                + (f'<a class="lnk rv d3" href="{ea(p["href"])}"{self.ext(p["href"])}>{e(p.get("cta", "Leer más"))} ↗</a>' if p.get("href") else "") + "</div></section>\n")

    def pasos(self):
        p = self.d.get("proceso")
        if not p: return ""
        st = "".join(f'<li class="paso c{i % 4} rv d{i % 2}"><h3>{e(x.get("titulo"))}</h3><p>{e(x.get("texto"))}</p><i>↗</i></li>' for i, x in enumerate(p.get("items", [])))
        return (f'<section class="pasos-s" id="proceso"><div class="wrap">' + (f'<h2 class="rv">{t2(p["titulo"])}</h2>' if p.get("titulo") else "")
                + f'<ol class="pasos">{st}</ol></div></section>\n')

    def paquetes(self):
        p = self.d.get("paquetes")
        if not p: return ""
        cards = "".join(f'<div class="plan{" top" if x.get("destacado") else ""} rv"><h3>{e(x.get("nombre"))}</h3><p>{e(x.get("texto", ""))}</p><b>{e(x.get("precio"))}'
                        + (f'<small>{e(x["periodo"])}</small>' if x.get("periodo") else "") + f'</b><ul>' + "".join(f"<li>{CHECK}{e(y)}</li>" for y in x.get("incluye", []))
                        + f'</ul>{self.btn(x.get("cta") or {"texto": self.t["contacto"]}, "btn " + ("blanco" if x.get("destacado") else "rosa"))}</div>' for x in p.get("items", []))
        return f'<section class="paquetes" id="paquetes"><div class="wrap"><h2 class="rv">{t2(p.get("titulo") or [self.t["menu"]["paquetes"]])}</h2><div class="plans">{cards}</div></div></section>\n'

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        tit = self.d.get("faq_titulo") or (["¿Preguntas?", "Tenemos respuestas."] if self.lang == "es" else ["Questions?", "We've got answers."])
        det = "".join(f'<details{" open" if i == 0 else ""}><summary>{e(x.get("p"))}<span aria-hidden="true"></span></summary><p>{e(x.get("r"))}</p></details>' for i, x in enumerate(items))
        return (f'<section class="faq" id="faq"><div class="wrap"><div class="faq-caja"><div></div><div><h2 class="rv">{e(tit[0])}<span class="rosa">{e(tit[1]) if len(tit) > 1 else ""}</span></h2>'
                f'<p class="baj">{e(self.d.get("faq_bajada", ""))}</p><div class="acc">{det}</div></div></div></div></section>\n')

    def testimonios(self):
        t = self.d.get("testimonios")
        if not t: return ""
        its = t.get("items", [])
        fotos = "".join(f'<div class="tf rv d{i % 3}">{self.foto(x["foto"], x.get("nombre", ""), "", 900)}</div>' for i, x in enumerate(its[:3]) if x.get("foto"))
        cards = "".join(f'<figure class="tq rv d{i % 3}"><div class="tq-c">' + (f'<img src="{self.img(x["foto"], 200)}" alt="" loading="lazy"/>' if x.get("foto") else "<i></i>")
                        + f'<span><b>{e(x.get("nombre"))}</b><em>★★★★★</em></span></div>' + (f'<h3>{e(x["destacado"])}</h3>' if x.get("destacado") else "")
                        + f'<blockquote>{e(x.get("texto"))}</blockquote></figure>' for i, x in enumerate(its))
        palabra = t.get("palabra") or (["Lo que dicen"] if self.lang == "es" else ["Clients say"])
        return (f'<section class="testimonios" id="testimonios"><div class="wrap"><div class="tfs">{fotos}</div><p class="fondo" aria-hidden="true">{"<br>".join(e(x) for x in palabra)}</p>'
                f'<div class="tqs">{cards}</div></div></section>\n')

    def cierre(self):
        c = self.d.get("cierre") or {}
        form = self.formulario(); datos = self.contacto_items()
        tit = c.get("titulo") or ([self.t["contacto"]])
        return (f'<section class="cierre" id="contacto"><div class="wrap ci-grid"><div><h2 class="rv">{t2(tit)}</h2>'
                + (f'<p class="rv">{e(c["texto"])}</p>' if c.get("texto") else "") + f'<div class="rv">{self.btn(c.get("cta") or {"texto": self.t["contacto"]}, "btn rosa")}</div>'
                + f'<div class="datos">' + "".join(f'<a href="{ea(h)}"{self.ext(h)}><small>{e(k)}</small>{e(v)}</a>' for k, v, h in datos) + f'</div></div><div class="rv d1">{form}</div></div></section>\n')

    def secciones(self):
        return [self.portada(), self.equipo(), self.programas(), self.articulo(), self.pasos(), self.paquetes(), self.faq(), self.testimonios(), self.cierre()]

    def footer(self, desde=""):
        c = self.c; es = self.lang == "es"
        nav = "".join(f'<a href="{desde}{h}">{e(t)} ↗</a>' for h, t in self.menu())
        redes = []
        if c.get("instagram"): redes.append(f'<a href="https://instagram.com/{ea(c["instagram"].lstrip("@"))}" target="_blank" rel="noopener" aria-label="Instagram">IG</a>')
        for k, lab in (("tiktok", "TT"), ("youtube", "YT"), ("linkedin", "IN")):
            if c.get(k): redes.append(f'<a href="{ea(c[k])}" target="_blank" rel="noopener">{lab}</a>')
        from datetime import date
        return (f'<footer class="pie"><div class="wrap pie-grid"><div><a href="{desde or "#top"}" class="marca">{e(self.m.get("nombre"))}</a>'
                + (f'<p>{e(self.d.get("marca", {}).get("lema", ""))}</p>' if self.d.get("marca", {}).get("lema") else "")
                + (f'<a class="correo" href="mailto:{ea(c["email"])}">{e(c["email"])}</a>' if c.get("email") else "") + f'<div class="redes">{"".join(redes)}</div></div>'
                f'<div class="pie-nav"><small>{"Explora" if es else "Explore"}</small>{nav}</div></div>'
                f'<div class="wrap pie-base"><span>© {date.today().year} {e(self.m.get("nombre"))}</span><div class="leg">{self.enlaces_legales(desde)}</div></div></footer>\n')
