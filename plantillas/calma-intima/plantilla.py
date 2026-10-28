"""Calma Íntima · plantilla firma de la familia Calma.

Consulta íntima y editorial. Firma: titular abajo a la izquierda sobre foto cálida,
etiquetas "(entre paréntesis)" en itálica, collage asimétrico, servicios con foto fija,
numeral gigante que cambia con el scroll, banda oscura (un testimonio a la vez + formulario
de líneas) y el nombre gigante en itálica en el pie.
"""
from generar_v3 import Gen3, e, ea

AST = '<svg class="ast" viewBox="0 0 32 32" aria-hidden="true"><path d="M14 0h4l-.6 12.2L27.9 5.6l2 3.5L19 14.6v2.8l10.9 5.5-2 3.5-10.5-6.6L18 32h-4l.6-12.2L4.1 26.4l-2-3.5L13 17.4v-2.8L2.1 9.1l2-3.5 10.5 6.6Z" fill="currentColor"/></svg>'
FLECHA_I = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5 8 12l7 7" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'
FLECHA_D = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 7 7-7 7" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'


def par(x):
    return f'<span class="par">({e(x)})</span> ' if x else ""


def t2(t):
    if isinstance(t, str): t = [x.strip() for x in t.split("|")]
    return " ".join(e(x) for x in t if x)


class Plantilla(Gen3):

    def nav(self):
        links = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in self.menu()[:5])
        cta = self.d.get("nav_cta") or self.t["contacto"]
        return (f'<nav class="nav" id="nav"><div class="nav-in"><a href="#top" class="marca">{e(self.m.get("nombre"))}</a>'
                f'<div class="links">{links}</div><a href="{ea(self.cta_href())}" class="btn crema pq"{self.ext(self.cta_href())}><i class="pto"></i>{e(cta)}</a></div></nav>\n')

    def portada(self):
        h = self.d.get("hero", {})
        foco = f' style="object-position:50% {int(h["foco"])}%"' if h.get("foco") is not None else ""
        img = self.foto(h.get("imagen"), h.get("alt", ""), "ph", 2400).replace("<img ", f"<img{foco} ", 1).replace(' loading="lazy"', ' fetchpriority="high"')
        lede = f'<p class="lede rv d2">{e(h["texto"])}</p>' if h.get("texto") else ""
        ctas = self.boton(h.get("cta"), "btn crema", False) + self.boton(h.get("cta2"), "btn vidrio", False)
        return (f'<header class="portada" id="top">{img}<div class="velo"></div><div class="wrap portada-in">'
                f'<h1 class="rv d1">{t2(h.get("titulo") or [self.m.get("nombre", "")])}</h1><div class="portada-pie">{lede}<div class="ctas rv d3">{ctas}</div></div></div></header>\n')

    def intro(self):
        s = self.d.get("sobre")
        if not s: return ""
        chica = self.foto(s.get("imagen_chica"), s.get("alt_chica", ""), "", 1000) if s.get("imagen_chica") else ""
        grande = self.foto(s.get("imagen"), s.get("alt", ""), "", 2000) if s.get("imagen") else ""
        ps = "".join(f"<p>{e(p)}</p>" for p in s.get("texto", []))
        boton = self.boton(s.get("cta"), "btn linea pq", False) if s.get("cta") else ""
        return (f'<section class="intro" id="sobre"><div class="wrap"><p class="intro-txt rv">{par(s.get("etiqueta", self.t["menu"]["sobre"]))}{e(s.get("bajada", ""))}</p>'
                f'<div class="collage">' + (f'<figure class="c-chica rv">{chica}</figure>' if chica else "") + (f'<figure class="c-grande rv d1">{grande}</figure>' if grande else "")
                + f'<div class="c-txt rv d2">{ps}{boton}</div></div></div></section>\n')

    def servicios(self):
        s = self.d.get("servicios")
        if not s: return ""
        its = "".join(f'<article class="srv"><h3 class="rv">{e(it.get("titulo"))}</h3><p class="rv d1">{e(it.get("texto"))}</p>'
                      + (f'<span class="pr rv d2">{e(it["precio"])}</span>' if it.get("precio") else "") + "</article>" for it in s.get("items", []))
        img = self.foto(s.get("imagen"), s.get("alt", ""), "", 1600)
        return (f'<section class="servicios" id="servicios"><div class="srv-col"><div class="srv-cab"><h2 class="sub rv">{par(s.get("etiqueta", self.t["menu"]["servicios"]))}{t2(s.get("titulo", ""))}</h2></div>{its}</div>'
                f'<div class="srv-foto"><div class="fijo">{img}</div></div></section>\n')

    def proceso(self):
        p = self.d.get("proceso")
        if not p: return ""
        st = "".join(f'<li class="paso" data-n="{i + 1:02d}">{AST}<h3>{e(x.get("titulo"))}</h3><p>{e(x.get("texto"))}</p></li>' for i, x in enumerate(p.get("items", [])))
        return (f'<section class="proceso" id="proceso"><div class="wrap"><h2 class="sub centro rv">{par(p.get("etiqueta", self.t["menu"]["proceso"]))}{t2(p.get("titulo", ""))}</h2>'
                f'<div class="pr-grid"><div class="pr-num"><span id="numero">01</span></div><ol class="pasos">{st}</ol></div></div></section>\n')

    def pausa(self):
        p = self.d.get("pausa")
        if not p or not p.get("imagen"): return ""
        return (f'<section class="pausa">{self.foto(p["imagen"], p.get("alt", ""), "", 2400)}<div class="velo"></div>'
                + (f'<p class="rv">{e(p["texto"])}</p>' if p.get("texto") else "") + "</section>\n")

    def oscura(self):
        t = self.d.get("testimonios"); its = (t or {}).get("items", [])
        form = self.formulario(); datos = self.contacto_items()
        co = self.d.get("contacto_seccion", {})
        out = '<div class="oscura">'
        if its:
            q = "".join(f'<figure class="tq{" on" if i == 0 else ""}"><blockquote>{e(x.get("texto"))}</blockquote><figcaption><i class="pto"></i>{e(x.get("nombre"))}'
                        + (f'<small>{e(x["rol"])}</small>' if x.get("rol") else "") + "</figcaption></figure>" for i, x in enumerate(its))
            nav = (f'<div class="tq-nav"><button type="button" data-tq="-1" aria-label="Anterior">{FLECHA_I}</button><button type="button" data-tq="1" aria-label="Siguiente">{FLECHA_D}</button></div>' if len(its) > 1 else "")
            out += (f'<section class="testimonios" id="testimonios"><div class="wrap"><h2 class="sub centro rv">{par(t.get("etiqueta", self.t["menu"]["testimonios"]))}{t2(t.get("titulo", ""))}</h2>'
                    f'<div class="tq-zona rv">{q}{nav}</div></div></section>')
        if form or datos:
            tit = co.get("titulo") or (["Escribir ya es", "un primer paso."] if self.lang == "es" else ["Reaching out is", "a first step."])
            puntos = "".join(f'<li>{AST}{e(x)}</li>' for x in co.get("puntos", []))
            lista = "".join(f'<a href="{ea(h)}"{self.ext(h)}><small>{e(k)}</small>{e(v)}</a>' for k, v, h in datos)
            out += (f'<section class="contacto" id="contacto"><div class="wrap ct-grid"><div><h2 class="sub rv">{par(co.get("etiqueta", self.t["contacto"]))}{t2(tit)}</h2>'
                    + (f'<ul class="puntos rv d1">{puntos}</ul>' if puntos else "") + (f'<p class="ct-baj rv d2">{e(co["bajada"])}</p>' if co.get("bajada") else "")
                    + f'<div class="ct-datos rv d2">{lista}</div></div><div class="ct-form rv d1">{form}</div></div></section>')
        return out + "</div>\n"

    def galeria(self):
        g = self.d.get("galeria"); fotos = self.fotos_galeria()
        if not fotos: return ""
        cards = "".join(f'<article class="nota rv d{i % 3}"><div class="n-foto">{self.foto(f.get("src"), f.get("alt", ""), "", 1100)}</div>'
                        + (f'<small><i class="pto"></i>{e(f["etiqueta"])}</small>' if f.get("etiqueta") else "")
                        + (f'<h3>{e(f["titulo"])}</h3>' if f.get("titulo") else "") + (f'<p>{e(f["texto"])}</p>' if f.get("texto") else "") + "</article>"
                        for i, f in enumerate(fotos[:3]))
        tit = (g.get("titulo") if isinstance(g, dict) else None) or self.t["galeria"]
        return (f'<section class="galeria" id="galeria"><div class="wrap"><h2 class="sub rv">{par(g.get("etiqueta") if isinstance(g, dict) else "")}{t2(tit)}</h2>'
                f'<div class="notas">{cards}</div></div></section>\n')

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        f = self.d.get("faq")
        tit = (f.get("titulo") if isinstance(f, dict) else None) or self.t["faq_t"]
        det = "".join(f'<details{" open" if i == 0 else ""}><summary><span class="q">{e(x.get("p"))}</span><span class="mas" aria-hidden="true"></span></summary><p>{e(x.get("r"))}</p></details>' for i, x in enumerate(items))
        return (f'<section class="faq" id="faq"><div class="wrap"><h2 class="sub centro rv">{par(self.t["menu"]["faq"])}{t2(tit)}</h2><div class="acc rv d1">{det}</div></div></section>\n')

    def cierre(self):
        c = self.d.get("cierre")
        if not c: return ""
        return (f'<section class="cierre"><div class="wrap"><h2 class="rv">{t2(c.get("titulo", ""))}</h2>'
                + (f'<p class="rv d1">{e(c["texto"])}</p>' if c.get("texto") else "")
                + f'<div class="rv d2">{self.boton(c.get("cta") or {"texto": self.t["contacto"]}, "btn negro", False)}</div></div></section>\n')

    def secciones(self):
        return [self.portada(), self.intro(), self.servicios(), self.proceso(), self.pausa(), self.oscura(), self.galeria(), self.faq(), self.cierre()]

    def footer(self, desde=""):
        es = self.lang == "es"
        nav = "".join(f'<a href="{desde}{h}">{e(t)}</a>' for h, t in self.menu())
        srv = "".join(f'<a href="{desde}#servicios">{e(x.get("titulo"))}</a>' for x in (self.d.get("servicios") or {}).get("items", [])[:5])
        datos = "".join(f'<a href="{ea(h)}"{self.ext(h)}>{e(v)}</a>' for k, v, h in self.contacto_items())
        from datetime import date
        return (f'<footer class="pie"><div class="wrap"><div class="pie-cols">'
                f'<div><h4>{"Navega" if es else "Navigate"}</h4>{nav}</div>'
                + (f'<div><h4>{"Servicios" if es else "Services"}</h4>{srv}</div>' if srv else "")
                + f'<div><h4>{self.t["contacto"]}</h4>{datos}</div></div>'
                f'<a href="{desde or "#top"}" class="gigante" data-fit>{e(self.m.get("nombre"))}</a>'
                f'<div class="pie-base"><span>© {date.today().year} {e(self.m.get("nombre"))}</span><div class="leg">{self.enlaces_legales(desde)}</div></div></div></footer>\n')
