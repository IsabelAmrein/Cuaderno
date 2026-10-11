# Cuaderno: guía rápida

## Cómo funciona
- `content/es/posts/*.md` y `content/en/posts/*.md`: artículos. Para enlazar la versión ES y EN usa el mismo `id:` en ambos.
- `site.json`: nombre, enlace de LinkedIn, dirección del sitio y textos de portada.
- `python3 build.py` genera la carpeta `docs/` (la web) y los borradores de LinkedIn en `linkedin/`.
- Requisitos (una vez): `pip install markdown pillow`.

Cabecera de un artículo:
```
---
id: mi-articulo          # el mismo en ES y EN
title: Título
date: 2026-11-02
accent: aqua             # aqua, sand, coral, violet, rose, moss
tags: [python, pandas]
summary: Resumen de 1-2 frases (sale en buscadores y LinkedIn).
linkedin: Gancho opcional para el post de LinkedIn.
draft: false             # true = no se publica
---
```
Imágenes: ponlas en `content/images/` y enlázalas como `/assets/img/nombre.png`.

## Publicar en GitHub Pages (gratis)
1. Crea un repositorio público (por ejemplo `cuaderno`) y sube todo el proyecto.
2. Settings, Pages, Source: *Deploy from a branch*, rama `main`, carpeta `/docs`.
3. En `site.json`, cambia `base_url` a `https://TU-USUARIO.github.io/cuaderno` y vuelve a ejecutar `build.py`.
4. Si más adelante compras dominio o hosting: pon el dominio en `base_url` y `custom_domain`, ejecuta `build.py` y sube el contenido de `docs/`.

## LinkedIn
- **Semiautomático (recomendado):** cada artículo genera `linkedin/<idioma>-<slug>.txt` con gancho, enlace y hashtags. Lo pegas en LinkedIn en un minuto. La vista previa (imagen y título) se genera sola.
- **Automático:** cada idioma tiene un feed (`/es/rss.xml`, `/en/rss.xml`). Puedes conectarlo con Make, Zapier o Buffer para que publique en tu perfil al detectar un artículo nuevo. Los textos serán más genéricos que los borradores.
- Tras publicar un artículo nuevo, pega su URL en el LinkedIn Post Inspector para refrescar la vista previa.

## SEO: lista de comprobación
- Ya incluido: títulos y descripciones únicos, URL canónicas, `hreflang` ES/EN, datos estructurados `BlogPosting`, `sitemap.xml`, `robots.txt`, RSS, imágenes Open Graph, HTML semántico.
- Da de alta el sitio en Google Search Console y Bing Webmaster Tools y envía `sitemap.xml`.
- Revisa cada versión con PageSpeed Insights (Lighthouse) y el Rich Results Test de Google.
- Escribe cada `summary` pensando en una búsqueda real y enlaza entre tus artículos.
