# Familias y los 42 diseños

Destiladas de 34 templates top de Framer (análisis propio de sus composiciones; nada de su código ni sus imágenes). Reglas compartidas: titular grande y apretado (letter-spacing negativo), peso normal salvo Cartel/Juego, texto de 16 a 18 px, botones píldora, mucho aire, aparición al hacer scroll.

Cada diseño = familia (carácter) + estructura de portada + paleta y tipografías + estilo de secciones. Se elige con `"variante": "<id>"` en sitio.json. Catálogo visual: `motor/catalogo.py`.

## Estructuras de portada
- **centro**: foto a sangre, texto centrado claro encima.
- **marco**: foto enmarcada con esquinas grandes, texto abajo a la izquierda.
- **dividida**: texto a la izquierda, foto alta a la derecha.
- **editorial**: titular enorme alineado a la izquierda, foto panorámica debajo.
- **collage**: titular centrado y tres fotos escalonadas (usa `hero.imagenes` o la galería).
- **cartel**: nombre gigante de borde a borde encima de la foto en blanco y negro.

Con pocas fotos: dividida, editorial o centro (1 foto). Collage necesita 3. Sin fotos: editorial o dividida se ven mejor que centro.

## Estilos de sección
- servicios: `tarjetas` | `lista` | `mosaico` (el primero grande en color de acento).
- testimonios: `grilla` | `destacado` (el primero enorme).
Se pueden forzar con `estilo_servicios` / `estilo_testimonios` en sitio.json.

## Noche
| id | nombre | portada | servicios | ideal para |
|---|---|---|---|---|
| `noche-clasica` | Noche Clásica | centro | tarjetas | entrenadores, deportistas, consultores premium |
| `noche-dividida` | Noche Dividida | dividida | lista | coaches, asesores, servicios 1 a 1 |
| `noche-lujo` | Noche Lujo | centro | lista | joyería, inmobiliaria de lujo, eventos, restaurantes de autor |
| `noche-neon` | Noche Neón | centro | mosaico | deportes, gaming, tecnología, eventos nocturnos |
| `noche-editorial` | Noche Editorial | editorial | lista | fotógrafos, productoras, arquitectura, estudios creativos |
| `noche-medianoche` | Noche Medianoche | dividida | tarjetas | consultoría, finanzas, software, abogados |

## Calma
| id | nombre | portada | servicios | ideal para |
|---|---|---|---|---|
| `calma-clasica` | Calma Clásica | marco | tarjetas | psicólogas, terapeutas, bienestar |
| `calma-salvia` | Calma Salvia | marco | lista | yoga, nutrición, medicina natural, spa |
| `calma-rosa` | Calma Rosa | dividida | tarjetas | belleza, estética, uñas, maquillaje, moda |
| `calma-arena` | Calma Arena | editorial | lista | escritoras, arquitectas de interiores, cerámica, hoteles boutique |
| `calma-lavanda` | Calma Lavanda | collage | tarjetas | coaching de vida, maternidad, doulas, astrología |
| `calma-boda` | Calma Boda | centro | lista | bodas, eventos, fotografía de bodas, floristerías |

## Cartel
| id | nombre | portada | servicios | ideal para |
|---|---|---|---|---|
| `cartel-naranja` | Cartel Naranja | cartel | tarjetas | creadoras de contenido, coaches, speakers |
| `cartel-amarillo` | Cartel Amarillo | cartel | lista | diseñadores, músicos, DJs, marca personal con carácter |
| `cartel-rojo` | Cartel Rojo | cartel | mosaico | agencias de marketing, eventos, campañas, lanzamientos |
| `cartel-cobalto` | Cartel Cobalto | cartel | lista | freelancers, desarrolladores, consultores independientes |
| `cartel-condensado` | Cartel Condensado | cartel | tarjetas | deportistas, boxeo, fitness, barberías |
| `cartel-bosque` | Cartel Bosque | editorial | lista | marcas sostenibles, paisajismo, outdoor, cafés de origen |

## Plano
| id | nombre | portada | servicios | ideal para |
|---|---|---|---|---|
| `plano-blanco` | Plano Blanco | editorial | lista | arquitectos, estudios de diseño, consultoría seria |
| `plano-gris` | Plano Gris | dividida | tarjetas | agencias digitales, software, startups |
| `plano-arquitecto` | Plano Arquitecto | dividida | lista | arquitectura, construcción, ingeniería, interiorismo |
| `plano-tinta` | Plano Tinta | editorial | lista | abogados, escritores, editoriales, investigación |
| `plano-azul` | Plano Azul | collage | tarjetas | ingeniería, contadores, consultoras técnicas |
| `plano-negro` | Plano Negro | editorial | lista | desarrolladores, estudios de sonido, portafolios técnicos |

## Pulso
| id | nombre | portada | servicios | ideal para |
|---|---|---|---|---|
| `pulso-atardecer` | Pulso Atardecer | dividida | tarjetas | fitness, bienestar activo, cursos online |
| `pulso-aurora` | Pulso Aurora | collage | tarjetas | apps, lanzamientos, listas de espera, tecnología amable |
| `pulso-electrico` | Pulso Eléctrico | centro | mosaico | eventos, música, IA, comunidades online |
| `pulso-limon` | Pulso Limón | editorial | lista | marketing, agencias jóvenes, productos de salud, juguerías |
| `pulso-coral` | Pulso Coral | dividida | mosaico | academias, idiomas, cursos para niños, food trucks |
| `pulso-oceano` | Pulso Océano | centro | tarjetas | turismo, buceo, escuelas de surf, viajes |

## Juego
| id | nombre | portada | servicios | ideal para |
|---|---|---|---|---|
| `juego-cafe` | Juego Café | editorial | tarjetas | cafés, panaderías, heladerías, restaurantes de barrio |
| `juego-stickers` | Juego Stickers | collage | tarjetas | creadores de contenido, tiendas online jóvenes, ilustradores |
| `juego-retro` | Juego Retro | centro | lista | pizzerías, bares, barberías, tiendas vintage |
| `juego-pop` | Juego Pop | dividida | mosaico | eventos infantiles, jugueterías, snacks, fiestas |
| `juego-pixel` | Juego Pixel | centro | tarjetas | gaming, esports, tiendas de tecnología, streamers |
| `juego-dulce` | Juego Dulce | collage | tarjetas | pastelerías, tiendas de regalos, belleza divertida |

## Clínica
| id | nombre | portada | servicios | ideal para |
|---|---|---|---|---|
| `clinica-blanca` | Clínica Blanca | dividida | tarjetas | consultorios, fisioterapia, medicina general |
| `clinica-azul` | Clínica Azul | dividida | tarjetas | clínicas, laboratorios, seguros, salud digital |
| `clinica-menta` | Clínica Menta | collage | tarjetas | pediatría, veterinarias, nutrición, farmacias |
| `clinica-dental` | Clínica Dental | centro | mosaico | odontología, ortodoncia, estética dental |
| `clinica-calida` | Clínica Cálida | marco | lista | psiquiatría, medicina integrativa, fertilidad, geriatría |
| `clinica-legal` | Clínica Legal | editorial | lista | abogados, contadores, notarías, asesoría financiera |
