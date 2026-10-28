# Esquema de sitio.json (v2)

Solo `variante` (o `familia`), `marca.nombre` y `hero` son obligatorios. Cada sección que falte simplemente no se dibuja. Las rutas de imagen son relativas al json (o absolutas, o URLs). En los textos, `**así**` se vuelve negrita.

Los titulares (`titulo`) van como lista de dos partes: `["Línea principal", "segunda línea en otro tono"]`. La segunda es opcional.

```jsonc
{
  "nivel": "principiante | amateur | experto",   // ver niveles.md (por defecto principiante)
  "variante": "calma-salvia",            // uno de los 42 ids de familias.md (o "familia" y se usa su primera variante)
  "estructura": "dividida",              // opcional: forzar otra portada
  "estilo_servicios": "lista", "estilo_testimonios": "destacado",  // opcionales
  "idioma": "es | en",
  "persona": true,                       // marca personal (schema Person) en vez de negocio
  "marca": {"nombre": "Lucía Ferrer", "inicial": "L", "acento": "#b5643f"},
  "acento_texto": "#ffffff",             // color del texto sobre el acento (si el acento es claro, usa oscuro)
  "seo": {"titulo": "…", "descripcion": "…", "url": "https://dominio.com", "imagen": "foto-og.jpg", "tipo": "ProfessionalService",
          "zona": "Laureles, Medellín",            // área que atiende (GEO)
          "cargo": "Psicóloga clínica",            // solo con persona: true
          "google_verificacion": "código de Search Console"},
  "legal": {"pais": "CO | US | EU | OTRO",       // por defecto CO en español, US en inglés
            "responsable": "Razón social o nombre", "id": "NIT 900… / EIN …", "email": "…", "direccion": "…",
            "datos_sensibles": false,              // true para salud: agrega el párrafo de datos sensibles
            "edad_minima": 18, "fecha": "2026-10-17"},  // opcionales
  "integraciones": {
    "formulario": "ninguno | web3forms | propio",  // por defecto web3forms si hay web3forms_key
    "supabase": true,                              // con propio: false = solo correo, sin guardar
    "posthog": {"key": "phc_…", "host": "https://us.i.posthog.com | https://eu.i.posthog.com", "cookies": false},
    "vercel_analytics": false
  },
  // NUNCA claves secretas aquí (Resend, Supabase service_role, PostHog personal phx_): van en Vercel.
  "contacto": {"whatsapp": "+57 300…", "whatsapp_mensaje": "Hola…", "email": "…", "instagram": "@…",
               "telefono": "…", "direccion": "…", "ciudad": "…", "mapa": "https://maps…",
               "tiktok": "url", "youtube": "url", "linkedin": "url", "web3forms_key": "…"},
  "nav_cta": "Agendar",                  // botón del menú (va al WhatsApp/correo)
  "hero": {"etiqueta": "Agenda abierta", "titulo": ["…", "…"], "texto": "…",
           "imagen": "portada.jpg", "video": "portada.mp4", "alt": "…",
           "cta": {"texto": "…", "href": "opcional"}, "cta2": {"texto": "…", "href": "#paquetes"},
           "datos": [{"t": "Años", "n": "9"}],          // barra de datos (2 a 6)
           "imagenes": ["a.jpg","b.jpg","c.jpg"],   // collage
           "nombre_grande": "Valentina Ríos", "foco": 38}, // foco: % vertical de la foto (cartel, centro, marco)
  "marquesina": ["Palabra", "Palabra"],
  "sobre": {"etiqueta": "Sobre mí", "titulo": ["…", "…"], "bajada": "…", "imagen": "…", "pie": "…",
            "texto": ["párrafo", "párrafo"], "cifras": [{"n": "12", "t": "años"}]},
  "servicios": {"titulo": [], "bajada": "", "con_imagen": false,
                "items": [{"titulo": "", "texto": "", "precio": "", "imagen": ""}]},
  "proceso": {"titulo": [], "bajada": "", "items": [{"titulo": "", "texto": ""}]},
  "galeria": {"titulo": [], "imagenes": ["a.jpg", "b.jpg"]},
  "testimonios": {"titulo": [], "items": [{"texto": "", "nombre": "", "rol": "", "foto": ""}]},
  "paquetes": {"titulo": [], "items": [{"nombre": "", "texto": "", "precio": "", "periodo": "/mes",
               "incluye": [""], "destacado": true, "cta": {"texto": "", "href": ""}}]},
  "faq": [{"p": "pregunta", "r": "respuesta"}],
  "cierre": {"etiqueta": "", "titulo": [], "texto": "", "cta": {"texto": ""}, "cta2": {}},
  "contacto_seccion": {"titulo": ["Hablemos", ""], "bajada": ""}
}
```

## Orden en la página
nav → portada → marquesina → sobre → servicios → proceso → galería → testimonios → paquetes → preguntas → cierre → contacto → pie.

## Botones
Sin `href`, todo botón principal abre WhatsApp con el mensaje (o el correo si no hay WhatsApp). Así la página ya convierte aunque la persona no tenga formulario.

## Lo que genera v2 además de index.html
- `privacidad/`, `terminos/`, `cookies/` (en inglés `privacy/`, `terms/`, `cookies/`), enlazadas en el pie.
- `404.html`, `vercel.json` (cabeceras de seguridad, URLs limpias, caché), `robots.txt` (abierto a buscadores de IA, cierra `/api/`), `sitemap.xml` (con `seo.url`), `llms.txt`.
- `assets/app.js`: todo el JS (menú, animaciones, formulario, PostHog, aviso de cookies, eventos). La configuración va en `<script type="application/json" id="cfg">`.
- Con `formulario: "propio"`: `web/api/contacto.js`, y junto al json `supabase.sql` y `LEEME-claves.txt` (no se publican).

## Eventos que envía a PostHog
`click_whatsapp`, `click_correo`, `click_telefono`, `click_boton` (con texto, zona y destino), `formulario_enviado` (con vía), `cookies_aceptadas`. Más `$pageview` y `$pageleave` automáticos.
