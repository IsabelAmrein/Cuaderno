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
def hero_svg(name):
    art_file = ROOT / "content" / "art" / f"{name}.svg"
    return art_file.read_text(encoding="utf-8") if art_file.exists() else None


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
    art_png = (ROOT / "content" / "art" / f"{hero}.png") if hero else None
    if art_png and art_png.exists():
        pic = Image.open(art_png).convert("RGBA")
        sc = min(430 / pic.width, 380 / pic.height)
        pic = pic.resize((int(pic.width * sc), int(pic.height * sc)))
        img.paste(pic, (740 + (430 - pic.width) // 2, 130 + (380 - pic.height) // 2), pic)
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
<script>if(!matchMedia('(prefers-reduced-motion: reduce)').matches&&'IntersectionObserver' in window)document.documentElement.classList.add('anim')</script>
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
    shutil.copytree(ROOT / "assets" / "fonts", OUT / "assets" / "fonts")
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
