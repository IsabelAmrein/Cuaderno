# Identidad visual de Isabel Amrein

**Nombre:** Isabel Amrein, en la cabecera; el nombre completo, Isabel Amrein De Luca, en la portada, Sobre mí, el pie y los datos estructurados. **Lema:** *Del dato al producto* (en inglés, *From data to product*). **Símbolo:** el monograma «IA» como favicon; la montaña con banderas ilustra la portada y los proyectos. Sustituye a los antiguos nombres «Cuaderno de Isabel» y «Rumbo». **Sin cuadrículas** de fondo en ningún sitio.

## Idea de la versión nocturna

**Idea:** un sitio para construir y mostrar proyectos. Fondo grafito con un punto cálido (sin azul), aguamarina para lo que se lee o se pulsa, ilustraciones semirrealistas y la montaña con banderas como símbolo. Cada artículo hereda la estructura y puede cambiar su color de acento y su cabecera.

El modo oscuro es el principal. El botón "Tema" ofrece una versión clara en tonos lino.

## Color
| Token | Oscuro (principal) | Claro (lino) | Uso |
|---|---|---|---|
| fondo `--paper` | #151716 | #F3F1EA | Fondo |
| superficie `--surface` | #1E2220 | #FFFFFF | Gráfico, código, filtros |
| tinta `--ink` | #E9EDEA | #24302B | Texto y puntos |
| tiza `--mute` | #98A39E | #5C6862 | Texto secundario, fechas |
| línea `--line` | #2C3230 | #D9D5C7 | Reglas y bordes |

**Acentos por artículo** (campo `accent`, oscuro / claro): `aqua` #6FE3C5 / #0B7A66 (por defecto), `sand` #D9B25F / #8F6A12, `coral` #F29277 / #B4492F, `violet` #B79BFF / #6A3DC4, `rose` #F08AB0 / #A8325F, `moss` #9BD774 / #3F7D20.

## Tipografía (licencia libre OFL, alojada en `assets/fonts`, sin servicios externos)
- **Newsreader** 500/600: títulos y marca. Serif de libro y revista, sobria y literaria.
- **Figtree** 400/500/600: texto de lectura, navegación y metadatos.
- **JetBrains Mono** 400: fechas, etiquetas y código.

Las licencias están en `assets/fonts/LICENSES.txt`. Para cambiar de fuente: copiar los archivos `.woff2` a `assets/fonts`, declararlos con `@font-face` al principio de `assets/style.css` y cambiar `--f-display` o `--f-body`.

Escala (×1.25): 14 / 18 / 22 / 28 / 36 px y un título de portada fluido de 34 a 59 px. Texto de lectura a 18 px con interlineado 1.7 y línea de 66 caracteres.

## Espaciado
- Base de 4 px; escala `--s1` a `--s8` = 4, 8, 12, 16, 24, 32, 48, 72 px.
- Letra: títulos con `letter-spacing` de −0.01 a −0.02 em; texto de lectura y mono en 0.
- Palabra: `word-spacing` normal en todo el sitio. La legibilidad se controla con la longitud de línea y el interlineado.
- Secciones separadas por 48 px; párrafos por 24 px.

## Reglas
1. Un único elemento llamativo: el gráfico de la portada y el dibujo de cada artículo.
2. Aguamarina para lo que se lee o se pulsa (títulos, enlaces, etiquetas). El resto, neutro.
3. Sin mayúsculas en etiquetas, sin numeraciones decorativas, sin flechas en enlaces.
4. Los artículos son una lista fechada (como un registro), no una parrilla de tarjetas.
5. Movimiento solo como respuesta a una acción (tocar el gráfico). Respeta `prefers-reduced-motion`.
6. Accesible: foco visible, contraste AA, navegable con teclado, modo oscuro y claro.

## Voz
Primera persona, frases directas, ejemplos propios. Ningún material de la formación se copia: se usa como referencia y se reconstruye con proyectos pequeños propios.

## Ilustraciones, fotos y gráficos (norma para todo lo que añadamos)
1. **Estilo semirrealista.** Todo gráfico, dibujo o imagen nuevo se hace con volumen: luz desde arriba a la izquierda, caras claras y oscuras, sombras bajo los objetos y detalles (brillos, pepitas, burbujas). Se construye con capas de formas y **degradados suaves** para la luz, con luz de borde y sombras de contacto. No se usan filtros de desenfoque ni imágenes de mapa de bits, para que siga siendo ligero y nítido en cualquier pantalla.
2. **Objetos con color propio, texto con el color del tema.** Los objetos y escenas (galleta, brújula, iceberg, montaña) llevan colores fijos y su propio fondo oscuro con esquinas redondeadas. Los textos y flechas de los diagramas usan los colores del tema, salvo dentro de una escena.
3. **Una cabecera por artículo**, sobre su idea central, recortada para llenar el marco (altura máxima 230 px). La misma ilustración se reutiliza, ya renderizada, en la imagen de LinkedIn.
4. **Dentro del texto**, los diagramas que expliquen una idea usan el mismo estilo (receta de galletas, montaña, iceberg, escalera con volumen).
5. **Fotos reales** (propias): sin caras de terceros ni niños, sin material confidencial ni datos internos de ninguna empresa, sin ubicación en los metadatos, optimizadas (menos de 200 KB) y con texto alternativo.
6. **Accesibilidad:** cada gráfico lleva descripción (`aria-label` o texto alternativo) y las ilustraciones decorativas se marcan como tales.

## Navegación y proyectos
- **Menú:** Proyectos, Entradas y Sobre mí. La portada muestra los proyectos como banderas de la montaña.
- **Estado de un proyecto**, como una etiqueta redonda: *en marcha* (contorno en el color de acento y un pequeño orbe en movimiento dentro), *terminado* (relleno) e *idea* (contorno punteado). El orbe es el mismo estado *composing* del indicador «Pensando…», a 20 px y en el color de acento de cada proyecto.
- **Cada proyecto** lleva su propia ilustración de cabecera y su color de acento (por ejemplo, verde para el reciclaje).
- **El programa actual de aprendizaje** se llama «Formación en Data Science e IA». No se usa la palabra «máster» para él.

## Portada y cabecera
- **Un vistazo basta:** la portada dice quién eres (nombre y cargo en mayúsculas pequeñas), qué haces (el lema y una frase en primera persona) y lo enseña con una animación de 26 s que cuenta **el ciclo completo**: *Trabajo con los datos*, *Los analizo*, *Creo modelos*, *Y modelos de Machine Learning*, *Gestiono el producto* y *Mido los resultados*, y vuelta a empezar. Cierra con la montaña de proyectos. Pocas palabras y nada que leer.
- **Cabecera:** el idioma se muestra con un globo y `ES ⇄ EN` (el idioma actual en el color de acento); el tema, con un icono de contraste. Todas las zonas táctiles miden al menos 44 px.
- **Miniaturas:** cada entrada y proyecto lleva su ilustración en formato 3:2 en las listas, además de la cabecera de su página, y una etiqueta de tipo (*Entrada* o *Proyecto*).

## Animaciones
- **Solo si ayudan a entender:** los títulos y párrafos aparecen suavemente al hacer scroll, las siete cajitas se construyen por partes y la aguja de la brújula se orienta hacia la meta.
- **Las ilustraciones del iceberg, la montaña y la receta de galletas se quedan quietas**, porque ya llevan mucha información.
- **Respetan `reducir movimiento` con una versión más suave, no con cero:** si el sistema lo pide, los textos y las cajitas aparecen con un desvanecimiento breve (200 ms), sin desplazarse, girar ni escalarse; la brújula se queda quieta ya orientada y el orbe muestra un fotograma fijo.
- **Ligeras:** CSS más un script mínimo.
- **Indicador "pensando":** un pequeño orbe en movimiento (el estado *composing*: una banda ondulante de puntos, de 32 px) en aguamarina junto al nombre del cuaderno, con el texto "Pensando…" o "Thinking…". Usa el motor de [thinking-orbs](https://github.com/Jakubantalik/thinking-orbs) (Jakub Antalik, licencia MIT), alojado en `assets/vendor`. Solo aparece si cargar o cambiar de página tarda más de 140 ms; no retrasa nada. Para verlo 4 segundos, añade `?orbs` a cualquier dirección.

### Reglas de movimiento
Basadas en la revisión de las skills de Emil Kowalski (ver `documentacion/auditorias`).
- Duraciones cortas: entre 150 y 250 ms para la interfaz. Solo se alarga con un motivo, como el giro decorativo de la brújula.
- Una curva decidida: `--ease-out: cubic-bezier(.23, 1, .32, 1)`. No la curva `ease` por defecto en lo deliberado.
- Solo se animan `transform` y `opacity`; nunca `width`, `height`, `margin` o `top`.
- Nada nace de escala 0: se empieza en 0,95 con transparencia.
- Escalonado entre elementos de 30 a 80 ms (usamos 60 ms).
- Nunca `transition: all`; se nombran las propiedades.
- `reducir movimiento` forma parte de la misma animación y da una versión suave, no cero.
- No se instala una librería de movimiento para lo que se resuelve con CSS.

### Nivel de calidad
- **Qué incluye una ilustración terminada:** luz principal arriba a la izquierda, un degradado en cada superficie, luz de borde, sombra de contacto bajo cada objeto y un detalle de ambiente (niebla, brillo, reflejo o estrellas).
- **Qué incluye una animación terminada:** un guion por escenas con continuidad (cada escena entra con un ligero zoom y sale hacia atrás), capas con profundidad, curvas de aceleración suaves y un detalle de cierre. Se juzga fotograma a fotograma y se renderiza a vídeo para verla como la verá el visitante.
- **Lo que no se hace:** fotografías ni vídeo real. Si se quiere un vídeo real, se aporta y se aloja en el propio sitio.
