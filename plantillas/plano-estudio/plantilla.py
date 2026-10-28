"""Plano Estudio · plantilla firma de la familia Plano.

Estudio técnico y sereno. Firma: lista de servicios en monoespaciada junto al titular,
frase gris grande con firma, obras 2x2 con nombre encima, cifras enormes, servicios con
miniaturas, proceso como tabla, cierre oscuro con tira de fotos y correo gigante en el pie.
"""
from generar_v3 import Gen3, e, ea

FIRMA = ('<svg class="firma" viewBox="0 0 320 110" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true">'
         '<path d="M18 80c10-40 30-66 42-62 10 4-12 50-24 66-6 8 4 4 14-6"/><path d="M58 70c8-6 16-6 14 2s4 10 14 0c8-8 10-20 4-20-8 0-6 26 8 26 12 0 24-28 28-44 2-8-6-2-8 10-4 22 0 36 10 34"/>'
         '<path d="M140 78c6-22 14-40 18-38s-8 34-4 38 16-36 22-36-6 30 0 34 18-20 24-34c3-7-4-4-6 6-4 18 2 30 12 28 14-2 30-24 36-36"/><path d="M60 92c70-10 150-14 236-8"/></svg>')
FL = '<span aria-hidden="true">→</span>'


def mono(x):
    return f'<span class="mono">{e(x)}</span>' if x else ""


def t2(t):
    if isinstance(t, str): t = [x.strip() for x in t.split("|")]
    return "<br>".join(e(x) for x in t if x)


class Plantilla(Gen3):

    def link(self, b):
        if not b: return ""
        if isinstance(b, str): b = {"texto": b}
        href = b.get("href") or self.cta_href()
        return f'<a class="lnk" href="{ea(href)}"{self.ext(href)}>{e(b["texto"])} {FL}</a>'

    def nav(self):
        links = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in self.menu()[:6])
        return (f'<nav class="nav" id="nav"><div class="nav-in"><a href="#top" class="marca">{e(self.m.get("nombre", "")).upper()}</a>'
                f'<div class="links">{links}<a href="#contacto" class="cta">{e(self.d.get("nav_cta") or self.t["contacto"])}</a></div></div></nav>\n')

    def portada(self):
        h = self.d.get("hero", {})
        lista = h.get("lista") or [x.get("titulo") for x in (self.d.get("servicios") or {}).get("items", [])]
        img = self.foto(h.get("imagen"), h.get("alt", ""), "ph", 2400).replace(' loading="lazy"', ' fetchpriority="high"')
        lugares = "".join(f"<span>+ {e(x)}</span>" for x in h.get("lugares", []))
        return (f'<header class="portada" id="top">{img}<div class="velo"></div><div class="wrap portada-in"><ul class="lista mono rv">'
                + "".join(f"<li>{e(x)}</li>" for x in lista if x) + f'</ul><div class="pt"><h1 class="rv d1">{t2(h.get("titulo") or [self.m.get("nombre", "")])}</h1>'
                + (f'<p class="rv d2">{e(h["texto"])}</p>' if h.get("texto") else "") + f'<div class="rv d3">{self.link(h.get("cta"))}</div></div>'
                + (f'<div class="lugares mono">{lugares}</div>' if lugares else "") + "</div></header>\n")

    def statement(self):
        s = self.d.get("sobre")
        if not s: return ""
        f = s.get("firma") or {}
        return (f'<section class="statement" id="sobre"><div class="wrap st-grid"><div>{mono(s.get("etiqueta", self.t["menu"]["sobre"]))}<span class="comillas" aria-hidden="true">99</span>'
                f'<p class="frase rv">{e(s.get("bajada", ""))}</p>{self.link(s.get("cta") or {"texto": "Ver servicios" if self.lang == "es" else "See services", "href": "#servicios"})}</div>'
                f'<div class="persona rv d1">' + (f'<div class="pe-foto">{self.foto(s.get("imagen"), s.get("alt", ""), "", 900)}</div>' if s.get("imagen") else "")
                + f'<div class="pe-txt"><b>{e(f.get("nombre", ""))}</b>{mono(f.get("rol", ""))}</div>{FIRMA}</div></div></section>\n')

    def obras(self):
        g = self.d.get("galeria"); fotos = self.fotos_galeria()
        if not fotos: return ""
        gd = g if isinstance(g, dict) else {}
        datos = "".join(f'<span><b>{e(x.get("n"))}</b>{mono(x.get("t"))}</span>' for x in gd.get("datos", []))
        cards = "".join(f'<article class="obra rv d{i % 2}"><div class="ob-foto">{self.foto(f.get("src"), f.get("alt", ""), "", 1400)}<span class="ob-n">{e(f.get("nombre", ""))}</span></div>'
                        f'<div class="ob-pie"><span>{mono(f.get("etiqueta", ""))}<b>{e(f.get("titulo", ""))}</b></span>{mono(f.get("texto", ""))}</div></article>' for i, f in enumerate(fotos[:4]))
        return (f'<section class="obras" id="galeria"><div class="wrap"><div class="cab">{mono(gd.get("etiqueta", ""))}<div class="cab-fila"><div><h2>{t2(gd.get("titulo") or [self.t["galeria"][0]])}</h2>'
                + (f'<p>{e(gd["bajada"])}</p>' if gd.get("bajada") else "") + f'</div><div class="datos">{datos}</div></div>'
                + (f'<div class="ver">{self.link(gd["ver_todo"])}</div>' if gd.get("ver_todo") else "") + f'</div><div class="ob-grid">{cards}</div></div></section>\n')

    def cifras(self):
        s = self.d.get("sobre") or {}
        cif = s.get("cifras", [])
        if not cif: return ""
        c = "".join(f'<div class="ci rv d{i % 3}">{mono(x.get("e", ""))}<b>{e(x.get("n"))}</b><p>{e(x.get("t"))}</p></div>' for i, x in enumerate(cif[:3]))
        tit = s.get("cifras_titulo") or (["En números"] if self.lang == "es" else ["By the numbers"])
        return (f'<section class="cifras"><div class="wrap"><div class="cab">{mono(s.get("cifras_etiqueta", "Datos" if self.lang == "es" else "Stats"))}<div class="cab-fila corrido"><h2>{t2(tit)}</h2>'
                + (f'<p>{e(s["cifras_bajada"])}</p>' if s.get("cifras_bajada") else "") + f'</div></div><div class="ci-grid">{c}</div></div></section>\n')

    def servicios(self):
        s = self.d.get("servicios")
        if not s: return ""
        filas = []
        for i, it in enumerate(s.get("items", [])):
            li = "".join(f"<li>{e(x)}</li>" for x in it.get("incluye", []))
            filas.append(f'<details class="sv"{" open" if i == 0 else ""}><summary>' + (f'<span class="sv-th">{self.foto(it["imagen"], "", "", 500)}</span>' if it.get("imagen") else '<span class="sv-th"></span>')
                         + f'<span class="sv-t">{mono(f"{i + 1:02d}")}<b>{e(it.get("titulo"))}</b></span><span class="mas" aria-hidden="true">+</span></summary>'
                         f'<div class="sv-in"><p>{e(it.get("texto", ""))}</p>' + (f'<ul>{li}</ul>' if li else "") + "</div></details>")
        return (f'<section class="servicios" id="servicios"><div class="wrap sv-grid"><div class="fijo">{mono(s.get("etiqueta", self.t["menu"]["servicios"]))}<h2>{t2(s.get("titulo", ""))}</h2>'
                + (f'<p>{e(s["bajada"])}</p>' if s.get("bajada") else "") + f'<div class="sv-cta">{mono(s.get("cta_etiqueta") or ("¿Hablamos?" if self.lang == "es" else "Let's talk"))}{self.link({"texto": self.d.get("nav_cta") or self.t["contacto"]})}</div></div>'
                f'<div class="svs">{"".join(filas)}</div></div></section>\n')

    def proceso(self):
        p = self.d.get("proceso")
        if not p: return ""
        filas = "".join(f'<li class="rv">{mono(f"#{i + 1:02d}")}<b>{e(x.get("titulo"))}</b><p>{e(x.get("texto"))}</p></li>' for i, x in enumerate(p.get("items", [])))
        return (f'<section class="proceso" id="proceso"><div class="wrap"><div class="cab">{mono(p.get("etiqueta", self.t["menu"]["proceso"]))}<div class="cab-fila corrido"><h2>{t2(p.get("titulo", ""))}</h2>'
                + (f'<p>{e(p["bajada"])}</p>' if p.get("bajada") else "") + f'</div></div><ol class="tabla">{filas}</ol></div></section>\n')

    def testimonios(self):
        t = self.d.get("testimonios")
        if not t: return ""
        x = (t.get("items") or [{}])[0]
        clientes = "".join(f'<span>{e(c)}</span>' for c in self.d.get("clientes", []))
        return (f'<section class="testimonios" id="testimonios"><div class="wrap"><div class="cab">{mono(t.get("etiqueta", self.t["menu"]["testimonios"]))}<div class="cab-fila corrido"><h2>{t2(t.get("titulo", ""))}</h2>'
                + (f'<p>{e(t["bajada"])}</p>' if t.get("bajada") else "") + f'</div></div><div class="tq-grid"><div><span class="comillas" aria-hidden="true">99</span><blockquote class="frase rv">{e(x.get("texto", ""))}</blockquote></div>'
                f'<div class="persona rv d1">' + (f'<div class="pe-foto">{self.foto(x.get("foto"), x.get("nombre", ""), "", 900)}</div>' if x.get("foto") else "")
                + f'<div class="pe-txt"><b>{e(x.get("nombre", ""))}</b>{mono(x.get("rol", ""))}</div></div></div>'
                + (f'{mono(t.get("clientes_titulo", "Confían en nosotros" if self.lang == "es" else "Trusted by"))}<div class="clientes">{clientes}</div>' if clientes else "") + "</div></section>\n")

    def paquetes(self):
        p = self.d.get("paquetes")
        if not p: return ""
        filas = "".join(f'<li class="rv"><span>{mono(x.get("periodo", ""))}<b>{e(x.get("nombre"))}</b></span><span class="pq-p">{e(x.get("precio"))}</span><p>{e(x.get("texto", ""))}</p></li>' for x in p.get("items", []))
        return (f'<section class="proceso" id="paquetes"><div class="wrap"><div class="cab">{mono(p.get("etiqueta", self.t["menu"]["paquetes"]))}<div class="cab-fila corrido"><h2>{t2(p.get("titulo", ""))}</h2></div></div>'
                f'<ol class="tabla precios">{filas}</ol></div></section>\n')

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        det = "".join(f'<details{" open" if i == 0 else ""}><summary>{mono(f"{i + 1:02d}")}<b>{e(x.get("p"))}</b><span class="mas" aria-hidden="true">+</span></summary><p>{e(x.get("r"))}</p></details>' for i, x in enumerate(items))
        return (f'<section class="faq" id="faq"><div class="wrap angosto">{mono(self.t["menu"]["faq"])}<h2>{t2(self.d.get("faq_titulo") or self.t["faq_t"])}</h2>'
                f'<div class="acc">{det}</div><p class="faq-pie">{mono(self.t["faq_p"])} {self.link({"texto": self.t["contacto"], "href": "#contacto"})}</p></div></section>\n')

    def cierre(self):
        c = self.d.get("cierre") or {}
        tira = "".join(f'<div>{self.foto(f, "", "", 900)}</div>' for f in c.get("imagenes", [])[:5])
        form = self.formulario()
        return (f'<section class="cierre" id="contacto"><div class="wrap angosto"><h2 class="rv">{t2(c.get("titulo") or [self.t["contacto"]])}</h2>'
                + (f'<p class="rv d1">{e(c["texto"])}</p>' if c.get("texto") else "") + f'<div class="rv d2">{self.link(c.get("cta") or {"texto": self.t["contacto"]})}</div>'
                + (f'<div class="ci-form rv">{form}</div>' if form else "") + "</div>" + (f'<div class="tira" style="--n:{len(c.get("imagenes", [])[:5])}">{tira}</div>' if tira else "") + "</section>\n")

    def secciones(self):
        return [self.portada(), self.statement(), self.obras(), self.cifras(), self.servicios(), self.proceso(), self.testimonios(), self.paquetes(), self.faq(), self.cierre()]

    def footer(self, desde=""):
        c = self.c; es = self.lang == "es"
        nav = "".join(f'<a href="{desde}{h}">{e(t)}</a>' for h, t in self.menu())
        redes = []
        if c.get("instagram"): redes.append(f'<a href="https://instagram.com/{ea(c["instagram"].lstrip("@"))}" target="_blank" rel="noopener">Instagram</a>')
        for k, lab in (("linkedin", "LinkedIn"), ("youtube", "YouTube")):
            if c.get(k): redes.append(f'<a href="{ea(c[k])}" target="_blank" rel="noopener">{lab}</a>')
        lema = self.d.get("marca", {}).get("lema", "")
        from datetime import date
        return (f'<footer class="pie"><div class="wrap"><div class="pie-top"><div>' + (f'<p class="lema">{e(lema)}</p>' if lema else "")
                + (f'<a class="correo" href="mailto:{ea(c["email"])}">{e(c["email"])}</a>' if c.get("email") else "")
                + (f'<span class="tel">{e(c.get("telefono") or c.get("whatsapp"))}</span>' if (c.get("telefono") or c.get("whatsapp")) else "")
                + (f'<span class="tel">{e(", ".join(x for x in (c.get("direccion"), c.get("ciudad")) if x))}</span>' if c.get("direccion") else "")
                + f'</div><div class="pie-cols"><div>{mono("Menú" if es else "Menu")}{nav}</div><div>{mono("Redes" if es else "Social")}{"".join(redes)}</div></div></div>'
                f'<div class="pie-base"><div class="leg">{self.enlaces_legales(desde)}</div><span>© {date.today().year} {e(self.m.get("nombre"))}</span></div></div></footer>\n')
