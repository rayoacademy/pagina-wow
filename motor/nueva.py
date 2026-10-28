#!/usr/bin/env python3
"""pagina-wow · arranca una página nueva desde una plantilla firma.

Uso:
  python3 nueva.py <plantilla> <carpeta>      crea <carpeta>/sitio.json y <carpeta>/fotos/
  python3 nueva.py --lista                     muestra las 14 plantillas con para quién sirven

Copia el ejemplo de la plantilla y sus fotos de muestra, así la vista previa se ve completa
desde el primer minuto. Después se cambian textos y fotos por los de la persona: el motor
avisa mientras queden fotos de muestra (no se pueden publicar, son de Unsplash para el catálogo).
"""
import json, os, shutil, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANT = os.path.join(SKILL, "plantillas")


def plantillas():
    out = []
    for pid in sorted(os.listdir(PLANT)):
        f = os.path.join(PLANT, pid, "ficha.json")
        if os.path.exists(f): out.append(json.load(open(f, encoding="utf-8")))
    return out


def preparar(pid, carpeta, pisar=False):
    """Deja en carpeta un sitio.json listo para generar. Devuelve la ruta del sitio.json."""
    src = os.path.join(PLANT, pid)
    if not os.path.exists(os.path.join(src, "ejemplo.json")):
        ids = ", ".join(p["id"] for p in plantillas())
        sys.exit(f"No existe la plantilla '{pid}'. Opciones: {ids}")
    sj = os.path.join(carpeta, "sitio.json")
    if os.path.exists(sj) and not pisar:
        sys.exit(f"Ya existe {sj}. No lo piso: usa otra carpeta o bórralo tú.")
    os.makedirs(carpeta, exist_ok=True)
    d = json.load(open(os.path.join(src, "ejemplo.json"), encoding="utf-8"))
    d["plantilla"] = pid
    # va de primera: así borrar la línea no deja una coma suelta. El motor avisa mientras exista.
    d = {"_muestras": True, **d}
    json.dump(d, open(sj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    mu = os.path.join(src, "muestras")
    if os.path.isdir(mu):
        dst = os.path.join(carpeta, "fotos"); os.makedirs(dst, exist_ok=True)
        for f in os.listdir(mu):
            if not os.path.exists(os.path.join(dst, f)): shutil.copy2(os.path.join(mu, f), os.path.join(dst, f))
    return sj


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("--lista", "-l"):
        for p in plantillas(): print(f"{p['id']:<20} {p.get('para', '')}")
        return
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    sj = preparar(sys.argv[1], os.path.abspath(sys.argv[2]))
    print("Lista:", sj)
    print("Siguiente: edita sitio.json y cambia las fotos de fotos/, luego  python3",
          os.path.join(SKILL, "motor", "listo.py"), os.path.dirname(sj))


if __name__ == "__main__":
    main()
