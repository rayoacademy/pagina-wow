---
name: pagina-wow
description: Crea y publica una página web completa con diseño nivel template premium (estilo Framer) para alguien que no sabe de diseño ni de código, solo con una entrevista corta. 14 plantillas firma, tres niveles (principiante, amateur, experto vibe coder), siempre con privacidad, términos, cookies, seguridad y SEO/GEO/AEO incluidos; opcional formulario, PostHog, Resend y Supabase. Úsala cuando alguien diga "hazme una página web", "quiero mi web", "necesito una landing para mi negocio", "una página para mi marca personal", "rediseña mi página", "mi web se ve fea", "publica mi página", "conéctale un formulario / PostHog", o pase un link de una página que le encanta para tener algo así.
---

# pagina-wow (v4)

Convierte una conversación de 5 minutos en una página web que se ve de agencia y que **queda publicada**. La persona no toca código en ningún nivel: responde preguntas, mira la vista previa, pide cambios y aprueba.

Todo se hace con tres comandos (rutas desde `~/.claude/skills/pagina-wow/`):

| paso | comando | qué hace |
|---|---|---|
| arrancar | `python3 motor/nueva.py <plantilla> <carpeta>` | copia el ejemplo y las fotos de muestra de la plantilla; `--lista` muestra las 14 |
| ver | `python3 motor/listo.py <carpeta> --ver` | genera, audita y abre la vista previa local (córrelo en segundo plano) |
| publicar | `python3 motor/listo.py <carpeta> --prod` | crea el proyecto en Vercel con el nombre de la marca y publica; se niega si hay errores o fotos de muestra |
| si algo falla | `python3 motor/listo.py <carpeta> --revisar` | diagnostica Python, Vercel, sesión, archivo, fotos, formulario y link publicado; dice qué hacer |

## Cómo hablarle a la persona
- Español simple, una instrucción por mensaje. Nada de "CSP", "deploy" o "JSON" en principiante: "la seguridad", "publicar", "el archivo de tu página".
- Muestra antes de explicar: una captura de celular vale más que un párrafo.
- Nunca le pidas que edite archivos. Ella dice qué quiere; tú cambias `sitio.json`.

## Niveles (decide con la pregunta 0 de la entrevista)
- **Principiante:** nunca ha hecho una web. La llevas de la mano hasta tenerla en internet. Botones a WhatsApp o correo.
- **Amateur:** ya usó Wix, Canva o similar. Escoge diseño en el catálogo; formulario Web3Forms y PostHog sin cookies.
- **Experto:** hace vibe coding. Formulario propio (Resend + Supabase), embudo en PostHog, dominio y Search Console.

Detalle, pasos de publicación por nivel y qué explicar: [references/niveles.md](references/niveles.md). Legal, seguridad y SEO/GEO/AEO salen **automáticos en los tres niveles**.

## Flujo (siempre en este orden)

1. **Entrevista.** [references/entrevista.md](references/entrevista.md): pregunta 0 (nivel) + dos tandas cortas, nunca una lista de diez. Incluye país y razón social para la parte legal, y **qué fotos tiene**. Si un dato ya se dio, no se vuelve a pedir.
2. **Recomienda una plantilla.** Con [references/plantillas.md](references/plantillas.md) escoge 2 o 3 de las 14 (tu favorita primero) según lo que siente el negocio **y las fotos que tiene**, una frase por cada una. Muestra el catálogo: `python3 motor/catalogo_v3.py <salida>` y `python3 motor/servir.py <salida> 4710` (en segundo plano). Si ninguna encaja, los 42 diseños por variables de [references/familias.md](references/familias.md) (sin `"plantilla"` en sitio.json). Con link de referencia: la plantilla más cercana, su lenguaje visual, nunca su código, textos ni imágenes.
3. **Arranca.** `python3 motor/nueva.py <id> <carpeta>`. Queda `sitio.json` con el contenido de ejemplo y `fotos/` con las muestras: la vista previa se ve completa desde el minuto uno.
4. **Escribe el contenido** en `sitio.json` según [references/esquema.md](references/esquema.md), desde lo que contó:
   - Nunca inventes cifras, testimonios, títulos ni clientes. Sin testimonios reales, se omite la sección.
   - Nada de em dashes (—). Titular de máximo 8 palabras en dos partes.
   - 4 a 6 preguntas frecuentes con respuesta directa en la primera frase (AEO).
   - `seo.titulo` marca · qué hace · dónde; `seo.descripcion` de 70 a 160 caracteres; `contacto.ciudad` o `seo.zona` (GEO).
   - Sus fotos van a `fotos/` (HEIC, PNG o JPG; el motor las comprime). Cuando no quede nada de ejemplo, borra la línea `"_muestras": true`.
5. **Genera y mira.** `python3 motor/listo.py <carpeta> --ver`. Lee lo que imprime: todo `ERROR` se corrige antes de mostrar; los `aviso` se resuelven o se le explican. Revisa escritorio (1440) y celular (390): portada completa, sin scroll horizontal, cero errores de consola (incluida CSP), imágenes cargan, `/privacidad/` `/terminos/` `/cookies/` abren, el formulario exige la casilla. Si cambiaste colores, mide contraste pegando `motor/contraste.js` en la consola (devuelve los textos bajo 4.5:1; los que van sobre foto se miran a ojo). No digas que está listo sin verlo.
6. **Itera.** Cambios en `sitio.json` y `listo.py` otra vez. No edites `web/` a mano: se sobrescribe (el enlace con Vercel en `web/.vercel` sí se conserva).
7. **Publica solo con su "sí" explícito.** `python3 motor/listo.py <carpeta> --prod`. Si la cuenta de Vercel tiene varios equipos, pide cuál y agrega `--equipo <nombre>`. Después pon la URL que imprime en `seo.url` y publica otra vez (canonical, sitemap, foto al compartir). Dominio: Vercel → Settings → Domains; el DNS lo cambia la persona.
8. **Cierra con la lista de lo que quedó** (link, qué conectamos, dónde ver las visitas) y dile una vez que los textos legales son plantillas, no asesoría legal.

## Lo que hay que saber de Vercel (probado el 26 oct 2026)
- El primer deploy de un proyecto nuevo queda como **producción** aunque no lleve `--prod`. Por eso no se publica nada antes del "sí".
- Los links de vista previa (sin `--prod`) **vienen protegidos**: solo abren con sesión en esa cuenta. Para que un cliente vea algo antes de publicar: capturas, la vista previa local, o apagar Settings → Deployment Protection.
- El link público es `https://<proyecto>.vercel.app`. CSS y JS van con huella de contenido, así que cada cambio publicado se ve de inmediato aunque Vercel los guarde un año en caché.

## Si algo falla (antes o después de publicar)
La persona puede volver días después con "no me llegan los mensajes" o "no se ve el cambio". Corre `listo.py <carpeta> --revisar`, busca el síntoma en [references/si-algo-falla.md](references/si-algo-falla.md), arréglalo tú y verifica antes de decir que quedó. A ella solo le pides lo que no puedes hacer tú (su login, copiar una clave de su correo, un registro DNS), de a una cosa.

## Reglas duras
- El login de Vercel, PostHog, Resend o Supabase lo hace la persona. Tú nunca escribes contraseñas.
- **Claves secretas** (Resend, Supabase `service_role`, PostHog personal `phx_`) solo en Vercel → Environment Variables. Nunca en `sitio.json`, en el chat ni en git. Las únicas claves que van en la página son públicas por diseño: Web3Forms y PostHog `phc_`.
- Sin cookies por defecto. El aviso de cookies aparece solo con `posthog.cookies: true`, con Aceptar y Rechazar del mismo tamaño y estilo.
- Si es salud: `legal.datos_sensibles: true` y recomienda revisión con abogado.
- Las fotos de `muestras/` son de Unsplash solo para el catálogo: nunca se publican en la página de un cliente (`listo.py` lo bloquea comparando los archivos).

## Fotos
- Lo mejor son fotos reales. Cada plantilla dice cuáles pide en su ficha (`references/plantillas.md`): sin las fotos correctas pierde la mitad del efecto.
- Sin fotos: Pulso Lanzamiento no necesita ninguna; Plano Estudio y Cartel Nombre aguantan con pocas. Avisa que con fotos sube mucho el nivel.
- Texto encima de foto: si la foto es muy clara y el texto no se lee, cambia la foto o súbele el velo en la plantilla; no lo dejes pasar.
- Nunca fotos de otras webs o templates. Para ambiente: bancos con licencia libre que la persona descarga.
- `seo.imagen` horizontal: es la que sale al compartir el link por WhatsApp.

## Archivos
- `motor/nueva.py`: arranca una carpeta desde una plantilla. `motor/listo.py`: genera, muestra y publica.
- `motor/generar_v3.py`: generador. Carga `plantillas/<id>/` y hereda de `generar_v2.py` lo legal, la seguridad, las integraciones, la auditoría y la huella de CSS/JS.
- `plantillas/<id>/`: las 14 plantillas (`ficha.json`, `ejemplo.json`, `muestras/`, `portada.jpg`, `plantilla.py`, `estilo.css`, `extra.js` opcional). Contrato en el docstring de `generar_v3.py`.
- `motor/nucleo.css`: lo funcional que comparten todas (formulario, legal, aviso de cookies, 404).
- `motor/catalogo_v3.py`: catálogo navegable de las 14. `motor/contraste.js`: medidor de contraste para la consola.
- `motor/servir.py`: vista previa local con las cabeceras de `vercel.json` y sin caché.
- `motor/legal.py`: privacidad, términos y cookies por país (CO, US, EU, OTRO), en español e inglés.
- `motor/generar_v2.py` + `familias/` + `motor/catalogo_v2.py`: los 42 diseños por variables (respaldo).
- `ejemplos/`: un `sitio.json` por familia (7), con niveles distintos.
- `references/historial/`: versiones anteriores de esta guía y de las referencias.
- Requisitos: Python 3. En Mac las fotos se comprimen con `sips`; en Windows/Linux hace falta `pip install pillow pillow-heif`. Para publicar: Node y `npm i -g vercel`.
