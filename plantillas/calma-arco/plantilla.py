"""Calma Arco · plantilla firma de la familia Calma.

Estudio de bienestar cálido. Firma: portada con borde inferior curvo, tarjetas con remate
en arco, banda salvia con ilustración de línea, testimonios tipo polaroid con firma a mano,
cierre que se curva hacia un pie verde bosque. Todo el HTML y el CSS son propios.
"""
from generar_v3 import Gen3, e, ea, dos

# ilustraciones de línea (dibujadas para esta plantilla)
RAMA = ('<svg class="rama {c}" viewBox="0 0 220 220" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" aria-hidden="true">'
        '<path d="M18 206C58 160 96 118 150 70c18-16 36-30 54-42"/>'
        '<path d="M60 160c-20-6-34-20-38-40 20 2 34 16 38 40Z"/><path d="M60 160c4-22 18-36 38-40-2 20-16 34-38 40Z"/>'
        '<path d="M96 122c-18-8-30-22-32-42 18 4 30 18 32 42Z"/><path d="M96 122c6-20 20-32 40-34-4 20-18 32-40 34Z"/>'
        '<path d="M132 88c-14-10-22-24-22-42 16 6 24 20 22 42Z"/><path d="M132 88c8-18 22-28 40-28-6 18-20 28-40 28Z"/>'
        '<path d="M168 58c-10-10-14-22-12-36 12 6 16 18 12 36Z"/><path d="M168 58c8-12 20-18 34-16-6 12-18 18-34 16Z"/></svg>')

FLOR = ('<svg class="flor" viewBox="0 0 200 260" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" aria-hidden="true">'
        '<path d="M70 258C68 200 72 150 64 96"/><path d="M128 258c4-60 16-110 40-150"/>'
        '<path d="M68 200c-18-4-30-16-34-34 18 2 30 14 34 34Z"/><path d="M134 210c14-10 30-12 44-6-12 10-28 12-44 6Z"/>'
        '<g transform="translate(64 80)"><circle r="9"/><path d="M0-10C-6-26-2-38 0-42 2-38 6-26 0-10ZM10 0c16-6 28-2 32 0-4 2-16 6-32 0ZM0 10c6 16 2 28 0 32-2-4-6-16 0-32ZM-10 0c-16 6-28 2-32 0 4-2 16-6 32 0Z"/>'
        '<path d="M7-7c8-14 20-18 24-20-2 4-8 14-24 20ZM7 7c14 8 18 20 20 24-4-2-14-8-20-24ZM-7 7c-8 14-20 18-24 20 2-4 8-14 24-20ZM-7-7c-14-8-18-20-20-24 4 2 14 8 20 24Z"/></g>'
        '<g transform="translate(168 104) scale(.78)"><circle r="9"/><path d="M0-10C-6-26-2-38 0-42 2-38 6-26 0-10ZM10 0c16-6 28-2 32 0-4 2-16 6-32 0ZM0 10c6 16 2 28 0 32-2-4-6-16 0-32ZM-10 0c-16 6-28 2-32 0 4-2 16-6 32 0Z"/>'
        '<path d="M7-7c8-14 20-18 24-20-2 4-8 14-24 20ZM7 7c14 8 18 20 20 24-4-2-14-8-20-24ZM-7 7c-8 14-20 18-24 20 2-4 8-14 24-20ZM-7-7c-14-8-18-20-20-24 4 2 14 8 20 24Z"/></g></svg>')

DESTELLO = '<svg class="destello" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><path d="M20 2c2 10 8 16 18 18-10 2-16 8-18 18-2-10-8-16-18-18 10-2 16-8 18-18Z"/></svg>'

HOJA = ('<svg class="hoja" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" aria-hidden="true">'
        '<path d="M5 19C5 10 11 4 20 4c0 9-6 15-15 15Z"/><path d="M5 19 14 10"/></svg>')

CURVA_PIE = '<svg class="curva-pie" viewBox="0 0 1440 140" preserveAspectRatio="none" aria-hidden="true"><path d="M0 0H1440Q720 230 0 0Z"/></svg>'


def t2(t):
    """titular de dos partes: la segunda en itálica"""
    if isinstance(t, str): t = [x.strip() for x in t.split("|")]
    a = e(t[0]) if t else ""
    b = e(t[1]) if len(t) > 1 and t[1] else ""
    return a + (f' <em>{b}</em>' if b else "")


class Plantilla(Gen3):

    # ---------- nav ----------
    def nav(self):
        links = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in self.menu()[:5])
        cta = self.d.get("nav_cta") or self.t["contacto"]
        return (f'<nav class="nav" id="nav"><div class="nav-in"><a href="#top" class="marca">{HOJA}<span>{e(self.m.get("nombre"))}</span></a>'
                f'<div class="links">{links}</div>{self.boton({"texto": cta}, "btn ac pq", False)}</div></nav>\n')

    # ---------- portada ----------
    def portada(self):
        h = self.d.get("hero", {})
        tit = h.get("titulo") or [self.m.get("nombre", "")]
        lede = f'<p class="lede rv d2">{e(h["texto"])}</p>' if h.get("texto") else ""
        ctas = self.boton(h.get("cta"), "btn ac") + self.boton(h.get("cta2"), "btn crema", False)
        etq = f'<span class="etq rv">{e(h["etiqueta"])}</span>' if h.get("etiqueta") else ""
        foco = f' style="object-position:50% {int(h["foco"])}%"' if h.get("foco") is not None else ""
        img = self.foto(h.get("imagen"), h.get("alt", self.m.get("nombre", "")), "ph", 2400).replace("<img ", f"<img{foco} ", 1).replace(' loading="lazy"', ' fetchpriority="high"')
        return (f'<header class="portada" id="top"><div class="portada-foto">{img}<div class="velo"></div></div>'
                f'<div class="wrap portada-in">{etq}<h1 class="t rv d1">{t2(tit)}</h1>{lede}<div class="ctas rv d3">{ctas}</div></div></header>\n')

    # ---------- filosofía (sobre: etiqueta, titulo, bajada) ----------
    def filosofia(self):
        s = self.d.get("sobre")
        if not s: return ""
        return (f'<section class="filosofia" id="sobre"><div class="wrap angosto">'
                + (f'<span class="ceja rv">{e(s.get("etiqueta", self.t["menu"]["sobre"]))}</span>')
                + f'<h2 class="t rv d1">{t2(s.get("titulo", ""))}</h2>'
                + (f'<p class="rv d2">{e(s["bajada"])}</p>' if s.get("bajada") else "")
                + "</div></section>\n")

    # ---------- banda salvia: el espacio (sobre.imagen + texto + cifras) ----------
    def banda(self):
        s = self.d.get("sobre") or {}
        if not (s.get("imagen") or s.get("texto")): return ""
        tit = s.get("titulo_imagen") or [self.m.get("nombre", "")]
        ps = "".join(f'<p>{e(p)}</p>' for p in s.get("texto", []))
        nums = "".join(f'<div><b>{e(n.get("n"))}</b><small>{e(n.get("t"))}</small></div>' for n in s.get("cifras", []))
        foto = f'<figure class="banda-foto rv">{self.foto(s.get("imagen"), s.get("alt", ""), "", 2200)}' + (f'<figcaption>{e(s["pie"])}</figcaption>' if s.get("pie") else "") + "</figure>" if s.get("imagen") else ""
        return (f'<section class="banda">{RAMA.format(c="arriba")}{RAMA.format(c="abajo")}<div class="wrap">'
                f'<h2 class="t rv">{t2(tit)}</h2>{foto}'
                + (f'<div class="banda-txt rv"><div class="cols">{ps}</div>' + (f'<div class="cifras">{nums}</div>' if nums else "") + "</div>" if ps or nums else "")
                + "</div></section>\n")

    # ---------- servicios: tarjetas en arco ----------
    def servicios(self):
        s = self.d.get("servicios")
        if not s: return ""
        cards = []
        for i, it in enumerate(s.get("items", [])):
            pr = f'<span class="precio">{e(it["precio"])}</span>' if it.get("precio") else ""
            cards.append(f'<article class="arco rv d{i % 3}"><div class="arco-foto">{self.foto(it.get("imagen"), it.get("titulo", ""), "", 1100)}</div>'
                         f'<div class="arco-b"><h3>{e(it.get("titulo"))}</h3><span class="raya"></span><p>{e(it.get("texto"))}</p>{pr}'
                         f'{self.boton({"texto": it.get("cta", self.d.get("nav_cta") or self.t["contacto"])}, "btn linea pq", False)}</div></article>')
        return (f'<section class="servicios" id="servicios"><div class="wrap"><div class="cab">'
                + (f'<span class="ceja rv">{e(s["etiqueta"])}</span>' if s.get("etiqueta") else "")
                + f'<h2 class="t rv d1">{t2(s.get("titulo", ""))}</h2>' + (f'<p class="rv d2">{e(s["bajada"])}</p>' if s.get("bajada") else "")
                + f'</div><div class="arcos" style="--n:{min(4, max(1, len(cards)))}">{"".join(cards)}</div></div></section>\n')

    # ---------- proceso: numerales en itálica ----------
    def proceso(self):
        p = self.d.get("proceso")
        if not p: return ""
        st = "".join(f'<li class="rv d{i % 3}"><span class="num">{i + 1:02d}</span><h3>{e(x.get("titulo"))}</h3><p>{e(x.get("texto"))}</p></li>' for i, x in enumerate(p.get("items", [])))
        return (f'<section class="proceso" id="proceso"><div class="wrap"><div class="cab">'
                + (f'<span class="ceja rv">{e(p["etiqueta"])}</span>' if p.get("etiqueta") else "")
                + f'<h2 class="t rv d1">{t2(p.get("titulo", ""))}</h2>' + (f'<p class="rv d2">{e(p["bajada"])}</p>' if p.get("bajada") else "")
                + f'</div><ol class="pasos" style="--n:{len(p.get("items", []))}">{st}</ol></div></section>\n')

    # ---------- testimonios: polaroids ----------
    def testimonios(self):
        t = self.d.get("testimonios")
        if not t: return ""
        cards = []
        for i, x in enumerate(t.get("items", [])):
            ft = f'<div class="pol-foto">{self.foto(x["foto"], x.get("nombre", ""), "", 900)}</div>' if x.get("foto") else ""
            cards.append(f'<figure class="pol{"" if x.get("foto") else " solo"} rv d{i % 3}" style="--r:{(-2.2, 1.6, -1.2, 2)[i % 4]}deg;--y:{(0, 34, 8, 40)[i % 4]}px">{ft}'
                         f'<blockquote>{e(x.get("texto"))}</blockquote><figcaption><span class="firma">{e(x.get("nombre"))}</span>'
                         + (f'<small>{e(x["rol"])}</small>' if x.get("rol") else "") + "</figcaption></figure>")
        return (f'<section class="testimonios" id="testimonios"><div class="wrap"><div class="cab claro">{DESTELLO}'
                f'<h2 class="t rv">{t2(t.get("titulo", ""))}</h2></div><div class="pols">{"".join(cards)}</div></div></section>\n')

    # ---------- galería editorial: una grande y dos chicas ----------
    def galeria(self):
        g = self.d.get("galeria")
        fotos = self.fotos_galeria()
        if not fotos: return ""
        tit = (g.get("titulo") if isinstance(g, dict) else None) or self.t["galeria"]
        def pieza(f, cls):
            cap = (f'<figcaption>' + (f'<small>{e(f["etiqueta"])}</small>' if f.get("etiqueta") else "") + (f'<b>{e(f["titulo"])}</b>' if f.get("titulo") else "")
                   + (f'<span>{e(f["texto"])}</span>' if f.get("texto") else "") + "</figcaption>") if (f.get("titulo") or f.get("texto")) else ""
            return f'<figure class="{cls} rv"><div class="g-foto">{self.foto(f.get("src"), f.get("alt", f.get("titulo", "")), "", 1600)}</div>{cap}</figure>'
        grande = pieza(fotos[0], "g-grande")
        chicas = "".join(pieza(f, "g-chica") for f in fotos[1:3])
        return (f'<section class="galeria" id="galeria"><div class="wrap"><div class="cab izq">'
                + (f'<span class="ceja rv">{e(g["etiqueta"])}</span>' if isinstance(g, dict) and g.get("etiqueta") else "")
                + f'<h2 class="t rv d1">{t2(tit)}</h2></div><div class="g-grid">{grande}<div class="g-lado">{chicas}</div></div></div></section>\n')

    # ---------- paquetes: tarjetas con remate en arco ----------
    def paquetes(self):
        p = self.d.get("paquetes")
        if not p: return ""
        cards = []
        for i, x in enumerate(p.get("items", [])):
            li = "".join(f"<li>{e(y)}</li>" for y in x.get("incluye", []))
            per = f'<small>{e(x["periodo"])}</small>' if x.get("periodo") else ""
            cards.append(f'<div class="paq{" top" if x.get("destacado") else ""} rv d{i % 3}"><h3>{e(x.get("nombre"))}</h3><p>{e(x.get("texto", ""))}</p>'
                         f'<div class="precio">{e(x.get("precio"))}{per}</div><ul>{li}</ul>{self.boton(x.get("cta") or {"texto": self.t["contacto"]}, "btn " + ("crema" if x.get("destacado") else "ac"))}</div>')
        return (f'<section class="paquetes" id="paquetes"><div class="wrap"><div class="cab">'
                + (f'<span class="ceja rv">{e(p["etiqueta"])}</span>' if p.get("etiqueta") else "")
                + f'<h2 class="t rv d1">{t2(p.get("titulo", ""))}</h2></div><div class="paqs" style="--n:{len(cards)}">{"".join(cards)}</div></div></section>\n')

    # ---------- preguntas ----------
    def faq(self):
        items = self.items("faq")
        if not items: return ""
        f = self.d.get("faq")
        tit = (f.get("titulo") if isinstance(f, dict) else None) or self.t["faq_t"]
        det = "".join(f'<details><summary>{e(x.get("p"))}<span aria-hidden="true"></span></summary><p>{e(x.get("r"))}</p></details>' for x in items)
        return (f'<section class="faq" id="faq"><div class="wrap angosto"><span class="ceja rv">{self.t["menu"]["faq"]}</span>'
                f'<h2 class="t rv d1">{t2(tit)}</h2><div class="acc rv d2">{det}</div></div></section>\n')

    # ---------- contacto ----------
    def contacto(self):
        its = self.contacto_items(); form = self.formulario()
        if not its and not form: return ""
        co = self.d.get("contacto_seccion", {})
        tit = co.get("titulo") or (["Escríbenos,", "te respondemos"] if self.lang == "es" else ["Write to us,", "we reply"])
        cards = "".join(f'<a class="dato rv d{i % 3}" href="{ea(h)}"{self.ext(h)}><small>{e(k)}</small><b>{e(v)}</b></a>' for i, (k, v, h) in enumerate(its))
        return (f'<section class="contacto" id="contacto"><div class="wrap angosto"><span class="ceja rv">{self.t["contacto"]}</span><h2 class="t rv d1">{t2(tit)}</h2>'
                + (f'<p class="rv d2">{e(co["bajada"])}</p>' if co.get("bajada") else "")
                + f'<div class="datos">{cards}</div>{form}</div></section>\n')

    # ---------- cierre con flor ----------
    def cierre(self):
        c = self.d.get("cierre")
        if not c: return ""
        return (f'<section class="cierre"><div class="wrap angosto">'
                + (f'<span class="ceja rv">{e(c["etiqueta"])}</span>' if c.get("etiqueta") else "")
                + f'<h2 class="t rv d1">{t2(c.get("titulo", ""))}</h2>' + (f'<p class="rv d2">{e(c["texto"])}</p>' if c.get("texto") else "")
                + f'<div class="ctas rv d3">{self.boton(c.get("cta") or {"texto": self.t["contacto"]}, "btn ac")}</div></div>{FLOR}</section>\n')

    def secciones(self):
        return [self.portada(), self.filosofia(), self.banda(), self.servicios(), self.proceso(), self.testimonios(),
                self.galeria(), self.paquetes(), self.faq(), self.contacto(), self.cierre()]

    # ---------- pie verde bosque ----------
    def footer(self, desde=""):
        c = self.c
        explora = "".join(f'<a href="{desde or ""}{h}">{e(t)}</a>' for h, t in self.menu())
        datos = "".join(f'<a href="{ea(h)}"{self.ext(h)}>{e(v)}</a>' for k, v, h in self.contacto_items())
        redes = "".join(f'<a href="{ea(c[k])}" target="_blank" rel="noopener">{lab}</a>' for k, lab in (("tiktok", "TikTok"), ("youtube", "YouTube"), ("linkedin", "LinkedIn")) if c.get(k))
        lema = self.d.get("marca", {}).get("lema") or self.d.get("seo", {}).get("descripcion", "")
        es = self.lang == "es"
        from datetime import date
        return (f'<footer class="pie">{CURVA_PIE}<div class="wrap">'
                f'<div class="pie-cols"><div><span class="ceja">{"Explora" if es else "Explore"}</span>{explora}</div>'
                f'<div><span class="ceja">{self.t["contacto"]}</span>{datos}{redes}</div></div>'
                f'<div class="pie-marca"><span class="l"></span><a href="{desde or "#top"}" class="marca">{HOJA}<span>{e(self.m.get("nombre"))}</span></a><span class="l"></span></div>'
                + (f'<p class="lema">{e(lema)}</p>' if lema else "")
                + f'<div class="pie-base"><span>© {date.today().year} {e(self.m.get("nombre"))}</span><div class="leg">{self.enlaces_legales(desde)}</div></div>'
                f'</div></footer>\n')
