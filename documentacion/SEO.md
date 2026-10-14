# SEO y descubribilidad

Qué se ha hecho para que buscadores y modelos de lenguaje entiendan y encuentren este sitio, y cómo mantenerlo.

## Qué hay
| Elemento | Dónde | Detalle |
|---|---|---|
| Título de cada página | `<title>` | Hasta 60 caracteres, descriptivo y único. Se puede acortar con `seo_title` en la cabecera del archivo |
| Descripción | `<meta name="description">` | De 120 a 160 caracteres, única por página. Sale de `summary` |
| Encabezados | `h1` y `h2` | Un solo `h1` por página |
| Idiomas | `hreflang` y `x-default` | Cada página enlaza con su pareja en español e inglés |
| URL canónica y redes | `canonical`, Open Graph y Twitter | Con imagen social propia de cada página |
| Datos estructurados | JSON-LD | `ProfilePage` y `Person` en Sobre mí; `BlogPosting` y `CreativeWork` con `BreadcrumbList` en entradas y proyectos |
| Mapa del sitio | `sitemap.xml` | Con alternativas por idioma y fechas |
| Rastreo | `robots.txt` | Permite todo y apunta al mapa del sitio y a `llms.txt` |
| Para modelos de lenguaje | `llms.txt` y `llms-full.txt` | Resumen y texto completo del sitio, en español e inglés |
| Enlaces internos | En cada entrada y proyecto | «Sigue leyendo», «Otros proyectos», proyecto al que pertenece y caja de autoría con enlace a Sobre mí y a LinkedIn |

## Importante: la raíz del dominio
`robots.txt`, `sitemap.xml` y `llms.txt` deben estar en la **raíz** del dominio para que los lean los buscadores. Hoy el sitio vive en `isabelamrein.github.io/Cuaderno/`, que es una subcarpeta. Estos archivos cobrarán efecto completo cuando se compre el dominio (tarea M-11 del roadmap).

## Cómo mantenerlo
1. Cada entrada y proyecto lleva `summary` de 120 a 160 caracteres.
2. Si el título pasa de 60 caracteres con el nombre del sitio, se añade `seo_title`.
3. Toda entrada se une a un proyecto con `projects:` y enlaza con `{{project:id}}`.
4. Tras cada cambio de contenido se regeneran `sitemap.xml`, `llms.txt` y `llms-full.txt` (lo hace `build.py`).
5. Se comprueba con las herramientas del navegador (datos estructurados y vista previa en LinkedIn) y, con dominio propio, con Google Search Console.

## Lo que no se promete
Nadie puede garantizar posiciones en un buscador. Lo que sí se controla es que el sitio sea claro, rápido, accesible y esté bien descrito.
