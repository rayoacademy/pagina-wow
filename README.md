# pagina-wow

Una skill para Claude Code que te hace tu página web conversando. Te hace unas preguntas cortas sobre tu negocio, te muestra 2 o 3 diseños de 14 plantillas propias, arma la página con tus textos y fotos, te enseña cómo se ve en el celular y en el computador, y la deja publicada en internet cuando dices "sí, publícala".

No tienes que saber de diseño ni de código.

## Qué necesitas
- **Claude Code.** Viene en el plan Pro de Claude. Lo más fácil es usarlo desde la app de escritorio de Claude, en la pestaña Code.
- **Python 3.** En Mac ya viene instalado. En Windows o Linux, instala también `pip install pillow pillow-heif` (para comprimir las fotos, incluidas las HEIC del iPhone).
- **Para publicar:** Node (nodejs.org) y `npm i -g vercel`. La cuenta de Vercel es gratis y el `vercel login` lo haces tú.

## Cómo se instala
Abre Claude Code y pégale esto:

> Instala esta skill en ~/.claude/skills/: https://github.com/rayoacademy/pagina-wow

O a mano: copia la carpeta del repositorio dentro de `~/.claude/skills/pagina-wow` (en Windows: `C:\Users\<tu usuario>\.claude\skills\pagina-wow`).

## Cómo se usa
Escríbele a Claude algo como "quiero mi página web" o "hazme una landing para mi estudio de yoga". Lo demás lo guía la skill.

## Qué trae cada página
- 14 diseños propios en 7 estilos: Calma, Noche, Cartel, Plano, Pulso, Juego y Clínica.
- Política de privacidad, términos y aviso de cookies según el país, y casilla de autorización en el formulario.
- Cabeceras de seguridad, página 404, SEO para Google y preparación para buscadores de inteligencia artificial.
- Opcional: formulario (Web3Forms o propio con Resend y Supabase) y estadísticas sin cookies (PostHog o Vercel Analytics).

## Si algo falla
Pídele a Claude que corra `python3 motor/listo.py <carpeta> --revisar`. Revisa todo lo que suele fallar y dice qué hacer. La guía de problemas está en `references/si-algo-falla.md`.

## Avisos
- Los textos legales son plantillas, no asesoría legal. Si tu negocio maneja datos de salud o de menores, revísalos con un abogado.
- Las fotos de `plantillas/*/muestras/` son de [Unsplash](https://unsplash.com/license), con su fuente en cada `CREDITOS.txt`. Sirven para el catálogo y para arrancar; la skill no deja publicar una página que las siga usando.
- Las plantillas se inspiran en el lenguaje visual de plantillas premium, pero su código está escrito desde cero.

## Licencia
MIT. Úsala, cámbiala y compártela.
