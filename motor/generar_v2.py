#!/usr/bin/env python3
"""pagina-wow v2 · igual que generar.py, más legal, seguridad, SEO/GEO/AEO e integraciones.

Uso:
  python3 generar_v2.py ruta/sitio.json [carpeta_salida]

Además de index.html crea:
  privacidad/ terminos/ cookies/ (o privacy/ terms/ en inglés), 404.html,
  vercel.json (cabeceras de seguridad), llms.txt, robots.txt, sitemap.xml,
  assets/app.js (todo el JS va en archivo para que la CSP no necesite 'unsafe-inline'),
  y con formulario propio: api/contacto.js + supabase.sql + LEEME-claves.txt.
Al final imprime una auditoría (errores y avisos). Ver references/esquema.md y references/niveles.md.
"""
import json, os, re, sys, hashlib
from datetime import date
from urllib.parse import urlparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar as V1
from generar import e, ea, dos
import legal as LG

TXT2 = {
    "es": dict(priv="Privacidad", term="Términos", cook="Cookies", pref="Preferencias de cookies", rutas=("privacidad", "terminos", "cookies"),
               t_priv="Política de privacidad", t_term="Términos y condiciones", t_cook="Política de cookies", act="Última actualización",
               acepto='Acepto la <a href="{u}" target="_blank" rel="noopener">política de privacidad</a> y autorizo el tratamiento de mis datos para responderme.',
               banner="Usamos cookies de estadística para saber qué funciona en la página. Solo se activan si aceptas.", si="Aceptar", no="Rechazar", mas="Más información",
               volver="Volver al inicio", n404=["Esta página", "no existe"], t404="Puede que el enlace esté mal escrito o que la página se haya movido.",
               tabla=("Nombre", "Tipo", "Para qué", "Duración")),
    "en": dict(priv="Privacy", term="Terms", cook="Cookies", pref="Cookie preferences", rutas=("privacy", "terms", "cookies"),
               t_priv="Privacy policy", t_term="Terms and conditions", t_cook="Cookie policy", act="Last updated",
               acepto='I accept the <a href="{u}" target="_blank" rel="noopener">privacy policy</a> and consent to my data being used to reply to me.',
               banner="We use analytics cookies to learn what works on this site. They only turn on if you accept.", si="Accept", no="Reject", mas="Learn more",
               volver="Back to home", n404=["This page", "does not exist"], t404="The link may be mistyped or the page may have moved.",
               tabla=("Name", "Type", "Purpose", "Duration")),
}

LOCALE = {("es", "CO"): "es_CO", ("es", "US"): "es_US", ("es", "EU"): "es_ES", ("en", "US"): "en_US", ("en", "EU"): "en_GB", ("es", "MX"): "es_MX"}

CSS_V2 = """
/* v2 · legal, consentimiento, banner */
.fcheck{display:flex;gap:.7rem;align-items:flex-start;font-size:.82rem;color:var(--muted);margin:.4rem 0 1.1rem;line-height:1.45;}
.fcheck input{width:18px;height:18px;flex:none;margin-top:.1rem;accent-color:var(--accent);}
.fcheck a{text-decoration:underline;text-underline-offset:2px;color:var(--ink);}
.hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden;}
.foot .leg{display:flex;flex-wrap:wrap;gap:1.2rem;font-size:.8rem;color:var(--muted2);}
.foot .leg a,.foot .leg button{color:inherit;background:none;border:0;font:inherit;cursor:pointer;padding:0;}
.foot .leg a:hover,.foot .leg button:hover{color:var(--ink);}
.legal{max-width:760px;margin:0 auto;padding:9rem clamp(16px,4vw,40px) 4rem;}
.legal h1{font-size:clamp(2.2rem,5vw,3.6rem);margin-bottom:.8rem;}
.legal .act{color:var(--muted);font-size:.85rem;margin-bottom:3rem;}
.legal h2{font-family:var(--f-display);font-size:1.3rem;font-weight:500;letter-spacing:-.02em;margin:2.4rem 0 .8rem;}
.legal p{color:color-mix(in srgb,var(--ink) 82%,transparent);margin-bottom:.9rem;}
.legal strong{color:var(--ink);font-weight:600;}
.legal table{width:100%;border-collapse:collapse;font-size:.85rem;margin:1rem 0 2rem;}
.legal th,.legal td{text-align:left;padding:.7rem .6rem;border-bottom:1px solid var(--line);vertical-align:top;}
.legal th{color:var(--muted);font-weight:500;}
.legal .btn{margin-top:2.4rem;}
.ckb{position:fixed;left:16px;right:16px;bottom:16px;z-index:80;max-width:560px;margin-left:auto;background:var(--surface);color:var(--ink);border:1px solid var(--line2);border-radius:18px;padding:18px 18px 16px;box-shadow:0 24px 60px -24px rgba(0,0,0,.5);display:none;font-size:.88rem;}
.ckb.show{display:block;}
.ckb p{color:color-mix(in srgb,var(--ink) 80%,transparent);margin-bottom:12px;}
.ckb p a{text-decoration:underline;}
.ckb .r{display:flex;gap:.6rem;flex-wrap:wrap;}
.ckb .btn{padding:.7rem 1.2rem;font-size:.84rem;}
.n404{min-height:100svh;display:grid;place-items:center;text-align:center;padding:2rem 16px;}
.n404 h1{font-size:clamp(2.6rem,7vw,5rem);margin-bottom:1rem;}
.n404 p{color:var(--muted);margin-bottom:2rem;}
"""

APP_JS = r"""/* pagina-wow v2 · app.js (sin dependencias). La configuración viene en <script type="application/json" id="cfg">. */
(function(){
var C={};try{C=JSON.parse(document.getElementById('cfg').textContent)}catch(_){}
var nav=document.getElementById('nav');
if(nav){var onS=function(){nav.classList.toggle('sc',scrollY>40)};onS();addEventListener('scroll',onS,{passive:true});}
var rv=document.querySelectorAll('.rv');
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});rv.forEach(function(el){io.observe(el)});}
else rv.forEach(function(el){el.classList.add('in')});
function fit(){document.querySelectorAll('[data-fit]').forEach(function(el){el.style.fontSize='100px';var p=el.parentElement,cs=getComputedStyle(p),w=p.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);el.style.fontSize=(100*w/el.getBoundingClientRect().width*0.98)+'px';});}
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);fit();addEventListener('resize',fit);

/* --- consentimiento y PostHog --- */
var KEY='pw_consent';
function leer(){try{return localStorage.getItem(KEY)}catch(_){return null}}
function guardar(v){try{localStorage.setItem(KEY,v)}catch(_){}}
var ph=C.posthog;
function cargarPH(persist){
  if(!ph||window.__ph)return;window.__ph=1;
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
  posthog.init(ph.key,{api_host:ph.host,ui_host:ph.ui_host,persistence:persist,person_profiles:'identified_only',disable_session_recording:true,capture_pageleave:true,respect_dnt:true});
}
function ev(n,p){try{if(window.posthog&&posthog.capture)posthog.capture(n,p||{})}catch(_){}}
window.pwEvento=ev;
var banner=document.getElementById('ckb');
function mostrar(){if(banner)banner.classList.add('show')}
if(ph){
  if(!ph.cookies)cargarPH('memory');
  else{var c=leer();if(c==='si')cargarPH('localStorage+cookie');else{cargarPH('memory');if(c!=='no')mostrar();}}
}
if(banner){
  banner.querySelector('[data-ck=si]').addEventListener('click',function(){guardar('si');banner.classList.remove('show');try{posthog.set_config({persistence:'localStorage+cookie'})}catch(_){}ev('cookies_aceptadas')});
  banner.querySelector('[data-ck=no]').addEventListener('click',function(){guardar('no');banner.classList.remove('show');try{posthog.set_config({persistence:'memory'})}catch(_){}
    document.cookie.split(';').forEach(function(c){var n=c.split('=')[0].trim();if(n.indexOf('ph_')===0){var d=location.hostname.split('.');for(var i=0;i<d.length;i++){var dom=d.slice(i).join('.');document.cookie=n+'=; Max-Age=0; path=/; domain='+dom;}document.cookie=n+'=; Max-Age=0; path=/';}});
    try{Object.keys(localStorage).forEach(function(k){if(k.indexOf('ph_')===0)localStorage.removeItem(k)})}catch(_){}});
}
document.querySelectorAll('[data-ck=abrir]').forEach(function(b){b.addEventListener('click',mostrar)});

/* --- eventos del embudo --- */
document.addEventListener('click',function(x){var a=x.target.closest&&x.target.closest('a');if(!a)return;var h=a.getAttribute('href')||'';
  var t=(a.textContent||'').trim().slice(0,60),zona=(a.closest('section,header,nav,footer')||{}).id||'';
  if(h.indexOf('wa.me')>-1)ev('click_whatsapp',{texto:t,zona:zona});
  else if(h.indexOf('mailto:')===0)ev('click_correo',{texto:t,zona:zona});
  else if(h.indexOf('tel:')===0)ev('click_telefono',{zona:zona});
  else if(a.classList.contains('btn'))ev('click_boton',{texto:t,zona:zona,destino:h});
});

/* --- formulario --- */
var f=document.getElementById('cf');
if(f){var ini=Date.now();
  f.addEventListener('submit',function(x){x.preventDefault();var b=f.querySelector('button');
    if(Date.now()-ini<2500)return;
    b.disabled=true;b.style.opacity=.6;
    var datos=Object.fromEntries(new FormData(f));datos.pagina=location.href;
    var url=C.form==='propio'?'/api/contacto':'https://api.web3forms.com/submit';
    fetch(url,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(datos)})
    .then(function(r){return r.json()}).then(function(j){if(!j.success)throw 0;f.style.display='none';document.getElementById('ok').classList.add('show');ev('formulario_enviado',{via:C.form});})
    .catch(function(){b.disabled=false;b.style.opacity=1;alert(C.err||'Error');});
  });
}
})();
"""

API_JS = r"""// pagina-wow v2 · función de Vercel para el formulario propio (nivel experto).
// Las claves NUNCA van en el código: se pegan en Vercel → Settings → Environment Variables.
//   RESEND_API_KEY      clave de resend.com (empieza por re_)
//   CONTACTO_PARA       correo donde llegan los mensajes
//   CONTACTO_DESDE      remitente verificado en Resend, ej. "Web <hola@tudominio.com>"
//   SUPABASE_URL        https://xxxx.supabase.co               (opcional: guardar los leads)
//   SUPABASE_SERVICE_ROLE_KEY  clave service_role (solo servidor) (opcional)
//   SUPABASE_TABLA      nombre de la tabla, por defecto "leads"  (opcional)
//   RESPUESTA_AUTOMATICA texto del correo de confirmación al cliente (opcional)
const MAX = { nombre: 120, email: 200, mensaje: 5000 };
const limpio = (s, n) => String(s || "").replace(/[\u0000-\u001f\u007f]/g, " ").trim().slice(0, n);

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") return res.status(405).json({ success: false });
  const origin = req.headers.origin || "";
  try { if (origin && new URL(origin).host !== req.headers.host) return res.status(403).json({ success: false }); } catch { return res.status(403).json({ success: false }); }
  let b = req.body;
  if (typeof b === "string") { try { b = JSON.parse(b); } catch { b = {}; } }
  b = b || {};
  if (b.empresa_web) return res.status(200).json({ success: true }); // trampa para bots
  const nombre = limpio(b.nombre, MAX.nombre), email = limpio(b.email, MAX.email), mensaje = limpio(b.mensaje, MAX.mensaje);
  if (!nombre || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !mensaje) return res.status(400).json({ success: false, error: "datos" });
  if (b.acepto !== "on" && b.acepto !== true) return res.status(400).json({ success: false, error: "consentimiento" });
  const pagina = limpio(b.pagina, 300);
  const E = process.env, errores = [];

  if (E.SUPABASE_URL && E.SUPABASE_SERVICE_ROLE_KEY) {
    const r = await fetch(`${E.SUPABASE_URL}/rest/v1/${E.SUPABASE_TABLA || "leads"}`, {
      method: "POST",
      headers: { apikey: E.SUPABASE_SERVICE_ROLE_KEY, Authorization: `Bearer ${E.SUPABASE_SERVICE_ROLE_KEY}`, "Content-Type": "application/json", Prefer: "return=minimal" },
      body: JSON.stringify({ nombre, email, mensaje, pagina, consentimiento: true }),
    }).catch((x) => ({ ok: false, status: String(x) }));
    if (!r.ok) errores.push("supabase " + r.status);
  }
  if (E.RESEND_API_KEY && E.CONTACTO_PARA && E.CONTACTO_DESDE) {
    const enviar = (cuerpo) => fetch("https://api.resend.com/emails", {
      method: "POST", headers: { Authorization: `Bearer ${E.RESEND_API_KEY}`, "Content-Type": "application/json" }, body: JSON.stringify(cuerpo),
    }).catch((x) => ({ ok: false, status: String(x) }));
    const r = await enviar({ from: E.CONTACTO_DESDE, to: E.CONTACTO_PARA.split(",").map((s) => s.trim()), reply_to: email,
      subject: `Nuevo mensaje de ${nombre}`, text: `Nombre: ${nombre}\nCorreo: ${email}\nPágina: ${pagina}\n\n${mensaje}` });
    if (!r.ok) errores.push("resend " + r.status);
    if (E.RESPUESTA_AUTOMATICA) await enviar({ from: E.CONTACTO_DESDE, to: email, subject: "Recibimos tu mensaje", text: E.RESPUESTA_AUTOMATICA });
  }
  if (errores.length || (!E.RESEND_API_KEY && !E.SUPABASE_URL)) {
    console.error("contacto:", errores.join(", ") || "sin claves configuradas");
    return res.status(500).json({ success: false });
  }
  return res.status(200).json({ success: true });
};
"""

SQL = """-- pagina-wow v2 · tabla para los mensajes del formulario. Pégalo en Supabase → SQL Editor → Run.
create table if not exists public.leads (
  id uuid primary key default gen_random_uuid(),
  creado timestamptz not null default now(),
  nombre text not null,
  email text not null,
  mensaje text not null,
  pagina text,
  consentimiento boolean not null default false
);
-- RLS activo y SIN políticas: nadie puede leer ni escribir desde el navegador.
-- Solo la función del servidor (con la clave service_role) puede guardar.
alter table public.leads enable row level security;
"""


class Gen2(V1.Gen):
    def __init__(self, path, out, sobre=None):
        super().__init__(path, out, sobre)
        self.t2 = TXT2[self.lang]
        self.nivel = self.d.get("nivel", "principiante")
        I = self.d.get("integraciones", {}) or {}
        self.I = I
        self.ph_cfg = I.get("posthog") if (I.get("posthog") or {}).get("key") else None
        if self.ph_cfg:
            h = self.ph_cfg.get("host", "https://us.i.posthog.com").rstrip("/")
            self.ph_cfg = {"key": self.ph_cfg["key"], "host": h, "ui_host": "https://eu.posthog.com" if "eu." in h else "https://us.posthog.com",
                           "cookies": bool(self.ph_cfg.get("cookies"))}
        modo = I.get("formulario")
        if not modo: modo = "web3forms" if self.c.get("web3forms_key") else "ninguno"
        self.form = modo
        L = dict(self.d.get("legal", {}) or {})
        L.setdefault("responsable", self.m.get("nombre", ""))
        L.setdefault("email", self.c.get("email", ""))
        if not L.get("direccion") and (self.c.get("direccion") or self.c.get("ciudad")):
            L["direccion"] = ", ".join(x for x in (self.c.get("direccion"), self.c.get("ciudad")) if x)
        L.setdefault("pais", "CO" if self.lang == "es" else "US")
        self.L = L
        self.prof = "../"  # prefijo de rutas en subpáginas
        self.rutas = dict(zip(("priv", "term", "cook"), self.t2["rutas"]))
        self.avisos, self.errores = [], []

    # ---------- qué usa la página (para los textos legales y la CSP) ----------
    def usa(self):
        return {"vercel": True, "fuentes": True, "whatsapp": bool(self.c.get("whatsapp") or self.c.get("email")),
                "formulario": self.form in ("web3forms", "propio"), "web3forms": self.form == "web3forms",
                "resend": self.form == "propio", "supabase": self.form == "propio" and self.I.get("supabase", True) is not False,
                "posthog": bool(self.ph_cfg), "vercel_analytics": bool(self.I.get("vercel_analytics")),
                "analitica": bool(self.ph_cfg or self.I.get("vercel_analytics")), "cookies": bool(self.ph_cfg and self.ph_cfg["cookies"])}

    def ruta(self, k, desde=""):
        return f"{desde}{self.rutas[k]}/"

    # ---------- contacto: consentimiento, honeypot, sin JS en línea ----------
    def contacto(self):
        c = self.c
        if self.form == "web3forms" and not c.get("web3forms_key"):
            self.errores.append("FORMULARIO: falta la clave de Web3Forms. La persona entra a web3forms.com, escribe el correo donde quiere recibir los mensajes y le llega una clave (gratis). Va en contacto.web3forms_key"); self.form = "ninguno"
        elif self.form == "web3forms" and not re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", str(c.get("web3forms_key")).strip()):
            self.errores.append("FORMULARIO: la clave de Web3Forms no tiene el formato correcto (son 36 caracteres tipo 1a2b3c4d-....). Cópiala completa del correo de web3forms.com")
        cards = []
        if c.get("whatsapp"): cards.append((self.t["wa"], c["whatsapp"], self.cta_href()))
        if c.get("email"): cards.append((self.t["correo"], c["email"], f'mailto:{c["email"]}'))
        if c.get("instagram"):
            u = c["instagram"].lstrip("@"); cards.append((self.t["ig"], "@" + u, f"https://instagram.com/{u}"))
        if c.get("telefono"): cards.append((self.t["tel"], c["telefono"], "tel:" + re.sub(r"[^\d+]", "", c["telefono"])))
        if c.get("direccion"): cards.append((c.get("ciudad", ""), c["direccion"], c.get("mapa", "#contacto")))
        if not cards and self.form == "ninguno": return ""
        ch = "".join(f'<a class="card ct rv d{i % 3}" href="{ea(h)}"{" target=_blank rel=noopener" if h.startswith("http") else ""}><small>{e(k)}</small><b>{e(v)}</b></a>' for i, (k, v, h) in enumerate(cards))
        form = ""
        if self.form in ("web3forms", "propio"):
            T = self.t
            ocultos = ""
            if self.form == "web3forms":
                ocultos = (f'<input type="hidden" name="access_key" value="{ea(c["web3forms_key"])}"/>'
                           f'<input type="hidden" name="subject" value="Nuevo mensaje desde la web de {ea(self.m.get("nombre"))}"/>'
                           '<input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true"/>')
            else:
                ocultos = '<div class="hp" aria-hidden="true"><label>Empresa<input name="empresa_web" tabindex="-1" autocomplete="off"/></label></div>'
            acepto = self.t2["acepto"].format(u=self.ruta("priv"))
            form = (f'<div class="card form rv"><form id="cf">{ocultos}'
                    f'<div class="frow"><div class="fg"><label for="f-n">{T["nombre"]}</label><input id="f-n" name="nombre" autocomplete="name" maxlength="120" required/></div>'
                    f'<div class="fg"><label for="f-e">{T["email"]}</label><input id="f-e" name="email" type="email" autocomplete="email" maxlength="200" required/></div></div>'
                    f'<div class="fg"><label for="f-m">{T["mensaje"]}</label><textarea id="f-m" name="mensaje" maxlength="5000" required></textarea></div>'
                    f'<label class="fcheck"><input type="checkbox" name="acepto" required/><span>{acepto}</span></label>'
                    f'<button class="btn p" style="width:100%">{T["enviar"]}</button></form><div class="ok" id="ok" role="status"><p>{T["gracias"]}</p></div></div>')
        co = self.d.get("contacto_seccion", {})
        return (f'<section class="pad t0" id="contacto"><div class="wrap">{self.head_block(co.get("etiqueta", self.t["contacto"]), co.get("titulo", ["Hablemos", ""] if self.lang == "es" else ["Let’s talk", ""]), co.get("bajada", ""))}'
                f'<div class="cont">{ch}</div>{form}</div></section>\n')

    # ---------- pie con enlaces legales ----------
    def footer(self, desde=""):
        c = self.c; cols = []
        if c.get("instagram"): cols.append(f'<a href="https://instagram.com/{ea(c["instagram"].lstrip("@"))}" target="_blank" rel="noopener">Instagram</a>')
        for k, lab in (("tiktok", "TikTok"), ("youtube", "YouTube"), ("linkedin", "LinkedIn")):
            if c.get(k): cols.append(f'<a href="{ea(c[k])}" target="_blank" rel="noopener">{lab}</a>')
        if c.get("email"): cols.append(f'<a href="mailto:{ea(c["email"])}">{e(c["email"])}</a>')
        T2 = self.t2
        leg = (f'<a href="{desde}{self.ruta("priv")}">{T2["priv"]}</a><a href="{desde}{self.ruta("term")}">{T2["term"]}</a><a href="{desde}{self.ruta("cook")}">{T2["cook"]}</a>'
               + (f'<button type="button" data-ck="abrir">{T2["pref"]}</button>' if self.usa()["cookies"] else ""))
        return (f'<footer><div class="wrap foot"><div class="brand">{e(self.m.get("nombre"))}</div><div class="cols">{"".join(cols)}</div>'
                f'<div class="c">© {date.today().year} {e(self.m.get("nombre"))}. {self.t["derechos"]}.</div><div class="leg">{leg}</div></div></footer>\n')

    def banner(self, desde=""):
        if not self.usa()["cookies"]: return ""
        T2 = self.t2
        return (f'<div class="ckb" id="ckb" role="dialog" aria-live="polite" aria-label="{T2["cook"]}"><p>{T2["banner"]} <a href="{desde}{self.ruta("cook")}">{T2["mas"]}</a></p>'
                f'<div class="r"><button type="button" class="btn s" data-ck="si">{T2["si"]}</button><button type="button" class="btn s" data-ck="no">{T2["no"]}</button></div></div>\n')

    # ---------- head con SEO/GEO/AEO ----------
    def jsonld(self, url, og_abs, desc):
        s = self.d.get("seo", {}); m = self.m; c = self.c
        tipo = s.get("tipo", "Person" if self.d.get("persona") else "ProfessionalService")
        org = {"@type": tipo, "@id": (url.rstrip("/") + "/#marca") if url else "#marca", "name": m.get("nombre"), "description": desc}
        if url: org["url"] = url
        if og_abs: org["image"] = og_abs
        if c.get("email"): org["email"] = c["email"]
        if c.get("telefono") or c.get("whatsapp"): org["telephone"] = c.get("telefono") or c.get("whatsapp")
        if c.get("ciudad") or c.get("direccion"):
            org["address"] = {"@type": "PostalAddress", **({"streetAddress": c["direccion"]} if c.get("direccion") else {}),
                              **({"addressLocality": c["ciudad"]} if c.get("ciudad") else {}), **({"addressCountry": self.L["pais"]} if self.L.get("pais") in ("CO", "US", "MX") else {})}
        if s.get("zona") or c.get("ciudad"): org["areaServed"] = s.get("zona") or c.get("ciudad")
        if tipo == "Person" and s.get("cargo"): org["jobTitle"] = s["cargo"]
        same = [f'https://instagram.com/{c["instagram"].lstrip("@")}'] if c.get("instagram") else []
        same += [c[k] for k in ("tiktok", "youtube", "linkedin") if c.get(k)]
        if same: org["sameAs"] = same
        ofertas = []
        for it in (self.d.get("servicios") or {}).get("items", []):
            o = {"@type": "Offer", "itemOffered": {"@type": "Service", "name": it.get("titulo"), "description": it.get("texto")}}
            ofertas.append(o)
        for it in (self.d.get("paquetes") or {}).get("items", []):
            ofertas.append({"@type": "Offer", "name": it.get("nombre"), "description": " · ".join(x for x in [it.get("texto"), it.get("precio")] if x)})
        if ofertas:
            key = "makesOffer"
            org[key] = ofertas
        graph = [org, {"@type": "WebSite", "name": m.get("nombre"), "inLanguage": self.lang, **({"url": url} if url else {}), "publisher": {"@id": org["@id"]}}]
        faq = self.d.get("faq"); items = (faq.get("items") if isinstance(faq, dict) else faq) or []
        if items:
            graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": x["p"], "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\*\*", "", x["r"])}} for x in items]})
        return {"@context": "https://schema.org", "@graph": graph}

    def cfg(self):
        return json.dumps({"posthog": self.ph_cfg, "form": self.form, "err": self.t["error"]}, ensure_ascii=False).replace("</", "<\\/")

    def head(self, titulo=None, descripcion=None, canon_path="", desde="", indexar=True, ld=True):
        s = self.d.get("seo", {}); m = self.m
        title = titulo or s.get("titulo") or m.get("nombre", "")
        desc = descripcion if descripcion is not None else s.get("descripcion", "")
        url = s.get("url", "").rstrip("/")
        canon = (url + "/" + canon_path) if url else ""
        og = self.img(s.get("imagen") or self.d.get("hero", {}).get("imagen"), 1200)
        og_abs = (og if og.startswith("http") else (url + "/" + og if url else "")) if og else ""
        acc = m.get("acento")
        vv = dict(self.var.get("vars", {}))
        if acc: vv["--accent"] = acc
        extra = (":root{" + ";".join(f"{k}:{v}" for k, v in vv.items()) + "}") if vv else ""
        if acc and self.d.get("acento_texto"): extra += f":root{{--accent-ink:{self.d['acento_texto']};}}"
        loc = LOCALE.get((self.lang, self.L.get("pais")), "es_CO" if self.lang == "es" else "en_US")
        theme = vv.get("--bg") or ("#0a0a0a" if self.fam == "noche" else "#ffffff")
        ver = f'<meta name="google-site-verification" content="{ea(s["google_verificacion"])}"/>' if s.get("google_verificacion") else ""
        ldj = json.dumps(self.jsonld(url, og_abs, desc), ensure_ascii=False).replace("</", "<\\/") if ld else ""
        va = '<script defer src="/_vercel/insights/script.js"></script>' if self.I.get("vercel_analytics") else ""
        return f"""<!DOCTYPE html>
<html lang="{self.lang}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{ea(title)}</title>
<meta name="description" content="{ea(desc)}"/>
{'' if indexar else '<meta name="robots" content="noindex"/>'}
{f'<link rel="canonical" href="{ea(canon)}"/>' if canon else ''}
{f'<link rel="alternate" hreflang="{self.lang}" href="{ea(canon)}"/><link rel="alternate" hreflang="x-default" href="{ea(canon)}"/>' if canon else ''}
<meta name="theme-color" content="{ea(theme)}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="{ea(m.get('nombre', ''))}"/>
<meta property="og:locale" content="{loc}"/>
<meta property="og:title" content="{ea(title)}"/>
<meta property="og:description" content="{ea(desc)}"/>
{f'<meta property="og:image" content="{ea(og_abs)}"/><meta property="og:image:alt" content="{ea(m.get("nombre", ""))}"/>' if og_abs else ''}
{f'<meta property="og:url" content="{ea(canon)}"/>' if canon else ''}
<meta name="twitter:card" content="summary_large_image"/>
{ver}
<link rel="icon" href="/favicon.svg" type="image/svg+xml"/>
{f'<script type="application/ld+json">{ldj}</script>' if ldj else ''}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{self.var["fuentes"]}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{desde}assets/site.css?v=3">
{f'<style>{extra}</style>' if extra else ''}
<script type="application/json" id="cfg">{self.cfg()}</script>
<script defer src="{desde}assets/app.js?v=3"></script>
{va}
</head>
<body class="fam-{self.fam} var-{self.var["id"]} hl-{self.est} sv-{self.svs} tq-{self.tqs}">
"""

    # ---------- subpáginas ----------
    def nav_simple(self, desde):
        return (f'<nav class="nav sc" id="nav"><div class="nav-in"><a href="{desde or "/"}" class="brand">{e(self.m.get("nombre"))}</a>'
                f'<a href="{desde or "/"}" class="btn s">{self.t2["volver"]}</a></div></nav>\n')

    def pagina_legal(self, clave):
        T2, desde = self.t2, "../"
        usa = self.usa()
        titulo = {"priv": T2["t_priv"], "term": T2["t_term"], "cook": T2["t_cook"]}[clave]
        tabla = ""
        if clave == "priv": secs = LG.privacidad(self.L, usa, self.lang)
        elif clave == "term": secs = LG.terminos(self.L, usa, self.lang)
        else:
            secs, filas = LG.cookies(self.L, usa, self.lang)
            if filas:
                th = "".join(f"<th>{x}</th>" for x in T2["tabla"])
                tabla = f"<table><thead><tr>{th}</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in f) + "</tr>" for f in filas) + "</tbody></table>"
        cuerpo = "".join(f"<h2>{e(h)}</h2>" + "".join(f"<p>{e(p)}</p>" for p in ps) for h, ps in secs)
        hoy = self.L.get("fecha") or date.today().isoformat()
        main = (f'<main class="legal"><h1 class="h">{e(titulo)}</h1><p class="act">{T2["act"]}: {e(hoy)}</p>{cuerpo}{tabla}'
                f'<a class="btn s" href="{desde}">{T2["volver"]}</a></main>\n')
        doc = self.head(titulo=f'{titulo} · {self.m.get("nombre", "")}', descripcion=f'{titulo} de {self.m.get("nombre", "")}.' if self.lang == "es" else f'{titulo} of {self.m.get("nombre", "")}.',
                        canon_path=self.ruta(clave), desde=desde, ld=False)
        doc += self.nav_simple(desde) + main + self.footer(desde) + self.banner(desde) + "</body>\n</html>\n"
        d = os.path.join(self.out, self.rutas[clave]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(re.sub(r"\n{2,}", "\n", doc))
        return doc

    def pagina_404(self):
        T2 = self.t2
        doc = self.head(titulo=f'404 · {self.m.get("nombre", "")}', descripcion="", desde="/", indexar=False, ld=False)
        doc += (f'<main class="n404"><div><h1 class="h">{dos(T2["n404"])}</h1><p>{T2["t404"]}</p><a class="btn p" href="/">{T2["volver"]} <span class="ar">→</span></a></div></main>'
                "</body>\n</html>\n")
        open(os.path.join(self.out, "404.html"), "w", encoding="utf-8").write(re.sub(r"\n{2,}", "\n", doc))

    # ---------- archivos de servidor ----------
    def csp(self):
        script = ["'self'"]; connect = ["'self'"]
        if self.form == "web3forms": connect.append("https://api.web3forms.com")
        if self.ph_cfg:
            h = self.ph_cfg["host"]; a = h.replace(".i.posthog.com", "-assets.i.posthog.com")
            script.append(a); connect += [h, a]
        img = ["'self'", "data:", "https:"]
        return "; ".join([
            "default-src 'self'", f"script-src {' '.join(script)}", "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com", f"img-src {' '.join(img)}", "media-src 'self' https:", f"connect-src {' '.join(connect)}",
            "frame-ancestors 'none'", "base-uri 'self'", "form-action 'self' https://api.web3forms.com", "object-src 'none'", "upgrade-insecure-requests"])

    def vercel_json(self):
        hdr = [{"key": "Content-Security-Policy", "value": self.csp()},
               {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
               {"key": "X-Content-Type-Options", "value": "nosniff"},
               {"key": "X-Frame-Options", "value": "DENY"},
               {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
               {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()"},
               {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"}]
        cfg = {"cleanUrls": True, "trailingSlash": True,
               "headers": [{"source": "/(.*)", "headers": hdr},
                           {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}]}
        open(os.path.join(self.out, "vercel.json"), "w").write(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")

    def llms_txt(self):
        s = self.d.get("seo", {}); m = self.m; c = self.c; h = self.d.get("hero", {})
        url = s.get("url", "").rstrip("/")
        limpiar = lambda x: re.sub(r"\*\*", "", str(x or ""))
        L = [f"# {m.get('nombre', '')}", "", f"> {limpiar(s.get('descripcion') or h.get('texto'))}", ""]
        tit = h.get("titulo"); tit = " ".join(tit) if isinstance(tit, list) else tit
        if tit: L += [limpiar(tit), ""]
        sv = (self.d.get("servicios") or {}).get("items", [])
        if sv:
            L += ["## Servicios" if self.lang == "es" else "## Services"] + [f"- **{limpiar(x.get('titulo'))}**: {limpiar(x.get('texto'))}" + (f" ({limpiar(x['precio'])})" if x.get("precio") else "") for x in sv] + [""]
        pk = (self.d.get("paquetes") or {}).get("items", [])
        if pk:
            L += ["## Precios" if self.lang == "es" else "## Pricing"] + [f"- **{limpiar(x.get('nombre'))}**: {limpiar(x.get('precio'))}{limpiar(x.get('periodo', ''))}. {limpiar(x.get('texto', ''))}" for x in pk] + [""]
        faq = self.d.get("faq"); items = (faq.get("items") if isinstance(faq, dict) else faq) or []
        if items:
            L += ["## Preguntas frecuentes" if self.lang == "es" else "## FAQ"]
            for x in items: L += [f"### {limpiar(x['p'])}", limpiar(x["r"]), ""]
        cont = [f"- WhatsApp: {c['whatsapp']}" if c.get("whatsapp") else "", f"- Email: {c['email']}" if c.get("email") else "",
                f"- Instagram: @{c['instagram'].lstrip('@')}" if c.get("instagram") else "", f"- Ciudad: {c['ciudad']}" if c.get("ciudad") else "",
                f"- Web: {url}/" if url else ""]
        L += ["## Contacto" if self.lang == "es" else "## Contact"] + [x for x in cont if x] + [""]
        if url:
            L += ["## Páginas" if self.lang == "es" else "## Pages", f"- [{self.t2['t_priv']}]({url}/{self.ruta('priv')})", f"- [{self.t2['t_term']}]({url}/{self.ruta('term')})", ""]
        open(os.path.join(self.out, "llms.txt"), "w", encoding="utf-8").write("\n".join(L))

    def robots_sitemap(self):
        url = self.d.get("seo", {}).get("url", "").rstrip("/")
        bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended"]
        r = "User-agent: *\nAllow: /\nDisallow: /api/\n\n# Buscadores de IA bienvenidos (GEO)\n" + "".join(f"User-agent: {b}\nAllow: /\n" for b in bots)
        if url: r += f"\nSitemap: {url}/sitemap.xml\n"
        open(os.path.join(self.out, "robots.txt"), "w").write(r)
        if url:
            hoy = date.today().isoformat()
            locs = [("", "1.0")] + [(self.ruta(k), "0.2") for k in ("priv", "term", "cook")]
            xs = "".join(f"<url><loc>{url}/{p}</loc><lastmod>{hoy}</lastmod><priority>{pr}</priority></url>" for p, pr in locs)
            open(os.path.join(self.out, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{xs}</urlset>\n')

    def servidor(self):
        if self.form != "propio": return
        os.makedirs(os.path.join(self.out, "api"), exist_ok=True)
        open(os.path.join(self.out, "api", "contacto.js"), "w").write(API_JS)
        # supabase.sql y LEEME van junto al json (no se publican)
        open(os.path.join(self.base, "supabase.sql"), "w").write(SQL)
        open(os.path.join(self.base, "LEEME-claves.txt"), "w").write(
            "Claves del formulario propio (nivel experto). Se pegan en Vercel → tu proyecto → Settings → Environment Variables.\n"
            "Nunca en sitio.json, nunca en el chat, nunca en git.\n\n"
            "RESEND_API_KEY        resend.com → API Keys (permiso: Sending access)\n"
            "CONTACTO_PARA         el correo donde quieres recibir los mensajes\n"
            "CONTACTO_DESDE        remitente de un dominio verificado en Resend, ej: Web <hola@tudominio.com>\n"
            "SUPABASE_URL          Supabase → Project Settings → API → Project URL        (opcional)\n"
            "SUPABASE_SERVICE_ROLE_KEY  Supabase → Project Settings → API → service_role (opcional, SOLO aquí)\n"
            "RESPUESTA_AUTOMATICA  texto del correo de confirmación al cliente             (opcional)\n\n"
            "Antes: corre supabase.sql en Supabase → SQL Editor.\n"
            "Después de pegar las claves: vuelve a publicar (vercel deploy) para que tomen efecto.\n")

    # ---------- auditoría ----------
    def auditar(self, doc):
        s = self.d.get("seo", {}); A, E = self.avisos, self.errores
        if "—" in doc: E.append("hay em dash (—) en el contenido")
        if not self.d.get("hero"): E.append("falta la sección hero")
        if self.d.get("_muestras"): A.append("MUESTRAS: todavía hay textos y fotos de ejemplo. Cámbialos por los de la persona y borra la línea \"_muestras\" de sitio.json; así no se puede publicar")
        t = s.get("titulo") or ""
        if not t: E.append("SEO: falta seo.titulo")
        elif not 25 <= len(t) <= 65: A.append(f"SEO: seo.titulo tiene {len(t)} caracteres (ideal 30 a 60)")
        dsc = s.get("descripcion") or ""
        if not dsc: E.append("SEO: falta seo.descripcion")
        elif not 70 <= len(dsc) <= 165: A.append(f"SEO: seo.descripcion tiene {len(dsc)} caracteres (ideal 70 a 160)")
        if not s.get("url"): A.append("SEO: sin seo.url no hay canonical, sitemap ni imagen para compartir. Ponla apenas haya dominio o link de Vercel.")
        if s.get("url") and not s["url"].startswith("https://"): E.append("SEO: seo.url debe empezar por https://")
        if not (s.get("imagen") or self.d.get("hero", {}).get("imagen")): A.append("SEO: sin imagen para compartir (seo.imagen); al mandar el link por WhatsApp no saldrá foto")
        faq = self.d.get("faq"); n = len((faq.get("items") if isinstance(faq, dict) else faq) or [])
        if n < 3: A.append(f"AEO: solo {n} preguntas frecuentes. Con 4 a 6 respuestas directas es más fácil que Google y los asistentes de IA citen la página.")
        if not (self.c.get("ciudad") or s.get("zona")): A.append("GEO: sin contacto.ciudad ni seo.zona; los buscadores no saben dónde atiendes")
        sin_alt = len(re.findall(r'<img src="[^"]+" alt=""', doc))
        if sin_alt: A.append(f"Accesibilidad: {sin_alt} imágenes sin texto alternativo")
        if not self.L.get("email"): E.append("Legal: falta un correo de contacto (legal.email o contacto.email); la política de privacidad lo exige")
        if not self.d.get("legal", {}).get("responsable"): A.append(f"Legal: legal.responsable no está; se usa '{self.L['responsable']}'. Si facturas como empresa, pon la razón social y el NIT/EIN en legal.id")
        if self.L.get("pais") == "EU": A.append("Legal UE: las fuentes se cargan desde Google; para cumplir al 100% con el RGPD conviene alojarlas en la propia página")
        if self.ph_cfg and "REEMPLAZAR" in self.ph_cfg["key"]: E.append("POSTHOG: falta la clave real. En PostHog: Settings > Project > Project API key (empieza por phc_). Va en integraciones.posthog.key")
        if self.ph_cfg and not self.ph_cfg["key"].startswith("phc_"): E.append("PostHog: la clave del proyecto debe empezar por phc_ (nunca pegues la personal phx_)")
        if self.form == "propio" and self.nivel == "principiante": A.append("Nivel: el formulario propio es de nivel experto; para principiante usa WhatsApp o Web3Forms")
        for k, v in (self.I or {}).items():
            if isinstance(v, dict) and any(re.match(r"(re_|sk_|eyJ|sbp_|phx_)", str(x)) for x in v.values()):
                E.append(f"SEGURIDAD: hay una clave secreta en integraciones.{k}. Bórrala de sitio.json y pégala solo en Vercel")

    # ---------- construir ----------
    def build(self):
        limpiar_salida(self.out)
        os.makedirs(os.path.join(self.out, "assets"), exist_ok=True)
        css = "\n".join(open(os.path.join(V1.FAM, f)).read() for f in ("base.css", "estructuras.css", f"{self.fam}.css")) + CSS_V2
        open(os.path.join(self.out, "assets/site.css"), "w").write(css)
        open(os.path.join(self.out, "assets/app.js"), "w").write(APP_JS)
        body = (self.nav() + self.hero() + self.marquesina() + self.sobre() + self.servicios() + self.proceso() + self.galeria()
                + self.testimonios() + self.paquetes() + self.faq() + self.cierre() + self.contacto() + self.footer() + self.banner())
        doc = self.head() + "<main>\n" + body.replace("<footer>", "</main>\n<footer>", 1) + "</body>\n</html>\n"
        doc = re.sub(r"\n{2,}", "\n", doc)
        open(os.path.join(self.out, "index.html"), "w", encoding="utf-8").write(doc)
        open(os.path.join(self.out, "favicon.svg"), "w").write(self.favicon())
        todo = doc + "".join(self.pagina_legal(k) for k in ("priv", "term", "cook"))
        self.pagina_404()
        self.vercel_json(); self.llms_txt(); self.robots_sitemap(); self.servidor(); huella(self.out)
        self.auditar(todo)
        u = self.usa()
        print(("OK " if not self.errores else "REVISAR ") + self.out)
        print(f"  nivel: {self.nivel} · formulario: {self.form} · analítica: {'PostHog' + (' con cookies + aviso' if u['cookies'] else ' sin cookies') if self.ph_cfg else ('Vercel' if u['vercel_analytics'] else 'ninguna')} · legal: {self.L['pais']}")
        for x in self.errores: print("  ERROR", x)
        for x in self.avisos: print("  aviso", x)
        return self.out


def limpiar_salida(out):
    """Vacía la carpeta de salida pero conserva .vercel (el enlace con el proyecto de Vercel).
    El respaldo va FUERA de out: antes quedaba adentro y rmtree se lo llevaba."""
    import shutil, tempfile
    os.makedirs(out, exist_ok=True)
    vc = os.path.join(out, ".vercel"); keep = None
    if os.path.exists(vc):
        keep = os.path.join(tempfile.mkdtemp(prefix="pw-vercel-"), ".vercel"); shutil.move(vc, keep)
    shutil.rmtree(out); os.makedirs(out)
    if keep: shutil.move(keep, vc); shutil.rmtree(os.path.dirname(keep), ignore_errors=True)


def huella(out):
    """Cambia ?v=3 por una huella del contenido en todas las páginas. Vercel guarda /assets un año
    (immutable), así que sin esto los visitantes seguirían viendo el CSS y el JS viejos tras un cambio."""
    import hashlib
    h = {f: hashlib.sha1(open(os.path.join(out, "assets", f), "rb").read()).hexdigest()[:10] for f in ("site.css", "app.js")}
    for raiz, _, archivos in os.walk(out):
        if ".vercel" in raiz: continue
        for a in archivos:
            if not a.endswith(".html"): continue
            p = os.path.join(raiz, a); t = open(p, encoding="utf-8").read()
            n = t.replace("assets/site.css?v=3", "assets/site.css?v=" + h["site.css"]).replace("assets/app.js?v=3", "assets/app.js?v=" + h["app.js"])
            if n != t: open(p, "w", encoding="utf-8").write(n)


if __name__ == "__main__":
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    Gen2(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None).build()
