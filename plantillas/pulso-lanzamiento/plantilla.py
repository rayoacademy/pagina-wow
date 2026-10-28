"""Pulso Lanzamiento · plantilla firma de la familia Pulso.

Lista de espera luminosa. Firma: aurora animada a pantalla completa, estrella de cuatro puntas
detrás del título, titular en dos tonos, correo y botón unidos en una cápsula, cuenta regresiva
y beneficios en vidrio. La captura de correos usa el mismo motor (Web3Forms o formulario propio).
"""
from generar_v3 import Gen3, e, ea

ESTRELLA = ('<svg class="estrella" viewBox="0 0 400 600" aria-hidden="true"><defs><linearGradient id="eg" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset=".5" stop-color="#e6fff6" stop-opacity=".9"/><stop offset="1" stop-color="#9ff2dc" stop-opacity=".55"/></linearGradient></defs>'
            '<path d="M200 0C208 190 230 270 400 300 230 330 208 410 200 600 192 410 170 330 0 300 170 270 192 190 200 0Z" fill="url(#eg)"/></svg>')
CHISPA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0c.8 7.6 3.6 10.6 12 12-8.4 1.4-11.2 4.4-12 12-.8-7.6-3.6-10.6-12-12C8.4 10.6 11.2 7.6 12 0Z" fill="currentColor"/></svg>'


def t2(t):
    if isinstance(t, str): t = [x.strip() for x in t.split("|")]
    a = e(t[0]) if t else ""
    b = e(t[1]) if len(t) > 1 and t[1] else ""
    return a + (f' <span class="verde">{b}</span>' if b else "")


class Plantilla(Gen3):

    def nav(self):
        return ""  # una sola acción: sin menú

    def caja_correo(self):
        """formulario mínimo de lista de espera: solo correo + autorización, sobre el mismo envío del motor"""
        T, c, es = self.t, self.c, self.lang == "es"
        h = self.d.get("hero", {})
        boton = e((h.get("cta") or {}).get("texto") or ("Avísame" if es else "Get notified"))
        if self.form == "ninguno":
            return f'<div class="capsula sola"><a class="boton" href="{ea(self.cta_href())}"{self.ext(self.cta_href())}>{boton}</a></div>'
        ocultos = ""
        if self.form == "web3forms":
            ocultos = (f'<input type="hidden" name="access_key" value="{ea(c.get("web3forms_key", ""))}"/>'
                       f'<input type="hidden" name="subject" value="Nueva persona en la lista de espera de {ea(self.m.get("nombre"))}"/>'
                       '<input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true"/>')
        else:
            ocultos = '<div class="hp" aria-hidden="true"><label>Empresa<input name="empresa_web" tabindex="-1" autocomplete="off"/></label></div>'
        ocultos += f'<input type="hidden" name="nombre" value="{"Lista de espera" if es else "Waitlist"}"/><input type="hidden" name="mensaje" value="{"Quiere unirse a la lista de espera" if es else "Wants to join the waitlist"}"/>'
        acepto = self.t2["acepto"].format(u=self.ruta("priv"))
        return (f'<form id="cf" class="espera">{ocultos}<div class="capsula"><label class="hp" for="f-e">{T["email"]}</label>'
                f'<input id="f-e" name="email" type="email" autocomplete="email" maxlength="200" required placeholder="{"Tu correo" if es else "Your email address"}"/>'
                f'<button class="boton">{boton}</button></div><label class="fcheck"><input type="checkbox" name="acepto" required/><span>{acepto}</span></label></form>'
                f'<div class="ok" id="ok" role="status"><p>{e(h.get("gracias") or ("¡Listo! Estás en la lista. Te avisamos primero." if es else "You are on the list. We will let you know first."))}</p></div>')

    def portada(self):
        h = self.d.get("hero", {}); c = self.c
        redes = []
        if c.get("instagram"): redes.append(f'<a href="https://instagram.com/{ea(c["instagram"].lstrip("@"))}" target="_blank" rel="noopener">Instagram</a>')
        for k, lab in (("linkedin", "LinkedIn"), ("tiktok", "TikTok"), ("youtube", "YouTube")):
            if c.get(k): redes.append(f'<a href="{ea(c[k])}" target="_blank" rel="noopener">{lab}</a>')
        cuenta = ""
        if h.get("fecha"):
            es = self.lang == "es"
            u = (("d", "días" if es else "days"), ("h", "horas" if es else "hours"), ("m", "min"), ("s", "seg" if es else "sec"))
            cuenta = f'<div class="cuenta rv d3" data-fecha="{ea(h["fecha"])}">' + "".join(f'<div><b data-u="{k}">00</b><small>{n}</small></div>' for k, n in u) + "</div>"
        datos = h.get("datos") or []
        prueba = f'<p class="prueba rv d3"><b>{e(datos[0].get("n"))}</b> {e(datos[0].get("t"))}</p>' if datos else ""
        return (f'<header class="portada" id="top"><div class="aurora" aria-hidden="true"><i class="a1"></i><i class="a2"></i><i class="a3"></i><i class="a4"></i></div>{ESTRELLA}'
                f'<div class="portada-in"><p class="chip rv"><span class="marca">{e(self.m.get("nombre"))}</span>{CHISPA}<span>{e(h.get("etiqueta", ""))}</span></p>'
                f'<h1 class="rv d1">{t2(h.get("titulo") or [self.m.get("nombre", "")])}</h1>' + (f'<p class="lede rv d2">{e(h["texto"])}</p>' if h.get("texto") else "")
                + f'<div class="rv d2">{self.caja_correo()}</div>{prueba}{cuenta}' + (f'<nav class="redes">{" · ".join(redes)}</nav>' if redes else "") + "</div></header>\n")

    def beneficios(self):
        s = self.d.get("servicios")
        if not s: return ""
        cards = "".join(f'<article class="vidrio rv d{i % 3}"><span class="n">{CHISPA}</span><h3>{e(it.get("titulo"))}</h3><p>{e(it.get("texto", ""))}</p></article>' for i, it in enumerate(s.get("items", [])))
        return (f'<section class="beneficios" id="servicios"><div class="wrap"><h2 class="rv">{t2(s.get("titulo") or [self.t["menu"]["servicios"]])}</h2>'
                + (f'<p class="baj rv">{e(s["bajada"])}</p>' if s.get("bajada") else "") + f'<div class="bens">{cards}</div></div></section>\n')

    def faq(self):
        items = self.items("faq")
        if not items: return ""
        det = "".join(f'<details class="vidrio"><summary>{e(x.get("p"))}<span aria-hidden="true">+</span></summary><p>{e(x.get("r"))}</p></details>' for x in items)
        return f'<section class="faq" id="faq"><div class="wrap angosto"><h2 class="rv">{t2(self.d.get("faq_titulo") or self.t["faq_t"])}</h2><div class="acc">{det}</div></div></section>\n'

    def secciones(self):
        return [self.portada(), self.beneficios(), self.faq()]

    def footer(self, desde=""):
        from datetime import date
        return (f'<footer class="pie"><span>© {date.today().year} {e(self.m.get("nombre"))}</span><div class="leg">{self.enlaces_legales(desde)}</div></footer>\n')

    def nav_simple(self, desde):
        return (f'<nav class="nav sc" id="nav"><div class="nav-in"><a href="{desde or "/"}" class="marca">{e(self.m.get("nombre"))}</a>'
                f'<a href="{desde or "/"}" class="btn linea">{self.t2["volver"]}</a></div></nav>\n')
