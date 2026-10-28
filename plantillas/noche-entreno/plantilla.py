"""Noche Entreno · plantilla firma de la familia Noche.

Gimnasio premium de noche. Firma: titular centrado en dos tonos sobre foto oscura, fotos
flotando alrededor de un título, servicios en fila con flecha, pasos en tarjetas con título
fijo, mosaico de cifras y fotos, resultados en filas alternadas y cierre con tarjeta de contacto.
"""
from generar_v3 import Gen3, e, ea

FLECHA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'


def t2(t):
    """dos tonos: primera línea gris, segunda blanca"""
    if isinstance(t, str): t = [x.strip() for x in t.split("|")]
    a = e(t[0]) if t else ""
    b = e(t[1]) if len(t) > 1 and t[1] else ""
    return f'<span class="g">{a}</span>' + (f'<span class="w">{b}</span>' if b else "")


class Plantilla(Gen3):

    def chip(self, x, cls=""):
        return f'<span class="chip {cls}"><i></i>{e(x)}</span>' if x else ""

    def nav(self):
        links = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in self.menu()[:5])
        cta = self.d.get("nav_cta") or self.t["contacto"]
        return (f'<nav class="nav" id="nav"><div class="nav-in"><a href="#top" class="marca">{e(self.m.get("nombre"))}</a>'
                f'<div class="links">{links}</div>{self.boton({"texto": cta}, "btn blanco pq", False)}</div></nav>\n')

    def portada(self):
        h = self.d.get("hero", {})
        foco = f' style="object-position:50% {int(h["foco"])}%"' if h.get("foco") is not None else ""
        img = self.foto(h.get("imagen"), h.get("alt", ""), "ph", 2400).replace("<img ", f"<img{foco} ", 1).replace(' loading="lazy"', ' fetchpriority="high"')
        ctas = self.boton(h.get("cta"), "btn blanco", False) + self.boton(h.get("cta2"), "btn oscuro", False)
        return (f'<header class="portada" id="top">{img}<div class="velo"></div><div class="wrap portada-in">{self.chip(h.get("etiqueta"), "rv")}'
                f'<h1 class="tt rv d1">{t2(h.get("titulo") or [self.m.get("nombre", "")])}</h1>'
                + (f'<p class="lede rv d2">{e(h["texto"])}</p>' if h.get("texto") else "")
                + f'<div class="ctas rv d3">{ctas}</div></div></header>\n')

    def flotantes(self):
        g = self.d.get("galeria"); fotos = self.fotos_galeria()
        if not fotos: return ""
        def card(f, cls):
            return (f'<figure class="flo {cls} rv"><div class="flo-foto">{self.foto(f.get("src"), f.get("alt", f.get("titulo", "")), "", 900)}</div>'
                    + (f'<figcaption><b>{e(f["titulo"])}</b>' + (f'<span>{e(f["texto"])}</span>' if f.get("texto") else "") + "</figcaption>" if f.get("titulo") else "") + "</figure>")
        f4 = (fotos + [{}] * 4)[:4]
        izq = card(f4[0], "a") + (card(f4[1], "b") if f4[1] else "")
        der = (card(f4[2], "c") if f4[2] else "") + (card(f4[3], "d") if f4[3] else "")
        tit = (g.get("titulo") if isinstance(g, dict) else None) or self.t["galeria"]
        return (f'<section class="flotantes" id="galeria"><div class="wrap fl-grid"><div class="fl-col">{izq}</div>'
                f'<div class="fl-centro">{self.chip(g.get("etiqueta") if isinstance(g, dict) else "", "rv")}<h2 class="tt rv d1">{t2(tit)}</h2>'
                + (f'<p class="rv d2">{e(g["bajada"])}</p>' if isinstance(g, dict) and g.get("bajada") else "")
                + f'</div><div class="fl-col der">{der}</div></div></section>\n')

    def cab(self, s, k, centro=False):
        return (f'<div class="cab{" centro" if centro else ""}"><div>{self.chip(s.get("etiqueta", self.t["menu"].get(k, "")), "rv")}<h2 class="tt rv d1">{t2(s.get("titulo", ""))}</h2></div>'
                + (f'<p class="rv d2">{e(s["bajada"])}</p>' if s.get("bajada") else "<span></span>") + "</div>")

    def servicios(self):
        s = self.d.get("servicios")
        if not s: return ""
        cards = "".join(f'<a class="srv rv d{i % 3}" href="{ea(it.get("href") or self.cta_href())}"{self.ext(it.get("href") or self.cta_href())}>'
                        f'<div class="srv-foto">{self.foto(it.get("imagen"), it.get("titulo", ""), "", 1000)}</div>'
                        f'<div class="srv-pie"><span><b>{e(it.get("titulo"))}</b>' + (f'<small>{e(it["precio"])}</small>' if it.get("precio") else "") + f'</span><i class="fl">{FLECHA}</i></div>'
                        + (f'<p>{e(it["texto"])}</p>' if it.get("texto") else "") + "</a>" for i, it in enumerate(s.get("items", [])))
        return f'<section class="servicios" id="servicios"><div class="wrap">{self.cab(s, "servicios")}<div class="srvs" style="--n:{min(4, len(s.get("items", [])) or 1)}">{cards}</div></div></section>\n'

    def proceso(self):
        p = self.d.get("proceso")
        if not p: return ""
        st = "".join(f'<li class="paso rv"><span class="n">{i + 1}</span><h3>{e(x.get("titulo"))}</h3><p>{e(x.get("texto"))}</p></li>' for i, x in enumerate(p.get("items", [])))
        return (f'<section class="proceso" id="proceso"><div class="wrap pr-grid"><div class="fijo">{self.chip(p.get("etiqueta", self.t["menu"]["proceso"]), "rv")}'
                f'<h2 class="tt rv d1">{t2(p.get("titulo", ""))}</h2>' + (f'<p class="rv d2">{e(p["bajada"])}</p>' if p.get("bajada") else "")
                + f'</div><ol class="pasos">{st}</ol></div></section>\n')

    def mosaico(self):
        s = self.d.get("sobre")
        if not s: return ""
        imgs = s.get("imagenes") or ([s["imagen"]] if s.get("imagen") else [])
        cif = s.get("cifras", [])
        def stat(c): return f'<div class="bt stat rv"><b>{e(c.get("n"))}</b><small>{e(c.get("t"))}</small></div>'
        def foto(i): return f'<div class="bt img rv">{self.foto(i, s.get("alt", ""), "", 1200)}</div>'
        celdas = []
        orden = [("img", 0), ("stat", 0), ("stat", 1), ("img", 1), ("stat", 2), ("stat", 3)]
        for tipo, k in orden:
            if tipo == "img" and k < len(imgs): celdas.append(foto(imgs[k]))
            if tipo == "stat" and k < len(cif): celdas.append(stat(cif[k]))
        ps = "".join(f"<p>{e(p)}</p>" for p in s.get("texto", []))
        return (f'<section class="mosaico" id="sobre"><div class="wrap mo-grid"><div>{self.chip(s.get("etiqueta", self.t["menu"]["sobre"]), "rv")}'
                f'<h2 class="tt rv d1">{t2(s.get("titulo", ""))}</h2>' + (f'<div class="rv d2">{self.boton(s["cta"], "btn oscuro", False)}</div>' if s.get("cta") else "")
                + f'</div><div><div class="mo-txt rv">{ps}</div><div class="bento">{"".join(celdas)}</div></div></div></section>\n')

    def resultados(self):
        t = self.d.get("testimonios")
        if not t: return ""
        filas = []
        for i, x in enumerate(t.get("items", [])):
            dat = "".join(f'<div><b>{e(c.get("n"))}</b><small>{e(c.get("t"))}</small></div>' for c in x.get("datos", []))
            fotos = x.get("fotos") or ([x["foto"]] if x.get("foto") else [])
            fh = "".join(f'<div class="rs-foto">{self.foto(f, x.get("nombre", ""), "", 1100)}</div>' for f in fotos[:2])
            filas.append(f'<article class="rs{" inv" if i % 2 else ""} rv"><div class="rs-txt"><blockquote>{e(x.get("texto"))}</blockquote>'
                         f'<p class="quien">{e(x.get("nombre"))}' + (f'<small>{e(x["rol"])}</small>' if x.get("rol") else "") + "</p>"
                         + (f'<div class="rs-dat">{dat}</div>' if dat else "") + f'</div><div class="rs-fotos" style="--n:{max(1, len(fotos[:2]))}">{fh}</div></article>')
        return f'<section class="resultados" id="testimonios"><div class="wrap">{self.cab(t, "testimonios")}<div class="rss">{"".join(filas)}</div></div></section>\n'

    def paquetes(self):
        p = self.d.get("paquetes")
        if not p: return ""
        cards = []
        for i, x in enumerate(p.get("items", [])):
            li = "".join(f"<li>{e(y)}</li>" for y in x.get("incluye", []))
            per = f'<small>{e(x["periodo"])}</small>' if x.get("periodo") else ""
            cards.append(f'<div class="pq{" top" if x.get("destacado") else ""} rv d{i % 3}"><h3>{e(x.get("nombre"))}</h3><p>{e(x.get("texto", ""))}</p>'
                         f'<div class="precio">{e(x.get("precio"))}{per}</div><ul>{li}</ul>{self.boton(x.get("cta") or {"texto": self.t["contacto"]}, "btn " + ("negro" if x.get("destacado") else "blanco"), False)}</div>')
        return f'<section class="paquetes" id="paquetes"><div class="wrap">{self.cab(p, "paquetes")}<div class="pqs" style="--n:{len(cards)}">{"".join(cards)}</div></div></section>\n'

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        f = self.d.get("faq")
        tit = (f.get("titulo") if isinstance(f, dict) else None) or self.t["faq_t"]
        det = "".join(f'<details><summary>{e(x.get("p"))}<span aria-hidden="true">+</span></summary><p>{e(x.get("r"))}</p></details>' for x in items)
        return (f'<section class="faq" id="faq"><div class="wrap faq-grid"><div><h2 class="tt rv">{t2(tit)}</h2><p class="rv d1">{self.t["faq_p"]}</p></div>'
                f'<div class="acc rv d1">{det}</div></div></section>\n')

    def cierre(self):
        c = self.d.get("cierre") or {}
        form = self.formulario(); datos = self.contacto_items()
        if not c and not form and not datos: return ""
        lado = ""
        if form: lado = f'<div class="ct-card rv d1"><h3>{self.t["contacto"]}</h3>{form}</div>'
        elif datos: lado = (f'<div class="ct-card rv d1"><h3>{self.t["contacto"]}</h3>'
                            + "".join(f'<a href="{ea(h)}"{self.ext(h)}><small>{e(k)}</small><b>{e(v)}</b><i class="fl">{FLECHA}</i></a>' for k, v, h in datos) + "</div>")
        fondo = self.foto(c.get("imagen"), "", "fondo", 2200) if c.get("imagen") else ""
        return (f'<section class="cierre" id="contacto">{fondo}<div class="velo"></div><div class="wrap ci-grid"><div>'
                f'<h2 class="tt rv">{t2(c.get("titulo", ["", ""]))}</h2>' + (f'<p class="rv d1">{e(c["texto"])}</p>' if c.get("texto") else "")
                + (f'<div class="rv d2">{self.boton(c.get("cta"), "btn blanco", False)}</div>' if c.get("cta") else "")
                + f'</div>{lado}</div></section>\n')

    def secciones(self):
        return [self.portada(), self.flotantes(), self.servicios(), self.proceso(), self.mosaico(), self.resultados(), self.paquetes(), self.faq(), self.cierre()]

    def footer(self, desde=""):
        es = self.lang == "es"
        lema = self.d.get("marca", {}).get("lema", "")
        nav = "".join(f'<a href="{desde}{h}">{e(t)}</a>' for h, t in self.menu())
        redes = []
        c = self.c
        if c.get("instagram"): redes.append(f'<a href="https://instagram.com/{ea(c["instagram"].lstrip("@"))}" target="_blank" rel="noopener">Instagram</a>')
        for k, lab in (("tiktok", "TikTok"), ("youtube", "YouTube"), ("linkedin", "LinkedIn")):
            if c.get(k): redes.append(f'<a href="{ea(c[k])}" target="_blank" rel="noopener">{lab}</a>')
        from datetime import date
        return (f'<footer class="pie"><div class="wrap"><div class="pie-top"><div><a href="{desde or "#top"}" class="marca">{e(self.m.get("nombre"))}</a>'
                + (f'<p>{e(lema)}</p>' if lema else "") + f'<div class="redes">{"".join(redes)}</div></div>'
                f'<div class="pie-nav"><h4>{"Páginas" if es else "Pages"}</h4>{nav}</div></div>'
                f'<div class="pie-base"><span>© {date.today().year} {e(self.m.get("nombre"))}</span><div class="leg">{self.enlaces_legales(desde)}</div></div></div></footer>\n')
