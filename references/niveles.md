# Niveles

Nadie en ningún nivel escribe código. El nivel dice **cuánto entiende la persona de lo que pasa por debajo** y, por eso, cuántas cosas conectamos. Lo decides con la pregunta 0 de la entrevista y lo guardas en `sitio.json → "nivel"`. Si dudas, empieza en principiante: subir de nivel después es solo agregar campos y regenerar.

| | Principiante | Amateur | Experto (vibe coder) |
|---|---|---|---|
| Quién es | Nunca ha hecho una web | Ya usó Canva, Wix, Linktree o algo así | Ya usa Claude Code, Cursor o similar y no le asusta crear cuentas de servicios |
| Diseño | Yo recomiendo 2 o 3 | Escoge en el catálogo de las 14 plantillas | Escoge y puede ajustar colores, fuentes y estructura |
| Contacto | Botones a WhatsApp o correo | + formulario Web3Forms | + formulario propio: Resend (correo) + Supabase (guarda los leads) |
| Estadísticas | Vercel Web Analytics (opcional, sin cookies) | PostHog sin cookies | PostHog con eventos de embudo; cookies con aviso solo si las quiere |
| Dominio | Lo guío clic por clic | Lo guío | Lo conecta solo con la checklist |
| SEO/GEO/AEO | Base automática | Base + revisar avisos | Base + Search Console + llms.txt revisado |
| Legal y seguridad | **Automático en todos** | **Automático** | **Automático** |

Lo que **todas** las páginas tienen sin preguntar: privacidad, términos y cookies según el país, casilla de autorización en formularios, cabeceras de seguridad (`vercel.json`), página 404, `robots.txt` abierto a buscadores de IA, `sitemap.xml`, `llms.txt`, datos estructurados (negocio, servicios, preguntas frecuentes) y la auditoría al generar.

---

## Principiante · publicar de la mano

El objetivo es que salga de la conversación con su página en internet y entendiendo solo lo necesario. Una instrucción por mensaje, nunca tres.

1. **Cuenta de Vercel.** "Vamos a crear tu cuenta gratis donde vive tu página." Corre `vercel login`: se abre el navegador, la persona entra con su correo o Google (ella escribe, tú nunca). Si `vercel` no está instalado: `npm i -g vercel` (si no hay Node, instálalo con el instalador oficial de nodejs.org; dile qué va a ver).
2. **Vista previa para ella.** Muéstrale primero la local (`listo.py <carpeta> --ver`) con capturas de celular y escritorio. Ojo: el link de vista previa de Vercel (sin `--prod`) **viene protegido**, solo lo abre quien tenga sesión en esa cuenta. Sirve si la cuenta es de ella; si es tuya, no se lo mandes.
3. **Cambios.** Los pide en palabras normales. Tú editas `sitio.json` y corres `listo.py` otra vez. Nunca edites `web/` a mano.
4. **Publicar.** Con su "sí, publícala": `python3 motor/listo.py <carpeta> --prod`. Crea el proyecto con el nombre de la marca (o `"vercel_proyecto"` en sitio.json), elige solo el equipo de Vercel si hay uno, y se niega si quedan errores o fotos de muestra. Explícale que el link `nombre.vercel.app` ya es su página real y lo puede poner en la bio de Instagram hoy mismo. Nota: el primer deploy de un proyecto nuevo Vercel lo deja como producción aunque sea vista previa; por eso no se publica nada antes de su "sí".
5. **Pon la URL en `seo.url`** (la que imprime `listo.py`, o su dominio) y corre otra vez con `--prod`: así salen la imagen al compartir por WhatsApp, el sitemap y el canonical.
6. **Dominio (opcional).** Si ya tiene uno: Vercel → su proyecto → Settings → Domains → escribe el dominio → Vercel muestra 1 o 2 registros DNS → ella los copia en donde compró el dominio (GoDaddy, Namecheap, Hostinger…). Acompáñala con capturas si se pierde. Puede tardar de minutos a unas horas. Si no tiene dominio, no lo empujes: vercel.app funciona.
7. **Estadísticas sin cookies (opcional).** Vercel → proyecto → Analytics → Enable, y `"integraciones": {"vercel_analytics": true}`. No pide claves ni aviso de cookies.

Qué NO hacer en principiante: formularios propios, claves de servicios, explicar CSP o DNS más allá del paso a paso.

## Amateur · formulario y estadísticas

Todo lo del principiante, más:

- **Formulario por correo (Web3Forms).** Ella entra a web3forms.com, pone su correo y recibe una clave. La pega en el chat o en `contacto.web3forms_key`. Esta clave es pública por diseño (solo sirve para enviarle correos a ella), por eso puede ir en la página.
- **PostHog sin cookies.** Ella crea cuenta en posthog.com (US o EU Cloud; EU si sus clientes están en Europa), crea un proyecto y copia la **Project API Key** (empieza por `phc_`). Va en `integraciones.posthog.key` y `host` (`https://us.i.posthog.com` o `https://eu.i.posthog.com`). Sin cookies no hay aviso que aceptar: cuenta visitas, páginas y clics de WhatsApp, pero no reconoce a la misma persona entre días. Para un negocio pequeño es suficiente.
- Explícale en una línea qué mira en PostHog: Web analytics (visitas), y los eventos `click_whatsapp`, `click_boton`, `formulario_enviado`.

## Experto · conexiones propias

Para quien ya hace vibe coding. Igual sin escribir código: tú generas todo, ella crea las cuentas y pega las claves en Vercel.

- **Formulario propio** (`"integraciones": {"formulario": "propio"}`). El generador crea `web/api/contacto.js` (función de Vercel), `supabase.sql` y `LEEME-claves.txt` junto a `sitio.json`.
  - **Resend:** cuenta en resend.com → Domains → agrega su dominio y copia los registros DNS → API Keys → crea una con "Sending access".
  - **Supabase (opcional):** proyecto nuevo → SQL Editor → pega `supabase.sql` → Run. Copia Project URL y la clave `service_role` (Project Settings → API).
  - **Las claves se pegan en Vercel → Settings → Environment Variables**, nunca en `sitio.json`, nunca en el chat. Nombres exactos en `LEEME-claves.txt`. Después, `vercel deploy` de nuevo.
  - Si no quiere Supabase: `"supabase": false` en integraciones y solo llegan correos.
  - Prueba: enviar el formulario en la vista previa y confirmar que llega el correo y aparece la fila en Supabase → Table Editor → leads.
- **PostHog con embudo.** Los eventos ya salen solos. Arma con ella un Funnel en PostHog: `$pageview` → `click_boton` → `click_whatsapp` o `formulario_enviado`.
- **Cookies.** Solo si quiere reconocer visitantes recurrentes o hacer grabaciones: `"cookies": true`. Entonces aparece el aviso con Aceptar / Rechazar (los dos con el mismo peso) y el enlace "Preferencias de cookies" en el pie. Sin aceptación, PostHog sigue en modo sin cookies.
- **Search Console.** search.google.com/search-console → propiedad de prefijo de URL → método etiqueta HTML → el código va en `seo.google_verificacion`. Regenera, publica, verifica y envía `sitemap.xml`.
- **Revisa `llms.txt`** con ella: es el resumen que leen los asistentes de IA. Debe decir qué hace, dónde, precios si los muestra, y responder las preguntas frecuentes.

## Seguridad: qué hace cada cosa (para explicarla si preguntan)
- `vercel.json` manda cabeceras: CSP (la página solo carga scripts propios y de los servicios que usa), HSTS (siempre https), no se puede meter dentro de otra web (anti clickjacking), no se filtra la URL completa a otros sitios, sin acceso a cámara, micrófono ni ubicación.
- Todo el JavaScript está en `assets/app.js`, sin código en línea, por eso la CSP es estricta.
- Formularios: campo trampa invisible para bots, espera mínima antes de enviar, límites de largo, casilla de autorización obligatoria. La función propia además rechaza envíos desde otros dominios.
- Ninguna clave secreta vive en la página. La auditoría marca ERROR si ve una clave de Resend, Supabase o PostHog personal en `sitio.json`.
- Antes de publicar, `python3 motor/servir.py web` sirve la página con las mismas cabeceras: si algo se rompe por la CSP, lo verás en la consola.

## Legal: lo que hay que decir siempre
- Los textos son **plantillas razonables para negocios pequeños, no asesoría legal**. Dilo una vez al publicar.
- Si maneja datos de salud (psicólogas, médicos, odontólogos), pon `legal.datos_sensibles: true` y recomiéndale revisarlo con un abogado.
- Colombia: si la empresa tiene activos de más de 100.000 UVT, además debe inscribir sus bases de datos en el Registro Nacional de Bases de Datos de la SIC. Para independientes casi nunca aplica.
- UE: las fuentes vienen de Google; la auditoría lo avisa. Para RGPD estricto hay que alojarlas en la página.
