"""Ilustraciones semirrealistas del cuaderno: formas vectoriales con luces y sombras (sin degradados ni filtros)."""
UI = "font-family:var(--f-ui)"
DI = "font-family:var(--f-display)"
CHIP = "-14,-6 -5,-14 8,-11 15,-2 9,10 -6,12 -15,5"
CHIP_HI = "-9,-5 -3,-10 5,-8 6,-3"


def _svg(vb_w, vb_h, body, inner_title=None, desc=None, deco=True, vb=None):
    if deco:
        return f'<svg class="motif" viewBox="{vb or f"0 0 {vb_w} {vb_h}"}" aria-hidden="true" focusable="false">{body}</svg>'
    return (f'<svg width="100%" viewBox="0 0 {vb_w} {vb_h}" role="img"><title>{inner_title}</title><desc>{desc}</desc>{body}</svg>')


# ---------- galleta ----------
def cookie_scene(deco=True, crop=False):
    bumps = [(443, 244.5), (408.3, 282.5), (360.7, 302.2), (309.2, 299.9), (263.5, 276.2), (232.1, 235.3), (221, 185), (232.1, 134.7), (263.5, 93.8), (309.2, 70.1)]
    chips = [(275, 140, 15, 1), (330, 118, -20, .9), (300, 192, 40, 1.1), (378, 178, -10, .95), (262, 218, 70, 1), (345, 245, -35, 1.05),
             (405, 230, 25, .9), (252, 170, -50, .85), (370, 275, 10, .9), (300, 272, -15, .85)]
    sp = [(290, 110), (355, 95), (262, 160), (318, 168), (395, 200), (285, 250), (335, 222), (420, 262), (240, 205), (360, 262), (305, 300), (380, 140)]
    b = ('<defs><clipPath id="ckc"><circle cx="340" cy="185" r="122"/></clipPath></defs>'
         '<rect x="0" y="0" width="680" height="370" rx="12" fill="#151716"/>'
         '<ellipse cx="340" cy="322" rx="132" ry="18" fill="#000" fill-opacity=".4"/>')
    b += '<g fill="#D3A257">' + "".join(f'<circle cx="{x}" cy="{y}" r="9"/>' for x, y in bumps) + "</g>"
    b += '<circle cx="340" cy="185" r="119" fill="#D9A95B"/><g clip-path="url(#ckc)">'
    b += '<ellipse cx="300" cy="135" rx="80" ry="52" transform="rotate(-25 300 135)" fill="#E8C27D" fill-opacity=".55"/>'
    b += '<ellipse cx="392" cy="245" rx="82" ry="56" transform="rotate(-25 392 245)" fill="#B07F3A" fill-opacity=".35"/>'
    b += '<circle cx="340" cy="185" r="115" fill="none" stroke="#B98A42" stroke-width="8"/>'
    b += '<g fill="#C28F43" fill-opacity=".65">' + "".join(f'<circle cx="{x}" cy="{y}" r="2.2"/>' for x, y in sp) + "</g>"
    b += '<g fill="#4A2B12">' + "".join(f'<g transform="translate({x} {y}) rotate({r}) scale({s})"><polygon points="{CHIP}"/><polygon points="{CHIP_HI}" fill="#7A4C25"/></g>' for x, y, r, s in chips) + "</g>"
    b += '<g fill="none" stroke="#F2DDA6" stroke-width="8"><circle cx="440" cy="100" r="44"/><circle cx="470" cy="142" r="26"/><circle cx="404" cy="70" r="26"/></g>'
    b += '<g fill="#151716"><circle cx="440" cy="100" r="40"/><circle cx="470" cy="142" r="22"/><circle cx="404" cy="70" r="22"/></g></g>'
    b += '<g fill="#D9A95B"><circle cx="458" cy="304" r="4"/><circle cx="484" cy="314" r="3"/><circle cx="432" cy="316" r="3"/><circle cx="500" cy="296" r="2.5"/></g>'
    return _svg(680, 370, b, "Galleta mordida con pepitas de chocolate", "Ilustración semirrealista de una galleta dorada con pepitas y un mordisco.", deco, vb="196 44 288 306" if crop else None)


def cookie_icon(cx, cy):
    chips = [(-9, -6, 10), (8, -10, -20), (-2, 4, 35), (11, 7, 5), (-12, 10, -40)]
    s = f'<ellipse cx="{cx}" cy="{cy+27}" rx="23" ry="5" fill="#000" fill-opacity=".3"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="26" fill="#D9A95B"/><circle cx="{cx}" cy="{cy}" r="23" fill="none" stroke="#B98A42" stroke-width="4"/>'
    s += f'<ellipse cx="{cx-8}" cy="{cy-9}" rx="12" ry="8" transform="rotate(-25 {cx-8} {cy-9})" fill="#E8C27D" fill-opacity=".6"/>'
    s += "".join(f'<g transform="translate({cx+x} {cy+y}) rotate({r}) scale(.38)"><polygon points="{CHIP}" fill="#4A2B12"/><polygon points="{CHIP_HI}" fill="#7A4C25"/></g>' for x, y, r in chips)
    return s


def ingredients_icon(cx, cy):
    s = f'<ellipse cx="{cx}" cy="{cy+16}" rx="40" ry="5" fill="#000" fill-opacity=".25"/>'
    s += f'<circle cx="{cx-26}" cy="{cy}" r="13" fill="#F1E4C3" stroke="#CDBE98" stroke-width="1.5"/><ellipse cx="{cx-30}" cy="{cy-5}" rx="5" ry="3.5" fill="#FFFFFF" fill-opacity=".7"/>'
    s += f'<rect x="{cx-12}" y="{cy-10}" width="26" height="22" rx="3" fill="#D8B23E"/><polygon points="{cx-12},{cy-10} {cx+14},{cy-10} {cx+20},{cy-15} {cx-6},{cy-15}" fill="#F0D874"/><polygon points="{cx+14},{cy-10} {cx+20},{cy-15} {cx+20},{cy+7} {cx+14},{cy+12}" fill="#B8932B"/>'
    s += f'<circle cx="{cx+34}" cy="{cy}" r="13" fill="#B98B5A" stroke="#8F6A41" stroke-width="1.5"/><ellipse cx="{cx+30}" cy="{cy-5}" rx="5" ry="3.5" fill="#E2C39A" fill-opacity=".8"/>'
    return s


def recipe_icon(cx, cy):
    s = f'<g transform="rotate(-5 {cx} {cy})"><rect x="{cx-20}" y="{cy-26}" width="40" height="52" rx="3" fill="#F3EBD8" stroke="#C9BFA5" stroke-width="1.5"/>'
    s += f'<polygon points="{cx+10},{cy-26} {cx+20},{cy-26} {cx+20},{cy-16}" fill="#D8CDB0"/>'
    s += "".join(f'<line x1="{cx-13}" y1="{cy-14+i*10}" x2="{cx+(8 if i%2 else 13)}" y2="{cy-14+i*10}" stroke="#8A7F66" stroke-width="2.5" stroke-linecap="round"/>' for i in range(4))
    return s + "</g>"


# ---------- brújula ----------
def compass_scene(deco=True, crop=False):
    b = ('<rect x="0" y="0" width="680" height="370" rx="12" fill="#151716"/>'
         '<ellipse cx="340" cy="328" rx="128" ry="16" fill="#000" fill-opacity=".4"/>'
         '<circle cx="340" cy="180" r="134" fill="#8B9599"/><circle cx="340" cy="180" r="124" fill="#C3CBCE"/>'
         '<path d="M224.4 137.9 A123 123 0 0 1 382.1 64.4" fill="none" stroke="#F1F5F6" stroke-width="9" stroke-linecap="round"/>'
         '<path d="M455.6 222.1 A123 123 0 0 1 297.9 295.6" fill="none" stroke="#5E686C" stroke-width="9" stroke-linecap="round"/>'
         '<circle cx="340" cy="180" r="112" fill="#7C868A"/><circle cx="340" cy="180" r="106" fill="#1B201E"/>'
         '<g transform="rotate(-90 340 180)"><circle cx="340" cy="180" r="96" fill="none" stroke="#8FA09A" stroke-width="10" stroke-dasharray="2.4 15.05" stroke-dashoffset="1.2"/>'
         '<circle cx="340" cy="180" r="96" fill="none" stroke="#6FE3C5" stroke-width="16" stroke-dasharray="3.5 48.86" stroke-dashoffset="1.75"/></g>'
         '<circle cx="340" cy="180" r="72" fill="none" stroke="#2C3230" stroke-width="2"/>'
         '<polygon points="340,84 331,102 349,102" fill="#6FE3C5"/>'
         '<g class="cp-needle" transform="rotate(55 340 180)"><polygon points="340,100 326,180 340,180" fill="#7EF0D6"/><polygon points="340,100 354,180 340,180" fill="#2FA88F"/>'
         '<polygon points="340,260 326,180 340,180" fill="#E4E9E7"/><polygon points="340,260 354,180 340,180" fill="#9AA3A0"/></g>'
         '<circle cx="340" cy="180" r="11" fill="#AEB7BA" stroke="#6E787C" stroke-width="2"/><circle cx="340" cy="180" r="4.5" fill="#1B201E"/><circle cx="337" cy="176" r="2" fill="#FFFFFF"/>'
         '<ellipse cx="294" cy="126" rx="72" ry="30" transform="rotate(-32 294 126)" fill="#FFFFFF" fill-opacity=".09"/>'
         '<path d="M258 120 A92 92 0 0 1 330 92" fill="none" stroke="#FFFFFF" stroke-opacity=".25" stroke-width="3" stroke-linecap="round"/>'
         '<circle class="cp-dot" style="--d:1.20s" cx="414.0" cy="128.0" r="3.2" fill="#6FE3C5"/><circle class="cp-dot" style="--d:1.32s" cx="429.3" cy="117.3" r="3.2" fill="#6FE3C5"/><circle class="cp-dot" style="--d:1.44s" cx="444.7" cy="106.7" r="3.2" fill="#6FE3C5"/><circle class="cp-dot" style="--d:1.56s" cx="460.0" cy="96.0" r="3.2" fill="#6FE3C5"/><circle class="cp-dot" style="--d:1.68s" cx="475.3" cy="85.3" r="3.2" fill="#6FE3C5"/><circle class="cp-dot" style="--d:1.80s" cx="490.7" cy="74.7" r="3.2" fill="#6FE3C5"/><circle class="cp-dot" style="--d:1.92s" cx="506.0" cy="64.0" r="3.2" fill="#6FE3C5"/>'
         '<ellipse cx="512" cy="62" rx="14" ry="5" fill="#000" fill-opacity=".35"/>'
         '<g class="cp-flag"><line x1="512" y1="60" x2="512" y2="20" stroke="#E9EDEA" stroke-width="3.5" stroke-linecap="round"/><polygon points="512,20 546,31 512,42" fill="#6FE3C5"/></g>')
    return _svg(680, 370, b, "Brújula con aro metálico y aguja en aguamarina", "Ilustración semirrealista de una brújula.", deco, vb="196 10 372 350" if crop else None)


# ---------- iceberg ----------
TIP = ('<polygon points="225,172 275,97 300,117 355,47 420,172" fill="#CDEAEA"/><polygon points="355,47 300,117 285,172 345,172" fill="#F4FBFA"/>'
       '<polygon points="355,47 345,172 420,172" fill="#A5D8DB"/><polygon points="275,97 300,117 285,172 225,172" fill="#CDEAEA"/>'
       '<polygon points="300,117 322,130 312,172 285,172" fill="#8CC3C9"/>'
       '<rect x="0" y="172" width="680" height="3" fill="#BFF4EA" fill-opacity=".7"/>'
       '<g fill="#BFF4EA" fill-opacity=".35"><rect x="120" y="182" width="80" height="2"/><rect x="470" y="184" width="100" height="2"/><rect x="200" y="192" width="50" height="2"/><rect x="500" y="196" width="60" height="2"/></g>')


def iceberg_scene(deco=True):
    b = ('<rect x="0" y="0" width="680" height="400" rx="12" fill="#0F1E1F"/><rect x="0" y="172" width="680" height="228" fill="#0E4A50"/>'
         '<rect x="0" y="262" width="680" height="138" fill="#0A3C42"/><rect x="0" y="332" width="680" height="68" fill="#072C31"/>'
         '<polygon points="200,174 445,174 500,217 485,292 380,337 250,344 175,292 160,217" fill="#5FC4C0" fill-opacity=".55"/>'
         '<polygon points="300,174 445,174 500,217 380,252" fill="#7EDAD4" fill-opacity=".35"/><polygon points="160,217 200,174 300,174 250,262" fill="#3FA9A8" fill-opacity=".35"/>'
         '<polygon points="250,344 380,337 380,252 250,262 175,292" fill="#2E8E90" fill-opacity=".3"/>'
         '<g fill="#D8FFF7" fill-opacity=".7">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in
          [(250, 215, 4), (310, 238, 3), (360, 205, 4), (420, 232, 3), (465, 250, 4), (215, 262, 3), (290, 290, 4), (345, 272, 3), (410, 300, 4), (320, 320, 3), (380, 228, 3), (270, 248, 3)]) + "</g>" + TIP)
    return _svg(680, 400, b, "Iceberg con burbujas de datos bajo el agua", "Ilustración semirrealista de un iceberg.", deco)


def iceberg_diagram(lang):
    L = {"es": dict(chips=["Recogida de datos", "Verificación de datos", "Extracción de características", "Configuración", "Gestión de recursos", "Herramientas de análisis", "Infraestructura de servicio", "Monitorización"],
                    tip=("Código", "del modelo"), seen="Lo que se ve", below="Lo que hay que sostener",
                    label="Iceberg: sobre el agua, el código del modelo; bajo el agua, recogida y verificación de datos, extracción de características, configuración, gestión de recursos, herramientas de análisis, infraestructura de servicio y monitorización.",
                    cap="Construir el modelo es solo la punta: casi todo el trabajo está bajo el agua."),
         "en": dict(chips=["Data collection", "Data verification", "Feature extraction", "Configuration", "Resource management", "Analysis tools", "Serving infrastructure", "Monitoring"],
                    tip=("Model", "code"), seen="What you see", below="What has to be maintained",
                    label="Iceberg: above the water, the model code; below it, data collection and verification, feature extraction, configuration, resource management, analysis tools, serving infrastructure and monitoring.",
                    cap="Building the model is only the tip: most of the work is under the water.")}[lang]
    b = ('<rect x="0" y="0" width="680" height="572" rx="12" fill="#0F1E1F"/><rect x="0" y="172" width="680" height="400" fill="#0E4A50"/>'
         '<rect x="0" y="300" width="680" height="272" fill="#0A3C42"/><rect x="0" y="440" width="680" height="132" fill="#072C31"/>'
         '<polygon points="150,174 530,174 640,230 650,430 560,512 130,522 30,440 40,230" fill="#5FC4C0" fill-opacity=".45"/>'
         '<polygon points="300,174 530,174 640,230 450,290" fill="#7EDAD4" fill-opacity=".3"/><polygon points="40,230 150,174 300,174 240,300" fill="#3FA9A8" fill-opacity=".3"/>'
         '<polygon points="130,522 560,512 450,290 240,300 30,440" fill="#2E8E90" fill-opacity=".25"/>' + TIP)
    b += f'<text x="470" y="98" fill="#6FE3C5" style="{UI};font-size:26px;font-weight:600">{L["tip"][0]}</text><text x="470" y="128" fill="#6FE3C5" style="{UI};font-size:26px;font-weight:600">{L["tip"][1]}</text>'
    b += f'<text x="20" y="156" fill="#98A39E" style="{UI};font-size:19px">{L["seen"]}</text>'
    for i, c in enumerate(L["chips"]):
        x, y = (70 if i % 2 == 0 else 350), 245 + (i // 2) * 58
        b += (f'<rect x="{x}" y="{y}" width="260" height="46" rx="10" fill="#0A2A2E" stroke="#5FC4C0" stroke-opacity=".55" stroke-width="1.5"/>'
              f'<text x="{x+130}" y="{y+30}" text-anchor="middle" fill="#E9EDEA" style="{UI};font-size:17px">{c}</text>')
    b += f'<text x="340" y="552" text-anchor="middle" fill="#98A39E" style="{UI};font-size:19px">{L["below"]}</text>'
    return f'<figure class="diagram"><svg viewBox="0 0 680 572" role="img" aria-label="{L["label"]}">{b}</svg><figcaption>{L["cap"]}</figcaption></figure>'


# ---------- montaña ----------
def mountain_scene(deco=True):
    b = ('<rect x="0" y="0" width="680" height="330" rx="12" fill="#0F1E1F"/>' + _mountain_body())
    return _svg(680, 330, b, "Montaña con camino y bandera", "Ilustración semirrealista de una montaña nevada con camino y campamentos.", deco)


def _mountain_body():
    b = '<g fill="#E9EDEA" fill-opacity=".5">' + "".join(f'<circle cx="{x}" cy="{y}" r="1.8"/>' for x, y in [(40, 30), (120, 60), (210, 25), (300, 50), (420, 28), (640, 40), (600, 90), (70, 110)]) + "</g>"
    b += '<polygon points="0,300 80,205 150,255 225,170 310,300" fill="#1B3335"/>'
    b += '<polygon points="0,300 60,272 110,245 170,215 230,190 300,165 340,150 400,120 450,100 500,78 540,58 570,50 520,160 470,235 380,300" fill="#7F8C88"/>'
    b += '<polygon points="110,245 170,215 230,190 300,165 340,150 300,205 200,262 120,290 60,272" fill="#6A7773"/>'
    b += '<polygon points="570,50 612,112 650,190 680,262 680,300 380,300 470,235 520,160" fill="#3A4542"/>'
    b += '<polygon points="570,50 534,82 552,90 522,120 556,112 580,96 592,80" fill="#F4FBFA"/><polygon points="570,50 592,80 580,96 556,112 590,125 612,112" fill="#B8D3D5"/>'
    b += '<polyline points="30,284 110,245 190,205 260,185 340,150 420,118 500,90 570,50" fill="none" stroke="#6FE3C5" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>'
    for cx, cy in ((110, 245), (340, 150)):
        b += f'<polygon points="{cx-13},{cy+10} {cx},{cy-14} {cx+13},{cy+10}" fill="#6FE3C5" stroke="#0F1E1F" stroke-width="2"/>'
    b += '<circle cx="570" cy="50" r="7" fill="#6FE3C5" stroke="#0F1E1F" stroke-width="2"/><line x1="570" y1="46" x2="570" y2="14" stroke="#E9EDEA" stroke-width="3" stroke-linecap="round"/><polygon points="570,14 600,24 570,34" fill="#6FE3C5"/>'
    return b


def mountain_diagram(lang):
    L = {"es": dict(cols=[("Datos", ["Reunir y etiquetar", "Limpiar y validar", "Cuidar la calidad"]), ("Modelo", ["Elegir algoritmo", "Evitar sobreajuste", "Validar y probar"]), ("Producción", ["Integrar en sistemas", "Vigilar rendimiento", "Reentrenar"])],
                    loop="Cuando los datos cambian, vuelta a empezar",
                    label="Montaña con tres tramos: datos, modelo y producción, y una flecha de vuelta a empezar cuando los datos cambian.",
                    cap="Un proyecto de ML se sube por tramos, y no termina en la cima: hay que volver a empezar cuando cambian los datos."),
         "en": dict(cols=[("Data", ["Collect and label", "Clean and validate", "Protect quality"]), ("Model", ["Choose algorithm", "Avoid overfitting", "Validate and test"]), ("Production", ["Integrate systems", "Monitor performance", "Retrain"])],
                    loop="When the data changes, start again",
                    label="Mountain with three stages: data, model and production, and an arrow back to the start when the data changes.",
                    cap="An ML project is climbed in stages, and it doesn't end at the summit: you start again when the data changes.")}[lang]
    b = '<rect x="0" y="0" width="680" height="530" rx="12" fill="#0F1E1F"/>' + _mountain_body() + '<rect x="0" y="300" width="680" height="230" rx="12" fill="#0B1413"/><rect x="0" y="300" width="680" height="30" fill="#0B1413"/>'
    for (cx, cy), (head, lines) in zip(((110, 255), (340, 160), (570, 60)), L["cols"]):
        b += f'<line x1="{cx}" y1="{cy+12}" x2="{cx}" y2="318" stroke="#6FE3C5" stroke-opacity=".35" stroke-width="2" stroke-dasharray="3 6"/>'
        b += f'<text x="{cx}" y="352" text-anchor="middle" fill="#6FE3C5" style="{DI};font-size:30px;font-weight:500">{head}</text>'
        for i, ln in enumerate(lines):
            b += f'<text x="{cx}" y="{388+i*29}" text-anchor="middle" fill="#E9EDEA" style="{UI};font-size:20px">{ln}</text>'
    b += ('<path d="M570 468 V478 Q570 494 554 494 H126 Q110 494 110 478 V474" fill="none" stroke="#98A39E" stroke-width="2.5" stroke-linecap="round"/>'
          '<polygon points="110,464 102,478 118,478" fill="#98A39E"/>'
          f'<text x="340" y="522" text-anchor="middle" fill="#98A39E" style="{UI};font-size:19px">{L["loop"]}</text>')
    return f'<figure class="diagram"><svg viewBox="0 0 680 534" role="img" aria-label="{L["label"]}">{b}</svg><figcaption>{L["cap"]}</figcaption></figure>'


# ---------- receta de galletas (diagrama) ----------
def galletas(lang):
    L = {"es": dict(t1="Programación tradicional", s1="Tú escribes la receta", t2="Machine Learning", s2="El algoritmo descubre la receta",
                    ing="Ingredientes", ing_s="los datos", rec="Receta", rec_s="las reglas", rec_m="el modelo", coo="Galletas", coo_s="las respuestas",
                    tag1="la escribes tú", tag2="la descubre el algoritmo",
                    label="Diagrama de la receta de galletas: en programación tradicional, ingredientes más receta dan galletas; en Machine Learning, ingredientes más galletas ya hechas dan la receta.",
                    cap="La receta de galletas: en programación tradicional escribes la receta; en Machine Learning, la receta es lo que aprende el algoritmo."),
         "en": dict(t1="Traditional programming", s1="You write the recipe", t2="Machine learning", s2="The algorithm discovers the recipe",
                    ing="Ingredients", ing_s="the data", rec="Recipe", rec_s="the rules", rec_m="the model", coo="Cookies", coo_s="the answers",
                    tag1="you write it", tag2="the algorithm finds it",
                    label="Cookie recipe diagram: in traditional programming, ingredients plus a recipe give cookies; in machine learning, ingredients plus finished cookies give the recipe.",
                    cap="The cookie recipe: in traditional programming you write the recipe; in machine learning, the recipe is what the algorithm learns.")}[lang]
    BW, BH, xs = 180, 120, [20, 250, 480]
    def icon(kind, cx, top):
        cy = top + 40
        return ingredients_icon(cx, cy) if kind == "ing" else recipe_icon(cx, cy) if kind == "rec" else cookie_icon(cx, cy)
    def box(i, kind, main, sub, oy, hi=False):
        x, top = xs[i], oy + 80
        cx = x + BW // 2
        stroke = ("var(--accent)", 3) if hi else ("var(--line)", 1.5)
        col = "var(--accent)" if hi else "var(--ink)"
        return (f'<rect x="{x}" y="{top}" width="{BW}" height="{BH}" rx="12" fill="var(--surface)" stroke="{stroke[0]}" stroke-width="{stroke[1]}"/>'
                + icon(kind, cx, top)
                + f'<text x="{cx}" y="{top+88}" text-anchor="middle" fill="{col}" style="{UI};font-size:24px;font-weight:600">{main}</text>'
                + f'<text x="{cx}" y="{top+110}" text-anchor="middle" fill="var(--mute)" style="{UI};font-size:18px">{sub}</text>')
    def lane(oy, title, sub, kinds, tag, tag_i):
        s = (f'<text x="20" y="{oy+32}" fill="var(--accent)" style="{DI};font-size:30px;font-weight:500">{title}</text>'
             f'<text x="20" y="{oy+58}" fill="var(--mute)" style="{UI};font-size:19px">{sub}</text>')
        for i, (k, m, sb, hi) in enumerate(kinds):
            s += box(i, k, m, sb, oy, hi)
        top = oy + 80
        s += f'<text x="{xs[0]+BW+25}" y="{top+72}" text-anchor="middle" fill="var(--mute)" style="{UI};font-size:34px">+</text>'
        ax, ay = xs[1] + BW + 8, top + 60
        s += (f'<line x1="{ax}" y1="{ay}" x2="{ax+26}" y2="{ay}" stroke="var(--mute)" stroke-width="3" stroke-linecap="round"/>'
              f'<polygon points="{ax+38},{ay} {ax+24},{ay-8} {ax+24},{ay+8}" fill="var(--mute)"/>')
        if tag_i == 2:
            s += f'<text x="662" y="{oy+226}" text-anchor="end" fill="var(--accent)" style="{UI};font-size:18px;font-weight:600">{tag}</text>'
        else:
            s += f'<text x="{xs[tag_i]+BW//2}" y="{oy+226}" text-anchor="middle" fill="var(--accent)" style="{UI};font-size:18px;font-weight:600">{tag}</text>'
        return s
    body = lane(0, L["t1"], L["s1"], [("ing", L["ing"], L["ing_s"], False), ("rec", L["rec"], L["rec_s"], True), ("coo", L["coo"], L["coo_s"], False)], L["tag1"], 1)
    body += '<line x1="20" y1="268" x2="660" y2="268" stroke="var(--line)" stroke-dasharray="5 6"/>'
    body += lane(290, L["t2"], L["s2"], [("ing", L["ing"], L["ing_s"], False), ("coo", L["coo"], L["coo_s"], False), ("rec", L["rec"], L["rec_m"], True)], L["tag2"], 2)
    return f'<figure class="diagram"><svg viewBox="0 0 680 540" role="img" aria-label="{L["label"]}">{body}</svg><figcaption>{L["cap"]}</figcaption></figure>'


# ---------- contenedores de reciclaje (cabecera del clasificador) ----------
def bins_scene(deco=True, crop=False):
    b = '<rect x="0" y="0" width="680" height="370" rx="12" fill="#0F1E1F"/>'
    b += '<g fill="#E9EDEA" fill-opacity=".5">' + "".join(f'<circle cx="{x}" cy="{y}" r="1.8"/>' for x, y in [(40, 30), (120, 60), (300, 26), (420, 40), (600, 34), (640, 90), (70, 120)]) + "</g>"
    b += '<rect x="0" y="318" width="680" height="52" rx="12" fill="#0B1413"/><rect x="0" y="318" width="680" height="14" fill="#0B1413"/>'
    pal = [("#E3B72E", "#B8912A", "#F2CD54"), ("#3F73C4", "#2F5896", "#5E92E0"), ("#3E9A5A", "#2F7544", "#5CB878"), ("#7D8789", "#5E686A", "#A0AAAC")]
    xs = [105, 225, 345, 465]
    for x, (main, shade, lid) in zip(xs, pal):
        b += f'<ellipse cx="{x+50}" cy="322" rx="58" ry="8" fill="#000" fill-opacity=".4"/>'
        b += f'<polygon points="{x},160 {x+100},160 {x+92},316 {x+8},316" fill="{main}"/>'
        b += f'<polygon points="{x+66},160 {x+100},160 {x+92},316 {x+62},316" fill="{shade}"/>'
        b += f'<polygon points="{x+6},166 {x+16},166 {x+22},310 {x+12},310" fill="#FFFFFF" fill-opacity=".14"/>'
        b += f'<rect x="{x+34}" y="130" width="32" height="12" rx="5" fill="{lid}"/>'
        b += f'<rect x="{x-6}" y="140" width="112" height="22" rx="6" fill="{lid}"/><rect x="{x-6}" y="154" width="112" height="8" rx="4" fill="{shade}" fill-opacity=".55"/>'
        b += f'<circle cx="{x+18}" cy="316" r="7" fill="#1B201E"/><circle cx="{x+82}" cy="316" r="7" fill="#1B201E"/>'
    ic = '#F4FBFA'
    b += f'<g fill="{ic}" fill-opacity=".92"><rect x="143" y="214" width="24" height="34" rx="3"/><ellipse cx="155" cy="214" rx="12" ry="3.5"/></g>'
    b += f'<g fill="{ic}" fill-opacity=".92"><rect x="261" y="208" width="28" height="38" rx="3"/></g><g stroke="#3F73C4" stroke-width="2.5" stroke-linecap="round"><line x1="267" y1="219" x2="283" y2="219"/><line x1="267" y1="227" x2="283" y2="227"/><line x1="267" y1="235" x2="278" y2="235"/></g>'
    b += f'<g fill="{ic}" fill-opacity=".92"><rect x="385" y="224" width="20" height="28" rx="4"/><rect x="391" y="210" width="8" height="16" rx="2"/></g>'
    b += f'<g fill="{ic}" fill-opacity=".92"><rect x="501" y="216" width="28" height="32" rx="3"/></g><path d="M507 216 C507 204 523 204 523 216" fill="none" stroke="{ic}" stroke-opacity=".92" stroke-width="3"/>'
    b += '<g transform="rotate(24 160 80)"><rect x="152" y="62" width="16" height="36" rx="4" fill="#CFE9F5" fill-opacity=".92"/><rect x="157" y="50" width="6" height="14" rx="2" fill="#CFE9F5" fill-opacity=".92"/><rect x="156" y="46" width="8" height="5" rx="2" fill="#6FE3C5"/></g>'
    b += '<path d="M214 34 C200 62 186 94 170 126" fill="none" stroke="#6FE3C5" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/><polygon points="170,128 163,114 177,116" fill="#6FE3C5"/>'
    return _svg(680, 370, b, "Cuatro contenedores de reciclaje: amarillo, azul, verde y gris", "Ilustración semirrealista de cuatro contenedores con una botella cayendo en el amarillo.", deco, vb="84 28 508 304" if crop else None)
