"""Clínica Confianza · plantilla firma de la familia Clínica.

Servicio profesional sereno. Firma: foto a sangre con titular en dos pesos, frase con mini foto
en píldora y avatares, tarjetas de cifras, seis servicios con ícono, foto grande con título,
por qué elegirnos en acordeón junto a una foto, equipo con esquina recortada y cierre oscuro.

Campos propios: sobre.pildora_tras (palabra tras la que va la mini foto), equipo {titulo, bajada, items[{nombre, rol, foto}]}, pausa {imagen, etiqueta, titulo, texto}
"""
from generar_v3 import Gen3, e, ea

FL = '<i class="cir" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2"/></svg></i>'
CHISPA = '<svg class="chispa" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0c.8 7.6 3.6 10.6 12 12-8.4 1.4-11.2 4.4-12 12-.8-7.6-3.6-10.6-12-12C8.4 10.6 11.2 7.6 12 0Z" fill="currentColor"/></svg>'
AST = '<svg class="ast" viewBox="0 0 40 40" aria-hidden="true"><path d="M20 2v36M2 20h36M7 7l26 26M33 7 7 33" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>'
ICONOS = ['<circle cx="12" cy="12" r="8"/><path d="m9 15 6-6M10 9h5v5"/>', '<circle cx="11" cy="11" r="6"/><path d="m20 20-4-4"/>', '<path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="3"/>',
          '<path d="M3 17 9 11l4 4 8-8"/><path d="M15 7h6v6"/>', '<path d="M12 2v20M17 6H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>', '<path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5"/>']


def t2(t):
    """dos pesos: primera parte blanca/negra, segunda gris"""
    if isinstance(t, str): t = [x.strip() for x in t.split("|")]
    a = e(t[0]) if t else ""
    b = e(t[1]) if len(t) > 1 and t[1] else ""
    return f'<span class="w1">{a}</span>' + (f' <span class="w2">{b}</span>' if b else "")


class Plantilla(Gen3):

    def chip(self, x):
        return f'<p class="chip">{CHISPA}{e(x)}</p>' if x else ""

    def btn(self, b, cls="btn negro"):
        if not b: return ""
        if isinstance(b, str): b = {"texto": b}
        href = b.get("href") or self.cta_href()
        return f'<a href="{ea(href)}" class="{cls}"{self.ext(href)}>{e(b["texto"])}{FL}</a>'

    def nav(self):
        links = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in self.menu()[:5])
        return (f'<nav class="nav" id="nav"><div class="nav-in"><a href="#top" class="marca"><i class="logo"></i>{e(self.m.get("nombre"))}</a><div class="links">{links}</div>'
                f'<a href="{ea(self.cta_href())}" class="btn blanco pq"{self.ext(self.cta_href())}>{e(self.d.get("nav_cta") or self.t["contacto"])}</a></div></nav>\n')

    def portada(self):
        h = self.d.get("hero", {})
        img = self.foto(h.get("imagen"), h.get("alt", ""), "ph", 2400).replace(' loading="lazy"', ' fetchpriority="high"')
        return (f'<header class="portada" id="top">{img}<div class="velo"></div><div class="wrap portada-in"><h1 class="rv">{t2(h.get("titulo") or [self.m.get("nombre", "")])}</h1>'
                + (f'<p class="rv d1">{e(h["texto"])}</p>' if h.get("texto") else "") + "</div></header>\n")

    def frase(self):
        s = self.d.get("sobre")
        if not s: return ""
        txt = e(s.get("bajada", ""))
        if s.get("pildora_tras") and s.get("imagen"):
            u = self.img(s["imagen"], 400)
            txt = txt.replace(e(s["pildora_tras"]), e(s["pildora_tras"]) + f' <img class="pildora" src="{u}" alt=""/>', 1)
        avs = "".join(f'<img src="{self.img(x["foto"], 200)}" alt=""/>' for x in (self.d.get("equipo") or {}).get("items", [])[:3] if x.get("foto"))
        prueba = f'<div class="prueba"><span class="avs">{avs}<i>+</i></span><small>{e(s.get("prueba", ""))}</small></div>' if avs else ""
        cif = "".join(f'<div class="cifra rv d{i % 3}"><b>{e(c.get("n"))}</b><small>{e(c.get("t"))}</small><span class="puntos" aria-hidden="true"><i></i><i></i><i></i></span></div>' for i, c in enumerate(s.get("cifras", [])[:3]))
        return (f'<section class="frase" id="sobre"><div class="wrap"><div class="centro">{self.chip(s.get("etiqueta", ""))}<p class="grande rv">{txt}</p>{prueba}</div>'
                + (f'<div class="cifras">{cif}</div>' if cif else "") + "</div></section>\n")

    def servicios(self):
        s = self.d.get("servicios")
        if not s: return ""
        cards = "".join(f'<article class="srv rv d{i % 3}"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">{ICONOS[i % len(ICONOS)]}</svg></span>'
                        f'<h3>{e(it.get("titulo"))}</h3><p>{e(it.get("texto", ""))}</p>' + (f'<small>{e(it["precio"])}</small>' if it.get("precio") else "") + "</article>"
                        for i, it in enumerate(s.get("items", [])))
        return (f'<section class="servicios" id="servicios"><div class="wrap"><div class="cab">{self.chip(s.get("etiqueta", self.t["menu"]["servicios"]))}<h2 class="rv">{t2(s.get("titulo", ""))}</h2>'
                + (f'<p class="rv d1">{e(s["bajada"])}</p>' if s.get("bajada") else "") + f'<div class="rv d2">{self.btn({"texto": self.d.get("nav_cta") or self.t["contacto"]})}</div></div>'
                f'<div class="srvs">{cards}</div></div></section>\n')

    def pausa(self):
        p = self.d.get("pausa")
        if not p or not p.get("imagen"): return ""
        return (f'<section class="banda">{self.foto(p["imagen"], p.get("alt", ""), "", 2400)}<div class="velo"></div><div class="wrap banda-in"><div>'
                + (f'<small>{e(p["etiqueta"])}</small>' if p.get("etiqueta") else "") + f'<h2>{e(p.get("titulo", ""))}</h2>' + (f'<p>{e(p["texto"])}</p>' if p.get("texto") else "")
                + f'</div>{self.btn({"texto": self.d.get("nav_cta") or self.t["contacto"]}, "btn blanco pq")}</div></section>\n')

    def porque(self):
        p = self.d.get("proceso")
        if not p: return ""
        det = "".join(f'<details{" open" if i == 0 else ""}><summary><span class="n">{i + 1:02d}</span>{e(x.get("titulo"))}<span class="fl" aria-hidden="true"></span></summary><p>{e(x.get("texto", ""))}</p></details>' for i, x in enumerate(p.get("items", [])))
        return (f'<section class="porque" id="proceso"><div class="wrap"><div class="pq-cab">{self.chip(p.get("etiqueta", ""))}<h2 class="rv">{t2(p.get("titulo", ""))}</h2>{AST}</div>'
                f'<div class="pq-grid"><div class="acc">{det}</div>' + (f'<figure class="pq-f rv">{self.foto(p["imagen"], p.get("alt", ""), "", 1400)}</figure>' if p.get("imagen") else "") + "</div></div></section>\n")

    def equipo(self):
        q = self.d.get("equipo")
        if not q: return ""
        cards = "".join(f'<figure class="miembro rv d{i % 3}"><div class="mi-w"><div class="mi-f">{self.foto(x.get("foto"), x.get("nombre", ""), "", 900)}</div><a class="esq" href="{ea(self.cta_href())}"{self.ext(self.cta_href())} aria-label="{e(x.get("nombre"))}">{FL}</a></div>'
                        f'<figcaption><b>{e(x.get("nombre"))}</b><small>{e(x.get("rol", ""))}</small></figcaption></figure>' for i, x in enumerate(q.get("items", [])))
        return (f'<section class="equipo" id="equipo"><div class="wrap"><div class="cab">{self.chip(q.get("etiqueta", "Equipo"))}<h2 class="rv">{t2(q.get("titulo", ""))}</h2>'
                + (f'<p class="rv d1">{e(q["bajada"])}</p>' if q.get("bajada") else "") + f'</div><div class="miembros">{cards}</div></div></section>\n')

    def testimonios(self):
        t = self.d.get("testimonios")
        if not t: return ""
        cards = "".join(f'<figure class="tq rv d{i % 3}"><b>★★★★★</b><blockquote>{e(x.get("texto"))}</blockquote><figcaption>{e(x.get("nombre"))}<small>{e(x.get("rol", ""))}</small></figcaption></figure>' for i, x in enumerate(t.get("items", [])))
        return f'<section class="testimonios" id="testimonios"><div class="wrap"><div class="cab">{self.chip(t.get("etiqueta", self.t["menu"]["testimonios"]))}<h2 class="rv">{t2(t.get("titulo", ""))}</h2></div><div class="tqs">{cards}</div></div></section>\n'

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        det = "".join(f'<details><summary>{e(x.get("p"))}<span class="fl" aria-hidden="true"></span></summary><p>{e(x.get("r"))}</p></details>' for x in items)
        return f'<section class="faq" id="faq"><div class="wrap angosto"><div class="cab">{self.chip(self.t["menu"]["faq"])}<h2 class="rv">{t2(self.t["faq_t"])}</h2></div><div class="acc">{det}</div></div></section>\n'

    def cierre(self):
        c = self.d.get("cierre") or {}
        form = self.formulario(); datos = self.contacto_items()
        lista = "".join(f'<a href="{ea(h)}"{self.ext(h)}><small>{e(k)}</small>{e(v)}</a>' for k, v, h in datos)
        foto = self.foto(c.get("imagen"), "", "fondo", 2200) if c.get("imagen") else ""
        return (f'<section class="cierre" id="contacto">{foto}<div class="velo"></div><div class="wrap ci-in">{self.chip(c.get("etiqueta", ""))}<h2 class="rv">{t2(c.get("titulo") or [self.t["contacto"]])}</h2>'
                + (f'<p class="rv">{e(c["texto"])}</p>' if c.get("texto") else "") + f'{self.btn(c.get("cta") or {"texto": self.t["contacto"]}, "btn blanco")}</div></section>\n'
                + (f'<section class="contacto"><div class="wrap ct-grid"><div class="datos">{lista}</div><div>{form}</div></div></section>\n' if (lista or form) else ""))

    def secciones(self):
        return [self.portada(), self.frase(), self.servicios(), self.pausa(), self.porque(), self.equipo(), self.testimonios(), self.faq(), self.cierre()]

    def footer(self, desde=""):
        from datetime import date
        nav = "".join(f'<a href="{desde}{h}">{e(t)}</a>' for h, t in self.menu())
        lema = self.d.get("marca", {}).get("lema", "")
        return (f'<footer class="pie"><div class="wrap pie-grid"><div><a href="{desde or "#top"}" class="marca"><i class="logo"></i>{e(self.m.get("nombre"))}</a>'
                + (f'<p>{e(lema)}</p>' if lema else "") + f'</div><div class="pie-nav"><h4>{"Enlaces" if self.lang == "es" else "Quick links"}</h4>{nav}</div></div>'
                f'<div class="wrap pie-base"><span>© {date.today().year} {e(self.m.get("nombre"))}</span><div class="leg">{self.enlaces_legales(desde)}</div></div></footer>\n')
