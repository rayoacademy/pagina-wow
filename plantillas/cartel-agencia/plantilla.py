"""Cartel Agencia · plantilla firma de la familia Cartel.

Agencia con actitud. Firma: palabra gigante condensada con degradado, panel rojo con foto,
cifras y etiquetas, marquesina de servicios, proceso en escalera, servicios desplegables,
casos con cliente y servicios, testimonios dispersos sobre negro, pregunta abierta en rojo.
"""
from generar_v3 import Gen3, e, ea

FL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2"/></svg>'


def t2(t):
    if isinstance(t, str): t = [x.strip() for x in t.split("|")]
    return "<br>".join(e(x) for x in t if x)


class Plantilla(Gen3):

    def btn(self, b, cls="btn rojo"):
        if not b: return ""
        if isinstance(b, str): b = {"texto": b}
        href = b.get("href") or self.cta_href()
        return f'<a href="{ea(href)}" class="{cls}"{self.ext(href)}>{e(b["texto"])}{FL}</a>'

    def nav(self):
        links = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in self.menu()[:6])
        return (f'<nav class="nav" id="nav"><div class="nav-in"><a href="#top" class="marca">{e(self.m.get("nombre"))}</a><div class="links">{links}</div>'
                f'{self.btn({"texto": self.d.get("nav_cta") or self.t["contacto"]}, "btn rojo pq")}</div></nav>\n')

    def portada(self):
        h = self.d.get("hero", {})
        palabra = h.get("nombre_grande") or self.m.get("nombre", "")
        datos = "".join(f'<div><b>{e(x.get("n"))}</b><small>{e(x.get("t"))}</small></div>' for x in h.get("datos", [])[:3])
        chips = "".join(f'<span>{e(x)}</span>' for x in h.get("chips", []))
        img = self.foto(h.get("imagen"), h.get("alt", ""), "ph", 2200).replace(' loading="lazy"', ' fetchpriority="high"')
        return (f'<header class="portada" id="top"><div class="wrap"><div class="sup"><span>{e(h.get("etiqueta", ""))}</span><span>{e(h.get("etiqueta2", ""))}</span></div>'
                f'<h1 class="palabra" data-fit>{e(palabra).upper()}</h1></div>'
                f'<div class="panel">{img}<div class="velo"></div><div class="wrap panel-in"><div class="datos">{datos}</div>'
                f'<div class="abajo"><div>' + (f'<p class="lede">{e(h["texto"])}</p>' if h.get("texto") else "")
                + f'<div class="ctas">{self.btn(h.get("cta"), "btn blanco")}{self.btn(h.get("cta2"), "btn vidrio")}</div></div><div class="chips">{chips}</div></div></div></div></header>\n')

    def marquesina(self):
        m = self.d.get("marquesina")
        if not m: return ""
        sp = "".join(f"<span>/ {e(x).upper()}</span>" for x in m) * 2
        return f'<div class="mq" aria-hidden="true"><div class="mq-t">{sp}</div></div>\n'

    def statement(self):
        s = self.d.get("sobre")
        if not s: return ""
        tit = s.get("titulo") or []
        if isinstance(tit, str): tit = [tit]
        lista = "".join(f"<li>{e(x).upper()}</li>" for x in s.get("puntos", []))
        frase = (f'<span class="osc">{e(tit[0])}</span> ' if tit else "") + (f'<span class="cla">{e(tit[1])}</span>' if len(tit) > 1 else "")
        clientes = "".join(f'<span class="cli"><i></i>{e(c)}</span>' for c in self.d.get("clientes", []))
        return (f'<section class="statement" id="sobre"><div class="wrap"><div class="st-grid"><ul class="rv">{lista}</ul><p class="frase rv d1">{frase}</p></div>'
                + (f'<div class="cl-cab"><h2 class="rv">{e(s.get("clientes_titulo", "Nuestros clientes" if self.lang == "es" else "Our clients"))}</h2>'
                   + (f'<p class="rv">{e(s["clientes_texto"])}</p>' if s.get("clientes_texto") else "") + f'</div><div class="clis">{clientes}</div>' if clientes else "")
                + "</div></section>\n")

    def cab(self, s, k, oscuro=False):
        return (f'<div class="cab"><h2 class="rv">{t2(s.get("titulo") or [self.t["menu"].get(k, "")])}</h2>'
                + (f'<p class="rv d1">{e(s["bajada"])}</p>' if s.get("bajada") else "") + "</div>")

    def proceso(self):
        p = self.d.get("proceso")
        if not p: return ""
        n = len(p.get("items", []))
        st = "".join(f'<li class="rv" style="--i:{i}"><b>{i + 1:02d}</b><h3>{e(x.get("titulo"))}</h3><p>{e(x.get("texto"))}</p></li>' for i, x in enumerate(p.get("items", [])))
        return f'<section class="proceso" id="proceso"><div class="wrap">{self.cab(p, "proceso")}<ol class="escalera" style="--n:{n}">{st}</ol></div></section>\n'

    def servicios(self):
        s = self.d.get("servicios")
        if not s: return ""
        filas = []
        for i, it in enumerate(s.get("items", [])):
            chips = "".join(f"<span>{e(c)}</span>" for c in it.get("chips", []))
            interior = (f'<div class="sv-in">' + (f'<div class="sv-foto">{self.foto(it["imagen"], it.get("titulo", ""), "", 1200)}</div>' if it.get("imagen") else "")
                        + f'<div class="sv-txt">' + (f'<b class="sv-n">{e(it["cifra"])}</b>' if it.get("cifra") else "") + f'<p>{e(it.get("texto", ""))}</p>'
                        + (f'<div class="sv-chips">{chips}</div>' if chips else "") + "</div></div>")
            filas.append(f'<details class="sv"{" open" if i == 0 else ""}><summary><span class="n">{i + 1:02d}</span><span class="tt"><small>{e(it.get("tipo", ""))}</small>{e(it.get("titulo"))}</span>'
                         f'{self.btn({"texto": it.get("cta", self.d.get("nav_cta") or self.t["contacto"])}, "btn rojo pq")}</summary>{interior}</details>')
        return (f'<section class="servicios" id="servicios"><div class="wrap">{self.cab(s, "servicios")}</div><div class="svs">{"".join(filas)}</div></section>\n')

    def casos(self):
        g = self.d.get("galeria"); fotos = self.fotos_galeria()
        if not fotos: return ""
        gd = g if isinstance(g, dict) else {}
        es = self.lang == "es"
        cards = "".join(f'<article class="caso rv"><div class="ca-txt"><h3>{e(f.get("titulo", ""))}</h3><p>{e(f.get("texto", ""))}</p>'
                        + (f'<small>{"Cliente" if es else "Client"}</small><span class="pto">{e(f["cliente"])}</span>' if f.get("cliente") else "")
                        + (f'<small>{"Servicios" if es else "Services"}</small><span class="pto">{" · ".join(e(x) for x in f.get("servicios", []))}</span>' if f.get("servicios") else "")
                        + f'{self.btn({"texto": f.get("cta", "Ver el caso" if es else "See the case"), "href": f.get("href", "#contacto")}, "btn rojo pq")}</div>'
                        f'<div class="ca-foto">{self.foto(f.get("src"), f.get("alt", ""), "", 1400)}</div></article>' for f in fotos)
        return f'<section class="casos" id="galeria"><div class="wrap">{self.cab(gd, "")}<div class="cas">{cards}</div></div></section>\n'

    def testimonios(self):
        t = self.d.get("testimonios")
        if not t: return ""
        cards = "".join(f'<figure class="tq rv" style="--x:{(4, 62, 14, 58, 30)[i % 5]}%;--y:{(0, 12, 40, 52, 78)[i % 5]}%"><b class="est">★★★★★</b>'
                        f'<blockquote>{e(x.get("texto"))}</blockquote>' + (f'<p class="fuerte">{e(x["destacado"])}</p>' if x.get("destacado") else "")
                        + f'<figcaption>{e(x.get("nombre"))}' + (f'<small>{e(x["rol"])}</small>' if x.get("rol") else "") + "</figcaption></figure>" for i, x in enumerate(t.get("items", [])))
        centro = self.foto(t.get("imagen"), "", "centro", 1600) if t.get("imagen") else ""
        return (f'<section class="testimonios" id="testimonios">{centro}<div class="velo"></div><h2 class="tq-t">{t2(t.get("titulo") or [self.t["menu"]["testimonios"]])}</h2>'
                f'<div class="wrap tqs" style="--n:{len(t.get("items", []))}">{cards}</div></section>\n')

    def paquetes(self):
        p = self.d.get("paquetes")
        if not p: return ""
        cards = []
        for x in p.get("items", []):
            li = "".join(f"<li>{e(y)}</li>" for y in x.get("incluye", []))
            top = x.get("destacado")
            cards.append(f'<div class="plan{" top" if top else ""} rv"><div class="pl-cab"><h3>{e(x.get("nombre"))}</h3>' + (f'<span class="pop">{"Popular"}</span>' if top else "")
                         + f'</div><p>{e(x.get("texto", ""))}</p><div class="precio">{e(x.get("precio"))}' + (f'<small>{e(x["periodo"])}</small>' if x.get("periodo") else "") + "</div>"
                         f'{self.btn(x.get("cta") or {"texto": "Escoger plan" if self.lang == "es" else "Select plan"}, "btn " + ("rojo" if top else "linea") + " ancho")}'
                         f'<h4>{"Incluye" if self.lang == "es" else "Features"}</h4><ul>{li}</ul></div>')
        return f'<section class="paquetes" id="paquetes"><div class="wrap">{self.cab(p, "paquetes")}<div class="plans">{"".join(cards)}</div></div></section>\n'

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        det = "".join(f'<details{" open" if i == 0 else ""}><summary>{e(x.get("p"))}<span aria-hidden="true"></span></summary><p>{e(x.get("r"))}</p></details>' for i, x in enumerate(items))
        return f'<section class="faq" id="faq"><div class="wrap">{self.cab({"titulo": self.d.get("faq_titulo") or self.t["faq_t"]}, "faq")}<div class="acc rv">{det}</div></div></section>\n'

    def cierre(self):
        c = self.d.get("cierre") or {}
        form = self.formulario(); datos = self.contacto_items()
        lista = "".join(f'<a href="{ea(h)}"{self.ext(h)}><small>{e(k)}</small>{e(v)}</a>' for k, v, h in datos)
        return (f'<section class="cierre" id="contacto"><div class="wrap ci-grid"><div><h2 class="rv">{t2(c.get("titulo") or [self.t["contacto"]])}</h2>'
                + (f'<p class="rv">{e(c["texto"])}</p>' if c.get("texto") else "") + f'<div class="rv">{self.btn(c.get("cta") or {"texto": self.t["contacto"]}, "btn blanco")}</div></div>'
                + f'<div class="ci-lado rv d1">{form or lista}</div></div></section>\n')

    def secciones(self):
        return [self.portada(), self.marquesina(), self.statement(), self.proceso(), self.servicios(), self.casos(), self.testimonios(), self.paquetes(), self.faq(), self.cierre()]

    def footer(self, desde=""):
        es = self.lang == "es"; c = self.c
        nav = "".join(f'<a href="{desde}{h}">{e(t)}</a>' for h, t in self.menu())
        redes = []
        if c.get("instagram"): redes.append(f'<a href="https://instagram.com/{ea(c["instagram"].lstrip("@"))}" target="_blank" rel="noopener">Instagram</a>')
        for k, lab in (("linkedin", "LinkedIn"), ("tiktok", "TikTok"), ("youtube", "YouTube")):
            if c.get(k): redes.append(f'<a href="{ea(c[k])}" target="_blank" rel="noopener">{lab}</a>')
        from datetime import date
        return (f'<footer class="pie"><div class="wrap"><div class="pie-top"><a href="{desde or "#top"}" class="marca">{e(self.m.get("nombre"))}</a>'
                f'<div class="col">{nav}</div><div class="col">{"".join(redes)}</div></div>'
                f'<div class="pie-g" data-fit>{e(self.m.get("nombre", "")).upper()}</div>'
                f'<div class="pie-base"><span>© {date.today().year} {e(self.m.get("nombre"))}</span><div class="leg">{self.enlaces_legales(desde)}</div></div></div></footer>\n')
