"""Noche Consultor · plantilla firma de la familia Noche.

Consultoría premium nocturna. Firma: menú en cápsula, titular con degradado, tarjeta grande
de foto/video con brillo, problema en panel de vidrio con checklist, línea de tiempo numerada,
precios en contenedor con cuadrícula, contacto con retrato + testimonio, cierre con resplandor.
"""
from generar_v3 import Gen3, e, ea

FL = '<i class="cir" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2"/></svg></i>'
CHECK = '<svg class="ck" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="9" fill="none" stroke="currentColor" stroke-opacity=".5"/><path d="m6 10.2 2.6 2.6L14 7.4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7Z" fill="currentColor"/></svg>'
ICONOS = ['<path d="M12 3v18M3 12h18" />', '<path d="M4 17 10 11l4 4 6-8" /><path d="M14 7h6v6" />', '<path d="M12 2c3 3 4 7 3 11l-3 3-3-3c-1-4 0-8 3-11Z" /><path d="M9 16l-3 4M15 16l3 4" />']
ESTRELLAS = "★★★★★"


def chip(x):
    return f'<span class="chip"><i></i>{e(x)}</span>' if x else ""


def tit(t):
    if isinstance(t, str): t = [x.strip() for x in t.split("|")]
    return " ".join(f'<span>{e(x)}</span>' for x in t if x)


class Plantilla(Gen3):

    def btn(self, b, cls="btn claro"):
        if not b: return ""
        if isinstance(b, str): b = {"texto": b}
        href = b.get("href") or self.cta_href()
        return f'<a href="{ea(href)}" class="{cls}"{self.ext(href)}>{e(b["texto"])}{FL}</a>'

    def nav(self):
        links = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in self.menu()[:5])
        cta = self.d.get("nav_cta") or self.t["contacto"]
        return (f'<nav class="nav" id="nav"><div class="nav-in"><a href="#top" class="marca"><i class="logo"></i>{e(self.m.get("nombre"))}</a>'
                f'<div class="capsula"><a href="#top" class="on">{"Inicio" if self.lang == "es" else "Home"}</a>{links}</div>{self.btn({"texto": cta}, "btn claro pq")}</div></nav>\n')

    def portada(self):
        h = self.d.get("hero", {})
        media = ""
        if h.get("video"):
            u = self.img(h["video"]); po = self.img(h.get("imagen")) or ""
            media = f'<video autoplay loop muted playsinline poster="{po}"><source src="{u}"/></video>'
        elif h.get("imagen"):
            media = self.foto(h["imagen"], h.get("alt", ""), "", 2200).replace(' loading="lazy"', ' fetchpriority="high"') + f'<span class="play">{PLAY}</span>'
        datos = h.get("datos") or []
        prueba = (f'<span class="prueba rv"><b>{ESTRELLAS}</b>{e(datos[0].get("n"))} {e(datos[0].get("t"))}</span>' if datos else (chip(h.get("etiqueta")) if h.get("etiqueta") else ""))
        return (f'<header class="portada" id="top"><div class="brillo"></div><div class="wrap portada-in">{prueba}'
                f'<h1 class="degr rv d1">{tit(h.get("titulo") or [self.m.get("nombre", "")])}</h1>'
                + (f'<p class="lede rv d2">{e(h["texto"])}</p>' if h.get("texto") else "")
                + f'<div class="ctas rv d3">{self.btn(h.get("cta"))}{self.btn(h.get("cta2"), "btn vidrio")}</div>'
                + (f'<div class="media rv">{media}</div>' if media else "") + '</div></header>\n')

    def problema(self):
        s = self.d.get("sobre")
        if not s: return ""
        puntos = s.get("puntos") or []
        lista = "".join(f'<li>{CHECK}{e(x)}</li>' for x in puntos)
        ps = "".join(f'<p>{e(p)}</p>' for p in ([s["bajada"]] if s.get("bajada") else []) + s.get("texto", []))
        return (f'<section class="problema" id="sobre"><div class="wrap"><div class="vidrio pr-card rv">'
                + (f'<div class="pr-foto">{self.foto(s.get("imagen"), s.get("alt", ""), "", 1400)}</div>' if s.get("imagen") else "")
                + f'<div class="pr-txt">{chip(s.get("etiqueta", self.t["menu"]["sobre"]))}<h2>{tit(s.get("titulo", ""))}</h2>{ps}'
                + (f'<ul class="checks">{lista}</ul>' if lista else "") + (self.btn(s.get("cta")) if s.get("cta") else "") + '</div></div></div></section>\n')

    def proceso(self):
        p = self.d.get("proceso")
        if not p: return ""
        st = "".join(f'<li class="rv"><span class="n">{i + 1:02d}</span><div class="vidrio paso"><small>{"Paso" if self.lang == "es" else "Step"} {i + 1:02d}</small><h3>{e(x.get("titulo"))}</h3><p>{e(x.get("texto"))}</p></div></li>'
                     for i, x in enumerate(p.get("items", [])))
        return (f'<section class="proceso" id="proceso"><div class="wrap pc-grid"><div class="fijo">{chip(p.get("etiqueta", self.t["menu"]["proceso"]))}<h2 class="rv">{tit(p.get("titulo", ""))}</h2>'
                + (f'<p class="rv d1">{e(p["bajada"])}</p>' if p.get("bajada") else "") + f'<div class="rv d2">{self.btn({"texto": self.d.get("nav_cta") or self.t["contacto"]})}</div></div>'
                f'<ol class="linea">{st}</ol></div></section>\n')

    def cab(self, s, k):
        return (f'<div class="cab">{chip(s.get("etiqueta", self.t["menu"].get(k, "")))}<h2 class="rv">{tit(s.get("titulo", ""))}</h2>'
                + (f'<p class="rv d1">{e(s["bajada"])}</p>' if s.get("bajada") else "") + "</div>")

    def testimonios(self):
        t = self.d.get("testimonios")
        if not t: return ""
        cards = []
        for i, x in enumerate(t.get("items", [])):
            av = self.img(x.get("foto"), 300)
            avh = f'<img src="{av}" alt="" loading="lazy"/>' if av else e((x.get("nombre") or "·")[:1])
            cards.append(f'<figure class="vidrio tq rv d{i % 3}"><b class="est">{ESTRELLAS}</b><blockquote>{e(x.get("texto"))}</blockquote>'
                         f'<figcaption><span class="av">{avh}</span><span>{e(x.get("nombre"))}' + (f'<small>{e(x["rol"])}</small>' if x.get("rol") else "") + "</span></figcaption></figure>")
        return f'<section class="testimonios" id="testimonios"><div class="wrap">{self.cab(t, "testimonios")}<div class="tqs">{"".join(cards)}</div></div></section>\n'

    def paquetes(self):
        p = self.d.get("paquetes")
        if not p: return ""
        cards = []
        for i, x in enumerate(p.get("items", [])):
            li = "".join(f"<li>{CHECK}{e(y)}</li>" for y in x.get("incluye", []))
            per = f'<small>{e(x["periodo"])}</small>' if x.get("periodo") else ""
            ico = f'<span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">{ICONOS[i % 3]}</svg></span>'
            badge = f'<span class="badge">{"Más elegido" if self.lang == "es" else "Most popular"}</span>' if x.get("destacado") else ""
            cards.append(f'<div class="plan{" top" if x.get("destacado") else ""}">{badge}{ico}<h3>{e(x.get("nombre"))}</h3><div class="precio">{e(x.get("precio"))}{per}</div>'
                         f'<p>{e(x.get("texto", ""))}</p>{self.btn(x.get("cta") or {"texto": self.d.get("nav_cta") or self.t["contacto"]}, "btn claro ancho")}<ul>{li}</ul></div>')
        return (f'<section class="paquetes" id="paquetes"><div class="wrap"><div class="caja rv">{self.cab(p, "paquetes")}'
                f'<div class="pqs" style="--n:{len(cards)}">{"".join(cards)}</div></div></div></section>\n')

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        f = self.d.get("faq")
        t = (f.get("titulo") if isinstance(f, dict) else None) or self.t["faq_t"]
        det = "".join(f'<details class="vidrio"{" open" if i == 0 else ""}><summary>{e(x.get("p"))}<span aria-hidden="true"></span></summary><p>{e(x.get("r"))}</p></details>' for i, x in enumerate(items))
        return (f'<section class="faq" id="faq"><div class="wrap"><div class="cab">{chip(self.t["menu"]["faq"])}<h2 class="rv">{tit(t)}</h2><p class="rv d1">{self.t["faq_p"]}</p></div>'
                f'<div class="acc rv">{det}</div></div></section>\n')

    def contacto(self):
        form = self.formulario(); datos = self.contacto_items()
        if not form and not datos: return ""
        co = self.d.get("contacto_seccion", {})
        t = co.get("titulo") or (["¿Listo?", "Hablemos."] if self.lang == "es" else ["Ready?", "Let's connect."])
        lado = form or ("".join(f'<a class="dato" href="{ea(h)}"{self.ext(h)}><small>{e(k)}</small><b>{e(v)}</b>{FL}</a>' for k, v, h in datos))
        q = ((self.d.get("testimonios") or {}).get("items") or [{}])[0]
        foto = co.get("imagen")
        retrato = ""
        if foto:
            avs = "".join(f'<img src="{self.img(x["foto"], 200)}" alt="" loading="lazy"/>' for x in (self.d.get("testimonios") or {}).get("items", []) if x.get("foto"))
            retrato = (f'<div class="retrato rv d1">{self.foto(foto, co.get("alt", ""), "", 1400)}'
                       + (f'<div class="vidrio sobre-foto"><p>“{e(q["texto"])}”</p><div class="fila"><span class="avs">{avs}</span><span><b class="est">{ESTRELLAS}</b>{e(q.get("nombre", ""))}</span></div></div>' if q.get("texto") else "")
                       + "</div>")
        return (f'<section class="contacto" id="contacto"><div class="wrap ct-grid"><div>{chip(co.get("etiqueta", self.t["contacto"]))}<h2 class="rv">{tit(t)}</h2>'
                + (f'<p class="rv d1">{e(co["bajada"])}</p>' if co.get("bajada") else "") + f'<div class="vidrio ct-caja rv d2">{lado}</div></div>{retrato}</div></section>\n')

    def blog(self):
        g = self.d.get("galeria"); fotos = self.fotos_galeria()
        if not fotos: return ""
        cards = "".join(f'<article class="vidrio post rv d{i % 2}"><div class="po-foto">{self.foto(f.get("src"), f.get("alt", ""), "", 1400)}</div>'
                        f'<h3>{e(f.get("titulo", ""))}</h3>' + (f'<p>{e(f["texto"])}</p>' if f.get("texto") else "")
                        + (self.btn({"texto": f.get("cta", "Leer más" if self.lang == "es" else "Read more"), "href": f.get("href", "#contacto")}, "btn claro pq") ) + "</article>"
                        for i, f in enumerate(fotos[:4]))
        return f'<section class="blog" id="galeria"><div class="wrap">{self.cab(g if isinstance(g, dict) else {}, "")}<div class="posts">{cards}</div></div></section>\n'

    def cierre(self):
        c = self.d.get("cierre")
        if not c: return ""
        chips = "".join(f'<span class="mini"><i></i>{e(x)}</span>' for x in c.get("puntos", []))
        return (f'<section class="cierre"><div class="wrap"><div class="resplandor rv"><h2>{tit(c.get("titulo", ""))}</h2>'
                + (f'<p>{e(c["texto"])}</p>' if c.get("texto") else "") + (f'<div class="minis">{chips}</div>' if chips else "")
                + f'{self.btn(c.get("cta") or {"texto": self.t["contacto"]})}</div></div></section>\n')

    def secciones(self):
        return [self.portada(), self.problema(), self.proceso(), self.testimonios(), self.paquetes(), self.faq(), self.contacto(), self.blog(), self.cierre()]

    def footer(self, desde=""):
        es = self.lang == "es"; c = self.c
        nav = "".join(f'<a href="{desde}{h}">{e(t)}</a>' for h, t in self.menu())
        redes = []
        if c.get("instagram"): redes.append(f'<a href="https://instagram.com/{ea(c["instagram"].lstrip("@"))}" target="_blank" rel="noopener">Instagram</a>')
        for k, lab in (("linkedin", "LinkedIn"), ("youtube", "YouTube"), ("tiktok", "TikTok")):
            if c.get(k): redes.append(f'<a href="{ea(c[k])}" target="_blank" rel="noopener">{lab}</a>')
        if c.get("email"): redes.append(f'<a href="mailto:{ea(c["email"])}">{e(c["email"])}</a>')
        lema = self.d.get("marca", {}).get("lema", "")
        from datetime import date
        return (f'<footer class="pie"><div class="wrap"><div class="pie-top"><div><a href="{desde or "#top"}" class="marca"><i class="logo"></i>{e(self.m.get("nombre"))}</a>'
                + (f'<p>{e(lema)}</p>' if lema else "") + f'</div><div class="col"><h4>{"Páginas" if es else "Pages"}</h4>{nav}</div><div class="col der"><h4>{"Redes" if es else "Social"}</h4>{"".join(redes)}</div></div>'
                f'<div class="pie-base"><span>© {date.today().year} {e(self.m.get("nombre"))}</span><div class="leg">{self.enlaces_legales(desde)}</div></div></div></footer>\n')
