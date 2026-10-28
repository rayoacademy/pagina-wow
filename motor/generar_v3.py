#!/usr/bin/env python3
"""pagina-wow v3 · plantillas firma.

Uso:
  python3 generar_v3.py ruta/sitio.json [carpeta_salida]

Si sitio.json trae "plantilla": "<id>", usa plantillas/<id>/ (HTML y CSS propios de esa
plantilla). Si no, cae al motor v2 (los 42 diseños por variables).
Legal, seguridad, SEO/GEO/AEO, integraciones y auditoría vienen de generar_v2.py.

Contrato de una plantilla (ver plantillas/README.md):
  plantillas/<id>/ficha.json   nombre, familia, fuentes, inspiración, para, fotos que pide
  plantillas/<id>/estilo.css   todo el CSS visual (define también las variables del núcleo)
  plantillas/<id>/plantilla.py class Plantilla(Gen3) con secciones() y, si quiere, nav/footer propios
  plantillas/<id>/extra.js     opcional: JS propio, se agrega al final de assets/app.js (sin JS en línea)
"""
import importlib.util, json, os, re, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar as V1
import generar_v2 as V2
from generar import e, ea, dos

SKILL = V1.SKILL
PLANT = os.path.join(SKILL, "plantillas")
NUCLEO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nucleo.css")


class Gen3(V2.Gen2):
    ID = None  # lo pone el cargador

    def __init__(self, path, out, sobre=None):
        d = json.load(open(path, encoding="utf-8"))
        if sobre: d.update(sobre)
        self.ficha = json.load(open(os.path.join(PLANT, self.ID, "ficha.json"), encoding="utf-8"))
        # el motor v2 necesita una variante para su favicon y variables: usamos la primera de la familia
        sobre2 = dict(sobre or {}); sobre2.setdefault("variante", V1.POR_FAMILIA[self.ficha["familia"]])
        super().__init__(path, out, sobre2)
        self.var = dict(self.var, fuentes=self.ficha["fuentes"], vars={}, id=self.ID)

    # ---------- ayudas para las plantillas ----------
    def items(self, k):
        x = self.d.get(k)
        if not x: return []
        return (x.get("items") if isinstance(x, dict) else x) or []

    def fotos_galeria(self):
        g = self.d.get("galeria")
        imgs = (g.get("imagenes") if isinstance(g, dict) else g) or []
        return [x if isinstance(x, dict) else {"src": x} for x in imgs]

    def foto(self, src, alt="", cls="", w=2000):
        u = self.img(src, w)
        if not u: return f'<div class="sinfoto {cls}"></div>'
        return f'<img class="{cls}" src="{u}" alt="{ea(alt)}" loading="lazy" decoding="async"/>'

    def ext(self, href):
        return ' target="_blank" rel="noopener"' if str(href).startswith("http") else ""

    def boton(self, b, cls="btn", flecha=True):
        if not b: return ""
        if isinstance(b, str): b = {"texto": b}
        href = b.get("href") or self.cta_href()
        return f'<a href="{ea(href)}" class="{cls}"{self.ext(href)}>{e(b["texto"])}' + (' <span class="ar" aria-hidden="true">›</span>' if flecha else "") + "</a>"

    def menu(self):
        etq = dict(self.t["menu"], **(self.d.get("menu_nombres") or {}))
        return [(f"#{k}", etq[k]) for k in ("sobre", "servicios", "proceso", "testimonios", "paquetes", "faq") if self.d.get(k)]

    def contacto_items(self):
        c, out = self.c, []
        if c.get("whatsapp"): out.append((self.t["wa"], c["whatsapp"], self.cta_href()))
        if c.get("email"): out.append((self.t["correo"], c["email"], f'mailto:{c["email"]}'))
        if c.get("instagram"):
            u = c["instagram"].lstrip("@"); out.append((self.t["ig"], "@" + u, f"https://instagram.com/{u}"))
        if c.get("telefono"): out.append((self.t["tel"], c["telefono"], "tel:" + re.sub(r"[^\d+]", "", c["telefono"])))
        if c.get("direccion"): out.append((c.get("ciudad", ""), c["direccion"], c.get("mapa", "#contacto")))
        return out

    def formulario(self):
        """El formulario del motor v2 (consentimiento, trampa, sin JS en línea), o '' si no hay."""
        html = V2.Gen2.contacto(self)
        m = re.search(r'(<div class="card form rv">.*?</div></div>)</div></section>', html, re.S)
        return m.group(1).replace('class="card form rv"', 'class="form rv"') if m else ""

    def enlaces_legales(self, desde=""):
        T2 = self.t2
        return (f'<a href="{desde}{self.ruta("priv")}">{T2["priv"]}</a><a href="{desde}{self.ruta("term")}">{T2["term"]}</a><a href="{desde}{self.ruta("cook")}">{T2["cook"]}</a>'
                + (f'<button type="button" data-ck="abrir">{T2["pref"]}</button>' if self.usa()["cookies"] else ""))

    # ---------- lo que cada plantilla define ----------
    def secciones(self):
        raise NotImplementedError

    def nav_simple(self, desde):
        return (f'<nav class="nav sc" id="nav"><div class="nav-in"><a href="{desde or "/"}" class="marca">{e(self.m.get("nombre"))}</a>'
                f'<a href="{desde or "/"}" class="btn linea">{self.t2["volver"]}</a></div></nav>\n')

    # ---------- textos del ejemplo que se quedaron ----------
    def restos_del_ejemplo(self):
        """Textos de ejemplo.json que siguen idénticos en sitio.json (cifras, lemas, promesas de otro negocio).
        Solo cuenta frases de 12 caracteres o más; rutas de fotos, URLs y claves técnicas no."""
        ej = json.load(open(os.path.join(PLANT, self.ID, "ejemplo.json"), encoding="utf-8"))
        def textos(x, ruta=""):
            if isinstance(x, dict):
                for k, v in x.items():
                    if k in ("plantilla", "idioma", "nivel", "host", "pais", "_muestras", "fuentes"): continue
                    yield from textos(v, f"{ruta}.{k}" if ruta else k)
            elif isinstance(x, list):
                for i, v in enumerate(x): yield from textos(v, f"{ruta}[{i}]")
            elif isinstance(x, str) and len(x) >= 12 and not re.match(r"(fotos/|https?://|#|\+?\d[\d ]+$)", x):
                yield ruta, x
        mios = {v for _, v in textos(self.d)}
        # frases que aparecen en 2 o más ejemplos son genéricas ("Preguntas frecuentes"): no cuentan
        comun = {}
        for pid in os.listdir(PLANT):
            f = os.path.join(PLANT, pid, "ejemplo.json")
            if os.path.exists(f):
                for v in {v for _, v in textos(json.load(open(f, encoding="utf-8")))}: comun[v] = comun.get(v, 0) + 1
        ok = set(self.d.get("_textos_ok") or [])  # textos que la persona decidió conservar a propósito
        return [(r, v) for r, v in textos(ej) if v in mios and comun.get(v, 0) < 2 and v not in ok]

    def auditar(self, doc):
        super().auditar(doc)
        if self.d.get("_muestras") or self.d.get("_catalogo"): return  # MUESTRAS ya lo cubre; en el catálogo el ejemplo es lo esperado
        r = self.restos_del_ejemplo()
        if r:
            ej = ", ".join(f'{k} ("{v[:40]}")' for k, v in r[:6]) + (f" y {len(r) - 6} más" if len(r) > 6 else "")
            self.avisos.append(f"EJEMPLO: quedan {len(r)} texto(s) del negocio de ejemplo: {ej}. Cámbialos o bórralos (si alguno es a propósito, ponlo en \"_textos_ok\"); así no se puede publicar")
        if self.nivel == "principiante" and self.form == "propio" or self.nivel == "amateur" and self.form == "propio":
            self.avisos.append("NIVEL: el formulario propio (Resend + Supabase) es para nivel experto. Para principiante o amateur usa web3forms o ninguno")

    # ---------- construir ----------
    def build(self):
        V2.limpiar_salida(self.out)
        os.makedirs(os.path.join(self.out, "assets"), exist_ok=True)
        css = open(NUCLEO).read() + "\n" + open(os.path.join(PLANT, self.ID, "estilo.css")).read()
        open(os.path.join(self.out, "assets/site.css"), "w").write(css)
        js = V2.APP_JS
        extra = os.path.join(PLANT, self.ID, "extra.js")
        if os.path.exists(extra): js += "\n/* plantilla " + self.ID + " */\n" + open(extra).read()
        open(os.path.join(self.out, "assets/app.js"), "w").write(js)
        body = self.nav() + "<main>\n" + "".join(self.secciones()) + "</main>\n" + self.footer() + self.banner()
        doc = self.head().replace('<body class="', f'<body class="pl-{self.ID} ', 1) + body + "</body>\n</html>\n"
        doc = re.sub(r"\n{2,}", "\n", doc)
        open(os.path.join(self.out, "index.html"), "w", encoding="utf-8").write(doc)
        open(os.path.join(self.out, "favicon.svg"), "w").write(self.favicon())
        todo = doc + "".join(self.pagina_legal(k) for k in ("priv", "term", "cook"))
        # pagina_legal escribe sin la clase de la plantilla: se la agregamos
        for k in ("priv", "term", "cook"):
            p = os.path.join(self.out, self.rutas[k], "index.html")
            s = open(p, encoding="utf-8").read().replace('<body class="', f'<body class="pl-{self.ID} legal-pg ', 1)
            open(p, "w", encoding="utf-8").write(s)
        self.pagina_404()
        p = os.path.join(self.out, "404.html"); s = open(p, encoding="utf-8").read().replace('<body class="', f'<body class="pl-{self.ID} ', 1)
        open(p, "w", encoding="utf-8").write(s)
        self.vercel_json(); self.llms_txt(); self.robots_sitemap(); self.servidor(); V2.huella(self.out)
        self.auditar(todo)
        u = self.usa()
        print(("OK " if not self.errores else "REVISAR ") + self.out)
        print(f"  plantilla: {self.ID} · nivel: {self.nivel} · formulario: {self.form} · analítica: {'PostHog' if self.ph_cfg else ('Vercel' if u['vercel_analytics'] else 'ninguna')} · legal: {self.L['pais']}")
        for x in self.errores: print("  ERROR", x)
        for x in self.avisos: print("  aviso", x)
        return self.out


def cargar(pid):
    ruta = os.path.join(PLANT, pid, "plantilla.py")
    assert os.path.exists(ruta), f"plantilla desconocida: {pid}. Opciones: {', '.join(sorted(x for x in os.listdir(PLANT) if os.path.isdir(os.path.join(PLANT, x))))}"
    spec = importlib.util.spec_from_file_location(f"plantilla_{pid.replace('-', '_')}", ruta)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    cls = mod.Plantilla; cls.ID = pid
    return cls


def generador(path, out=None, sobre=None):
    d = json.load(open(path, encoding="utf-8"))
    if sobre: d.update(sobre)
    pid = d.get("plantilla")
    if pid: return cargar(pid)(path, out, sobre)
    return V2.Gen2(path, out, sobre)


if __name__ == "__main__":
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    generador(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None).build()
