# Identidad visual: cuaderno de laboratorio

**Idea:** un cuaderno de datos. Fondo de papel milimetrado, tinta azul marino y un gráfico de puntos con su recta de regresión como símbolo. Cada artículo hereda la estructura y cambia su color de acento y su dibujo (generado a partir del identificador del artículo, por lo que es único y estable).

## Color
| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| papel `--paper` | #F1F3F6 | #0E1325 | Fondo |
| superficie `--surface` | #FFFFFF | #161C33 | Gráfico, código, filtros |
| tinta `--ink` | #161B33 | #E8EBF5 | Texto y puntos |
| tiza `--mute` | #576078 | #98A1BB | Texto secundario, fechas |
| línea `--line` | #D3D8E2 | #2A3250 | Reglas y bordes |

**Acentos por artículo** (campo `accent`): `cobalt` #2540D9, `magenta` #B8236B, `teal` #0B7A75, `amber` #9A5B05, `violet` #6A3DC4, `moss` #3F7D20. Cada uno tiene su variante clara para el modo oscuro.

## Tipografía (licencia libre, Google Fonts)
- **Bricolage Grotesque** 500/600/700: títulos, navegación y metadatos.
- **Source Serif 4** 400/600: texto de lectura. Línea de 66 caracteres, interlineado 1.7.
- **JetBrains Mono** 400: fechas, etiquetas y código.

Escala (×1.25): 14 / 18 / 22 / 28 / 36 px y un título de portada fluido de 34 a 62 px.

## Espaciado
- Base de 4 px; escala `--s1` a `--s8` = 4, 8, 12, 16, 24, 32, 48, 72 px.
- Letra: títulos con `letter-spacing` de −0.02 a −0.035 em (más cerrado cuanto mayor); texto de lectura y mono en 0.
- Palabra: `word-spacing` normal en todo el sitio. La legibilidad se controla con la longitud de línea y el interlineado.
- Secciones separadas por 48 px; párrafos por 24 px.

## Reglas
1. Un único elemento llamativo: el gráfico de la portada y el dibujo de cada artículo.
2. Sin mayúsculas en etiquetas, sin numeraciones decorativas, sin flechas en enlaces.
3. Los artículos son una lista fechada (como un registro), no una parrilla de tarjetas.
4. Movimiento solo como respuesta a una acción (tocar el gráfico). Respeta `prefers-reduced-motion`.
5. Accesible: foco visible, contraste AA, navegable con teclado, modo claro y oscuro.

## Voz
Primera persona, frases directas, ejemplos propios. Ningún material del máster se copia: se usa como referencia y se reconstruye con mini proyectos propios.
