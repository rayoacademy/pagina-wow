# Si algo falla

Primero corre `python3 motor/listo.py <carpeta> --revisar`: revisa Python, Vercel, la sesión, el archivo de la página, las fotos, el formulario y si el link publicado responde, y dice qué hacer en cada caso. Después busca el síntoma aquí. A la persona le hablas en simple: qué pasó, qué vas a hacer tú y, si hace falta, una sola cosa que haga ella.

## Al generar
| síntoma | causa | qué hacer |
|---|---|---|
| "sitio.json tiene un error de escritura cerca de la línea N" | una coma de más o una comilla sin cerrar | arréglalo tú en esa línea; nunca le pidas a la persona que edite el archivo |
| `FOTO: no existe ...` | el nombre en sitio.json no coincide con el archivo (mayúsculas, extensión .HEIC/.jpg) | `ls <carpeta>/fotos` y corrige el nombre |
| `EJEMPLO: quedan textos...` | quedó una frase, cifra o promesa del negocio de ejemplo | cámbiala por la real o bórrala; si es a propósito, `"_textos_ok"` |
| `MUESTRAS` | todavía están las fotos o textos de la plantilla | pon lo de la persona y borra `"_muestras"` |
| "no pude comprimir" (Windows/Linux) | falta Pillow | `pip install pillow pillow-heif` |
| una foto del iPhone (HEIC) no sale en Windows | falta pillow-heif | lo mismo; o que la mande como JPG |

## Al ver la vista previa
| síntoma | causa | qué hacer |
|---|---|---|
| cambié algo y no se ve | el navegador guardó la versión anterior | recarga con Cmd/Ctrl + Shift + R (la vista local ya no guarda caché, así que casi nunca pasa) |
| errores rojos de "Content Security Policy" en la consola | un script, fuente o imagen de un dominio no permitido | no lo permitas a mano: usa las integraciones del motor, que agregan su dominio a la CSP |
| el texto encima de la foto no se lee | la foto de la persona es muy clara | cambia la foto o sube el velo de esa plantilla |
| el puerto está ocupado | otra vista previa sigue abierta | `listo.py` busca uno libre solo; si no, ciérrala |

## Al publicar
| síntoma | causa | qué hacer |
|---|---|---|
| "Falta Vercel" | no está instalado | Node desde nodejs.org y `npm i -g vercel` |
| "no hay sesión" / pide login | la persona no ha entrado | ella corre `vercel login` y entra con su correo o Google (tú nunca escribes la contraseña) |
| "varios equipos" | la cuenta de Vercel tiene más de un equipo | pregúntale cuál y repite con `--equipo <nombre>` |
| el link que le mandé pide iniciar sesión | era un link de vista previa (vienen protegidos) | mándale el público `https://<proyecto>.vercel.app` (sale con `--prod`) o apaga Settings > Deployment Protection |
| "No publico: ..." | quedan errores, muestras, textos del ejemplo o fotos que no existen | resuelve lo que dice; el freno está para no publicar algo ajeno |
| publiqué y el cambio no aparece | caché del navegador del visitante | espera un minuto y recarga; CSS y JS llevan huella, así que el cambio llega solo |
| al compartir por WhatsApp no sale foto | falta `seo.url` o `seo.imagen` | pon la URL final en `seo.url`, una foto horizontal en `seo.imagen` y publica otra vez |

## Formulario
| síntoma | causa | qué hacer |
|---|---|---|
| sale "No se pudo enviar" | clave de Web3Forms mal copiada, o falta | que copie de nuevo la clave del correo de web3forms.com (36 caracteres) |
| se envía pero no llega el correo | Web3Forms la manda al correo con que se registró; puede estar en spam | revisar spam y marcar "no es spam"; confirmar que el correo de registro es el correcto |
| formulario propio: error 500 | faltan variables en Vercel o están mal escritas | revisa los nombres exactos en `LEEME-claves.txt`, pégalos en Vercel > Settings > Environment Variables y publica otra vez |
| formulario propio: llega el correo pero no se guarda | no se corrió `supabase.sql` o la clave no es la `service_role` | correr el SQL en Supabase > SQL Editor y revisar la variable |
| Resend no envía | dominio sin verificar en Resend | verificar el dominio en Resend o usar su remitente de prueba mientras tanto |

## Estadísticas y dominio
| síntoma | causa | qué hacer |
|---|---|---|
| PostHog no muestra visitas | la clave sigue en `phc_REEMPLAZAR`, o la persona rechazó cookies | poner la clave del proyecto; sin cookies igual cuenta visitas, solo no reconoce a la misma persona entre días |
| el dominio no abre | el DNS todavía se está propagando o los registros quedaron mal | revisar en Vercel > Domains qué registro pide y compararlo con lo que puso donde compró el dominio; puede tardar horas |

## Si nada de esto aplica
Lee el error completo, reprodúcelo con `listo.py`, arregla en `sitio.json` o en la plantilla (nunca en `web/`), verifica en la vista previa y cuéntale a la persona en una línea qué pasó y qué quedó. Si el problema está en la skill misma, anótalo en el HANDOFF para corregirlo.
