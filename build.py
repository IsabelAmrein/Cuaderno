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
               projects="Proyectos", all_projects="Ver todos los proyectos", proj_path="proyectos", proj_lede="Lo que estoy construyendo y aprendiendo. Cada proyecto tiene su estado, sus herramientas y sus entradas.",
               st_en_marcha="En marcha", st_terminado="Terminado", st_idea="Idea", related="Entradas relacionadas", part_of="Parte del proyecto", see_project="Ver el proyecto",
               code="Código", demo="Demostración", back_projects="Volver a los proyectos", no_projects="Aún no hay proyectos publicados.", updated="Actualizado",
               all="Ver todas las entradas", min="min de lectura", topics="Tema", all_topics="Todos",
               skip="Saltar al contenido", theme="Tema", share="Compartir en LinkedIn",
               back="Volver a las entradas", other="Read in English", empty="Aún no hay entradas publicadas.",
               list_lede="Apuntes y reflexiones sobre datos, IA y producto, explicados con mis propios ejemplos.",
               cta="Lo cuento con más detalle en Rumbo:", nf="Página no encontrada",
               nf_text="Esa página no existe o se ha movido.", home="Ir al inicio", rights="Todos los derechos reservados",
               thinking="Pensando…", class_by="Clase de", thanks="Gracias a {name} por la clase en la que se basa este artículo.", thanks_short="Gracias a {name} por la clase."),
    "en": dict(name="English", articles="Entries", about="About", latest="Latest entries", see_projects="See the projects", route="Route with flags: each flag is a project", goal="Goal",
               projects="Projects", all_projects="See all projects", proj_path="projects", proj_lede="What I'm building and learning. Each project has its status, tools and entries.",
               st_en_marcha="In progress", st_terminado="Done", st_idea="Idea", related="Related entries", part_of="Part of the project", see_project="See the project",
               code="Code", demo="Demo", back_projects="Back to projects", no_projects="No projects published yet.", updated="Updated",
               all="See all entries", min="min read", topics="Topic", all_topics="All",
               skip="Skip to content", theme="Theme", share="Share on LinkedIn",
               back="Back to entries", other="Leer en español", empty="No entries published yet.",
               list_lede="Notes and reflections on data, AI and product, explained with my own examples.",
               cta="Full write-up on Rumbo:", nf="Page not found",
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


def rumbo_svg(posts, lang, goal_label="", links=True):
    """Portada: una montaña con camino y banderas. posts: entradas de la más antigua a la más reciente (máximo 6)."""
    ST = [(110, 245), (190, 205), (260, 185), (340, 150), (420, 118), (500, 90)]
    posts = posts[-len(ST):]
    s = ['<rect width="680" height="330" rx="12" fill="#0F1E1F"/>']
    s.append('<g fill="#E9EDEA" fill-opacity=".5">' + "".join(f'<circle cx="{x}" cy="{y}" r="1.8"/>' for x, y in [(40, 30), (120, 60), (210, 25), (300, 50), (420, 28), (640, 40), (600, 90), (70, 110)]) + "</g>")
    s += ['<polygon points="0,300 80,205 150,255 225,170 310,300" fill="#1B3335"/>',
          '<polygon points="0,300 60,272 110,245 170,215 230,190 300,165 340,150 400,120 450,100 500,78 540,58 570,50 520,160 470,235 380,300" fill="#7F8C88"/>',
          '<polygon points="110,245 170,215 230,190 300,165 340,150 300,205 200,262 120,290 60,272" fill="#6A7773"/>',
          '<polygon points="570,50 612,112 650,190 680,262 680,300 380,300 470,235 520,160" fill="#3A4542"/>',
          '<polygon points="570,50 534,82 552,90 522,120 556,112 580,96 592,80" fill="#F4FBFA"/><polygon points="570,50 592,80 580,96 556,112 590,125 612,112" fill="#B8D3D5"/>',
          '<rect x="0" y="300" width="680" height="30" rx="12" fill="#0B1413"/><rect x="0" y="300" width="680" height="12" fill="#0B1413"/>',
          '<polyline points="30,284 110,245 190,205 260,185 340,150 420,118 500,90 570,50" fill="none" stroke="#6FE3C5" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>']
    for i, (x, y) in enumerate(ST):
        if i < len(posts):
            ttl = posts[i]["title"]; ttl = ttl if len(ttl) <= 36 else ttl[:35] + "…"
            w = min(len(ttl) * 7.4 + 22, 330); cx = max(w / 2 + 8, min(680 - w / 2 - 8, x))
            op, cl = ((f'<a class="fl" href="{posts[i]["url"]}" aria-label="{esc(posts[i]["title"])}"><title>{esc(posts[i]["title"])}</title>', "</a>") if links else ("<g>", "</g>"))
            s.append(op +
                     f'<rect x="{x-18}" y="{y-48}" width="44" height="58" fill="transparent"/>'
                     f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y-36}" stroke="#E9EDEA" stroke-width="2.5" stroke-linecap="round"/>'
                     f'<polygon points="{x},{y-36} {x+26},{y-27} {x},{y-18}" fill="#6FE3C5"/><circle cx="{x}" cy="{y}" r="5.5" fill="#6FE3C5" stroke="#0F1E1F" stroke-width="2"/>'
                     f'<g class="lb" opacity="0"><rect x="{cx-w/2:.1f}" y="{y-80}" width="{w:.1f}" height="24" rx="8" fill="#1E2220" stroke="#6FE3C5" stroke-opacity=".6"/>'
                     f'<text x="{cx:.1f}" y="{y-63}" text-anchor="middle" fill="#E9EDEA" style="font-family:var(--f-ui);font-size:13px">{esc(ttl)}</text></g>' + cl)
        else:
            s.append(f'<g aria-hidden="true"><line x1="{x}" y1="{y}" x2="{x}" y2="{y-36}" stroke="#E9EDEA" stroke-opacity=".5" stroke-width="2" stroke-dasharray="2 3"/>'
                     f'<polygon points="{x},{y-36} {x+26},{y-27} {x},{y-18}" fill="none" stroke="#6FE3C5" stroke-opacity=".7" stroke-width="1.5" stroke-dasharray="3 3"/>'
                     f'<circle cx="{x}" cy="{y}" r="3.5" fill="none" stroke="#6FE3C5" stroke-opacity=".7"/></g>')
    s.append('<g aria-hidden="true"><line x1="570" y1="50" x2="570" y2="14" stroke="#E9EDEA" stroke-width="3" stroke-linecap="round"/><polygon points="570,14 604,26 570,38" fill="#6FE3C5"/>'
             '<circle cx="570" cy="50" r="6" fill="#6FE3C5" stroke="#0F1E1F" stroke-width="2"/></g>')
    return "".join(s)


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
           f'<a href="{p(lang, "about")}"{" aria-current=page" if active == "about" else ""}>{t["about"]}</a>'
           f'<a href="{other_href}" hreflang="{other}" lang="{other}">{T[other]["name"]}</a>'
           f'<button class="icon-btn" type="button" data-theme-toggle aria-label="{t["theme"]}">{t["theme"]}</button>')
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
    if not posts:
        return f'<p class="empty">{T[lang]["empty"]}</p>'
    out = ['<ul class="log">']
    for x in posts:
        tags = "".join(f"<span>{esc(g)}</span>" for g in x["tags"])
        out.append(
            f'<li data-tags="{esc(",".join(x["tags"]))}"><a class="log-row accent-{x["accent"]}" href="{x["url"]}">'
            f'<time datetime="{x["date"].isoformat()}">{fmt_date(x["date"], lang)}</time>'
            f'<div><h3>{esc(x["title"])}</h3><p>{esc(x["summary"])}</p><span class="tags">{tags}</span></div></a></li>')
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
        out.append(f'<li><a class="log-row accent-{x["accent"]}" href="{x["url"]}">{status_chip(x, lang)}'
                   f'<div><h3>{esc(x["title"])}</h3><p>{esc(x["summary"])}</p><span class="tags">{stack}</span></div></a></li>')
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
                hero=meta.get("hero", ""), linkedin=meta.get("linkedin", ""), related_title=meta.get("related_title", ""), body=body, url=p(l, pj(l), meta.get("slug", f.stem))))
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
                linkedin=meta.get("linkedin", ""), teacher=meta.get("teacher", ""), order=int(meta.get("order", 0)), quote=meta.get("quote", ""), hero=meta.get("hero", ""), teacher_url=meta.get("teacher_url", ""),
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
        ruta = rumbo_svg(projects[l], l)
        hero = f"""<section class="hero"><div class="wrap">
<div class="hero-text"><h1>{esc(CFG['tagline'][l])}</h1><p>{esc(CFG['intro'][l])}</p>
<p class="cta"><a class="btn" href="{p(l, pj(l))}">{t['see_projects']}</a><a class="btn ghost" href="{p(l, 'about')}">{t['about']}</a></p></div>
<div class="hero-art"><svg viewBox="0 0 680 330" role="group" aria-label="{esc(t['route'])}">{ruta}</svg></div></div></section>
<section class="section"><div class="wrap"><h2>{t['projects']}</h2>{proj_rows(list(reversed(projects[l])), l)}
<p class="more"><a href="{p(l, pj(l))}">{t['all_projects']}</a></p></div></section>
<section class="section"><div class="wrap"><h2>{t['latest']}</h2>{rows(posts[l][:5], l)}
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
        write(OUT / l / "blog" / "index.html", page(l, title=t["articles"], desc=t["list_lede"], body=body,
                                                    url=p(l, "blog"), alts=alts_for("blog"), active="blog"))

        # lista de proyectos
        body = f'<section class="section"><div class="wrap"><h1 class="page-title">{t["projects"]}</h1><p class="lede">{t["proj_lede"]}</p>{proj_rows(list(reversed(projects[l])), l)}</div></section>'
        write(OUT / l / pj(l) / "index.html", page(l, title=t["projects"], desc=t["proj_lede"], body=body, url=p(l, pj(l)),
                                                   alts={x: p(x, pj(x)) for x in LANGS}, active="projects"))

        # sobre mí
        af = ROOT / "content" / l / "about.md"
        if af.exists():
            meta, abody = parse(af)
            body = (f'<section class="section"><div class="prose-head"><h1 class="page-title">{esc(meta.get("title", t["about"]))}</h1></div>'
                    f'<article class="prose" style="margin-top:0">{render_md(abody)}</article></section>')
            write(OUT / l / "about" / "index.html", page(l, title=meta.get("title", t["about"]), desc=meta.get("summary", CFG["description"][l]),
                                                         body=body, url=p(l, "about"), alts=alts_for("about"), active="about"))

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
            body = f"""<article>
<header class="post-head"><div class="wrap"><div>
<div class="post-meta">{status_chip(x, l)}<time datetime="{x['updated'].isoformat()}">{t['updated']} {fmt_date(x['updated'], l)}</time></div>
<h1>{esc(x['title'])}</h1>{sub}<div class="tags">{stack}</div>{enl}</div>{hero_svg(x['hero']) or motif_svg(x['id'])}</div></header>
<div class="prose">{x['html']}</div>
{relsec}
<footer class="post-foot"><a href="{share}" target="_blank" rel="noopener">{t['share']}</a><a href="{p(l, pj(l))}">{t['back_projects']}</a>{alt_link}</footer>
</article>"""
            ld = {"@context": "https://schema.org", "@type": "CreativeWork", "name": x["title"], "description": x["summary"], "inLanguage": l,
                  "dateCreated": x["date"].isoformat(), "dateModified": x["updated"].isoformat(), "keywords": ", ".join(x["stack"]),
                  "image": absu(BASE + og_path), "mainEntityOfPage": absu(x["url"]), "author": author_ld(l)}
            write(OUT / l / pj(l) / x["slug"] / "index.html", page(l, title=x["title"], desc=x["summary"], body=body, url=x["url"], alts=alts,
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
            body = f"""<article>
<header class="post-head"><div class="wrap"><div>
<div class="post-meta"><time datetime="{x['date'].isoformat()}">{fmt_date(x['date'], l)}</time><span>{x['minutes']} {t['min']}</span>{meta_teacher}{proj_meta}</div>
<h1>{esc(x['title'])}</h1><div class="tags">{tags}</div></div>{hero_svg(x['hero']) or motif_svg(x['id'])}</div></header>
<div class="prose">{x['html']}{credit}</div>
<footer class="post-foot"><a href="{share}" target="_blank" rel="noopener">{t['share']}</a><a href="{p(l, 'blog')}">{t['back']}</a>{proj_foot}{alt_link}</footer>
</article>"""
            ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": x["title"], "description": x["summary"],
                  "datePublished": x["date"].isoformat(), "dateModified": x["updated"].isoformat(), "inLanguage": l,
                  "image": absu(BASE + og_path), "keywords": ", ".join(x["tags"]), "mainEntityOfPage": absu(x["url"]),
                  "author": author_ld(l)}
            write(OUT / l / "blog" / x["slug"] / "index.html", page(l, title=x["title"], desc=x["summary"], body=body, url=x["url"],
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
    write(OUT / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {absu(BASE)}/sitemap.xml\n")

    # raíz: elige idioma según el navegador
    links = "".join(f'<li><a href="{p(l)}" hreflang="{l}">{T[l]["name"]}</a></li>' for l in LANGS)
    write(OUT / "index.html", f"""<!doctype html><html lang="{LANGS[0]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(CFG['title'][LANGS[0]])}</title><link rel="canonical" href="{absu(p(LANGS[0]))}">
<link rel="alternate" hreflang="x-default" href="{absu(p(LANGS[0]))}">{"".join(f'<link rel="alternate" hreflang="{l}" href="{absu(p(l))}">' for l in LANGS)}
<noscript><meta http-equiv="refresh" content="0;url={p(LANGS[0])}"></noscript>
<script>var l=(navigator.language||'{LANGS[0]}').slice(0,2);location.replace('{BASE}/'+({json.dumps(LANGS)}.indexOf(l)>-1?l:'{LANGS[0]}')+'/')</script>
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
