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
    "es": dict(name="Español", articles="Artículos", about="Sobre mí", latest="Últimos artículos",
               all="Ver todos los artículos", min="min de lectura", topics="Tema", all_topics="Todos",
               skip="Saltar al contenido", theme="Tema", share="Compartir en LinkedIn",
               back="Volver a artículos", other="Read in English", empty="Aún no hay artículos publicados.",
               plot_hint="Toca el gráfico para añadir un dato; la recta se reajusta.", reset="Reiniciar",
               plot_label="Gráfico de puntos con una recta de regresión que se recalcula al añadir datos",
               list_lede="Apuntes y mini proyectos de lo que voy aprendiendo, explicados con mis propios ejemplos.",
               cta="Lo cuento con más detalle en el cuaderno:", nf="Página no encontrada",
               nf_text="Esa página no existe o se ha movido.", home="Ir al inicio", rights="Todos los derechos reservados",
               class_by="Clase de", thanks="Gracias a {name} por la clase en la que se basa este artículo.", thanks_short="Gracias a {name} por la clase."),
    "en": dict(name="English", articles="Articles", about="About", latest="Latest articles",
               all="See all articles", min="min read", topics="Topic", all_topics="All",
               skip="Skip to content", theme="Theme", share="Share on LinkedIn",
               back="Back to articles", other="Leer en español", empty="No articles published yet.",
               plot_hint="Tap the chart to add a data point; the line refits.", reset="Reset",
               plot_label="Scatter plot with a regression line that refits as you add data",
               list_lede="Notes and mini projects from what I'm learning, explained with my own examples.",
               cta="Full write-up in the notebook:", nf="Page not found",
               nf_text="That page doesn't exist or has moved.", home="Go to home", rights="All rights reserved",
               class_by="Class by", thanks="Thanks to {name} for the class this article is based on.", thanks_short="Thanks to {name} for the class."),
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
COOKIE_PTS = [(60, 114), (76, 126), (88, 98), (102, 110), (112, 86), (126, 70), (136, 88), (148, 58), (150, 76), (96, 134), (120, 104)]


def compass_svg():
    s = ['<svg class="motif" viewBox="0 0 260 200" aria-hidden="true" focusable="false">',
         '<g stroke="var(--mute)" stroke-opacity=".5" stroke-width="3" stroke-linecap="round"><line x1="190" y1="120" x2="246" y2="120"/><line x1="176" y1="140" x2="226" y2="140"/><line x1="198" y1="160" x2="240" y2="160"/></g>',
         '<circle cx="95" cy="125" r="62" fill="var(--surface)" stroke="var(--accent)" stroke-width="3"/>',
         '<g stroke="var(--accent)" stroke-width="3" stroke-linecap="round"><line x1="95" y1="69" x2="95" y2="79"/><line x1="95" y1="171" x2="95" y2="181"/><line x1="39" y1="125" x2="49" y2="125"/><line x1="141" y1="125" x2="151" y2="125"/></g>',
         '<g transform="rotate(37 95 125)"><polygon points="95,81 87,125 103,125" fill="var(--accent)"/><polygon points="95,169 87,125 103,125" fill="var(--mute)"/></g>',
         '<circle cx="95" cy="125" r="5" fill="var(--paper)" stroke="var(--accent)" stroke-width="2"/>',
         '<line x1="124" y1="86" x2="158" y2="42" stroke="var(--accent)" stroke-width="2.5" stroke-dasharray="2 7" stroke-linecap="round"/>',
         '<line x1="164" y1="38" x2="164" y2="8" stroke="var(--ink)" stroke-width="3" stroke-linecap="round"/>',
         '<polygon points="164,8 192,18 164,28" fill="var(--accent)"/>', "</svg>"]
    return "".join(s)


def draw_compass(d, col):
    import math
    k, ox, oy = 1.5, 745, 100
    P = lambda x, y: (ox + x * k, oy + y * k)
    mute = (86, 93, 90)
    for (x1, y1, x2, y2) in ((190, 120, 246, 120), (176, 140, 226, 140), (198, 160, 240, 160)):
        d.line([P(x1, y1), P(x2, y2)], fill=mute, width=5)
    cx, cy = P(95, 125)
    d.ellipse([cx - 62 * k, cy - 62 * k, cx + 62 * k, cy + 62 * k], fill="#1E2220", outline=col, width=5)
    for (x1, y1, x2, y2) in ((95, 69, 95, 79), (95, 171, 95, 181), (39, 125, 49, 125), (141, 125, 151, 125)):
        d.line([P(x1, y1), P(x2, y2)], fill=col, width=5)
    a = math.radians(37)
    def rot(x, y):
        dx, dy = x - 95, y - 125
        return P(95 + dx * math.cos(a) - dy * math.sin(a), 125 + dx * math.sin(a) + dy * math.cos(a))
    d.polygon([rot(95, 81), rot(87, 125), rot(103, 125)], fill=col)
    d.polygon([rot(95, 169), rot(87, 125), rot(103, 125)], fill="#98A39E")
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill="#151716", outline=col, width=3)
    (ax, ay), (bx, by) = P(124, 86), P(158, 42)
    n = 9
    for i in range(n + 1):
        px, py = ax + (bx - ax) * i / n, ay + (by - ay) * i / n
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=col)
    d.line([P(164, 38), P(164, 8)], fill="#E9EDEA", width=5)
    d.polygon([P(164, 8), P(192, 18), P(164, 28)], fill=col)


def hero_svg(name):
    if name == "compass":
        return compass_svg()
    if name == "iceberg":
        dots = "".join(f'<circle cx="{x}" cy="{y}" r="3.6" fill="var(--ink)"/>' for x, y in ICE_DOTS)
        return ('<svg class="motif" viewBox="0 0 260 200" aria-hidden="true" focusable="false">'
                '<rect x="0" y="100" width="260" height="100" fill="var(--accent)" fill-opacity=".07"/>'
                f'<polygon points="{_pts(ICE_TIP)}" fill="var(--accent)"/>'
                f'<polygon points="{_pts(ICE_BODY)}" fill="var(--surface)" stroke="var(--accent)" stroke-width="2.5"/>'
                '<line x1="0" y1="100" x2="260" y2="100" stroke="var(--accent)" stroke-opacity=".6" stroke-width="2"/>'
                + dots + '</svg>')
    if name != "cookie":
        return None
    s = ['<svg class="motif" viewBox="0 0 260 200" aria-hidden="true" focusable="false">',
         '<circle cx="105" cy="100" r="72" fill="#D9B25F" stroke="#8A6A1F" stroke-width="2.5"/>',
         '<line x1="14" y1="150" x2="170" y2="41" stroke="var(--paper)" stroke-opacity=".85" stroke-width="8" stroke-linecap="round"/>',
         '<line x1="14" y1="150" x2="170" y2="41" stroke="var(--accent)" stroke-width="3.5" stroke-linecap="round"/>']
    s += [f'<circle cx="{x}" cy="{y}" r="5.2" fill="#5B4010"/>' for x, y in COOKIE_PTS]
    s.append('<rect x="182" y="64" width="68" height="112" rx="7" fill="var(--surface)" stroke="var(--accent)" stroke-width="3"/>')
    s += [f'<line x1="194" y1="{y}" x2="{x2}" y2="{y}" stroke="var(--accent)" stroke-width="3" stroke-linecap="round"/>'
          for y, x2 in ((94, 238), (114, 238), (134, 238), (154, 222))]
    s.append("</svg>")
    return "".join(s)


ICE_TIP = [(86, 100), (112, 52), (124, 62), (148, 24), (180, 100)]
ICE_BODY = [(62, 100), (204, 100), (240, 128), (230, 172), (146, 190), (52, 172), (28, 128)]
ICE_DOTS = [(66, 132), (92, 150), (84, 116), (116, 136), (130, 164), (146, 124), (166, 150), (188, 130), (204, 152), (110, 112), (176, 114), (150, 176)]


def _pts(poly):
    return " ".join(f"{x},{y}" for x, y in poly)


def draw_iceberg(d, col):
    k, ox, oy = 1.5, 745, 100
    P = lambda x, y: (ox + x * k, oy + y * k)
    d.line([P(0, 100), P(260, 100)], fill="#3A6B5F", width=4)
    d.polygon([P(*p) for p in ICE_BODY], fill="#1E2220", outline=col, width=4)
    d.polygon([P(*p) for p in ICE_TIP], fill=col)
    for x, y in ICE_DOTS:
        px, py = P(x, y)
        d.ellipse([px - 5.5, py - 5.5, px + 5.5, py + 5.5], fill="#E9EDEA")


def draw_cookie(d, col):
    k, ox, oy = 1.5, 745, 100
    P = lambda x, y: (ox + x * k, oy + y * k)
    cx, cy = P(105, 100)
    d.ellipse([cx - 72 * k, cy - 72 * k, cx + 72 * k, cy + 72 * k], fill="#D9B25F", outline="#8A6A1F", width=4)
    d.line([P(14, 150), P(170, 41)], fill="#151716", width=14)
    d.line([P(14, 150), P(170, 41)], fill=col, width=7)
    for x, y in COOKIE_PTS:
        px, py = P(x, y)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill="#5B4010")
    x0, y0 = P(182, 64)
    x1, y1 = P(250, 176)
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill="#1E2220", outline=col, width=5)
    for y, xe in ((94, 238), (114, 238), (134, 238), (154, 222)):
        d.line([P(194, y), P(xe, y)], fill=col, width=5)


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
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill="#1E2220")
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill="#1E2220")
    col = ACCENTS.get(accent, ACCENTS["aqua"])
    d.rectangle([0, 0, W, 16], fill=col)
    if hero == "cookie":
        draw_cookie(d, col)
    elif hero == "iceberg":
        draw_iceberg(d, col)
    elif hero == "compass":
        draw_compass(d, col)
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
    full_title = site_title if url == p(lang) else f"{title} | {site_title}"
    alts = alts or {}
    other = [l for l in LANGS if l != lang][0]
    other_href = alts.get(other, p(other))
    og = og or f"{BASE}/assets/og/{lang}-home.png"
    head_alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{absu(h)}">' for l, h in {**alts, lang: url}.items())
    head_alts += f'<link rel="alternate" hreflang="x-default" href="{absu(alts.get(LANGS[0], url) if lang != LANGS[0] else url)}">'
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    v = hashlib.md5((ROOT / "assets/style.css").read_bytes()).hexdigest()[:8]
    nav = (f'<a href="{p(lang, "blog")}"{" aria-current=page" if active == "blog" else ""}>{t["articles"]}</a>'
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
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Figtree:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400&display=swap">
<link rel="stylesheet" href="{BASE}/assets/style.css?v={v}">
{ld}
</head>
<body class="accent-{accent}">
<a class="skip" href="#main">{t['skip']}</a>
<header class="site-head"><div class="wrap">
<a class="brand" href="{p(lang)}">{esc(site_title)}</a>
<nav class="nav" aria-label="Principal">{nav}</nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<span>© {dt.date.today().year} {esc(CFG['name'])}</span>
<span style="display:flex;gap:1.5rem">{foot_links}</span>
</div></footer>
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
    if (ROOT / "content/images").exists():
        shutil.copytree(ROOT / "content/images", OUT / "assets/img")
    (OUT / ".nojekyll").write_text("")
    if CFG.get("custom_domain"):
        (OUT / "CNAME").write_text(CFG["custom_domain"])
    for old in (ROOT / "linkedin").glob("*.txt"):
        old.unlink()

    # 1) cargar artículos
    posts = {l: [] for l in LANGS}
    for l in LANGS:
        for f in sorted((ROOT / "content" / l / "posts").glob("*.md")):
            meta, body = parse(f)
            if str(meta.get("draft", "")).lower() == "true":
                continue
            words = len(re.findall(r"\w+", body))
            body = re.sub(r"\{\{include:(\w+)\}\}", lambda m: (ROOT / "content" / l / "snippets" / f"{m.group(1)}.html").read_text(encoding="utf-8"), body)
            slug = meta.get("slug", f.stem)
            posts[l].append(dict(
                id=meta.get("id", slug), slug=slug, lang=l, title=meta["title"],
                date=dt.date.fromisoformat(meta["date"]),
                updated=dt.date.fromisoformat(meta.get("updated", meta["date"])),
                summary=meta.get("summary", ""), tags=meta.get("tags", []) if isinstance(meta.get("tags", []), list) else [meta["tags"]],
                accent=meta.get("accent", "aqua") if meta.get("accent", "aqua") in ACCENTS else "aqua",
                linkedin=meta.get("linkedin", ""), teacher=meta.get("teacher", ""), order=int(meta.get("order", 0)), quote=meta.get("quote", ""), hero=meta.get("hero", ""), teacher_url=meta.get("teacher_url", ""), html=render_md(body), minutes=max(1, round(words / 200)),
                url=p(l, "blog", slug)))
        posts[l].sort(key=lambda x: (x["date"], x["order"], x["id"]), reverse=True)
    by_id = {l: {x["id"]: x for x in posts[l]} for l in LANGS}

    for l in LANGS:
        t, site_title = T[l], CFG["title"][l]
        og_image(OUT / "assets/og" / f"{l}-home.png", site_title, "home-" + l, "aqua", CFG["name"])
        alts_for = lambda *parts: {x: p(x, *parts) for x in LANGS}

        # inicio
        hero = f"""<section class="hero"><div class="wrap">
<div><h1>{esc(CFG['hero'][l])}</h1><p>{esc(CFG['intro'][l])}</p></div>
<figure class="plot" style="margin:0">
<canvas id="plot" tabindex="0" role="img" aria-label="{esc(t['plot_label'])}"></canvas>
<figcaption class="plot-foot"><span>{t['plot_hint']}</span><button type="button" id="plot-reset">{t['reset']}</button></figcaption>
</figure></div></section>
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

        # sobre mí
        af = ROOT / "content" / l / "about.md"
        if af.exists():
            meta, abody = parse(af)
            body = (f'<section class="section"><div class="prose-head"><h1 class="page-title">{esc(meta.get("title", t["about"]))}</h1></div>'
                    f'<article class="prose" style="margin-top:0">{render_md(abody)}</article></section>')
            write(OUT / l / "about" / "index.html", page(l, title=meta.get("title", t["about"]), desc=meta.get("summary", CFG["description"][l]),
                                                         body=body, url=p(l, "about"), alts=alts_for("about"), active="about"))

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
            credit = f'<p class="credit">{t["thanks"].format(name=tlink)}</p>' if x["teacher"] else ""
            alt_link = "".join(f'<a href="{u}" hreflang="{ol}" lang="{ol}">{t["other"]}</a>' for ol, u in alts.items() if ol != l)
            body = f"""<article>
<header class="post-head"><div class="wrap"><div>
<div class="post-meta"><time datetime="{x['date'].isoformat()}">{fmt_date(x['date'], l)}</time><span>{x['minutes']} {t['min']}</span>{meta_teacher}</div>
<h1>{esc(x['title'])}</h1><div class="tags">{tags}</div></div>{hero_svg(x['hero']) or motif_svg(x['id'])}</div></header>
<div class="prose">{x['html']}{credit}</div>
<footer class="post-foot"><a href="{share}" target="_blank" rel="noopener">{t['share']}</a><a href="{p(l, 'blog')}">{t['back']}</a>{alt_link}</footer>
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
    print("OK:", {l: len(posts[l]) for l in LANGS}, "artículos →", OUT)


if __name__ == "__main__":
    main()
