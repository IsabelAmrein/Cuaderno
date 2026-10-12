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
| 7 | **Sin servicios de terceros** | Privacidad de lectores y control total | No hay analítica ni comentarios por defecto |
| 8 | **Animaciones** suaves con CSS y un script mínimo | Cuidado visual sin librerías | Se desactivan con `reducir movimiento` |
| 9 | Material de clase **solo como referencia** | Es confidencial y debe ser contenido original | Los artículos usan ejemplos propios y citan al profesor por su nombre |
| 10 | **Una versión, un zip** con limpieza de obsoletos y previsualización previa | Evitar archivos que ya no valen en cada commit | Proceso definido en `PUBLICAR.md` y en el agente Arquitecto |
| 11 | Equipo de **agentes** coordinados por el Arquitecto | Claridad, estimaciones y calidad repetible | Documentado en `agentes/` |
