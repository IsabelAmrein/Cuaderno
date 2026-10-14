#!/usr/bin/env python3
"""Genera el sitio estático en ./docs a partir de ./content y ./site.json.

Uso:  pip install markdown pillow   (una sola vez)
      python3 build.py
"""
import datetime as dt
import email.utils
import hashlib
import html
import json
import random
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

import markdown
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"
CFG = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
LANGS = CFG["langs"]
U = urlparse(CFG["base_url"])
ORIGIN = f"{U.scheme}://{U.netloc}"
BASE = U.path.rstrip("/")          # "" en sitios de usuario, "/cuaderno" en sitios de proyecto

ACCENTS = {"aqua": "#6FE3C5", "sand": "#D9B25F", "coral": "#F29277",
           "violet": "#B79BFF", "rose": "#F08AB0", "moss": "#9BD774"}

T = {
    "es": dict(name="Español", articles="Entradas", about="Sobre mí", latest="Últimas entradas", see_projects="Ver los proyectos", route="Ruta con banderas: cada bandera es un proyecto", goal="Meta",
               projects="Proyectos", kind_project="Proyecto", kind_entry="Entrada", list_title="Entradas sobre datos, IA y producto", list_desc="Entradas de Isabel Amrein: apuntes sobre datos, IA generativa y producto, explicados con mis propios ejemplos, con los errores incluidos porque también enseñan.", proj_title="Proyectos de datos e IA", proj_desc="Proyectos de datos e IA de Isabel Amrein De Luca: qué construyo, con qué herramientas, cómo va cada uno y las entradas que lo explican.", proj_short="Lo que construyo: cada proyecto con su estado y sus herramientas.", entries_short="Lo que aprendo: apuntes explicados con mis propios ejemplos.",
               theme_label="Cambiar entre tema claro y oscuro", pause="Pausar la animación", play="Reanudar la animación", keep_reading="Sigue leyendo", other_projects="Otros proyectos",
               ex_alt="Animación del ciclo completo: trabajo con los datos, los analizo, creo modelos y modelos de Machine Learning, gestiono el producto, mido los resultados y vuelvo a empezar. Al final, cada bandera de la montaña es un proyecto.",
               ex_s=("Trabajo con los datos", "Los analizo", "Creo modelos", "Y modelos de Machine Learning", "Gestiono el producto", "Mido los resultados"), ex_n=("Datos", "Análisis", "Modelos", "Machine Learning", "Producto", "Medición"), ex_c4="Todo el ciclo, un proyecto tras otro", ex_chip="En marcha",
               author_blurb="Escribo sobre datos, IA y producto. Trabajo en préstamos personales y aquí cuento lo que construyo y lo que aprendo.", all_projects="Ver todos los proyectos", proj_path="proyectos", proj_lede="Lo que estoy construyendo y aprendiendo. Cada proyecto tiene su estado, sus herramientas y sus entradas.",
               st_en_marcha="En marcha", st_terminado="Terminado", st_idea="Idea", related="Entradas relacionadas", part_of="Parte del proyecto", see_project="Ver el proyecto",
               code="Código", demo="Demostración", back_projects="Volver a los proyectos", no_projects="Aún no hay proyectos publicados.", updated="Actualizado",
               all="Ver todas las entradas", min="min de lectura", topics="Tema", all_topics="Todos",
               skip="Saltar al contenido", theme="Tema", share="Compartir en LinkedIn",
               back="Volver a las entradas", other="Read in English", empty="Aún no hay entradas publicadas.",
               list_lede="Apuntes y reflexiones sobre datos, IA y producto, explicados con mis propios ejemplos.",
               cta="Lo cuento con más detalle en mi sitio:", nf="Página no encontrada",
               nf_text="Esa página no existe o se ha movido.", home="Ir al inicio", rights="Todos los derechos reservados",
               thinking="Pensando…", class_by="Clase de", thanks="Gracias a {name} por la clase en la que se basa este artículo.", thanks_short="Gracias a {name} por la clase."),
    "en": dict(name="English", articles="Entries", about="About", latest="Latest entries", see_projects="See the projects", route="Route with flags: each flag is a project", goal="Goal",
               projects="Projects", kind_project="Project", kind_entry="Entry", list_title="Entries on data, AI and product", list_desc="Entries by Isabel Amrein: notes on data, generative AI and product, explained with my own examples, mistakes included because they teach as well.", proj_title="Data and AI projects", proj_desc="Data and AI projects by Isabel Amrein De Luca: what I build, with which tools, how each one is going and the entries that explain it.", proj_short="What I build: each project with its status and its tools.", entries_short="What I learn: notes explained with my own examples.",
               theme_label="Switch between light and dark theme", pause="Pause the animation", play="Resume the animation", keep_reading="Keep reading", other_projects="More projects",
               ex_alt="Animation of the whole cycle: I work with data, analyse it, build models and machine learning models, manage the product, measure the results and start again. At the end, every flag on the mountain is a project.",
               ex_s=("I work with data", "I analyse it", "I build models", "And machine learning models", "I manage the product", "I measure the results"), ex_n=("Data", "Analysis", "Models", "Machine Learning", "Product", "Measurement"), ex_c4="The whole cycle, one project after another", ex_chip="In progress",
               author_blurb="I write about data, AI and product. I work in personal loans and here I share what I build and what I learn.", all_projects="See all projects", proj_path="projects", proj_lede="What I'm building and learning. Each project has its status, tools and entries.",
               st_en_marcha="In progress", st_terminado="Done", st_idea="Idea", related="Related entries", part_of="Part of the project", see_project="See the project",
               code="Code", demo="Demo", back_projects="Back to projects", no_projects="No projects published yet.", updated="Updated",
               all="See all entries", min="min read", topics="Topic", all_topics="All",
               skip="Skip to content", theme="Theme", share="Share on LinkedIn",
               back="Back to entries", other="Leer en español", empty="No entries published yet.",
               list_lede="Notes and reflections on data, AI and product, explained with my own examples.",
               cta="Full write-up on my site:", nf="Page not found",
               nf_text="That page doesn't exist or has moved.", home="Go to home", rights="All rights reserved",
               thinking="Thinking…", class_by="Class by", thanks="Thanks to {name} for the class this article is based on.", thanks_short="Thanks to {name} for the class."),
}
MONTHS = {
    "es": "ene feb mar abr may jun jul ago sep oct nov dic".split(),
    "en": "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(),
}


# ---------- utilidades ----------
def esc(s):
    return html.escape(str(s), quote=True)


def p(lang, *parts):
    """Ruta absoluta del sitio (con base) para una página."""
    return f"{BASE}/{lang}/" + "".join(x + "/" for x in parts)


ICON_THEME = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg>'
ICON_GLOBE = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/></svg>'
ICON_SWAP = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 8h11l-3-3M17 16H6l3 3"/></svg>'
ICON_PAUSE = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>'
ICON_PLAY = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false" fill="currentColor"><path d="M8 5l11 7-11 7z"/></svg>'


def pj(lang):
    return T[lang]["proj_path"]


def absu(path):
    return ORIGIN + path


def fmt_date(d, lang):
    return f"{d.day} {MONTHS[lang][d.month - 1]} {d.year}" if lang == "es" else f"{MONTHS[lang][d.month - 1]} {d.day}, {d.year}"


def parse(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
    meta, body = {}, raw
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.lstrip().startswith("#"):
                k, v = line.split(":", 1)
                k, v = k.strip(), v.strip()
                if v.startswith("[") and v.endswith("]"):
                    v = [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
                else:
                    v = v.strip("\"'")
                meta[k] = v
        body = m.group(2)
    return meta, body


def render_md(body):
    out = markdown.markdown(body, extensions=["fenced_code", "tables", "footnotes", "attr_list", "sane_lists"])
    out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return out.replace('src="/assets/', f'src="{BASE}/assets/').replace('href="/assets/', f'href="{BASE}/assets/')


# ---------- motivo único por artículo (puntos + recta) ----------
def ols(pts):
    n = len(pts)
    sx = sum(x for x, _ in pts); sy = sum(y for _, y in pts)
    sxy = sum(x * y for x, y in pts); sxx = sum(x * x for x, _ in pts)
    d = n * sxx - sx * sx
    m = (n * sxy - sx * sy) / d if d else 0
    return m, (sy - m * sx) / n


def motif_points(key):
    rnd = random.Random(int(hashlib.sha256(key.encode()).hexdigest()[:12], 16))
    slope, curv, noise = rnd.uniform(-.7, .7), rnd.uniform(-1.4, 1.4), rnd.uniform(.05, .14)
    n = rnd.randint(18, 30)
    pts = []
    for _ in range(n):
        x = rnd.random()
        y = .5 + slope * (x - .5) + curv * ((x - .5) ** 2 - .08) + rnd.gauss(0, noise)
        pts.append((x, min(.98, max(.02, y))))
    return pts


def motif_svg(key):
    pts = motif_points(key)
    m, b = ols(pts)
    W, H, pad = 260, 200, 14
    X = lambda x: pad + x * (W - 2 * pad)
    Y = lambda y: H - pad - y * (H - 2 * pad)
    s = [f'<svg class="motif" viewBox="0 0 {W} {H}" aria-hidden="true" focusable="false">',
         f'<path d="M{pad} {pad}V{H-pad}H{W-pad}" fill="none" stroke="currentColor" stroke-opacity=".35"/>']
    for x, y in pts:
        s.append(f'<line x1="{X(x):.1f}" y1="{Y(y):.1f}" x2="{X(x):.1f}" y2="{Y(m*x+b):.1f}" stroke="currentColor" stroke-opacity=".35"/>')
    s.append(f'<line x1="{X(0):.1f}" y1="{Y(b):.1f}" x2="{X(1):.1f}" y2="{Y(m+b):.1f}" stroke="currentColor" stroke-width="2.5"/>')
    for x, y in pts:
        s.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="3.2" fill="var(--ink)"/>')
    s.append("</svg>")
    return "".join(s)


# ---------- ilustraciones de cabecera a medida (campo hero: del artículo) ----------
def hero_svg(name):
    art_file = ROOT / "content" / "art" / f"{name}.svg"
    return art_file.read_text(encoding="utf-8") if art_file.exists() else None


ROUTE = "M30 284 L110 245 L190 205 L260 185 L340 150 L420 118 L500 90 L570 50"
STATIONS = [(110, 245), (190, 205), (260, 185), (340, 150), (420, 118), (500, 90)]


def rumbo_svg(posts, lang, goal_label="", links=True, bg=True, uid=""):
    """Montaña con camino y banderas (una por proyecto). posts: de más antiguo a más reciente (máximo 6).
    uid evita que se repitan los identificadores cuando hay varias copias en la misma página."""
    P = f"rb{uid}"
    u = lambda n: f"url(#{P}-{n})"
    posts = posts[-len(STATIONS):]
    d = (f'<defs>'
         f'<linearGradient id="{P}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#08171A"/><stop offset="1" stop-color="#123231"/></linearGradient>'
         f'<linearGradient id="{P}-far" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#27504F"/><stop offset="1" stop-color="#112B2C"/></linearGradient>'
         f'<linearGradient id="{P}-lit" x1=".1" y1="0" x2=".9" y2="1"><stop offset="0" stop-color="#CBD6D1"/><stop offset=".55" stop-color="#8E9B96"/><stop offset="1" stop-color="#5B6864"/></linearGradient>'
         f'<linearGradient id="{P}-mid" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9AA7A2"/><stop offset="1" stop-color="#52605C"/></linearGradient>'
         f'<linearGradient id="{P}-shade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#586461"/><stop offset="1" stop-color="#232C2B"/></linearGradient>'
         f'<linearGradient id="{P}-snow" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D1E6E8"/></linearGradient>'
         f'<linearGradient id="{P}-snow2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C9DFE2"/><stop offset="1" stop-color="#86ADB4"/></linearGradient>'
         f'<linearGradient id="{P}-ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E1D1E"/><stop offset="1" stop-color="#091213"/></linearGradient>'
         f'<linearGradient id="{P}-flag" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A9F6E2"/><stop offset="1" stop-color="#38C3A2"/></linearGradient>'
         f'<radialGradient id="{P}-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#A9F6E2" stop-opacity=".6"/><stop offset="1" stop-color="#6FE3C5" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="{P}-mist" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#E9FFF8" stop-opacity=".24"/><stop offset="1" stop-color="#E9FFF8" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="{P}-hz" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#6FE3C5" stop-opacity=".2"/><stop offset="1" stop-color="#6FE3C5" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="{P}-vg" cx=".5" cy=".5" r=".78"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".42"/></radialGradient>'
         f'<clipPath id="{P}-clip"><rect class="rclip" x="0" y="0" width="680" height="330"/></clipPath></defs>')
    s = [d]
    if bg:
        s.append(f'<rect width="680" height="330" rx="12" fill="{u("sky")}"/>')
        s.append('<g fill="#E9EDEA" fill-opacity=".5">' + "".join(f'<circle cx="{x}" cy="{y}" r="1.7"/>' for x, y in [(40, 30), (120, 60), (210, 25), (300, 50), (420, 28), (640, 40), (600, 90), (70, 110)]) + "</g>")
    s.append(f'<ellipse cx="340" cy="296" rx="380" ry="70" fill="{u("hz")}"/>')
    s.append(f'<circle class="sg" cx="570" cy="50" r="78" fill="{u("glow")}"/>')
    s += [f'<polygon points="120,300 200,238 260,270 330,214 420,300" fill="{u("far")}" fill-opacity=".55"/>',
          f'<polygon points="0,300 80,205 150,255 225,170 310,300" fill="{u("far")}"/>',
          f'<polygon points="0,300 60,272 110,245 170,215 230,190 300,165 340,150 400,120 450,100 500,78 540,58 570,50 520,160 470,235 380,300" fill="{u("lit")}"/>',
          f'<polygon points="110,245 170,215 230,190 300,165 340,150 300,205 200,262 120,290 60,272" fill="{u("mid")}" fill-opacity=".85"/>',
          f'<polygon points="570,50 612,112 650,190 680,262 680,300 380,300 470,235 520,160" fill="{u("shade")}"/>',
          f'<polygon points="570,50 534,82 552,90 522,120 556,112 580,96 592,80" fill="{u("snow")}"/><polygon points="570,50 592,80 580,96 556,112 590,125 612,112" fill="{u("snow2")}"/>',
          '<polyline points="0,300 60,272 110,245 170,215 230,190 300,165 340,150 400,120 450,100 500,78 540,58 570,50" fill="none" stroke="#F1FFFA" stroke-opacity=".38" stroke-width="1.6" stroke-linejoin="round"/>',
          f'<ellipse class="ms" cx="210" cy="296" rx="230" ry="26" fill="{u("mist")}"/><ellipse class="ms ms2" cx="520" cy="298" rx="210" ry="20" fill="{u("mist")}"/>']
    if bg:
        s.append(f'<rect x="0" y="300" width="680" height="30" rx="12" fill="{u("ground")}"/><rect x="0" y="300" width="680" height="12" fill="{u("ground")}"/>')
    s.append(f'<polyline class="rt" clip-path="{u("clip")}" points="30,284 110,245 190,205 260,185 340,150 420,118 500,90 570,50" fill="none" stroke="#6FE3C5" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>')
    for i, (x, y) in enumerate(STATIONS):
        spark = f'<path class="sp" opacity="0" style="--k:{i};transform-box:fill-box;transform-origin:center" d="M{x+13} {y-39} l1.6 4.4 4.4 1.6 -4.4 1.6 -1.6 4.4 -1.6 -4.4 -4.4 -1.6 4.4 -1.6z" fill="#FFFFFF"/>'
        if i < len(posts):
            ttl = posts[i]["title"]; ttl = ttl if len(ttl) <= 36 else ttl[:35] + "…"
            w = min(len(ttl) * 7.4 + 22, 330); cx = max(w / 2 + 8, min(680 - w / 2 - 8, x))
            op, cl = ((f'<a class="fl" href="{posts[i]["url"]}" aria-label="{esc(posts[i]["title"])}"><title>{esc(posts[i]["title"])}</title>', "</a>") if links else ("<g>", "</g>"))
            s.append(op +
                     f'<rect x="{x-18}" y="{y-48}" width="44" height="58" fill="transparent"/>'
                     f'<g class="fg" style="--k:{i};transform-box:view-box;transform-origin:{x}px {y}px">'
                     f'<ellipse cx="{x}" cy="{y+3}" rx="9" ry="2.6" fill="#000" fill-opacity=".4"/>'
                     f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y-36}" stroke="#E9EDEA" stroke-width="2.5" stroke-linecap="round"/>'
                     f'<polygon class="fp" points="{x},{y-36} {x+26},{y-27} {x},{y-18}" fill="{u("flag")}"/><circle cx="{x}" cy="{y}" r="5.5" fill="#6FE3C5" stroke="#0F1E1F" stroke-width="2"/></g>'
                     + spark +
                     f'<g class="lb" opacity="0"><rect x="{cx-w/2:.1f}" y="{y-80}" width="{w:.1f}" height="24" rx="8" fill="#1E2220" stroke="#6FE3C5" stroke-opacity=".6"/>'
                     f'<text x="{cx:.1f}" y="{y-63}" text-anchor="middle" fill="#E9EDEA" style="font-family:var(--f-ui);font-size:13px">{esc(ttl)}</text></g>' + cl)
        else:
            s.append(f'<g aria-hidden="true"><line x1="{x}" y1="{y}" x2="{x}" y2="{y-36}" stroke="#E9EDEA" stroke-opacity=".5" stroke-width="2" stroke-dasharray="2 3"/>'
                     f'<polygon points="{x},{y-36} {x+26},{y-27} {x},{y-18}" fill="none" stroke="#6FE3C5" stroke-opacity=".7" stroke-width="1.5" stroke-dasharray="3 3"/>'
                     f'<circle cx="{x}" cy="{y}" r="3.5" fill="none" stroke="#6FE3C5" stroke-opacity=".7"/></g>')
    s.append(f'<g class="fg sf" aria-hidden="true" style="--k:6;transform-box:view-box;transform-origin:570px 50px"><line x1="570" y1="50" x2="570" y2="14" stroke="#E9EDEA" stroke-width="3" stroke-linecap="round"/>'
             f'<polygon class="fp" points="570,14 604,26 570,38" fill="{u("flag")}"/><circle cx="570" cy="50" r="6" fill="#6FE3C5" stroke="#0F1E1F" stroke-width="2"/></g>')
    s.append(f'<g class="mk" opacity="0"><circle r="15" fill="{u("glow")}"/><circle r="4.2" fill="#FFFFFF"/></g>')
    if bg:
        s.append(f'<rect width="680" height="330" rx="12" fill="{u("vg")}" pointer-events="none"/>')
    return "".join(s)


def explainer_svg(projects, lang):
    """Animación de 26 s en bucle: el ciclo completo (datos, análisis, modelos, Machine Learning, producto y medición) y la montaña de proyectos.
    Sin movimiento, solo se ve la montaña."""
    import math, random
    t = T[lang]
    rnd = random.Random(11)
    CX, CY, R = 340, 148, 100
    defs = ('<defs>'
            '<linearGradient id="ex-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07151A"/><stop offset=".7" stop-color="#0F2B2D"/><stop offset="1" stop-color="#123533"/></linearGradient>'
            '<radialGradient id="ex-aura" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#6FE3C5" stop-opacity=".34"/><stop offset="1" stop-color="#6FE3C5" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="ex-aurb" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#4DB8E8" stop-opacity=".26"/><stop offset="1" stop-color="#4DB8E8" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="ex-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#B8FFEE" stop-opacity=".95"/><stop offset=".35" stop-color="#6FE3C5" stop-opacity=".45"/><stop offset="1" stop-color="#6FE3C5" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="ex-disc" cx=".5" cy=".42" r=".6"><stop offset="0" stop-color="#1B3333"/><stop offset="1" stop-color="#0B1718"/></radialGradient>'
            '<linearGradient id="ex-card" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#26393A"/><stop offset="1" stop-color="#121D1E"/></linearGradient>'
            '<linearGradient id="ex-edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6FE3C5" stop-opacity=".9"/><stop offset=".5" stop-color="#6FE3C5" stop-opacity=".12"/><stop offset="1" stop-color="#6FE3C5" stop-opacity=".5"/></linearGradient>'
            '<linearGradient id="ex-bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9F6E2"/><stop offset="1" stop-color="#2FA88F"/></linearGradient>'
            '<linearGradient id="ex-ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E1D1E"/><stop offset="1" stop-color="#091213"/></linearGradient>'
            '<radialGradient id="ex-vg" cx=".5" cy=".5" r=".78"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></radialGradient>'
            '</defs>')
    stars = "".join(f'<circle class="st" cx="{rnd.randint(16, 664)}" cy="{rnd.randint(14, 250)}" r="{rnd.choice((.8, 1.1, 1.5))}" fill="#E9F7F2" style="animation-delay:-{rnd.uniform(0, 4):.1f}s"/>' for _ in range(34))
    bokeh = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#ex-aura)" opacity=".5"/>' for x, y, r in ((70, 60, 34), (610, 230, 42), (590, 40, 26), (90, 250, 30)))
    amb = (f'<rect width="680" height="350" rx="12" fill="url(#ex-sky)"/>'
           f'<g class="aur"><ellipse class="a1" cx="170" cy="120" rx="250" ry="120" fill="url(#ex-aura)"/><ellipse class="a2" cx="540" cy="90" rx="260" ry="120" fill="url(#ex-aurb)"/></g>{bokeh}{stars}')
    ground = '<rect x="0" y="300" width="680" height="50" rx="12" fill="url(#ex-ground)"/><rect x="0" y="300" width="680" height="14" fill="url(#ex-ground)"/><line x1="0" y1="300.5" x2="680" y2="300.5" stroke="#6FE3C5" stroke-opacity=".12"/>'
    pos = [(CX + R * math.cos(math.radians(a)), CY + R * math.sin(math.radians(a))) for a in (-90, -30, 30, 90, 150, 210)]
    # ---- anillo: pista, flechas de sentido, nodos y etiquetas
    track = f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="#6FE3C5" stroke-opacity=".22" stroke-width="1.6" stroke-dasharray="3 7"/><circle cx="{CX}" cy="{CY}" r="80" fill="url(#ex-disc)" stroke="#6FE3C5" stroke-opacity=".16"/>'
    arrows = "".join(f'<path d="M-4 -4.5 L5 0 L-4 4.5z" fill="#6FE3C5" fill-opacity=".55" transform="translate({CX + R * math.cos(math.radians(a)):.1f} {CY + R * math.sin(math.radians(a)):.1f}) rotate({a + 90})"/>' for a in (-60, 0, 60, 120, 180, 240))
    nodes, labs = [], []
    for k, (x, y) in enumerate(pos):
        nodes.append(f'<g><circle class="hl" cx="{x:.1f}" cy="{y:.1f}" r="22" fill="url(#ex-glow)" style="--k:{k};transform-origin:{x:.1f}px {y:.1f}px"/><circle cx="{x:.1f}" cy="{y:.1f}" r="7.5" fill="#0F2223" stroke="#6FE3C5" stroke-width="2"/><circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#6FE3C5"/></g>')
        dx, dy, anc = ((0, -20, "middle"), (20, 5, "start"), (20, 5, "start"), (0, 31, "middle"), (-20, 5, "end"), (-20, 5, "end"))[k]
        labs.append(f'<text class="lab" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anc}" style="--k:{k}">{esc(t["ex_n"][k])}</text>')
    orbit = f'<g class="orbit" style="transform-origin:{CX}px {CY}px"><circle cx="{CX}" cy="{CY - R}" r="16" fill="url(#ex-glow)"/><circle cx="{CX}" cy="{CY - R}" r="5" fill="#FFFFFF"/></g>'
    caps = "".join(f'<text class="cap capk" x="340" y="334" style="--k:{k}">{esc(t["ex_s"][k])}</text>' for k in range(6))

    def vis(k, inner):
        return f'<g class="vis" style="--k:{k}"><g transform="translate({CX} {CY}) scale(1.22)">{inner}</g></g>'
    # 0 datos
    v0 = "".join(f'<circle class="dr" cx="{rnd.randint(-56, 56)}" cy="{rnd.randint(-50, 50)}" r="{rnd.choice((2.2, 3, 3.8, 4.8))}" fill="{"#6FE3C5" if i % 3 else "#E9EDEA"}" fill-opacity="{rnd.choice((.6, .85, 1))}" style="--dx:{rnd.randint(-9, 9)}px;--dy:{rnd.randint(-8, 8)}px;animation-delay:-{rnd.uniform(0, 3):.1f}s"/>' for i in range(16))
    v0 += '<g fill="#E9EDEA" fill-opacity=".5"><rect x="-58" y="40" width="22" height="3" rx="1.5"/><rect x="-58" y="47" width="14" height="3" rx="1.5"/><rect x="30" y="-48" width="26" height="3" rx="1.5"/><rect x="38" y="-41" width="18" height="3" rx="1.5"/></g>'
    # 1 análisis
    hs = (20, 32, 26, 44, 38)
    v1 = "".join(f'<rect class="br" x="{-52 + n * 22}" y="{30 - h}" width="15" height="{h}" rx="4" fill="url(#ex-bar)" style="--k:{1};--o:{n * .12:.2f}s"/>' for n, h in enumerate(hs))
    v1 += '<line x1="-56" y1="34" x2="56" y2="34" stroke="#2C3A3A" stroke-width="1.5"/><polyline class="dl" points="-46,10 -24,-2 -2,4 20,-18 42,-26" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" pathLength="1" style="--k:1;--o:.7s"/><circle class="pp" cx="42" cy="-26" r="4.6" fill="#FFFFFF" style="--k:1;--o:1.5s"/>'
    # 2 modelos estadísticos (segmentación y regresión)
    clus = (((-28, -16), "#6FE3C5"), ((28, -22), "#D9B25F"), ((2, 28), "#B79BFF"))
    v2 = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="26" ry="18" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-opacity=".6" stroke-dasharray="3 3" class="fd" style="--k:2;--o:{2.0 + n * .2:.1f}s"/>' for n, ((cx, cy), col) in enumerate(clus))
    for n, ((cx, cy), col) in enumerate(clus):
        v2 += "".join(f'<circle class="pp" cx="{cx + rnd.randint(-17, 17)}" cy="{cy + rnd.randint(-11, 11)}" r="3.2" fill="{col}" style="--k:2;--o:{n * .3 + m * .08:.2f}s"/>' for m in range(7))
    v2 += '<line class="dl" x1="-58" y1="34" x2="58" y2="-36" stroke="#FFFFFF" stroke-opacity=".9" stroke-width="2.4" stroke-linecap="round" pathLength="1" style="--k:2;--o:1.1s"/>'
    # 3 Machine Learning (red que aprende)
    lay = ((-46, (-30, 0, 30)), (0, (-42, -14, 14, 42)), (46, (-22, 22)))
    ls, nn = [], []
    for (xa, ya_l), (xb, yb_l) in zip(lay, lay[1:]):
        for ya in ya_l:
            for yb in yb_l:
                ls.append(f'<line class="fd" x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="#6FE3C5" stroke-opacity=".45" stroke-width="1.1" style="--k:3;--o:.2s"/>')
    for x, ys in lay:
        for y in ys:
            nn.append(f'<circle class="pp" cx="{x}" cy="{y}" r="5" fill="#6FE3C5" style="--k:3;--o:{abs(x) * .004 + .1:.2f}s"/><circle cx="{x - 1.4}" cy="{y - 1.6}" r="1.7" fill="#E9FFF8" opacity=".9"/>')
    pls = "".join(f'<line class="np2" x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" pathLength="1" stroke="#E9FFF8" stroke-width="2.2" stroke-linecap="round" style="--k:3;--o:{.9 + n * .22:.2f}s"/>' for n, (xa, ya, xb, yb) in enumerate(((-46, -30, 0, -14), (0, -14, 46, 22), (-46, 30, 0, 42), (0, 42, 46, -22), (-46, 0, 0, 14))))
    v3 = "".join(ls) + pls + "".join(nn)
    # 4 producto
    v4 = ('<ellipse cx="0" cy="56" rx="48" ry="5" fill="#000" fill-opacity=".4"/><rect x="-46" y="-52" width="92" height="104" rx="13" fill="url(#ex-card)"/><rect x="-45.5" y="-51.5" width="91" height="103" rx="12.5" fill="none" stroke="url(#ex-edge)" stroke-width="1.2"/>'
          '<circle cx="-30" cy="-36" r="6" fill="url(#ex-bar)"/><rect x="-19" y="-40" width="38" height="5" rx="2.5" fill="#E9EDEA" fill-opacity=".9"/><rect x="-19" y="-31" width="24" height="4" rx="2" fill="#98A39E" fill-opacity=".7"/>'
          + "".join(f'<rect class="br" x="{-34 + n * 17}" y="{14 - h}" width="11" height="{h}" rx="3" fill="url(#ex-bar)" style="--k:4;--o:{n * .1:.2f}s"/>' for n, h in enumerate((14, 24, 18, 32)))
          + '<rect x="-34" y="26" width="68" height="14" rx="7" fill="url(#ex-bar)"/><rect x="-18" y="31" width="36" height="4" rx="2" fill="#0F1E1F" fill-opacity=".85"/>'
          '<g class="pp" style="--k:4;--o:1.6s"><circle cx="42" cy="-50" r="10" fill="#6FE3C5"/><path d="M37 -50 l4 4 7 -8" fill="none" stroke="#0F1E1F" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g>')
    # 5 medición (indicador con aguja)
    v5 = ('<path d="M-50 22 A50 50 0 0 1 50 22" fill="none" stroke="#2C3A3A" stroke-width="11" stroke-linecap="round"/>'
          '<path class="dl" d="M-50 22 A50 50 0 0 1 50 22" fill="none" stroke="url(#ex-bar)" stroke-width="11" stroke-linecap="round" pathLength="1" style="--k:5;--o:.5s;stroke-dasharray:1"/>'
          '<g class="nd2" style="--k:5;--o:.5s;transform-origin:0px 22px"><line x1="0" y1="22" x2="0" y2="-26" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round"/></g>'
          '<circle cx="0" cy="22" r="7" fill="#E9EDEA"/><circle cx="0" cy="22" r="2.6" fill="#0F1E1F"/>'
          '<text class="fd" x="0" y="52" text-anchor="middle" fill="#A9F6E2" style="font:600 16px var(--f-ui);--k:5;--o:1.6s">+12 %</text>')
    ring = (f'<g class="ring">{track}{arrows}{"".join(nodes)}{"".join(labs)}{vis(0, v0)}{vis(1, v1)}{vis(2, v2)}{vis(3, v3)}{vis(4, v4)}{vis(5, v5)}{orbit}{caps}</g>')
    s4 = f'<g class="sc sc4"><g class="cam">{rumbo_svg(projects, lang, bg=False, uid="x")}</g><text class="cap" x="340" y="334">{esc(t["ex_c4"])}</text></g>'
    vg = '<rect width="680" height="350" rx="12" fill="url(#ex-vg)" pointer-events="none"/>'
    return defs + amb + ground + ring + s4 + vg


def thumb_html(hero, key):
    svg = (hero_svg(hero) if hero else None) or motif_svg(key)
    svg = svg.replace('class="motif"', 'class="motif" preserveAspectRatio="xMidYMid slice"', 1)
    return f'<span class="thumb" aria-hidden="true">{svg}</span>'


def process_photo():
    """Si existe content/img/isabel.(jpg|png|webp), la recorta en cuadrado, la reduce y le quita los metadatos (ubicación incluida)."""
    from PIL import Image, ImageOps
    for f in sorted((ROOT / "content" / "img").glob("isabel.*")) if (ROOT / "content" / "img").exists() else []:
        im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
        im = ImageOps.fit(im, (480, 480), Image.LANCZOS, centering=(0.5, 0.35))
        dest = OUT / "assets" / "img"
        dest.mkdir(parents=True, exist_ok=True)
        im.save(dest / "isabel.jpg", "JPEG", quality=82, optimize=True)  # se guarda sin EXIF
        return f"{BASE}/assets/img/isabel.jpg"
    return None


def process_banner():
    """Banner de Sobre mí: content/img/banner.jpg. Se recorta la franja gris inferior, se reduce a dos tamaños y se guarda sin metadatos."""
    from PIL import Image
    f = ROOT / "content" / "img" / "banner.jpg"
    if not f.exists():
        return None
    im = Image.open(f).convert("RGB")
    im = im.crop((0, 0, im.width, im.height - 20))          # quita la franja translúcida del borde inferior
    dest = OUT / "assets" / "img"
    dest.mkdir(parents=True, exist_ok=True)
    out = {}
    for w in (700, 1400):
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(dest / f"banner-{w}.jpg", "JPEG", quality=80, optimize=True, progressive=True)
        out[w] = (f"{BASE}/assets/img/banner-{w}.jpg", r.width, r.height)
    return out


def banner_html(b):
    if not b:
        return ""
    (u7, _, _), (u14, w, h) = b[700], b[1400]
    return (f'<div class="about-banner"><img src="{u14}" srcset="{u7} 700w, {u14} 1400w" sizes="100vw" width="{w}" height="{h}" alt="" decoding="async" fetchpriority="high"></div>')


def profile_card(lang, photo):
    t, pr = T[lang], CFG["profile"][lang]
    ini = "".join(w[0] for w in CFG["name"].split()[:2]).upper()
    avatar = (f'<img class="avatar" src="{photo}" alt="{esc(CFG["name"])}" width="144" height="144">' if photo else f'<span class="avatar mono" aria-hidden="true">{ini}</span>')
    facts = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in pr["facts"])
    return (f'<aside class="profile">{avatar}<div><p class="p-name">{esc(CFG["name"])}</p><p class="p-role">{esc(CFG["job_title"][lang])} · {esc(pr["headline"])}</p>'
            f'<dl class="facts">{facts}</dl><p class="cta"><a class="btn" href="{CFG["linkedin"]}" rel="me noopener" target="_blank">{esc(pr["cta"])}</a></p></div></aside>')


def author_box(lang):
    t = T[lang]
    return (f'<aside class="author-box"><p><strong>{esc(CFG["name"])}</strong> · {esc(CFG["job_title"][lang])}. {t["author_blurb"]}</p>'
            f'<p><a href="{p(lang, "about")}">{t["about"]}</a> · <a href="{CFG["linkedin"]}" rel="me noopener" target="_blank">LinkedIn</a></p></aside>')


def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": absu(u)} for i, (n, u) in enumerate(items)]}


# ---------- imagen Open Graph (para la vista previa en LinkedIn) ----------
def font(size, bold=False, mono=False):
    names = (["DejaVuSansMono.ttf"] if mono else ["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"])
    for base in ("/usr/share/fonts/truetype/dejavu/", "/Library/Fonts/", "C:/Windows/Fonts/"):
        for n in names + (["Arial Bold.ttf", "arialbd.ttf"] if bold else ["Arial.ttf", "arial.ttf"]):
            try:
                return ImageFont.truetype(base + n, size)
            except OSError:
                continue
    return ImageFont.load_default(size)


def draw_scatter(d, key, col):
    pts = motif_points(key)
    m, b = ols(pts)
    ox, oy, pw, ph = 800, 90, 340, 300
    X = lambda x: ox + x * pw
    Y = lambda y: oy + ph - y * ph
    for x, y in pts:
        d.line([(X(x), Y(y)), (X(x), Y(m * x + b))], fill=col + "66" if False else col, width=1)
    d.line([(X(0), Y(b)), (X(1), Y(m + b))], fill=col, width=5)
    for x, y in pts:
        d.ellipse([X(x) - 6, Y(y) - 6, X(x) + 6, Y(y) + 6], fill="#E9EDEA")


def og_image(path, title, key, accent, site_title, hero=None, quote=None):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#151716")
    d = ImageDraw.Draw(img)
    col = ACCENTS.get(accent, ACCENTS["aqua"])
    d.rectangle([0, 0, W, 16], fill=col)
    art_png = (ROOT / "content" / "art" / f"{hero}.png") if hero else None
    if art_png and art_png.exists():
        pic = Image.open(art_png).convert("RGBA")
        bw, bx = (500, 670) if hero == "rumbo" else (430, 740)
        sc = min(bw / pic.width, 380 / pic.height)
        pic = pic.resize((int(pic.width * sc), int(pic.height * sc)))
        img.paste(pic, (bx + (bw - pic.width) // 2, 130 + (380 - pic.height) // 2), pic)
    else:
        draw_scatter(d, key, col)
    def wrap_title(size):
        f = font(size, bold=True)
        lines, cur = [], ""
        for w in title.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) > 640 and cur:
                lines.append(cur); cur = w
            else:
                cur = t
        lines.append(cur)
        return f, lines
    f, lines = wrap_title(58)
    step = 74
    if len(lines) > 3:
        f, lines = wrap_title(48)
        step = 62
    y = 140
    for ln in lines[:5]:
        d.text((70, y), ln, font=f, fill="#E9EDEA")
        y += step
    if quote:
        qf, qw, qlines, qcur = font(28), 620, [], ""
        for w in quote.split():
            t = (qcur + " " + w).strip()
            if d.textlength(t, font=qf) > qw and qcur:
                qlines.append(qcur); qcur = w
            else:
                qcur = t
        qlines.append(qcur)
        qy = y + 22
        for ln in qlines[:3]:
            d.text((70, qy), ln, font=qf, fill=col)
            qy += 38
    d.text((70, H - 80), site_title, font=font(30, mono=True), fill="#98A39E")
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)


# ---------- plantilla común ----------
def page(lang, *, title, desc, body, url, alts=None, og=None, accent="aqua", kind="website",
         jsonld=None, active=None, hero=False):
    t = T[lang]
    site_title = CFG["title"][lang]
    full_title = f"{site_title}: {CFG['tagline'][lang]}" if url == p(lang) else f"{title} | {site_title}"
    alts = alts or {}
    other = [l for l in LANGS if l != lang][0]
    other_href = alts.get(other, p(other))
    og = og or f"{BASE}/assets/og/{lang}-home.png"
    head_alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{absu(h)}">' for l, h in {**alts, lang: url}.items())
    head_alts += f'<link rel="alternate" hreflang="x-default" href="{absu(alts.get(LANGS[0], url) if lang != LANGS[0] else url)}">'
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    v = hashlib.md5((ROOT / "assets/style.css").read_bytes()).hexdigest()[:8]
    nav = (f'<a href="{p(lang, pj(lang))}"{" aria-current=page" if active == "projects" else ""}>{t["projects"]}</a>'
           f'<a href="{p(lang, "blog")}"{" aria-current=page" if active == "blog" else ""}>{t["articles"]}</a>'
           f'<a href="{p(lang, "about")}"{" aria-current=page" if active == "about" else ""}>{t["about"]}</a>')
    cur, oth = lang.upper(), other.upper()
    tools = (f'<div class="head-tools"><a class="lang-switch" href="{other_href}" hreflang="{other}" lang="{other}" data-lang="{other}" aria-label="{esc(t["other"])}" title="{esc(T[other]["name"])}">'
             f'{ICON_GLOBE}<span class="cur">{cur}</span>{ICON_SWAP}<span>{oth}</span></a>'
             f'<button class="icon-btn theme-btn" type="button" data-theme-toggle aria-label="{esc(t["theme_label"])}" title="{esc(t["theme_label"])}">{ICON_THEME}</button></div>')
    foot_links = f'<a href="{CFG["linkedin"]}" rel="me noopener" target="_blank">LinkedIn</a> <a href="{p(lang)}rss.xml">RSS</a>'
    if CFG.get("email"):
        foot_links += f' <a href="mailto:{esc(CFG["email"])}">Email</a>'
    return f"""<!doctype html>
<html lang="{lang}" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#151716">
<script>(function(){{try{{var t=localStorage.getItem('theme');if(!t){{t='dark'}}document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}}})()</script>
<script>if('IntersectionObserver' in window){{var d=document.documentElement;d.classList.add('anim');if(matchMedia('(prefers-reduced-motion: reduce)').matches)d.classList.add('rm')}}</script>
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{absu(url)}">
{head_alts}
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="{esc(site_title)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{absu(url)}">
<meta property="og:image" content="{absu(og)}">
<meta property="og:locale" content="{lang}">
<meta name="twitter:card" content="summary_large_image">
<meta name="author" content="{esc(CFG['name'])}">
<link rel="alternate" type="application/rss+xml" title="{esc(site_title)}" href="{p(lang)}rss.xml">
<link rel="icon" type="image/svg+xml" href="{BASE}/assets/favicon.svg">
<link rel="preload" href="{BASE}/assets/fonts/figtree-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{BASE}/assets/fonts/newsreader-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{BASE}/assets/style.css?v={v}">
{ld}
</head>
<body class="accent-{accent}">
<a class="skip" href="#main">{t['skip']}</a>
<header class="site-head"><div class="wrap">
<span class="brandbox"><a class="brand" href="{p(lang)}">{esc(site_title)}</a><span class="think" id="think" role="status" hidden><canvas aria-hidden="true"></canvas><span>{t['thinking']}</span></span></span>
{tools}
<nav class="nav" aria-label="Principal">{nav}</nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<span>© {dt.date.today().year} {esc(CFG['name'])}</span>
<span style="display:flex;gap:1.5rem">{foot_links}</span>
</div></footer>
<script src="{BASE}/assets/vendor/thinking-orbs.js?v={hashlib.md5((ROOT / 'assets/vendor/thinking-orbs.js').read_bytes()).hexdigest()[:8]}" defer></script>
<script src="{BASE}/assets/main.js?v={hashlib.md5((ROOT / 'assets/main.js').read_bytes()).hexdigest()[:8]}" defer></script>
</body>
</html>
"""


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def rows(posts, lang):
    t = T[lang]
    if not posts:
        return f'<p class="empty">{t["empty"]}</p>'
    out = ['<ul class="log">']
    for x in posts:
        tags = "".join(f"<span>{esc(g)}</span>" for g in x["tags"])
        out.append(
            f'<li data-tags="{esc(",".join(x["tags"]))}"><a class="log-row accent-{x["accent"]}" href="{x["url"]}">{thumb_html(x["hero"], x["id"])}'
            f'<div><div class="meta"><span class="kind">{t["kind_entry"]}</span><time datetime="{x["date"].isoformat()}">{fmt_date(x["date"], lang)}</time></div>'
            f'<h3>{esc(x["title"])}</h3><p>{esc(x["summary"])}</p><span class="tags">{tags}</span></div></a></li>')
    out.append("</ul>")
    return "".join(out)


def status_chip(x, lang):
    t = T[lang]
    orb = '<canvas class="orb-live" aria-hidden="true"></canvas>' if x["status"] == "en-marcha" else ""
    return f'<span class="chip status s-{x["status"]}">{orb}{t["st_" + x["status"].replace("-", "_")]}</span>'


def proj_rows(items, lang):
    t = T[lang]
    if not items:
        return f'<p class="empty">{t["no_projects"]}</p>'
    out = ['<ul class="log">']
    for x in items:
        stack = "".join(f"<span>{esc(g)}</span>" for g in x["stack"])
        out.append(f'<li><a class="log-row accent-{x["accent"]}" href="{x["url"]}">{thumb_html(x["hero"], x["id"])}'
                   f'<div><div class="meta"><span class="kind">{t["kind_project"]}</span>{status_chip(x, lang)}</div>'
                   f'<h3>{esc(x["title"])}</h3><p>{esc(x["summary"])}</p><span class="tags">{stack}</span></div></a></li>')
    out.append("</ul>")
    return "".join(out)


def author_ld(l):
    return {"@type": "Person", "name": CFG["name"], "jobTitle": CFG.get("job_title", {}).get(l, ""),
            "sameAs": [CFG["linkedin"]]}


# ---------- construcción ----------
def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    for f in ("style.css", "main.js", "favicon.svg"):
        shutil.copy(ROOT / "assets" / f, OUT / "assets" / f)
    shutil.copytree(ROOT / "assets" / "fonts", OUT / "assets" / "fonts")
    shutil.copytree(ROOT / "assets" / "vendor", OUT / "assets" / "vendor")
    if (ROOT / "content/images").exists():
        shutil.copytree(ROOT / "content/images", OUT / "assets/img")
    (OUT / ".nojekyll").write_text("")
    if CFG.get("custom_domain"):
        (OUT / "CNAME").write_text(CFG["custom_domain"])
    for old in (ROOT / "linkedin").glob("*.txt"):
        old.unlink()

    photo = process_photo()
    banner = process_banner()

    # 1) cargar proyectos (primero los datos, para poder enlazarlos con {{project:id}})
    projects = {l: [] for l in LANGS}
    for l in LANGS:
        d = ROOT / "content" / l / "projects"
        for f in (sorted(d.glob("*.md")) if d.exists() else []):
            meta, body = parse(f)
            if str(meta.get("draft", "")).lower() == "true":
                continue
            slug = meta.get("slug", f.stem)
            st = meta.get("status", "en-marcha")
            stack = meta.get("stack", [])
            projects[l].append(dict(
                id=meta.get("id", slug), slug=slug, lang=l, title=meta["title"], subtitle=meta.get("subtitle", ""), summary=meta.get("summary", ""),
                status=st if st in ("en-marcha", "terminado", "idea") else "en-marcha", stack=stack if isinstance(stack, list) else [stack],
                repo=meta.get("repo", ""), demo=meta.get("demo", ""), date=dt.date.fromisoformat(meta["date"]),
                updated=dt.date.fromisoformat(meta.get("updated", meta["date"])),
                accent=meta.get("accent", "aqua") if meta.get("accent", "aqua") in ACCENTS else "aqua",
                hero=meta.get("hero", ""), linkedin=meta.get("linkedin", ""), related_title=meta.get("related_title", ""), seo_title=meta.get("seo_title", ""), body=body, url=p(l, pj(l), meta.get("slug", f.stem))))
        projects[l].sort(key=lambda x: (x["date"], x["id"]))
    pby = {l: {x["id"]: x for x in projects[l]} for l in LANGS}

    def expand(body, l):
        body = re.sub(r"\{\{include:(\w+)\}\}", lambda m: (ROOT / "content" / l / "snippets" / f"{m.group(1)}.html").read_text(encoding="utf-8"), body)
        return re.sub(r"\{\{project:([\w-]+)\}\}", lambda m: pby[l][m.group(1)]["url"], body)

    # 2) cargar artículos
    posts = {l: [] for l in LANGS}
    for l in LANGS:
        for f in sorted((ROOT / "content" / l / "posts").glob("*.md")):
            meta, body = parse(f)
            if str(meta.get("draft", "")).lower() == "true":
                continue
            words = len(re.findall(r"\w+", body))
            body = expand(body, l)
            slug = meta.get("slug", f.stem)
            prs = meta.get("projects", [])
            posts[l].append(dict(
                id=meta.get("id", slug), slug=slug, lang=l, title=meta["title"],
                date=dt.date.fromisoformat(meta["date"]),
                updated=dt.date.fromisoformat(meta.get("updated", meta["date"])),
                summary=meta.get("summary", ""), tags=meta.get("tags", []) if isinstance(meta.get("tags", []), list) else [meta["tags"]],
                accent=meta.get("accent", "aqua") if meta.get("accent", "aqua") in ACCENTS else "aqua",
                linkedin=meta.get("linkedin", ""), seo_title=meta.get("seo_title", ""), teacher=meta.get("teacher", ""), order=int(meta.get("order", 0)), quote=meta.get("quote", ""), hero=meta.get("hero", ""), teacher_url=meta.get("teacher_url", ""),
                projects=prs if isinstance(prs, list) else [prs], html=render_md(body), minutes=max(1, round(words / 200)),
                url=p(l, "blog", slug)))
        posts[l].sort(key=lambda x: (x["date"], x["order"], x["id"]), reverse=True)
    for l in LANGS:
        for x in projects[l]:
            x["html"] = render_md(expand(x["body"], l))
    by_id = {l: {x["id"]: x for x in posts[l]} for l in LANGS}

    for l in LANGS:
        t, site_title = T[l], CFG["title"][l]
        og_image(OUT / "assets/og" / f"{l}-home.png", site_title, "home-" + l, "aqua", CFG["name"], hero="rumbo", quote=CFG["tagline"][l])
        alts_for = lambda *parts: {x: p(x, *parts) for x in LANGS}

        # inicio
        ex = explainer_svg(projects[l], l)
        kicker = f'{CFG["name"]} · {CFG["job_title"][l]}'
        hero = f"""<section class="hero"><div class="wrap">
<div class="hero-text"><p class="kicker">{esc(kicker)}</p><h1>{esc(CFG['tagline'][l])}</h1><p class="intro">{esc(CFG['intro'][l])}</p>
<p class="cta"><a class="btn" href="{p(l, pj(l))}">{t['see_projects']}</a><a class="btn ghost" href="{p(l, 'about')}">{t['about']}</a></p></div>
<div class="hero-art"><div class="ex"><svg viewBox="0 0 680 350" role="group" aria-label="{esc(t['ex_alt'])}">{ex}</svg>
<button class="ex-pause" type="button" aria-pressed="false" data-pause="{esc(t['pause'])}" data-play="{esc(t['play'])}" aria-label="{esc(t['pause'])}" title="{esc(t['pause'])}"><span class="i-pause">{ICON_PAUSE}</span><span class="i-play">{ICON_PLAY}</span></button></div></div></div></section>
<section class="section"><div class="wrap"><h2>{t['projects']}</h2><p class="lede">{t['proj_short']}</p>{proj_rows(list(reversed(projects[l])), l)}
<p class="more"><a href="{p(l, pj(l))}">{t['all_projects']}</a></p></div></section>
<section class="section"><div class="wrap"><h2>{t['latest']}</h2><p class="lede">{t['entries_short']}</p>{rows(posts[l][:5], l)}
<p class="more"><a href="{p(l, 'blog')}">{t['all']}</a></p></div></section>"""
        write(OUT / l / "index.html", page(l, title=site_title, desc=CFG["description"][l], body=hero, url=p(l),
                                           alts=alts_for(), jsonld={"@context": "https://schema.org", "@type": "WebSite",
                                           "name": site_title, "url": absu(p(l)), "inLanguage": l,
                                           "author": author_ld(l)}))

        # lista de artículos
        all_tags = sorted({g for x in posts[l] for g in x["tags"]})
        flt = ""
        if all_tags:
            flt = (f'<div class="filters" role="group" aria-label="{t["topics"]}"><button type="button" data-filter="" aria-pressed="true">{t["all_topics"]}</button>'
                   + "".join(f'<button type="button" data-filter="{esc(g)}" aria-pressed="false">{esc(g)}</button>' for g in all_tags) + "</div>")
        body = f'<section class="section"><div class="wrap"><h1 class="page-title">{t["articles"]}</h1><p class="lede">{t["list_lede"]}</p>{flt}{rows(posts[l], l)}</div></section>'
        write(OUT / l / "blog" / "index.html", page(l, title=t["list_title"], desc=t["list_desc"], body=body,
                                                    url=p(l, "blog"), alts=alts_for("blog"), active="blog"))

        # lista de proyectos
        body = f'<section class="section"><div class="wrap"><h1 class="page-title">{t["projects"]}</h1><p class="lede">{t["proj_lede"]}</p>{proj_rows(list(reversed(projects[l])), l)}</div></section>'
        write(OUT / l / pj(l) / "index.html", page(l, title=t["proj_title"], desc=t["proj_desc"], body=body, url=p(l, pj(l)),
                                                   alts={x: p(x, pj(x)) for x in LANGS}, active="projects"))

        # sobre mí
        af = ROOT / "content" / l / "about.md"
        if af.exists():
            meta, abody = parse(af)
            body = (banner_html(banner) + f'<section class="section"><div class="prose-head"><h1 class="page-title">{esc(meta.get("title", t["about"]))}</h1>{profile_card(l, photo)}</div>'
                    f'<article class="prose" style="margin-top:0">{render_md(expand(abody, l))}</article></section>')
            person = {**author_ld(l), "jobTitle": CFG["job_title"][l], "url": absu(p(l, "about")), "sameAs": [CFG["linkedin"]], "description": CFG["description"][l],
                      "knowsAbout": ["Data Science", "Generative AI", "Consumer lending", "Data strategy", "Product management"]}
            if photo:
                person["image"] = absu(photo)
            ld_about = {"@context": "https://schema.org", "@type": "ProfilePage", "inLanguage": l, "name": meta.get("title", t["about"]), "mainEntity": person}
            write(OUT / l / "about" / "index.html", page(l, title=meta.get("seo_title", meta.get("title", t["about"])), desc=meta.get("summary", CFG["description"][l]),
                                                         body=body, url=p(l, "about"), alts=alts_for("about"), active="about", jsonld=ld_about))

        # proyectos
        for x in projects[l]:
            alts = {ol: pby[ol][x["id"]]["url"] for ol in LANGS if x["id"] in pby[ol]}
            og_path = f"/assets/og/{l}-p-{x['slug']}.png"
            og_image(OUT / og_path.lstrip("/"), x["title"], x["id"], x["accent"], site_title, hero=x["hero"], quote=x["subtitle"])
            rel = sorted([y for y in posts[l] if x["id"] in y["projects"]], key=lambda y: (y["date"], y["order"], y["id"]))
            stack = "".join(f"<span>{esc(g)}</span>" for g in x["stack"])
            enl = "".join(f'<a href="{esc(u)}" rel="noopener" target="_blank">{lab}</a>' for lab, u in ((t["code"], x["repo"]), (t["demo"], x["demo"])) if u)
            enl = f'<p class="proj-links">{enl}</p>' if enl else ""
            sub = f'<p class="subtitle">{esc(x["subtitle"])}</p>' if x["subtitle"] else ""
            relsec = (f'<section class="section related"><div class="wrap"><h2>{esc(x["related_title"] or t["related"])}</h2>{rows(rel, l)}</div></section>') if rel else ""
            share = f"https://www.linkedin.com/sharing/share-offsite/?url={absu(x['url'])}"
            alt_link = "".join(f'<a href="{u}" hreflang="{ol}" lang="{ol}">{t["other"]}</a>' for ol, u in alts.items() if ol != l)
            otros = [y for y in projects[l] if y["id"] != x["id"]]
            others = f'<section class="section related"><div class="wrap"><h2>{t["other_projects"]}</h2>{proj_rows(otros, l)}</div></section>' if otros else ""
            body = f"""<article>
<header class="post-head"><div class="wrap"><div>
<div class="post-meta">{status_chip(x, l)}<time datetime="{x['updated'].isoformat()}">{t['updated']} {fmt_date(x['updated'], l)}</time></div>
<h1>{esc(x['title'])}</h1>{sub}<div class="tags">{stack}</div>{enl}</div>{hero_svg(x['hero']) or motif_svg(x['id'])}</div></header>
<div class="prose">{x['html']}</div>
{relsec}{others}{author_box(l)}
<footer class="post-foot"><a href="{share}" target="_blank" rel="noopener">{t['share']}</a><a href="{p(l, pj(l))}">{t['back_projects']}</a>{alt_link}</footer>
</article>"""
            ld = {"@context": "https://schema.org", "@graph": [{"@type": "CreativeWork", "name": x["title"], "description": x["summary"], "inLanguage": l,
                  "dateCreated": x["date"].isoformat(), "dateModified": x["updated"].isoformat(), "keywords": ", ".join(x["stack"]),
                  "image": absu(BASE + og_path), "mainEntityOfPage": absu(x["url"]), "author": author_ld(l)},
                  crumbs([(site_title, p(l)), (t["projects"], p(l, pj(l))), (x["title"], x["url"])])]}
            write(OUT / l / pj(l) / x["slug"] / "index.html", page(l, title=x["seo_title"] or x["title"], desc=x["summary"], body=body, url=x["url"], alts=alts,
                                                                    og=BASE + og_path, accent=x["accent"], kind="article", jsonld=ld, active="projects"))
            hashtags = " ".join("#" + re.sub(r"[^\w]", "", g.title().replace(" ", "")) for g in x["stack"])
            write(ROOT / "linkedin" / f"{l}-project-{x['slug']}.txt", f"{x['linkedin'] or x['summary']}\n\n{t['cta']}\n{absu(x['url'])}\n\n{hashtags}\n")

        # artículos
        for x in posts[l]:
            alts = {ol: by_id[ol][x["id"]]["url"] for ol in LANGS if x["id"] in by_id[ol]}
            og_path = f"/assets/og/{l}-{x['slug']}.png"
            og_image(OUT / og_path.lstrip("/"), x["title"], x["id"], x["accent"], site_title, hero=x["hero"], quote=x["quote"])
            tags = "".join(f"<span>{esc(g)}</span>" for g in x["tags"])
            share = f"https://www.linkedin.com/sharing/share-offsite/?url={absu(x['url'])}"
            tname = esc(x["teacher"])
            tlink = f'<a href="{esc(x["teacher_url"])}" rel="noopener" target="_blank">{tname}</a>' if x["teacher_url"] else f"<strong>{tname}</strong>"
            meta_teacher = f'<span>{t["class_by"]} {tname}</span>' if x["teacher"] else ""
            prj = [pby[l][i] for i in x["projects"] if i in pby[l]]
            proj_meta = ("<span>" + t["projects"] + ": " + " · ".join(f'<a href="{q["url"]}">{esc(q["title"])}</a>' for q in prj) + "</span>") if prj else ""
            proj_foot = "".join(f'<a href="{q["url"]}">{t["see_project"]}: {esc(q["title"])}</a>' for q in prj)
            credit = f'<p class="credit">{t["thanks"].format(name=tlink)}</p>' if x["teacher"] else ""
            alt_link = "".join(f'<a href="{u}" hreflang="{ol}" lang="{ol}">{t["other"]}</a>' for ol, u in alts.items() if ol != l)
            afines = sorted([y for y in posts[l] if y["id"] != x["id"]], key=lambda y: (-len(set(y["tags"]) & set(x["tags"])), -y["date"].toordinal()))[:2]
            seguir = f'<section class="section related"><div class="wrap"><h2>{t["keep_reading"]}</h2>{rows(afines, l)}</div></section>' if afines else ""
            body = f"""<article>
<header class="post-head"><div class="wrap"><div>
<div class="post-meta"><time datetime="{x['date'].isoformat()}">{fmt_date(x['date'], l)}</time><span>{x['minutes']} {t['min']}</span>{meta_teacher}{proj_meta}</div>
<h1>{esc(x['title'])}</h1><div class="tags">{tags}</div></div>{hero_svg(x['hero']) or motif_svg(x['id'])}</div></header>
<div class="prose">{x['html']}{credit}</div>
{seguir}{author_box(l)}
<footer class="post-foot"><a href="{share}" target="_blank" rel="noopener">{t['share']}</a><a href="{p(l, 'blog')}">{t['back']}</a>{proj_foot}{alt_link}</footer>
</article>"""
            ld = {"@context": "https://schema.org", "@graph": [{"@type": "BlogPosting", "headline": x["title"], "description": x["summary"],
                  "datePublished": x["date"].isoformat(), "dateModified": x["updated"].isoformat(), "inLanguage": l,
                  "image": absu(BASE + og_path), "keywords": ", ".join(x["tags"]), "mainEntityOfPage": absu(x["url"]),
                  "author": author_ld(l)}, crumbs([(site_title, p(l)), (t["articles"], p(l, "blog")), (x["title"], x["url"])])]}
            write(OUT / l / "blog" / x["slug"] / "index.html", page(l, title=x["seo_title"] or x["title"], desc=x["summary"], body=body, url=x["url"],
                                                                     alts=alts, og=BASE + og_path, accent=x["accent"], kind="article",
                                                                     jsonld=ld, active="blog"))
            # borrador para LinkedIn (fuera de docs, no se publica)
            hook = x["linkedin"] or x["summary"]
            hashtags = " ".join("#" + re.sub(r"[^\w]", "", g.title().replace(" ", "")) for g in x["tags"])
            thanks_line = (t["thanks_short"].format(name=x["teacher"]) + "\n\n") if x["teacher"] else ""
            write(ROOT / "linkedin" / f"{l}-{x['slug']}.txt", f"{hook}\n\n{t['cta']}\n{absu(x['url'])}\n\n{thanks_line}{hashtags}\n")

        # RSS
        items = "".join(
            f"<item><title>{esc(x['title'])}</title><link>{absu(x['url'])}</link><guid isPermaLink=\"true\">{absu(x['url'])}</guid>"
            f"<pubDate>{email.utils.format_datetime(dt.datetime.combine(x['date'], dt.time(8, 0), dt.timezone.utc))}</pubDate>"
            f"<description>{esc(x['summary'])}</description>" + "".join(f"<category>{esc(g)}</category>" for g in x["tags"]) + "</item>"
            for x in posts[l])
        write(OUT / l / "rss.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>
<title>{esc(site_title)}</title><link>{absu(p(l))}</link><description>{esc(CFG['description'][l])}</description><language>{l}</language>
<atom:link href="{absu(p(l))}rss.xml" rel="self" type="application/rss+xml"/>{items}</channel></rss>
""")

    # sitemap con hreflang
    urls = []
    def entry(loc, alts, lastmod=None):
        links = "".join(f'<xhtml:link rel="alternate" hreflang="{a}" href="{absu(h)}"/>' for a, h in alts.items())
        urls.append(f"<url><loc>{absu(loc)}</loc>{f'<lastmod>{lastmod}</lastmod>' if lastmod else ''}{links}</url>")
    for parts in ((), ("blog",), ("about",)):
        for l in LANGS:
            if parts == ("about",) and not (ROOT / "content" / l / "about.md").exists():
                continue
            entry(p(l, *parts), {x: p(x, *parts) for x in LANGS})
    for l in LANGS:
        entry(p(l, pj(l)), {x: p(x, pj(x)) for x in LANGS})
        for x in projects[l]:
            entry(x["url"], {ol: pby[ol][x["id"]]["url"] for ol in LANGS if x["id"] in pby[ol]}, x["updated"].isoformat())
    for l in LANGS:
        for x in posts[l]:
            entry(x["url"], {ol: by_id[ol][x["id"]]["url"] for ol in LANGS if x["id"] in by_id[ol]}, x["updated"].isoformat())
    write(OUT / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                               'xmlns:xhtml="http://www.w3.org/1999/xhtml">' + "".join(urls) + "</urlset>\n")
    write(OUT / "robots.txt", f"User-agent: *\nAllow: /\n\n# Resumen del sitio para modelos de lenguaje: {absu(BASE)}/llms.txt\nSitemap: {absu(BASE)}/sitemap.xml\n")

    # llms.txt y llms-full.txt: el sitio resumido para modelos de lenguaje (https://llmstxt.org)
    def plain(body, l):
        body = re.sub(r"\{\{include:\w+\}\}", "", body)
        body = re.sub(r"\{\{project:([\w-]+)\}\}", lambda m: absu(pby[l][m.group(1)]["url"]), body)
        return re.sub(r"<[^>]+>", "", body).strip()
    resumen = [f"# {CFG['title']['es']}: {CFG['tagline']['es']}", "", f"> {CFG['description']['es']}", "",
               f"Sitio personal y bilingüe (español e inglés) de {CFG['name']}, {CFG['job_title']['es']}. Perfil profesional: {CFG['linkedin']}. "
               "Contiene proyectos (lo que construye, con su estado, herramientas y resultados) y entradas (apuntes con ejemplos propios).", ""]
    completo = list(resumen)
    for l in LANGS:
        t = T[l]
        resumen += [f"## {'Español' if l == 'es' else 'English'}", "", f"### {t['projects']}"] + [f"- [{x['title']}]({absu(x['url'])}): {x['summary']}" for x in reversed(projects[l])]
        resumen += ["", f"### {t['articles']}"] + [f"- [{x['title']}]({absu(x['url'])}): {x['summary']}" for x in posts[l]]
        resumen += ["", f"### {t['about']}", f"- [{t['about']}]({absu(p(l, 'about'))}): {CFG['description'][l]}", ""]
        completo += [f"## {'Español' if l == 'es' else 'English'}", ""]
        for kind, items in (("projects", reversed(projects[l])), ("posts", posts[l])):
            for x in items:
                src = next((q for q in (ROOT / "content" / l / kind).glob("*.md") if parse(q)[0].get("id", q.stem) == x["id"]), None)
                completo += [f"### {x['title']}", f"URL: {absu(x['url'])}", f"Resumen: {x['summary']}", "", plain(parse(src)[1], l) if src else "", ""]
    resumen += ["## Optional", f"- [Mapa del sitio]({absu(BASE)}/sitemap.xml)", f"- [Texto completo]({absu(BASE)}/llms-full.txt)", ""]
    write(OUT / "llms.txt", "\n".join(resumen))
    write(OUT / "llms-full.txt", "\n".join(completo))

    # raíz: elige idioma según el navegador
    links = "".join(f'<li><a href="{p(l)}" hreflang="{l}">{T[l]["name"]}</a></li>' for l in LANGS)
    write(OUT / "index.html", f"""<!doctype html><html lang="{LANGS[0]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(CFG['title'][LANGS[0]])}</title><link rel="canonical" href="{absu(p(LANGS[0]))}">
<link rel="alternate" hreflang="x-default" href="{absu(p(LANGS[0]))}">{"".join(f'<link rel="alternate" hreflang="{l}" href="{absu(p(l))}">' for l in LANGS)}
<noscript><meta http-equiv="refresh" content="0;url={p(LANGS[0])}"></noscript>
<script>(function(){{var S={json.dumps(LANGS)},l=null;try{{l=localStorage.getItem('lang')}}catch(e){{}}if(S.indexOf(l)<0){{l=null;var n=navigator.languages||[navigator.language||''];for(var i=0;i<n.length&&!l;i++){{var c=(n[i]||'').slice(0,2).toLowerCase();if(S.indexOf(c)>-1)l=c}}}}location.replace('{BASE}/'+(l||'{LANGS[0]}')+'/')}})()</script>
</head><body style="font-family:system-ui;padding:2rem"><ul>{links}</ul></body></html>
""")
    write(OUT / "404.html", f"""<!doctype html><html lang="{LANGS[0]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>404</title><meta name="robots" content="noindex"></head><body style="font-family:system-ui;padding:2rem;line-height:1.6">
{"".join(f'<p lang="{l}"><strong>{T[l]["nf"]}.</strong> {T[l]["nf_text"]} <a href="{p(l)}">{T[l]["home"]}</a></p>' for l in LANGS)}
</body></html>
""")
    print("OK:", {l: len(posts[l]) for l in LANGS}, "entradas;", {l: len(projects[l]) for l in LANGS}, "proyectos →", OUT)


if __name__ == "__main__":
    main()
