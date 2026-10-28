"""Plano Color · plantilla firma de la familia Plano.

Estudio creativo en blanco puro. Firma: titular en mayúsculas con símbolos y partes en gris,
mosaico de 5 fotos de color, frase del estudio con foto del equipo, fila de logos, lista de
servicios separada por cuadritos, barra en cápsula para el cierre, nombre gigante sobre negro.
"""
from generar_v3 import Gen3, e, ea

SIMBOLOS = ["✹", "✦", "●", "■", "✺"]


class Plantilla(Gen3):

    def nav(self):
        links = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in self.menu()[:4])
        return (f'<nav class="nav" id="nav"><div class="nav-in"><div class="izq"><a href="#top" class="marca"><i class="logo"></i>{e(self.m.get("nombre", "")).upper()}®</a>{links}</div>'
                f'<a href="#contacto" class="cta">{e(self.d.get("nav_cta") or self.t["contacto"]).upper()}</a></div></nav>\n')

    def portada(self):
        h = self.d.get("hero", {})
        partes = h.get("frase") or [self.m.get("nombre", "")]
        html = ""
        for i, p in enumerate(partes):
            gris = i % 2 == 1
            html += f'<span class="{"gris" if gris else "osc"}">{e(p).upper()}</span>'
            if i < len(partes) - 1: html += f' <i class="sim">{SIMBOLOS[i % len(SIMBOLOS)]}</i> '
        fotos = h.get("imagenes", [])
        arriba = "".join(f'<div class="mo-f">{self.foto(f, "", "", 1200)}</div>' for f in fotos[:3])
        abajo = "".join(f'<div class="mo-f">{self.foto(f, "", "", 1600)}</div>' for f in fotos[3:5])
        return (f'<header class="portada" id="top"><div class="wrap"><h1 class="frase rv">{html}</h1>'
                f'<div class="mosaico rv d1"><div class="fila3">{arriba}</div>' + (f'<div class="fila2">{abajo}</div>' if abajo else "") + "</div></div></header>\n")

    def estudio(self):
        s = self.d.get("sobre")
        if not s: return ""
        ps = "".join(f"<p>{e(p)}</p>" for p in s.get("texto", []))
        clientes = "".join(f'<span><i>{SIMBOLOS[i % len(SIMBOLOS)]}</i>{e(c)}</span>' for i, c in enumerate(self.d.get("clientes", [])))
        return (f'<section class="estudio" id="sobre"><div class="wrap es-grid"><div class="es-txt rv">{ps}</div>'
                + (f'<div class="es-foto rv d1">{self.foto(s.get("imagen"), s.get("alt", ""), "", 900)}</div>' if s.get("imagen") else "")
                + "</div>" + (f'<div class="wrap"><p class="cl-t">✹ {e(s.get("clientes_titulo", "Marcas que confían en nosotros" if self.lang == "es" else "Startups & global brands")).upper()}</p></div>'
                              f'<div class="logos" aria-label="Clientes"><div class="logos-t">{clientes}{clientes}</div></div>' if clientes else "") + "</section>\n")

    def galeria(self):
        fotos = self.fotos_galeria()
        if not fotos: return ""
        g = "".join(f'<div class="gr-f rv d{i % 2}">{self.foto(f.get("src"), f.get("alt", ""), "", 1800)}</div>' for i, f in enumerate(fotos[:2]))
        return f'<section class="grandes" id="galeria"><div class="wrap"><div class="gr">{g}</div></div></section>\n'

    def servicios(self):
        s = self.d.get("servicios")
        if not s: return ""
        cols = "".join(f'<p class="rv">{e(p)}</p>' for p in s.get("texto", []))
        lista = " ".join(f'<span>■ {e(it.get("titulo", "")).upper()}</span>' for it in s.get("items", []))
        icono = f'<div class="ico rv">{self.foto(s["imagen"], "", "", 300)}</div>' if s.get("imagen") else ""
        return (f'<section class="servicios" id="servicios"><div class="wrap"><div class="cols">{cols}</div>{icono}'
                f'<p class="lista rv">{lista} ■</p></div></section>\n')

    def proceso(self):
        p = self.d.get("proceso")
        if not p: return ""
        st = "".join(f'<li class="rv"><b>{e(SIMBOLOS[i % len(SIMBOLOS)])} {i + 1:02d}</b><h3>{e(x.get("titulo", "")).upper()}</h3><p>{e(x.get("texto"))}</p></li>' for i, x in enumerate(p.get("items", [])))
        return f'<section class="proceso" id="proceso"><div class="wrap"><h2 class="rv">{e(" ".join(p.get("titulo") or [self.t["menu"]["proceso"]])).upper()}</h2><ol>{st}</ol></div></section>\n'

    def testimonios(self):
        t = self.d.get("testimonios")
        if not t: return ""
        q = "".join(f'<figure class="rv"><blockquote>“{e(x.get("texto"))}”</blockquote><figcaption>{e(x.get("nombre", "")).upper()}' + (f' · {e(x["rol"])}' if x.get("rol") else "") + "</figcaption></figure>" for x in t.get("items", []))
        return f'<section class="testimonios" id="testimonios"><div class="wrap"><h2 class="rv">{e(" ".join(t.get("titulo") or [self.t["menu"]["testimonios"]])).upper()}</h2><div class="tqs">{q}</div></div></section>\n'

    def paquetes(self):
        p = self.d.get("paquetes")
        if not p: return ""
        c = "".join(f'<div class="plan{" top" if x.get("destacado") else ""} rv"><h3>{e(x.get("nombre", "")).upper()}</h3><b>{e(x.get("precio"))}</b><p>{e(x.get("texto", ""))}</p><ul>'
                    + "".join(f"<li>■ {e(y)}</li>" for y in x.get("incluye", [])) + f'</ul>{self.boton(x.get("cta") or {"texto": self.t["contacto"]}, "btn", False)}</div>' for x in p.get("items", []))
        return f'<section class="paquetes" id="paquetes"><div class="wrap"><h2 class="rv">{e(" ".join(p.get("titulo") or [self.t["menu"]["paquetes"]])).upper()}</h2><div class="plans">{c}</div></div></section>\n'

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        det = "".join(f'<details><summary>{e(x.get("p"))}<span aria-hidden="true">+</span></summary><p>{e(x.get("r"))}</p></details>' for x in items)
        return f'<section class="faq" id="faq"><div class="wrap fq"><h2 class="rv">{e(" ".join(self.t["faq_t"])).upper()}</h2><div class="acc">{det}</div></div></section>\n'

    def cierre(self):
        c = self.d.get("cierre") or {}
        fila = "".join(f'<div class="ro-f rv d{i % 3}">{self.foto(f, "", "", 1200)}</div>' for i, f in enumerate(c.get("imagenes", [])[:3]))
        av = self.img(c.get("avatar") or (self.d.get("sobre") or {}).get("imagen"), 200)
        form = self.formulario()
        datos = "".join(f'<a href="{ea(h)}"{self.ext(h)}><small>{e(k).upper()}</small>{e(v)}</a>' for k, v, h in self.contacto_items())
        tit = c.get("titulo") or (["¿Listo para hacer", "algo que destaque?"] if self.lang == "es" else ["Ready to start something", "that stands out?"])
        return ((f'<section class="fila-final"><div class="wrap"><div class="ro">{fila}</div></div></section>\n' if fila else "")
                + f'<section class="cierre" id="contacto"><div class="wrap"><a class="capsula rv" href="{ea(self.cta_href())}"{self.ext(self.cta_href())}>'
                + (f'<img class="av" src="{av}" alt=""/>' if av else '<i class="av"></i>') + f'<b>{"<br>".join(e(x).upper() for x in tit)}</b>'
                + (f'<small>{e(c["texto"])}</small>' if c.get("texto") else "") + f'<span class="lets">{e(c.get("cta", {}).get("texto", "Hablemos" if self.lang == "es" else "Let’s build")).upper()}</span></a>'
                + (f'<div class="ci-datos rv">{datos}</div>' if datos else "") + (f'<div class="ci-form rv">{form}</div>' if form else "") + "</div></section>\n")

    def secciones(self):
        return [self.portada(), self.estudio(), self.galeria(), self.servicios(), self.proceso(), self.testimonios(), self.paquetes(), self.faq(), self.cierre()]

    def footer(self, desde=""):
        c = self.c; redes = []
        if c.get("instagram"): redes.append(f'<a href="https://instagram.com/{ea(c["instagram"].lstrip("@"))}" target="_blank" rel="noopener">INSTAGRAM</a>')
        for k, lab in (("linkedin", "LINKEDIN"), ("tiktok", "TIKTOK"), ("youtube", "YOUTUBE")):
            if c.get(k): redes.append(f'<a href="{ea(c[k])}" target="_blank" rel="noopener">{lab}</a>')
        lema = self.d.get("marca", {}).get("lema", "")
        from datetime import date
        return (f'<footer class="pie"><div class="wrap"><div class="pie-g" data-fit>{e(self.m.get("dominio") or self.m.get("nombre", "")).upper()}®</div>'
                f'<div class="pie-fila"><p class="lema">{"<br>".join(e(x) for x in (lema if isinstance(lema, list) else [lema])).upper()}</p><div class="redes">{"".join(redes)}</div></div>'
                f'<div class="pie-base"><span>© {date.today().year} {e(self.m.get("nombre"))}</span><div class="leg">{self.enlaces_legales(desde)}</div></div></div></footer>\n')
