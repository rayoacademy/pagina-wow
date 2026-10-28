# pagina-wow · cómo se instala

Una skill de Claude Code que entrevista a una persona, le arma una página web con diseño de agencia y la deja publicada en internet. Quien la usa no escribe código: conversa con Claude.

## Instalar (una vez)
1. Copia la carpeta `pagina-wow` dentro de `~/.claude/skills/` (en Windows: `C:\Users\<tu usuario>\.claude\skills\`).
2. Ten Python 3 (en Mac ya viene). En Windows o Linux, además: `pip install pillow pillow-heif` (para comprimir las fotos, incluidas las HEIC del iPhone).
3. Para publicar: instala Node desde nodejs.org y luego `npm i -g vercel`. La cuenta de Vercel es gratis; el `vercel login` lo haces tú.

## Usar
Abre Claude Code y escribe algo como: "quiero mi página web" o "hazme una landing para mi estudio de yoga". Claude te hace unas preguntas cortas, te muestra 2 o 3 diseños, arma la página con tus textos y fotos, te enseña cómo se ve en celular y computador, y la publica cuando digas "sí, publícala".

## Qué trae cada página
- 14 diseños propios en 7 estilos (Calma, Noche, Cartel, Plano, Pulso, Juego, Clínica).
- Privacidad, términos y cookies según tu país; casilla de autorización en el formulario.
- Seguridad (cabeceras), página 404, SEO para Google y para buscadores de IA.
- Opcional: formulario, estadísticas sin cookies (PostHog o Vercel), formulario propio con Resend y Supabase.

Los textos legales son plantillas, no asesoría legal. Las fotos de `plantillas/*/muestras/` son de Unsplash y solo sirven para el catálogo: la skill no deja publicarlas.
