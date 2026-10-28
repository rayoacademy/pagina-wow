#!/usr/bin/env python3
"""pagina-wow · un solo comando para generar, ver y publicar.

Uso:
  python3 listo.py <carpeta>              genera <carpeta>/web y dice qué falta, en palabras simples
  python3 listo.py <carpeta> --ver        además abre la vista previa local (se queda corriendo)
  python3 listo.py <carpeta> --publicar   vista previa en internet (vercel deploy, sin --prod)
  python3 listo.py <carpeta> --prod       publica de verdad. Solo con aprobación explícita de la persona
  python3 listo.py <carpeta> --revisar    si algo falla: diagnostica y dice qué hacer (no cambia nada)
  Opcional: --equipo <nombre> si la cuenta de Vercel tiene varios equipos.

<carpeta> es la que tiene sitio.json (la crea nueva.py).
Antes de publicar se niega si hay errores o si quedan fotos y textos de muestra.
"""
import json, os, re, shutil, socket, subprocess, sys, webbrowser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_v3 import generador

MOTOR = os.path.dirname(os.path.abspath(__file__))


def puerto_libre(desde=4700):
    for p in range(desde, desde + 50):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", p)) != 0: return p
    return desde


def generar(carpeta):
    sj = os.path.join(carpeta, "sitio.json")
    if not os.path.exists(sj): sys.exit(f"No encuentro {sj}. Créalo con: python3 {MOTOR}/nueva.py <plantilla> {carpeta}")
    try:
        d = json.load(open(sj, encoding="utf-8"))
    except json.JSONDecodeError as x:
        lineas = open(sj, encoding="utf-8").read().splitlines()
        cerca = "\n".join(f"  {i + 1}: {lineas[i]}" for i in range(max(0, x.lineno - 3), min(len(lineas), x.lineno + 1)))
        sys.exit(f"sitio.json tiene un error de escritura cerca de la línea {x.lineno}.\n{cerca}\n"
                 "Lo más común: una coma de más al final de una lista o una comilla sin cerrar.")
    g = generador(sj, os.path.join(carpeta, "web"))
    g.build()
    return g, d


def resumen(g, d):
    print()
    if g.errores: print(f"Hay {len(g.errores)} cosa(s) que corregir antes de mostrarla (arriba, las líneas ERROR).")
    elif d.get("_muestras"): print("Se generó con fotos y textos de ejemplo. Sirve para mirar el diseño; falta poner lo de la persona.")
    elif any(x.startswith(("EJEMPLO", "FOTO:")) for x in g.avisos): print("Se puede mirar, pero antes de publicar hay que resolver los avisos EJEMPLO o FOTO de arriba.")
    else: print("Lista para mirar. " + ("Revisa los avisos de arriba." if g.avisos else "Sin avisos."))


def fotos_de_muestra(carpeta):
    """Fotos de la carpeta que son idénticas a las de muestra de alguna plantilla (de Unsplash, solo para el catálogo)."""
    import hashlib
    h = lambda p: hashlib.sha1(open(p, "rb").read()).hexdigest()
    plant = os.path.join(os.path.dirname(MOTOR), "plantillas")
    muestras = {h(os.path.join(r, f)) for r, _, fs in os.walk(plant) if r.endswith("muestras") for f in fs if not f.endswith(".txt")}
    out = []
    for r, _, fs in os.walk(carpeta):
        if os.sep + "web" in r or "/.vercel" in r: continue
        out += [f for f in fs if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".mp4")) and h(os.path.join(r, f)) in muestras]
    return out


def publicar(carpeta, d, g, prod):
    if g.errores: sys.exit("No publico: primero corrige los ERROR de arriba.")
    if d.get("_muestras"): sys.exit("No publico: todavía tiene fotos y textos de muestra (borra \"_muestras\" de sitio.json cuando estén los reales).")
    frenos = [x for x in g.avisos if x.startswith(("EJEMPLO", "FOTO:"))]
    if frenos: sys.exit("No publico:\n  " + "\n  ".join(frenos))
    m = fotos_de_muestra(carpeta)
    if m: sys.exit("No publico: estas fotos siguen siendo las de muestra: " + ", ".join(sorted(set(m))) + ". Cámbialas por fotos de la persona.")
    if not shutil.which("vercel"): sys.exit("Falta Vercel. Instálalo con: npm i -g vercel  y luego: vercel login (lo hace la persona).")
    web = os.path.join(carpeta, "web")
    equipo = opcion("--equipo")
    if not os.path.exists(os.path.join(web, ".vercel", "project.json")):
        # cada página en su propio proyecto (si no, todas caerían en uno llamado "web" y se pisarían)
        nombre = d.get("vercel_proyecto") or slug((d.get("marca") or {}).get("nombre") or os.path.basename(carpeta))
        link = lambda eq: subprocess.run([shutil.which("vercel"), "link", "--yes", "--project", nombre] + (["--scope", eq] if eq else []), cwd=web, capture_output=True, text=True)
        r = link(equipo)
        if r.returncode != 0 or not os.path.exists(os.path.join(web, ".vercel", "project.json")):
            equipo = elegir_equipo(r.stdout + r.stderr)
            if equipo: r = link(equipo)
        if r.returncode != 0: print(r.stdout[-800:], r.stderr[-800:]); sys.exit("No pude crear el proyecto en Vercel. Si dice que no hay sesión: vercel login")
        print("Proyecto de Vercel:", nombre)
    print("Publicando" + (" en producción" if prod else " una vista previa") + "...")
    r = subprocess.run([shutil.which("vercel"), "deploy", "--yes"] + (["--prod"] if prod else []), cwd=web, capture_output=True, text=True)
    res = leer_json(r.stdout)
    url = (res.get("deployment") or {}).get("url") if res else None
    if r.returncode != 0 or not url:
        print(r.stdout[-1500:], r.stderr[-1500:]); sys.exit("Vercel no terminó. Si dice que no hay sesión, la persona corre: vercel login")
    proyecto = json.load(open(os.path.join(web, ".vercel", "project.json"))).get("projectName")
    publico = f"https://{proyecto}.vercel.app"
    print("Link de este deploy:", url)
    if prod: print("Link público (el que se comparte):", publico)
    elif responde(publico): print("Lo que está publicado hoy (sin este cambio):", publico)
    if not prod:
        print("Ojo: el link de vista previa solo abre con sesión de Vercel (viene protegido). Para que otra persona lo vea:"
              " publica con --prod o apaga Settings > Deployment Protection en Vercel.")
    if prod and not (d.get("seo") or {}).get("url"):
        print(f"Siguiente: pon {publico} (o el dominio propio) en seo.url de sitio.json y corre otra vez con --prod,"
              " para que salgan canonical, sitemap y la foto al compartir.")
    return url


def opcion(nombre):
    a = sys.argv
    return a[a.index(nombre) + 1] if nombre in a and a.index(nombre) + 1 < len(a) else None


def slug(t):
    import unicodedata
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:90] or "mi-pagina"


def leer_json(t):
    """El primer objeto JSON del texto (Vercel mezcla mensajes de progreso con su respuesta)."""
    for m in re.finditer(r"\{", t):
        try: return json.JSONDecoder().raw_decode(t[m.start():])[0]
        except json.JSONDecodeError: continue
    return {}


def elegir_equipo(salida):
    """Vercel pide equipo cuando no puede preguntar. Con uno solo, se usa ese; con varios, se le pregunta a la persona."""
    res = leer_json(salida)
    if res.get("reason") != "missing_scope": return None
    eq = [c.get("name") for c in res.get("choices", [])]
    if len(eq) == 1: return eq[0]
    sys.exit("Tu cuenta de Vercel tiene varios equipos: " + ", ".join(eq) + ". Repite agregando: --equipo <nombre>")


def responde(url):
    import urllib.request
    try: return urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=10).status == 200
    except Exception: return False


def revisar(carpeta):
    """Diagnóstico en palabras simples: qué está bien y qué hay que hacer. No cambia nada."""
    import platform
    ok = lambda t: print("  ok   ", t)
    mal = lambda t, h: print("  FALTA", t, "->", h)
    print("Revisando", carpeta)
    ok(f"Python {platform.python_version()}") if sys.version_info >= (3, 8) else mal("Python 3.8 o más", "instala Python desde python.org")
    if not shutil.which("sips"):
        try: import PIL; ok("Pillow para comprimir fotos")
        except ImportError: mal("Pillow (comprimir fotos)", "pip install pillow pillow-heif")
    sj = os.path.join(carpeta, "sitio.json"); d = {}
    if not os.path.exists(sj): mal("sitio.json", f"créalo con: python3 {MOTOR}/nueva.py <plantilla> {carpeta}")
    else:
        try: d = json.load(open(sj, encoding="utf-8")); ok("sitio.json se lee bien")
        except json.JSONDecodeError as x: mal(f"sitio.json tiene un error cerca de la línea {x.lineno}", "una coma de más o una comilla sin cerrar")
    if d:
        fotos = set()
        def buscar(x):
            if isinstance(x, dict): [buscar(v) for v in x.values()]
            elif isinstance(x, list): [buscar(v) for v in x]
            elif isinstance(x, str) and re.match(r"fotos/", x): fotos.add(x)
        buscar(d)
        faltan = sorted(f for f in fotos if not os.path.exists(os.path.join(carpeta, f)))
        ok(f"{len(fotos)} fotos encontradas") if not faltan else mal("fotos: " + ", ".join(faltan), "revisa nombres y mayúsculas en sitio.json")
        if d.get("_muestras"): mal("todavía tiene muestras", "pon textos y fotos reales y borra \"_muestras\"")
        m = fotos_de_muestra(carpeta)
        if m: mal("fotos de muestra: " + ", ".join(sorted(set(m))), "cámbialas por fotos de la persona")
        form = (d.get("integraciones") or {}).get("formulario") or ("web3forms" if (d.get("contacto") or {}).get("web3forms_key") else "ninguno")
        if form == "web3forms":
            k = str((d.get("contacto") or {}).get("web3forms_key", ""))
            ok("clave de Web3Forms con formato correcto") if re.fullmatch(r"[0-9a-fA-F-]{36}", k) and not k.startswith("00000000") else mal("clave real de Web3Forms", "web3forms.com, con el correo donde quiere recibir los mensajes")
        if form == "propio": print("  nota  formulario propio: las claves van en Vercel (ver LEEME-claves.txt); se prueban enviando un mensaje en el link publicado")
        ph = (d.get("integraciones") or {}).get("posthog") or {}
        if ph and "REEMPLAZAR" in str(ph.get("key", "")): mal("clave de PostHog", "Settings > Project > Project API key (phc_...)")
    v = shutil.which("vercel")
    if not v: mal("Vercel", "instala Node (nodejs.org) y luego: npm i -g vercel")
    else:
        r = subprocess.run([v, "whoami"], capture_output=True, text=True, timeout=60)
        ok(f"sesión de Vercel: {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else '?'}") if r.returncode == 0 else mal("sesión de Vercel", "la persona corre: vercel login")
    pj = os.path.join(carpeta, "web", ".vercel", "project.json")
    if os.path.exists(pj):
        u = f"https://{json.load(open(pj)).get('projectName')}.vercel.app"
        ok(f"publicado y responde: {u}") if responde(u) else mal(f"{u} no responde", "publica con --prod o revisa el proyecto en vercel.com")
    else: print("  nota  todavía no se ha publicado")
    print("Guía de problemas: references/si-algo-falla.md")


def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    carpeta = os.path.abspath(sys.argv[1]); op = set(sys.argv[2:])
    if "--revisar" in op: revisar(carpeta); return
    g, d = generar(carpeta)
    resumen(g, d)
    if "--publicar" in op or "--prod" in op:
        publicar(carpeta, d, g, "--prod" in op); return
    if "--ver" in op:
        p = puerto_libre(); url = f"http://localhost:{p}/"
        print("Vista previa:", url, "(Ctrl+C para cerrar)")
        if os.environ.get("PAGINA_WOW_SIN_NAVEGADOR") != "1": webbrowser.open(url)
        sys.stdout.flush()  # execvp reemplaza el proceso: sin esto el link nunca se imprime
        os.execvp(sys.executable, [sys.executable, os.path.join(MOTOR, "servir.py"), os.path.join(carpeta, "web"), str(p)])
    else:
        print(f"Para verla: python3 {MOTOR}/listo.py {carpeta} --ver")


if __name__ == "__main__":
    main()
