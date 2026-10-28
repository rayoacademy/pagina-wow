#!/usr/bin/env python3
"""pagina-wow · genera una página completa a partir de un sitio.json.

Uso:
  python3 generar.py ruta/sitio.json [carpeta_salida]

La salida (por defecto: carpeta 'web' junto al json) queda lista para `vercel deploy`.
Solo se dibujan las secciones que existen en el json. Ver references/esquema.md.
"""
import json, os, re, sys, shutil, subprocess, html as H

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAM = os.path.join(SKILL, "familias")

FUENTES = {
    "noche": "family=Inter+Tight:wght@300;400;500;600&family=Inter:wght@400;500;600",
    "calma": "family=Instrument+Serif:ital@0;1&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600",
    "cartel": "family=Archivo:wdth,wght@62..125,500..900&family=Inter:wght@400;500;600",
}

TXT = {
    "es": dict(menu=dict(sobre="Sobre mí", servicios="Servicios", proceso="Cómo funciona", testimonios="Testimonios", paquetes="Precios", faq="Preguntas"),
               contacto="Contacto", faq_t=["Preguntas", "frecuentes"], faq_p="¿Tienes otra pregunta? Escríbeme.", enviar="Enviar mensaje",
               nombre="Nombre", email="Email", mensaje="Mensaje", gracias="¡Mensaje enviado! Te respondo muy pronto.", error="No se pudo enviar. Inténtalo de nuevo.",
               wa="WhatsApp", ig="Instagram", correo="Correo", tel="Teléfono", galeria=["Galería", ""], derechos="Todos los derechos reservados"),
    "en": dict(menu=dict(sobre="About", servicios="Services", proceso="How it works", testimonios="Reviews", paquetes="Pricing", faq="FAQ"),
               contacto="Contact", faq_t=["Frequently", "asked questions"], faq_p="Have another question? Write to me.", enviar="Send message",
               nombre="Name", email="Email", mensaje="Message", gracias="Message sent! I'll reply soon.", error="Could not send. Please try again.",
               wa="WhatsApp", ig="Instagram", correo="Email", tel="Phone", galeria=["Gallery", ""], derechos="All rights reserved"),
}

def e(s):  # escapar texto, permitiendo **negrita**
    s = H.escape(str(s or ""), quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)

def ea(s): return H.escape(str(s or ""), quote=True)

def dos(t):
    """Titular en dos tonos: lista [linea1, linea2] o texto con ' | '."""
    if isinstance(t, str): t = [x.strip() for x in t.split("|")]
    a = e(t[0]) if t else ""
    b = e(t[1]) if len(t) > 1 and t[1] else ""
    return f'<span class="w">{a}</span>' + (f'<span class="g">{b}</span>' if b else "")

class Gen:
    def __init__(self, path, out):
        self.base = os.path.dirname(os.path.abspath(path))
        self.d = json.load(open(path, encoding="utf-8"))
        self.out = out or os.path.join(self.base, "web")
        self.fam = self.d.get("familia", "noche")
        assert self.fam in FUENTES, f"familia desconocida: {self.fam}"
        self.lang = self.d.get("idioma", "es")
        self.t = TXT[self.lang]
        self.m = self.d.get("marca", {})
        self.c = self.d.get("contacto", {})
        self.imgs = {}

    # ---------- imágenes ----------
    def img(self, src, w=2000):
        if not src: return None
        if src.startswith("http"): return src
        p = src if os.path.isabs(src) else os.path.join(self.base, src)
        if not os.path.exists(p):
            print("  aviso: no existe la imagen", src); return None
        if p in self.imgs: return self.imgs[p]
        name = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(os.path.basename(p))[0].lower()).strip("-")
        dst = f"assets/{name}.jpg"
        os.makedirs(os.path.join(self.out, "assets"), exist_ok=True)
        full = os.path.join(self.out, dst)
        ext = os.path.splitext(p)[1].lower()
        if ext in (".mp4", ".webm", ".mov"):
            dst = f"assets/{name}{ext}"; shutil.copy2(p, os.path.join(self.out, dst))
        else:
            r = subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "78", "-Z", str(w), p, "--out", full], capture_output=True)
            if r.returncode != 0: shutil.copy2(p, full)
        self.imgs[p] = "/" + dst
        return "/" + dst

    def ph(self, src, cls="", alt="", cap="", style=""):
        u = self.img(src)
        st = f' style="{style}"' if style else ""
        if u:
            return f'<div class="ph {cls}"{st}><img src="{u}" alt="{ea(alt)}" loading="lazy"/>' + (f'<span class="cap">{e(cap)}</span>' if cap else "") + "</div>"
        ini = ea(self.m.get("inicial") or (self.m.get("nombre", "·")[:1]))
        return f'<div class="ph vacia {cls}"{st}><span class="marca">{ini}</span>' + (f'<span class="cap">{e(cap)}</span>' if cap else "") + "</div>"

    # ---------- partes ----------
    def cta_href(self):
        c = self.c
        if c.get("whatsapp"):
            num = re.sub(r"\D", "", c["whatsapp"])
            msg = c.get("whatsapp_mensaje", "Hola, vi tu página y quiero más información.")
            from urllib.parse import quote
            return f"https://wa.me/{num}?text={quote(msg)}"
        if c.get("email"): return f"mailto:{c['email']}"
        return "#contacto"

    def btn(self, b, cls="p", arrow=True):
        if not b: return ""
        if isinstance(b, str): b = {"texto": b}
        href = b.get("href") or self.cta_href()
        ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        return f'<a href="{ea(href)}" class="btn {cls}"{ext}>{e(b["texto"])}' + (' <span class="ar">→</span>' if arrow and cls == "p" else "") + "</a>"

    def nav(self):
        d = self.d; links = []
        for k in ["sobre", "servicios", "proceso", "testimonios", "paquetes", "faq"]:
            if d.get(k): links.append(f'<a href="#{k}">{self.t["menu"][k]}</a>')
        cta = self.d.get("nav_cta") or self.t["contacto"]
        return (f'<nav class="nav" id="nav"><div class="nav-in"><a href="#top" class="brand">{e(self.m.get("nombre"))}</a>'
                f'<div class="links">{"".join(links[:5])}</div>'
                f'<a href="{ea(self.cta_href())}" class="btn p"{" target=_blank rel=noopener" if self.cta_href().startswith("http") else ""}>{e(cta)}</a></div></nav>\n')

    def meta_bar(self, items):
        if not items: return ""
        cells = "".join(f'<div><small>{e(x.get("t"))}</small><b>{e(x.get("n"))}</b></div>' for x in items)
        return f'<div class="meta rv d3" style="--n:{len(items)}">{cells}</div>'

    def media_bg(self, h):
        v = h.get("video")
        if v:
            u = self.img(v); poster = self.img(h.get("imagen")) or ""
            return f'<div class="bgm ph"><video autoplay loop muted playsinline poster="{poster}"><source src="{u}"/></video></div>'
        return self.ph(h.get("imagen"), "bgm", h.get("alt", self.m.get("nombre", "")))

    def hero(self):
        h = self.d.get("hero", {})
        chip = f'<span class="chip live rv">{e(h.get("etiqueta"))}</span>' if h.get("etiqueta") else ""
        ctas = self.btn(h.get("cta")) + self.btn(h.get("cta2"), "s")
        lede = f'<p class="lede rv d2">{e(h.get("texto"))}</p>' if h.get("texto") else ""
        if self.fam == "cartel":
            nombre = e(h.get("nombre_grande") or self.m.get("nombre"))
            sub = h.get("titulo")
            return (f'<header class="hero" id="top"><div class="wrap hero-in">'
                    f'<div class="hero-top"><div>{chip}' + (f'<h2 class="h rv d1" style="font-size:clamp(1.6rem,3vw,2.6rem);margin-bottom:1rem">{dos(sub)}</h2>' if sub else "") + f'{lede}</div>'
                    f'<div class="cta-row rv d3">{ctas}</div></div>'
                    f'<div class="stage rv"' + (f' style="--foco:{int(h["foco"])}%"' if h.get("foco") is not None else "") + f'>{self.media_bg(h)}<h1 class="h name" data-fit>{nombre}</h1></div>'
                    f'{self.meta_bar(h.get("datos"))}</div></header>\n')
        return (f'<header class="hero" id="top">{self.media_bg(h)}<div class="sh"></div><div class="wrap hero-in">{chip}'
                f'<h1 class="h rv d1">{dos(h.get("titulo", self.m.get("nombre", "")))}</h1>{lede}'
                f'<div class="cta-row rv d3">{ctas}</div>{self.meta_bar(h.get("datos"))}</div></header>\n')

    def head_block(self, chip, titulo, derecha="", live=False):
        r = derecha if derecha.startswith("<") else (f'<p class="rv d2">{e(derecha)}</p>' if derecha else "<span></span>")
        return (f'<div class="head"><div><span class="chip{" live" if live else ""} rv">{e(chip)}</span>'
                f'<h2 class="h rv d1">{dos(titulo)}</h2></div>{r}</div>')

    def marquesina(self):
        m = self.d.get("marquesina")
        if not m: return ""
        sp = "".join(f"<span>{e(x)}</span>" for x in m) * 2
        return f'<div class="mq" aria-hidden="true"><div class="mq-t">{sp}</div></div>\n'

    def sobre(self):
        s = self.d.get("sobre")
        if not s: return ""
        ps = "".join(f"<p>{e(p)}</p>" for p in s.get("texto", []))
        nums = s.get("cifras") or []
        nh = ("<div class=\"nums\">" + "".join(f'<div><b>{e(n.get("n"))}</b><small>{e(n.get("t"))}</small></div>' for n in nums) + "</div>") if nums else ""
        return (f'<section class="pad" id="sobre"><div class="wrap">{self.head_block(s.get("etiqueta", self.t["menu"]["sobre"]), s.get("titulo", ""), s.get("bajada", ""))}'
                f'<div class="sobre">{self.ph(s.get("imagen"), "rv", s.get("alt", ""), s.get("pie", ""))}<div class="card rv d1">{ps}{nh}</div></div></div></section>\n')

    def servicios(self):
        s = self.d.get("servicios")
        if not s: return ""
        items = s.get("items", []); n = 3 if len(items) % 3 == 0 or len(items) > 4 else 2
        cards = []
        for i, it in enumerate(items):
            ph = self.ph(it.get("imagen"), "", it.get("titulo", "")) if it.get("imagen") or s.get("con_imagen") else ""
            pr = f'<div class="pr">{e(it["precio"])}</div>' if it.get("precio") else ""
            cards.append(f'<article class="sv rv d{i % 3}">{ph}<div class="b"><span class="i">{i + 1:02d}</span><h3>{e(it.get("titulo"))}</h3><p>{e(it.get("texto"))}</p>{pr}</div></article>')
        return (f'<section class="pad t0" id="servicios"><div class="wrap">{self.head_block(s.get("etiqueta", self.t["menu"]["servicios"]), s.get("titulo", ""), s.get("bajada", ""))}'
                f'<div class="serv" style="--n:{n}">{"".join(cards)}</div></div></section>\n')

    def proceso(self):
        p = self.d.get("proceso")
        if not p: return ""
        st = "".join(f'<article class="step rv"><span class="n">{i + 1:02d}</span><div><h3>{e(x.get("titulo"))}</h3><p>{e(x.get("texto"))}</p></div></article>' for i, x in enumerate(p.get("items", [])))
        return (f'<section class="pad alt" id="proceso"><div class="wrap proc"><div class="stick"><span class="chip rv">{e(p.get("etiqueta", self.t["menu"]["proceso"]))}</span>'
                f'<h2 class="h rv d1">{dos(p.get("titulo", ""))}</h2><p class="rv d2">{e(p.get("bajada", ""))}</p></div><div class="steps">{st}</div></div></section>\n')

    def galeria(self):
        g = self.d.get("galeria")
        if not g: return ""
        imgs = g.get("imagenes", []) if isinstance(g, dict) else g
        figs = "".join(self.ph(x if isinstance(x, str) else x.get("src"), "", (x.get("alt") if isinstance(x, dict) else "")) for x in imgs)
        tit = g.get("titulo", self.t["galeria"]) if isinstance(g, dict) else self.t["galeria"]
        return (f'<section class="pad t0" id="galeria"><div class="wrap">{self.head_block(g.get("etiqueta", "Galería") if isinstance(g, dict) else "Galería", tit, g.get("bajada", "") if isinstance(g, dict) else "")}'
                f'<div class="gal rv">{figs}</div></div></section>\n')

    def testimonios(self):
        t = self.d.get("testimonios")
        if not t: return ""
        items = t.get("items", [])
        cards = []
        for i, x in enumerate(items):
            u = self.img(x.get("foto"))
            av = f'<img src="{u}" alt=""/>' if u else e((x.get("nombre") or "·")[:1])
            cards.append(f'<figure class="card tq rv d{i % 3}"><blockquote>“{e(x.get("texto"))}”</blockquote><figcaption class="who"><span class="av">{av}</span><span>{e(x.get("nombre"))}<small>{e(x.get("rol", ""))}</small></span></figcaption></figure>')
        n = min(3, len(items)) or 1
        return (f'<section class="pad t0" id="testimonios"><div class="wrap">{self.head_block(t.get("etiqueta", self.t["menu"]["testimonios"]), t.get("titulo", ""), t.get("bajada", ""))}'
                f'<div class="testi" style="--n:{n}">{"".join(cards)}</div></div></section>\n')

    def paquetes(self):
        p = self.d.get("paquetes")
        if not p: return ""
        cards = []
        for i, x in enumerate(p.get("items", [])):
            li = "".join(f"<li>{e(y)}</li>" for y in x.get("incluye", []))
            per = f' <small>{e(x["periodo"])}</small>' if x.get("periodo") else ""
            cards.append(f'<div class="card pk{" top" if x.get("destacado") else ""} rv d{i % 3}"><h3>{e(x.get("nombre"))}</h3><p>{e(x.get("texto", ""))}</p>'
                         f'<div class="pr">{e(x.get("precio"))}{per}</div><ul>{li}</ul>{self.btn(x.get("cta") or {"texto": self.t["contacto"]})}</div>')
        n = len(cards)
        return (f'<section class="pad t0" id="paquetes"><div class="wrap">{self.head_block(p.get("etiqueta", self.t["menu"]["paquetes"]), p.get("titulo", ""), p.get("bajada", ""))}'
                f'<div class="paq" style="--n:{n}">{"".join(cards)}</div></div></section>\n')

    def faq(self):
        f = self.d.get("faq")
        if not f: return ""
        items = f.get("items", []) if isinstance(f, dict) else f
        det = "".join(f'<details{" open" if i == 0 else ""}><summary>{e(x.get("p"))}</summary><p>{e(x.get("r"))}</p></details>' for i, x in enumerate(items))
        tit = (f.get("titulo") if isinstance(f, dict) else None) or self.t["faq_t"]
        return (f'<section class="pad alt" id="faq"><div class="wrap faq"><div class="l"><span class="chip rv">{self.t["menu"]["faq"]}</span>'
                f'<h2 class="h rv d1">{dos(tit)}</h2><p class="rv d2">{self.t["faq_p"]}</p></div><div class="acc rv">{det}</div></div></section>\n')

    def cierre(self):
        c = self.d.get("cierre")
        if not c: return ""
        return (f'<section class="pad"><div class="wrap"><div class="cierre rv">{self.ph(c.get("imagen"))}<div>'
                + (f'<span class="chip">{e(c.get("etiqueta"))}</span>' if c.get("etiqueta") else "")
                + f'<h2 class="h">{dos(c.get("titulo", ""))}</h2><p>{e(c.get("texto", ""))}</p>'
                f'<div class="cta-row">{self.btn(c.get("cta") or {"texto": self.t["contacto"]})}{self.btn(c.get("cta2"), "s")}</div></div></div></div></section>\n')

    def contacto(self):
        c = self.c
        cards = []
        if c.get("whatsapp"): cards.append((self.t["wa"], c["whatsapp"], self.cta_href()))
        if c.get("email"): cards.append((self.t["correo"], c["email"], f'mailto:{c["email"]}'))
        if c.get("instagram"):
            u = c["instagram"].lstrip("@"); cards.append((self.t["ig"], "@" + u, f"https://instagram.com/{u}"))
        if c.get("telefono"): cards.append((self.t["tel"], c["telefono"], "tel:" + re.sub(r"[^\d+]", "", c["telefono"])))
        if c.get("direccion"): cards.append((c.get("ciudad", ""), c["direccion"], c.get("mapa", "#contacto")))
        if not cards and not c.get("web3forms_key"): return ""
        ch = "".join(f'<a class="card ct rv d{i % 3}" href="{ea(h)}"{" target=_blank rel=noopener" if h.startswith("http") else ""}><small>{e(k)}</small><b>{e(v)}</b></a>' for i, (k, v, h) in enumerate(cards))
        form = ""
        if c.get("web3forms_key"):
            T = self.t
            form = (f'<div class="card form rv"><form id="cf" onsubmit="enviar(event)"><input type="hidden" name="access_key" value="{ea(c["web3forms_key"])}"/>'
                    f'<input type="hidden" name="subject" value="Nuevo mensaje desde la web de {ea(self.m.get("nombre"))}"/>'
                    f'<input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off"/>'
                    f'<div class="frow"><div class="fg"><label>{T["nombre"]}</label><input name="nombre" required/></div><div class="fg"><label>{T["email"]}</label><input name="email" type="email" required/></div></div>'
                    f'<div class="fg"><label>{T["mensaje"]}</label><textarea name="mensaje" required></textarea></div>'
                    f'<button class="btn p" style="width:100%">{T["enviar"]}</button></form><div class="ok" id="ok"><p>{T["gracias"]}</p></div></div>')
        co = self.d.get("contacto_seccion", {})
        return (f'<section class="pad t0" id="contacto"><div class="wrap">{self.head_block(co.get("etiqueta", self.t["contacto"]), co.get("titulo", ["Hablemos", ""] if self.lang == "es" else ["Let’s talk", ""]), co.get("bajada", ""))}'
                f'<div class="cont">{ch}</div>{form}</div></section>\n')

    def footer(self):
        c = self.c; cols = []
        if c.get("instagram"): cols.append(f'<a href="https://instagram.com/{ea(c["instagram"].lstrip("@"))}" target="_blank" rel="noopener">Instagram</a>')
        for k, lab in (("tiktok", "TikTok"), ("youtube", "YouTube"), ("linkedin", "LinkedIn")):
            if c.get(k): cols.append(f'<a href="{ea(c[k])}" target="_blank" rel="noopener">{lab}</a>')
        if c.get("email"): cols.append(f'<a href="mailto:{ea(c["email"])}">{e(c["email"])}</a>')
        from datetime import date
        return (f'<footer><div class="wrap foot"><div class="brand">{e(self.m.get("nombre"))}</div><div class="cols">{"".join(cols)}</div>'
                f'<div class="c">© {date.today().year} {e(self.m.get("nombre"))}. {self.t["derechos"]}.</div></div></footer>\n')

    # ---------- documento ----------
    def head(self):
        s = self.d.get("seo", {}); m = self.m
        title = s.get("titulo") or m.get("nombre", "")
        desc = s.get("descripcion", "")
        url = s.get("url", "")
        og = self.img(s.get("imagen") or self.d.get("hero", {}).get("imagen"), 1200)
        og_abs = (url.rstrip("/") + og) if (og and url and og.startswith("/")) else (og or "")
        acc = m.get("acento")
        ld = {"@context": "https://schema.org", "@type": s.get("tipo", "ProfessionalService" if not self.d.get("persona") else "Person"),
              "name": m.get("nombre"), "description": desc}
        if url: ld["url"] = url
        if og_abs: ld["image"] = og_abs
        if self.c.get("ciudad"): ld["address"] = {"@type": "PostalAddress", "addressLocality": self.c["ciudad"]}
        if self.c.get("telefono") or self.c.get("whatsapp"): ld["telephone"] = self.c.get("telefono") or self.c.get("whatsapp")
        same = [f'https://instagram.com/{self.c["instagram"].lstrip("@")}'] if self.c.get("instagram") else []
        same += [self.c[k] for k in ("tiktok", "youtube", "linkedin") if self.c.get(k)]
        if same: ld["sameAs"] = same
        faq = self.d.get("faq"); faq_items = (faq.get("items") if isinstance(faq, dict) else faq) or []
        ldf = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": x["p"], "acceptedAnswer": {"@type": "Answer", "text": x["r"]}} for x in faq_items]} if faq_items else None
        extra = f":root{{--accent:{acc};}}" if acc else ""
        if acc and self.d.get("acento_texto"): extra += f":root{{--accent-ink:{self.d['acento_texto']};}}"
        return f"""<!DOCTYPE html>
<html lang="{self.lang}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{ea(title)}</title>
<meta name="description" content="{ea(desc)}"/>
{f'<link rel="canonical" href="{ea(url)}"/>' if url else ''}
<meta property="og:type" content="website"/>
<meta property="og:title" content="{ea(title)}"/>
<meta property="og:description" content="{ea(desc)}"/>
{f'<meta property="og:image" content="{ea(og_abs)}"/>' if og_abs else ''}
{f'<meta property="og:url" content="{ea(url)}"/>' if url else ''}
<meta name="twitter:card" content="summary_large_image"/>
<link rel="icon" href="/favicon.svg" type="image/svg+xml"/>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{f'<script type="application/ld+json">{json.dumps(ldf, ensure_ascii=False)}</script>' if ldf else ''}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{FUENTES[self.fam]}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v=1">
{f'<style>{extra}</style>' if extra else ''}
</head>
<body class="fam-{self.fam}">
"""

    JS = """<script>
const nav=document.getElementById('nav');const onS=()=>nav.classList.toggle('sc',scrollY>40);onS();addEventListener('scroll',onS,{passive:true});
const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));
function fit(){document.querySelectorAll('[data-fit]').forEach(el=>{el.style.fontSize='100px';const w=el.parentElement.clientWidth;el.style.fontSize=(100*w/el.getBoundingClientRect().width*0.98)+'px';});}
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);fit();addEventListener('resize',fit);
function enviar(ev){ev.preventDefault();const f=ev.target,b=f.querySelector('button');b.disabled=true;b.style.opacity=.6;
fetch('https://api.web3forms.com/submit',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(f)))})
.then(r=>r.json()).then(j=>{if(!j.success)throw 0;f.style.display='none';document.getElementById('ok').classList.add('show');})
.catch(()=>{b.disabled=false;b.style.opacity=1;alert(ERR);});}
</script>
"""

    def favicon(self):
        ini = H.escape((self.m.get("inicial") or self.m.get("nombre", "·")[:1]).upper())
        bg = {"noche": "#0a0a0a", "calma": "#b5643f", "cartel": "#0c0c0c"}[self.fam]
        fg = {"noche": "#f5f5f4", "calma": "#fffaf3", "cartel": self.m.get("acento", "#ff4a1c")}[self.fam]
        ff = {"noche": "Helvetica, Arial, sans-serif", "calma": "Georgia, 'Times New Roman', serif", "cartel": "'Arial Black', Helvetica, Arial, sans-serif"}[self.fam]
        fw = {"noche": "600", "calma": "400", "cartel": "900"}[self.fam]
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="15" fill="{bg}"/>'
                f'<text x="32" y="44" text-anchor="middle" font-family="{ff}" font-weight="{fw}" font-size="38" fill="{fg}">{ini}</text></svg>')

    def build(self):
        if os.path.exists(self.out):
            vc = os.path.join(self.out, ".vercel"); keep = None
            if os.path.exists(vc): keep = vc + "_tmp"; shutil.move(vc, keep)
            shutil.rmtree(self.out); os.makedirs(self.out)
            if keep: shutil.move(keep, vc)
        os.makedirs(os.path.join(self.out, "assets"), exist_ok=True)
        css = open(os.path.join(FAM, "base.css")).read() + "\n" + open(os.path.join(FAM, f"{self.fam}.css")).read()
        open(os.path.join(self.out, "assets/site.css"), "w").write(css)
        body = (self.nav() + self.hero() + self.marquesina() + self.sobre() + self.servicios() + self.proceso() + self.galeria()
                + self.testimonios() + self.paquetes() + self.faq() + self.cierre() + self.contacto() + self.footer())
        js = self.JS.replace("ERR", json.dumps(self.t["error"]))
        doc = self.head() + body + js + "</body>\n</html>\n"
        doc = re.sub(r"\n{2,}", "\n", doc)
        open(os.path.join(self.out, "index.html"), "w", encoding="utf-8").write(doc)
        open(os.path.join(self.out, "favicon.svg"), "w").write(self.favicon())
        url = self.d.get("seo", {}).get("url", "").rstrip("/")
        open(os.path.join(self.out, "robots.txt"), "w").write("User-agent: *\nAllow: /\n" + (f"Sitemap: {url}/sitemap.xml\n" if url else ""))
        if url:
            open(os.path.join(self.out, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{url}/</loc></url></urlset>\n')
        # chequeos duros
        prob = []
        if "—" in doc: prob.append("hay em dash (—) en el contenido")
        for k in ("hero",):
            if not self.d.get(k): prob.append(f"falta la sección {k}")
        print(("OK " if not prob else "REVISAR ") + self.out, *prob, sep="\n  ")
        return self.out

if __name__ == "__main__":
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    Gen(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None).build()
