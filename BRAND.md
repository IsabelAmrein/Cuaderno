# Identidad visual: cuaderno de laboratorio, versión nocturna

**Idea:** un cuaderno de datos que se lee de noche. Fondo grafito con un punto cálido (sin azul), papel milimetrado muy tenue y un gráfico de puntos con su recta de regresión como símbolo. El aguamarina marca títulos, enlaces y detalles. Cada artículo hereda la estructura y puede cambiar su color de acento y su dibujo (generado a partir del identificador del artículo).

El modo oscuro es el principal. El botón "Tema" ofrece una versión clara en tonos lino.

## Color
| Token | Oscuro (principal) | Claro (lino) | Uso |
|---|---|---|---|
| fondo `--paper` | #151716 | #F3F1EA | Fondo |
| superficie `--surface` | #1E2220 | #FFFFFF | Gráfico, código, filtros |
| tinta `--ink` | #E9EDEA | #24302B | Texto y puntos |
| tiza `--mute` | #98A39E | #5C6862 | Texto secundario, fechas |
| línea `--line` | #2C3230 | #D9D5C7 | Reglas y bordes |
| cuadrícula `--grid` | #1F2422 | #E4E0D3 | Papel milimetrado de la portada |

**Acentos por artículo** (campo `accent`, oscuro / claro): `aqua` #6FE3C5 / #0B7A66 (por defecto), `sand` #D9B25F / #8F6A12, `coral` #F29277 / #B4492F, `violet` #B79BFF / #6A3DC4, `rose` #F08AB0 / #A8325F, `moss` #9BD774 / #3F7D20.

## Tipografía (licencia libre, Google Fonts)
- **Fraunces** 500/600: títulos y marca. Serif suave y cálida.
- **Figtree** 400/500/600: texto de lectura, navegación y metadatos.
- **JetBrains Mono** 400: fechas, etiquetas y código.

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
Primera persona, frases directas, ejemplos propios. Ningún material del máster se copia: se usa como referencia y se reconstruye con mini proyectos propios.
