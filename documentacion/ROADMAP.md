# Roadmap

> Estimaciones en [`agentes/subagentes`](agentes/subagentes). Se revisan en cada versión. El detalle de cada versión está en el [`CHANGELOG`](CHANGELOG.md).

## Hecho
- Sitio estático bilingüe con tema oscuro y modo claro, y publicado en GitHub Pages.
- Identidad visual y norma de ilustración semirrealista.
- Tipografías alojadas en el propio sitio.
- Página Sobre mí, RSS, sitemap, `hreflang` e imágenes sociales.
- Dos entradas: Machine Learning y Estrategia de datos.
- Animaciones suaves con reglas de movimiento y versión suave para `reducir movimiento`.
- Indicador "Pensando…" con el orbe *composing*.
- Arquitecto y nueve subagentes, con documentación, checklists y lecciones aprendidas.
- Auditor de proyectos públicos con su herramienta, cuatro informes e inventario de dependencias.
- Revisión del feedback externo (versión 1.3): portada con animación del ciclo completo, nombre Isabel Amrein, cabecera con iconos, miniaturas, ficha en Sobre mí, idioma, pantallas pequeñas, SEO y un nivel de calidad visual superior.
- Rediseño: nombre Isabel Amrein (antes Cuaderno de Isabel y Rumbo), portada con la montaña de banderas y orbes vivos en los proyectos en marcha.
- Proyectos y entradas separados, con los proyectos «Formación en Data Science e IA» y «Clasificador de reciclaje».
- Sobre mí aligerado: sin herramientas ni proyectos del trabajo (están en LinkedIn) y con el párrafo «Cómo trabajo». Artículo de bienvenida eliminado.

## En preparación (versión 1.4)
- Resultados del clasificador de reciclaje (M-01 y M-02).
- Foto para Sobre mí (M-15) y confirmación de los textos de la animación.

## Siguiente
| Id | Mini objetivo | Responsable | Estimación |
|---|---|---|---|
| M-01 | Montar el clasificador de reciclaje en Teachable Machine y recoger resultados | Isabel | 45 a 60 min |
| M-02 | Publicar los resultados en la página del proyecto Clasificador de reciclaje, en ES y EN | Redactor, Ilustrador, Calidad | 20 + 30 + 15 min |
| M-03 | Decidir si hay foto en Sobre mí e integrarla | Isabel, Maquetador, Guardián | 5 + 20 + 5 min |
| M-04 | Alta en Google Search Console y envío del sitemap | Isabel, SEO y LinkedIn | 15 + 10 min |
| M-05 | Automatizar `build.py` con GitHub Actions (el Auditor revisa antes cualquier acción de terceros) | Maquetador, Auditor | 45 a 60 + 15 min |
| M-06 | Script de pruebas de calidad: enlaces, texto alternativo, consola y `reducir movimiento` | Calidad | 60 a 90 min |
| M-07 | Dominio propio (opcional) | Isabel, SEO y LinkedIn | 20 + 10 min |
| M-08 | Leer los informes del Auditor y decidir qué skills de Emil Kowalski se instalan (ver [SKILLS.md](agentes/SKILLS.md)) | Isabel y Auditor | 20 a 30 min |
| M-15 | **Enviar una foto para Sobre mí:** buena luz, de frente, sin terceros ni datos al fondo. Se recorta, se reduce y se le quitan los metadatos de ubicación. Hay que dejarla en `content/img/isabel.jpg` | Isabel y Maquetador | 5 + 10 min |
| M-16 | Con el dominio: comprobar en Search Console qué páginas se indexan y que `robots.txt` y `llms.txt` quedan en la raíz | Isabel y SEO y LinkedIn | 20 min |
| M-09 | Revisión trimestral de todas las dependencias | Auditor | 30 min |
| M-10 | Probar el indicador "Pensando…" en una conexión lenta real | Isabel | 5 min |
| M-11 | **Al comprar el dominio:** poner `base_url` y `custom_domain` en `site.json`, regenerar (se crea el archivo `CNAME`), configurar los DNS en el registrador y activar HTTPS en GitHub Pages. El repositorio no se renombra | Isabel y Publicación | 20 a 30 min + espera de DNS |
| M-14 | Convertir el gráfico interactivo retirado de la portada en un experimento, "La recta que aprende" (el código está en el historial) | Maquetador | 30 a 45 min |

## Ciclo estándar de un artículo nuevo
| Paso | Responsable | Tiempo |
|---|---|---|
| Dictado | Isabel | 15 min |
| Borrador ES y EN | Redactor | 30 a 45 min |
| Verificación de datos | Investigador | 10 min |
| Cabecera y diagramas | Ilustrador | 45 a 90 min |
| Metadatos y LinkedIn | SEO y LinkedIn | 10 min |
| Privacidad | Guardián | 10 a 15 min |
| Calidad | Calidad | 20 a 30 min |
| Documentación | Arquitecto | 10 min |
| Zip y publicación | Publicación e Isabel | 15 a 25 min |

Total orientativo: **2,5 a 3,5 horas** repartidas entre varios pasos.
