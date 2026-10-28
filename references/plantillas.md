# Plantillas firma (v3)

Son la opción por defecto. Cada una tiene su propia composición (HTML y CSS propios), inspirada en una referencia concreta de Framer pero escrita desde cero. Los 42 diseños por variables (`familias.md`) quedan como respaldo para cuando ninguna plantilla encaje.

Se arrancan con `python3 motor/nueva.py <id> <carpeta>` y se generan con `python3 motor/listo.py <carpeta>`. Legal, seguridad, SEO e integraciones salen igual que en v2.

Cada carpeta `plantillas/<id>/` trae `ficha.json` (para quién, firma, fotos que pide), `ejemplo.json` (un sitio.json completo), `muestras/` (fotos de ejemplo de Unsplash con `CREDITOS.txt`, solo para el catálogo y el arranque: no se publican), `portada.jpg` (miniatura del catálogo), `plantilla.py`, `estilo.css` y a veces `extra.js`.

Para arrancar una página: `python3 motor/nueva.py <id> <carpeta>` (copia el ejemplo y las muestras). Contraste medido en las 14 el 26 oct 2026 con `motor/contraste.js`.

## Cómo escoger
- Primero por lo que siente el negocio (columna «se siente»), después por las fotos que tiene la persona: cada plantilla pide fotos distintas y **sin las fotos correctas pierde la mitad del efecto**.
- Recomienda 2 o 3 (tu favorita primero) y muestra el catálogo: `python3 motor/catalogo_v3.py <salida>` y abre `<salida>/index.html` con `python3 motor/servir.py <salida>`.
- Si la persona no tiene fotos: Pulso Lanzamiento no necesita ninguna; Plano Estudio y Cartel Nombre aguantan con pocas (blanco y negro).

## Calma

| id | se siente | para | fotos que pide |
|---|---|---|---|
| `calma-arco` | estudio de bienestar cálido: crema y salvia, serif clásica con itálica, curvas suaves | yoga, pilates, spa, terapeutas, nutrición, medicina integrativa, retiros | portada: horizontal, luz cálida, personas en movimiento; sobre.imagen: el espacio, horizontal; servicios[].imagen: verticales, una por servicio (3 o 4); galeria: 3 fotos para el bloque editorial; testimonios[].foto: opcional |
| `calma-intima` | consulta íntima y editorial: crema, negro cálido, sans media con itálica serif, mucho aire | psicólogas, terapeutas, coaches 1 a 1, psiquiatría, acompañamiento de duelo, sexología | portada: horizontal cálida, personas cercanas (luz de tarde); sobre.imagen: horizontal, la consulta o la persona; sobre.imagen_chica: retrato vertical; servicios.imagen: vertical con luz y sombra; pausa.imagen: horizontal tranquila, un espacio; galeria: 3 fotos de objetos o espacios |

## Noche

| id | se siente | para | fotos que pide |
|---|---|---|---|
| `noche-consultor` | consultoría premium nocturna: negro profundo, vidrio, brillos suaves, titular con degradado | consultores, coaches de negocio, mentores, agencias B2B, abogados corporativos, asesores financieros | portada: retrato o escena oscura horizontal (o hero.video); sobre.imagen: vertical, alguien trabajando; contacto_seccion.imagen: retrato vertical sonriendo; galeria: 2 fotos de talleres o trabajo; testimonios[].foto: avatares |
| `noche-entreno` | gimnasio premium de noche: negro, grises, titulares finos en dos tonos, fotos con contraste | entrenadores personales, gimnasios boutique, boxeo, nutrición deportiva, fisioterapia deportiva, academias de deporte | portada: horizontal oscura, grupo o silueta; galeria: 4 fotos verticales (coach, comida, seguimiento, acompañamiento); servicios[].imagen: 4 verticales de entrenamiento; sobre.imagenes: 2 fotos para el mosaico; testimonios[].foto: una por resultado; cierre.imagen: horizontal oscura |

## Cartel

| id | se siente | para | fotos que pide |
|---|---|---|---|
| `cartel-agencia` | agencia con actitud: crema y rojo, palabra gigante condensada, bloques de color fuertes | agencias de marketing, estudios de diseño, productoras, agencias de eventos, equipos de lanzamiento | portada: retrato con luz de color o escena con carácter; servicios[0].imagen: producto o trabajo destacado; galeria: casos de éxito (1 foto por caso); testimonios.imagen: foto central oscura; sobre.imagen: equipo trabajando |
| `cartel-nombre` | portafolio de marca personal con carácter: blanco y negro, amarillo eléctrico, nombre gigante | creadoras de contenido, diseñadores, fotógrafos, speakers, consultores independientes, artistas, DJs | portada: retrato frontal (se pasa a blanco y negro); galeria: 4 trabajos o proyectos, horizontales; sobre.imagen: retrato vertical; servicios.imagen: textura o patrón oscuro (opcional) |

## Plano

| id | se siente | para | fotos que pide |
|---|---|---|---|
| `plano-color` | estudio creativo: blanco puro, mayúsculas con símbolos, el color lo ponen las fotos | estudios de diseño, agencias creativas, fotógrafos de producto, marcas de moda, estudios 3D, productoras | hero.imagenes: 5 fotos de color (3 arriba, 2 abajo); sobre.imagen: foto del equipo; galeria: 2 fotos grandes; cierre.imagenes: 3 fotos para la fila final |
| `plano-estudio` | estudio técnico y sereno: gris claro, monoespaciada para etiquetas, fotos en blanco y negro, mucha retícula | arquitectura, interiorismo, ingeniería, construcción, estudios de diseño, abogados, consultoras técnicas | portada: horizontal clara (arquitectura, espacio); sobre.imagen: retrato en blanco y negro de quien dirige; galeria: 4 obras o proyectos; servicios[].imagen: miniaturas (opcional); testimonios[].foto: retrato; cierre.imagenes: 5 fotos para la tira |

## Pulso

| id | se siente | para | fotos que pide |
|---|---|---|---|
| `pulso-energia` | fitness y bienestar activo con energía: duotono rosa a azul, degradados pastel, titulares enormes | fitness, entrenamiento online, nutrición, apps de bienestar, academias de baile, cursos online | portada: retrato sobre fondo liso (se pasa a duotono); equipo: 1 a 4 retratos verticales; servicios[].imagen: objeto o detalle de cada programa; pausa.imagen: foto horizontal de acción; testimonios[].foto: retratos |
| `pulso-lanzamiento` | lista de espera luminosa: aurora de turquesa, verde y azul, estrella de cuatro puntas, una sola acción | lanzamientos, listas de espera, apps nuevas, cursos por abrir, preventas, eventos | ninguna: no necesita fotos; la aurora es CSS |

## Juego

| id | se siente | para | fotos que pide |
|---|---|---|---|
| `juego-cafe` | café de barrio con humor: café oscuro, crema mantequilla, marca en letra burbuja, todo en minúscula | cafés, panaderías, heladerías, restaurantes de barrio, bares, food trucks, tiendas de postres | portada: foto con actitud (persona con el producto); mosaico: 4 a 6 fotos de gente y producto (campo mosaico); carta.imagen: el local; tienda.imagen: producto para vender (opcional) |
| `juego-stickers` | portafolio juguetón con guiños de Figma: lienzo blanco, cajas de selección, notas adhesivas, colores primarios y letra pixelada | diseñadores UX/UI, ilustradores, creadores de contenido, estudios pequeños, desarrolladores freelance, tiendas jóvenes | sobre.imagenes: 2 polaroids (tú y tu espacio); sobre.avatar: retrato pequeño; galeria: 1 foto por proyecto (3 o 4) |

## Clínica

| id | se siente | para | fotos que pide |
|---|---|---|---|
| `clinica-confianza` | servicio profesional sereno y serio: blanco roto, negro, sans ligera, fotos de personas reales | centros médicos, consultorios, abogados, contadores, notarías, aseguradoras, consultoras | portada: horizontal con personas atendiendo; sobre.imagen: detalle pequeño para la píldora; pausa.imagen: foto grande del equipo o del servicio; proceso.imagen: vertical o cuadrada; equipo.items[].foto: retratos verticales; cierre.imagen: espacio oscuro |
| `clinica-estetica` | clínica cálida y confiable: crema y café suave, serif amable, tarjetas redondeadas, vidrio sobre fotos | dermatología, estética, odontología estética, spas médicos, fisioterapia, nutrición clínica, pediatría | portada: horizontal cálida de piel o del espacio; galeria: 4 fotos (tratamientos y pacientes); sobre.imagen: retrato del profesional; bento.imagen: foto vertical; proceso.imagen: atención en consulta; testimonios.imagen: retrato vertical; cierre.imagen: detalle de producto o manos |

## Campos propios de algunas plantillas
Además del esquema común (`esquema.md`), algunas plantillas leen campos extra. Mira su `ejemplo.json`:
- **En casi todas** (revísalos siempre, son los que más se olvidan):
  - `marca.lema`: frase corta que sale en el pie de página (calma-arco, clinica-confianza, noche-consultor, noche-entreno, plano-color, plano-estudio, pulso-energia). Si no hay una frase real del negocio, bórrala.
  - `menu_nombres`: cómo se llaman las secciones en el menú (todas menos juego-cafe y pulso-lanzamiento). Ajústalos al negocio: "Estudio" o "Programas" no sirven para un abogado o una fisio.
  - `hero.etiqueta` y cualquier `cifras`/`datos`: son promesas y números. Si no son de la persona, se borran (nunca se dejan los del ejemplo).
- El motor avisa con `EJEMPLO:` si un texto del ejemplo quedó igual, y `listo.py` no publica hasta resolverlo. Si la persona quiere conservar una frase que coincide, va en `"_textos_ok": ["la frase"]`.
- `juego-cafe` pone todo en minúscula (marca, preguntas, precios): avísale a la persona antes de escogerla.
- `plano-estudio`: `servicios.cta_etiqueta` cambia el "¿Hablamos?" junto al botón.
- `calma-arco`: `sobre.titulo_imagen`, `menu_nombres`.
- `calma-intima`: `sobre.imagen_chica`, `sobre.cta`, `servicios.imagen`, `pausa {imagen, texto}`, `contacto_seccion.puntos`.
- `noche-entreno`: `sobre.imagenes` (mosaico), `testimonios[].datos` (cifras por resultado), `cierre.imagen`.
- `noche-consultor`: `sobre.puntos`, `contacto_seccion.imagen`, `cierre.puntos`, `hero.datos` (prueba social).
- `cartel-nombre`: `hero.nombre_grande`, `galeria.ver_todo`, `cierre.grande`.
- `cartel-agencia`: `hero.etiqueta2`, `hero.chips`, `clientes`, `sobre.puntos`, `servicios.items[].tipo/cifra/chips`, `galeria.imagenes[].cliente/servicios`, `testimonios.imagen`, `testimonios.items[].destacado`.
- `plano-estudio`: `hero.lista`, `hero.lugares`, `sobre.firma`, `sobre.cifras[].e`, `galeria.datos`, `galeria.imagenes[].nombre`, `clientes`, `cierre.imagenes` (5).
- `plano-color`: `hero.frase` (partes que alternan oscuro y gris), `hero.imagenes` (5), `marca.dominio`, `servicios.texto`, `cierre.imagenes` (3).
- `pulso-energia`: `equipo {palabra, items, cifras}`, `pausa`, `faq_titulo`, `faq_bajada`, `testimonios.palabra`.
- `pulso-lanzamiento`: `hero.fecha` (cuenta regresiva ISO), `hero.gracias`. Sin menú: una sola acción.
- `juego-cafe`: `mosaico` (paneles y fotos), `carta`, `carta_imagen`, `tienda`, `hero.info`.
- `juego-stickers`: `hero.notas`, `hero.cursores`, `sobre.avatar`, `sobre.imagenes` (2 polaroids). Los testimonios salen como comentario de Figma.
- `clinica-estetica`: `hero.arco`, `sobre.iconos`, `sobre.firma`, `sobre.puntos`, `bento`, `proceso.imagen`, `testimonios.imagen`.
- `clinica-confianza`: `sobre.pildora_tras`, `sobre.prueba`, `equipo`, `pausa`.

## Fotos de muestra
Las del catálogo son de Unsplash (licencia libre) y su fuente está en `plantillas/<id>/muestras/CREDITOS.txt`. Son solo para mostrar: la página final de una persona usa **sus** fotos.
