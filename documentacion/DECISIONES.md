# Decisiones de arquitectura

Cada decisión indica qué se eligió, por qué y qué consecuencias tiene.

| Nº | Decisión | Motivo | Consecuencia |
|---|---|---|---|
| 1 | Sitio **estático** (HTML, CSS y JavaScript) generado con Python | Sin servidor, sin panel y gratis; Isabel pidió algo que no se modificara desde la página | Cada cambio requiere regenerar y subir los archivos |
| 2 | **GitHub Pages** desde la carpeta `docs` | Gratis y se puede migrar después a un hosting | `docs` es salida y no se edita a mano |
| 3 | **Bilingüe** con páginas separadas y `hreflang` | Mejor SEO y lectura en dos idiomas | Cada artículo existe en `es` y `en` con el mismo `id` |
| 4 | **Tema oscuro** neutro con **aguamarina** y modo claro opcional | Preferencia de Isabel: profesional pero cálido y sin azul | Los colores viven en variables CSS |
| 5 | Tipografías **Newsreader, Figtree y JetBrains Mono** alojadas en el sitio | Licencia libre, privacidad y rapidez | Archivos en `assets/fonts` con sus licencias |
| 6 | Ilustración **semirrealista** en SVG | Calidez sin pesar ni depender de terceros | Norma de estilo en `BRAND.md` |
| 7 | **Sin servicios de terceros** | Privacidad de lectores y control total | No hay analítica ni comentarios por defecto. Solo se admiten librerías de licencia libre alojadas en el propio sitio, con su licencia incluida |
| 8 | **Animaciones** suaves con CSS y un script mínimo, con las reglas de movimiento de `BRAND.md` | Cuidado visual sin librerías; duraciones cortas y curva decidida | Con `reducir movimiento` pasan a un desvanecimiento breve, no desaparecen |
| 9 | Material de clase **solo como referencia** | Es confidencial y debe ser contenido original | Los artículos usan ejemplos propios y citan al profesor por su nombre |
| 10 | **Una versión, un zip** con limpieza de obsoletos y previsualización previa | Evitar archivos que ya no valen en cada commit | Proceso definido en `PUBLICAR.md` y en el agente Arquitecto |
| 11 | Equipo de **agentes** coordinados por el Arquitecto | Claridad, estimaciones y calidad repetible | Documentado en `agentes/` |
| 12 | Indicador **"pensando"** con el motor de `thinking-orbs` (MIT), sin React, alojado en `assets/vendor` (15 KB) | Isabel quería que se viera "pensar" al cargar un artículo | Solo aparece si algo tarda más de 140 ms; respeta `reducir movimiento`; `?orbs` en la dirección lo muestra 4 s como demostración |
| 13 | Todo proyecto público (librería, fuente, imagen o *skill*) **pasa por el Auditor** antes de incorporarse | Evitar riesgos de licencia, seguridad y privacidad, y no depender de proyectos frágiles | Informe en `auditorias`, inventario en `DEPENDENCIAS.md` y aprobación de Isabel |
| 14 | La **documentación se actualiza antes de cada zip** | Isabel lo pidió: el repositorio debe contar lo que contiene | `CHANGELOG`, roadmap, decisiones y dependencias al día en cada versión |
| 15 | El sitio pasa a llamarse **Rumbo**, con el lema *Del dato al producto*, y la portada es una **montaña con banderas** (una por entrada), sin cuadrícula | Isabel quiere un sitio para volcar proyectos, no solo apuntes de la formación; el nombre antiguo y el gráfico de la portada no le convencían | Se retira el gráfico interactivo de la portada. El nombre del repositorio y la dirección web no cambian hasta decidirlo (M-11) |
| 16 | **Sobre mí breve**: sin lista de herramientas ni artículo de presentación | Duplicaban LinkedIn, envejecen rápido y el artículo sonaba poco profesional | El detalle de la trayectoria vive en LinkedIn y las herramientas se mostrarán en cada proyecto |
| 17 | Los **proyectos** tienen página propia, separada de las **entradas**. Todo lo de la formación es un proyecto («Formación en Data Science e IA») y el clasificador de reciclaje es otro, enlazados | Isabel quiere volcar proyectos y que lo construido no se mezcle con los apuntes | Menú Proyectos, Entradas y Sobre mí; la portada muestra proyectos; la web no usa «máster» para el programa actual |
| 18 | **Combinación** de la montaña y la lista con estado: la portada sigue con la montaña de banderas y los proyectos se listan con su estado, con un orbe vivo en los que están en marcha | Isabel quería mantener la montaña y la idea de «laboratorio abierto» con el orbe | El orbe pasa de indicador de carga a parte de la marca; se detiene con `reducir movimiento` |
| 19 | **Sobre mí sin «Algunos proyectos»** | Repetía LinkedIn, mencionaba datos del trabajo (objetivos, aplicación interna) y chocaba con el menú Proyectos | Los proyectos reales viven en su propia sección |
