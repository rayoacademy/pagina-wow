#!/usr/bin/env python3
"""pagina-wow · vista previa local con las MISMAS cabeceras de seguridad que Vercel.

Uso:
  python3 servir.py carpeta/web [puerto]

Lee web/vercel.json y aplica sus cabeceras (CSP incluida), las URLs limpias y la 404.
Así los errores de CSP aparecen en la consola antes de publicar.
Quita 'upgrade-insecure-requests' porque en local no hay https, y nunca guarda caché.
/api/* no corre aquí: se prueba en la vista previa de Vercel.
"""
import json, os, sys, re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

raiz = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "web")
puerto = int(sys.argv[2]) if len(sys.argv) > 2 else 4700
def leer_cfg():
    # se relee en cada pedido: si regeneras la página, la vista previa toma el vercel.json nuevo
    p = os.path.join(raiz, "vercel.json")
    return json.load(open(p)) if os.path.exists(p) else {}


def cabeceras(ruta):
    out, cfg = {}, leer_cfg()
    for regla in cfg.get("headers", []):
        patron = "^" + regla["source"].replace("(.*)", ".*") + "$"
        if re.match(patron, ruta):
            for h in regla["headers"]:
                v = h["value"]
                if h["key"] == "Content-Security-Policy": v = v.replace("; upgrade-insecure-requests", "")
                if h["key"] in ("Strict-Transport-Security", "Cache-Control"): continue
                out[h["key"]] = v
    return out


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=raiz, **k)

    def end_headers(self):
        for k, v in cabeceras(self.path.split("?")[0]).items(): self.send_header(k, v)
        # en local nunca se guarda caché: cada cambio se ve al recargar
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_head(self):
        p = self.path.split("?")[0]
        f = os.path.join(raiz, p.lstrip("/"))
        if p.startswith("/api/"):
            self.send_error(501, "La función /api solo corre en Vercel"); return None
        if not os.path.exists(f) and os.path.exists(f + ".html"): self.path = p + ".html"
        elif not os.path.exists(f) and not os.path.isdir(f):
            self.send_response(404); self.send_header("Content-Type", "text/html; charset=utf-8")
            body = open(os.path.join(raiz, "404.html"), "rb").read() if os.path.exists(os.path.join(raiz, "404.html")) else b"404"
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return None
        return super().send_head()

    def log_message(self, *a): pass


print(f"http://localhost:{puerto}/  ({raiz})")
ThreadingHTTPServer(("127.0.0.1", puerto), H).serve_forever()
