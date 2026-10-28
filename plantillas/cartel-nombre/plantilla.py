"""Cartel Nombre · plantilla firma de la familia Cartel.

Portafolio de marca personal. Firma: retrato en blanco y negro con el nombre gigante
amarillo de borde a borde, trabajos en cuadrícula, "la mente detrás" con cifras,
servicios en mayúsculas amarillas sobre textura oscura y un "escríbeme" gigante.
"""
from generar_v3 import Gen3, e, ea

GRID = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 2h4v4H2zM10 2h4v4h-4zM2 10h4v4H2zM10 10h4v4h-4z" fill="currentColor"/></svg>'


def linea(t):
    if isinstance(t, str): t = [x.strip() for x in t.split("|")]
    return "<br>".join(e(x) for x in t if x)


class Plantilla(Gen3):

    def eti(self, x):
        return f'<span class="eti">{e(x)}</span>' if x else ""

    def nav(self):
        links = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in self.menu()[:5])
        return (f'<nav class="nav" id="nav"><div class="pastilla"><a href="#top" class="marca">{e(self.m.get("nombre", "")).upper()}</a>'
                f'<button type="button" class="menu-b" aria-label="Menú" aria-expanded="false">{GRID}</button>'
                f'<div class="menu">{links}<a href="#contacto">{e(self.d.get("nav_cta") or self.t["contacto"])}</a></div></div></nav>\n')

    def portada(self):
        h = self.d.get("hero", {})
        foco = f' style="object-position:50% {int(h["foco"])}%"' if h.get("foco") is not None else ""
        img = self.foto(h.get("imagen"), h.get("alt", ""), "ph", 2400).replace("<img ", f"<img{foco} ", 1).replace(' loading="lazy"', ' fetchpriority="high"')
        nombre = h.get("nombre_grande") or self.m.get("nombre", "")
        tit = h.get("titulo") or []
        if isinstance(tit, str): tit = [tit]
        return (f'<header class="portada" id="top">{img}<div class="velo"></div><div class="portada-in">'
                + (f'<p class="rol rv">' + (f'<span class="am">{e(tit[0])}</span>' if tit else "") + (f'<span>{e(tit[1])}</span>' if len(tit) > 1 else "") + "</p>" if tit else "")
                + f'<h1 class="gigante" data-fit>{e(nombre).upper()}</h1></div></header>\n')

    def trabajos(self):
        g = self.d.get("galeria"); fotos = self.fotos_galeria()
        if not fotos: return ""
        gd = g if isinstance(g, dict) else {}
        cards = "".join(f'<article class="obra rv d{i % 2}"><a href="{ea(f.get("href", "#contacto"))}"{self.ext(f.get("href", ""))}><div class="ob-foto">{self.foto(f.get("src"), f.get("alt", f.get("titulo", "")), "", 1400)}</div>'
                        f'<h3>{e(f.get("titulo", "")).upper()}</h3>' + (f'<p>{e(f["texto"])}</p>' if f.get("texto") else "") + "</a></article>" for i, f in enumerate(fotos))
        ver = f'<a class="ver" href="{ea(gd["ver_todo"]["href"])}"{self.ext(gd["ver_todo"]["href"])}>{e(gd["ver_todo"]["texto"]).upper()} →</a>' if gd.get("ver_todo") else ""
        return (f'<section class="trabajos" id="galeria"><div class="wrap"><div class="cab"><div>{self.eti(gd.get("etiqueta", "Proyectos"))}<h2>{linea(gd.get("titulo") or ["Trabajos"])}</h2></div>{ver}</div>'
                f'<div class="obras">{cards}</div></div></section>\n')

    def mente(self):
        s = self.d.get("sobre")
        if not s: return ""
        ps = "".join(f"<p>{e(p)}</p>" for p in s.get("texto", []))
        nums = "".join(f'<div><b>{e(n.get("n"))}</b><small>{e(n.get("t"))}</small></div>' for n in s.get("cifras", []))
        cta = f'<a class="ver" href="{ea(self.cta_href())}"{self.ext(self.cta_href())}>{e(s.get("cta", {}).get("texto", self.t["contacto"])).upper()} →</a>'
        return (f'<section class="mente" id="sobre"><div class="wrap me-grid"><div class="me-txt rv">{self.eti(s.get("etiqueta", self.t["menu"]["sobre"]))}<h2>{linea(s.get("titulo", ""))}</h2>{ps}{cta}</div>'
                f'<div class="rv d1"><div class="me-foto">{self.foto(s.get("imagen"), s.get("alt", ""), "", 1400)}</div>' + (f'<div class="nums">{nums}</div>' if nums else "") + "</div></div></section>\n")

    def servicios(self):
        s = self.d.get("servicios")
        if not s: return ""
        fondo = self.foto(s["imagen"], "", "fondo", 2000) if s.get("imagen") else ""
        lis = "".join(f'<li class="rv">{e(it.get("titulo", "")).upper()}</li>' for it in s.get("items", []))
        return (f'<section class="servicios" id="servicios">{fondo}<div class="velo"></div><div class="wrap">{self.eti(s.get("etiqueta", self.t["menu"]["servicios"]))}'
                f'<ul>{lis}</ul>' + (f'<p class="rv">{e(s["bajada"])}</p>' if s.get("bajada") else "") + "</div></section>\n")

    def testimonios(self):
        t = self.d.get("testimonios")
        if not t: return ""
        q = "".join(f'<figure class="cita rv"><blockquote>{e(x.get("texto"))}</blockquote><figcaption>{e(x.get("nombre", "")).upper()}' + (f'<span>{e(x["rol"])}</span>' if x.get("rol") else "") + "</figcaption></figure>" for x in t.get("items", []))
        return f'<section class="testimonios" id="testimonios"><div class="wrap">{self.eti(t.get("etiqueta", self.t["menu"]["testimonios"]))}<div class="citas">{q}</div></div></section>\n'

    def proceso(self):
        p = self.d.get("proceso")
        if not p: return ""
        st = "".join(f'<li class="rv"><span>{i + 1:02d}</span><h3>{e(x.get("titulo", "")).upper()}</h3><p>{e(x.get("texto"))}</p></li>' for i, x in enumerate(p.get("items", [])))
        return f'<section class="proceso" id="proceso"><div class="wrap"><div class="cab"><div>{self.eti(p.get("etiqueta", self.t["menu"]["proceso"]))}<h2>{linea(p.get("titulo", ""))}</h2></div></div><ol>{st}</ol></div></section>\n'

    def paquetes(self):
        p = self.d.get("paquetes")
        if not p: return ""
        cards = "".join(f'<div class="paq{" top" if x.get("destacado") else ""} rv"><h3>{e(x.get("nombre", "")).upper()}</h3><b>{e(x.get("precio"))}' + (f'<small>{e(x["periodo"])}</small>' if x.get("periodo") else "") + f'</b><p>{e(x.get("texto", ""))}</p><ul>' + "".join(f"<li>{e(y)}</li>" for y in x.get("incluye", [])) + f'</ul>{self.boton(x.get("cta") or {"texto": self.t["contacto"]}, "btn", False)}</div>' for x in p.get("items", []))
        return f'<section class="paquetes" id="paquetes"><div class="wrap"><div class="cab"><div>{self.eti(p.get("etiqueta", self.t["menu"]["paquetes"]))}<h2>{linea(p.get("titulo", ""))}</h2></div></div><div class="paqs">{cards}</div></div></section>\n'

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        det = "".join(f'<details><summary>{e(x.get("p"))}<span aria-hidden="true">+</span></summary><p>{e(x.get("r"))}</p></details>' for x in items)
        return f'<section class="faq" id="faq"><div class="wrap me-grid"><div>{self.eti(self.t["menu"]["faq"])}<h2>{linea(self.t["faq_t"])}</h2></div><div class="acc">{det}</div></div></section>\n'

    def cierre(self):
        c = self.d.get("cierre") or {}
        form = self.formulario(); datos = self.contacto_items()
        grande = c.get("grande") or ("ESCRÍBEME" if self.lang == "es" else "GET IN TOUCH")
        tit = c.get("titulo")
        return (f'<section class="cierre" id="contacto"><div class="wrap">'
                + (f'<p class="ci-txt rv">{linea(tit)}</p>' if tit else "")
                + (f'<div class="ci-datos rv">' + "".join(f'<a href="{ea(h)}"{self.ext(h)}><small>{e(k).upper()}</small>{e(v)}</a>' for k, v, h in datos) + "</div>" if datos else "")
                + (f'<div class="ci-form rv">{form}</div>' if form else "")
                + f'</div><a class="gigante cierre-g" href="{ea(self.cta_href())}"{self.ext(self.cta_href())} data-fit>{e(grande)}</a></section>\n')

    def secciones(self):
        return [self.portada(), self.trabajos(), self.mente(), self.servicios(), self.proceso(), self.testimonios(), self.paquetes(), self.faq(), self.cierre()]

    def footer(self, desde=""):
        c = self.c; redes = []
        if c.get("instagram"): redes.append(f'<a href="https://instagram.com/{ea(c["instagram"].lstrip("@"))}" target="_blank" rel="noopener">INSTAGRAM</a>')
        for k, lab in (("tiktok", "TIKTOK"), ("youtube", "YOUTUBE"), ("linkedin", "LINKEDIN")):
            if c.get(k): redes.append(f'<a href="{ea(c[k])}" target="_blank" rel="noopener">{lab}</a>')
        from datetime import date
        return (f'<footer class="pie"><div class="pie-in"><div class="redes">{"".join(redes)}</div><div class="leg">{self.enlaces_legales(desde)}</div>'
                f'<span>{e(self.m.get("nombre", "")).upper()} {date.today().year}©</span></div></footer>\n')
