# Rumbo

*Del dato al producto.* Sitio personal estático y bilingüe (español e inglés) de Isabel Amrein De Luca con proyectos y apuntes sobre datos, IA generativa y producto. Se genera con Python y se publica gratis en GitHub Pages.

> Antes se llamaba «Cuaderno de Isabel». El repositorio y la dirección web siguen llamándose `Cuaderno` hasta que se decida si se cambian (ver el roadmap).

- **Web:** https://isabelamrein.github.io/Cuaderno/
- **Documentación completa:** [`documentacion/`](documentacion/README.md)
- **Equipo de agentes (Arquitecto y subagentes):** [`documentacion/agentes`](documentacion/agentes/ARQUITECTO.md)

## Estructura
| Carpeta o archivo | Qué es |
|---|---|
| `content/` | Artículos, Sobre mí, componentes y arte |
| `assets/` | Estilos, scripts, favicon y tipografías |
| `herramientas/` | Generadores de diagramas e ilustraciones y la herramienta del Auditor |
| `build.py` | Genera el sitio |
| `site.json` | Configuración del sitio |
| `docs/` | **Salida**: lo que publica GitHub Pages. No se edita a mano |
| `linkedin/` | Borradores de publicaciones |
| `documentacion/` | Arquitectura, decisiones, agentes y roadmap |
| `BRAND.md` | Identidad visual y norma de ilustración |

## Generar el sitio
```
pip install markdown pillow
python3 build.py
```

## Un artículo nuevo
Crea dos archivos Markdown con el mismo `id`, uno en `content/es/posts/` y otro en `content/en/posts/`.

```
---
id: mi-articulo
title: Título
date: 2026-11-02
accent: aqua             # aqua, sand, coral, violet, rose, moss
hero: compass            # cabecera de content/art (opcional)
quote: Frase breve       # sale bajo el título en la imagen de LinkedIn (opcional)
teacher: Nombre Apellido # crédito de la clase (opcional)
tags: [python, pandas]
summary: Resumen de una o dos frases.
linkedin: Gancho para el post de LinkedIn.
draft: false
---
```
Los componentes se insertan con `{{include:nombre}}` (archivos en `content/es|en/snippets/`).

## Indicador "pensando"
Aparece junto al nombre del cuaderno si cargar o cambiar de página tarda más de 140 ms. Para verlo como demostración, añade `?orbs` a la dirección. Usa el motor de [thinking-orbs](https://github.com/Jakubantalik/thinking-orbs) (MIT), alojado en `assets/vendor`.

## Publicar
Antes de generar un zip se actualiza la documentación (`documentacion/CHANGELOG.md`). Para subirlo, sigue [`documentacion/PUBLICAR.md`](documentacion/PUBLICAR.md) y no dejarás archivos obsoletos en el repositorio.
