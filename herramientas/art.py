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
CP_DEFS = ('<defs>'
           '<linearGradient id="cp-bezel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FAFCFC"/><stop offset=".28" stop-color="#9CA6AA"/><stop offset=".52" stop-color="#E6EBED"/><stop offset=".78" stop-color="#6F797D"/><stop offset="1" stop-color="#C9D0D3"/></linearGradient>'
           '<linearGradient id="cp-bezel2" x1="1" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#788286"/><stop offset="1" stop-color="#2F3638"/></linearGradient>'
           '<radialGradient id="cp-face" cx=".4" cy=".34" r=".8"><stop offset="0" stop-color="#37443F"/><stop offset=".6" stop-color="#1B221F"/><stop offset="1" stop-color="#0C100F"/></radialGradient>'
           '<linearGradient id="cp-glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".26"/><stop offset=".42" stop-color="#FFFFFF" stop-opacity=".04"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
           '<linearGradient id="cp-nl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C6FFF1"/><stop offset="1" stop-color="#6FE3C5"/></linearGradient>'
           '<linearGradient id="cp-nr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#37BFA0"/><stop offset="1" stop-color="#1B6B5C"/></linearGradient>'
           '<linearGradient id="cp-sl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#C5CDCA"/></linearGradient>'
           '<linearGradient id="cp-sr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#AEB8B5"/><stop offset="1" stop-color="#737D7A"/></linearGradient>'
           '<radialGradient id="cp-cap" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#F4F7F8"/><stop offset="1" stop-color="#7F898D"/></radialGradient>'
           '<radialGradient id="cp-shadow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".6"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
           '<radialGradient id="cp-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#A9F6E2" stop-opacity=".55"/><stop offset="1" stop-color="#6FE3C5" stop-opacity="0"/></radialGradient>'
           '<linearGradient id="cp-flag" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A9F6E2"/><stop offset="1" stop-color="#38C3A2"/></linearGradient>'
           '<radialGradient id="cp-vg" cx=".5" cy=".5" r=".78"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".42"/></radialGradient>'
           '</defs>')


def compass_scene(deco=True, crop=False):
    b = (CP_DEFS + '<rect x="0" y="0" width="680" height="370" rx="12" fill="#151716"/>'
         '<ellipse cx="340" cy="334" rx="150" ry="20" fill="url(#cp-shadow)"/>'
         '<circle cx="512" cy="52" r="62" fill="url(#cp-glow)"/>'
         '<circle cx="340" cy="180" r="134" fill="url(#cp-bezel)"/><circle cx="340" cy="180" r="124" fill="url(#cp-bezel2)"/>'
         '<path d="M224.4 137.9 A123 123 0 0 1 382.1 64.4" fill="none" stroke="#FFFFFF" stroke-opacity=".85" stroke-width="7" stroke-linecap="round"/>'
         '<path d="M455.6 222.1 A123 123 0 0 1 297.9 295.6" fill="none" stroke="#000000" stroke-opacity=".35" stroke-width="7" stroke-linecap="round"/>'
         + "".join(f'<circle cx="340" cy="180" r="{r}" fill="none" stroke="#FFFFFF" stroke-opacity=".09" stroke-width=".8"/>' for r in (118, 121, 128, 131)) +
         "".join(f'<g transform="rotate({a} 340 180)"><circle cx="340" cy="63" r="4.6" fill="#8D979B"/><circle cx="340" cy="63" r="4.6" fill="none" stroke="#000" stroke-opacity=".35"/><line x1="337.4" y1="60.6" x2="342.6" y2="65.4" stroke="#2B3234" stroke-width="1.4" stroke-linecap="round"/></g>' for a in (45, 135, 225, 315)) +
         '<circle cx="340" cy="180" r="114" fill="#0A0D0C"/><circle cx="340" cy="180" r="108" fill="url(#cp-face)"/>'
         '<g transform="rotate(-90 340 180)"><circle cx="340" cy="180" r="96" fill="none" stroke="#8FA09A" stroke-width="10" stroke-dasharray="2.4 15.05" stroke-dashoffset="1.2"/>'
         '<circle cx="340" cy="180" r="96" fill="none" stroke="#6FE3C5" stroke-width="16" stroke-dasharray="3.5 48.86" stroke-dashoffset="1.75"/></g>'
         '<circle cx="340" cy="180" r="72" fill="none" stroke="#FFFFFF" stroke-opacity=".08" stroke-width="2"/>'
         '<polygon points="340,84 331,102 349,102" fill="#6FE3C5"/>'
         '<ellipse cx="344" cy="188" rx="15" ry="9" fill="#000" fill-opacity=".35" transform="rotate(55 340 180)"/>'
         '<g class="cp-needle" transform="rotate(55 340 180)"><polygon points="340,100 326,180 340,180" fill="url(#cp-nl)"/><polygon points="340,100 354,180 340,180" fill="url(#cp-nr)"/>'
         '<polygon points="340,260 326,180 340,180" fill="url(#cp-sl)"/><polygon points="340,260 354,180 340,180" fill="url(#cp-sr)"/></g>'
         '<circle cx="340" cy="180" r="11" fill="url(#cp-cap)" stroke="#5E686C" stroke-width="1.5"/><circle cx="340" cy="180" r="4.5" fill="#141918"/><circle cx="337" cy="176.5" r="2" fill="#FFFFFF"/>'
         '<circle cx="340" cy="180" r="108" fill="url(#cp-glass)"/>'
         '<path d="M258 120 A92 92 0 0 1 330 92" fill="none" stroke="#FFFFFF" stroke-opacity=".3" stroke-width="3" stroke-linecap="round"/>')
    b += "".join(f'<circle class="cp-dot" style="--d:{1.2+0.12*i:.2f}s" cx="{414+92*i/6:.1f}" cy="{128-64*i/6:.1f}" r="3.2" fill="#6FE3C5"/>' for i in range(7))
    b += ('<ellipse cx="512" cy="62" rx="14" ry="5" fill="#000" fill-opacity=".4"/>'
          '<g class="cp-flag"><line x1="512" y1="60" x2="512" y2="20" stroke="#E9EDEA" stroke-width="3.5" stroke-linecap="round"/><polygon points="512,20 546,31 512,42" fill="url(#cp-flag)"/></g>')
    b += '<rect x="0" y="0" width="680" height="370" rx="12" fill="url(#cp-vg)" pointer-events="none"/>'
    return _svg(680, 370, b, "Brújula con aro metálico y aguja en aguamarina", "Ilustración semirrealista de una brújula.", deco, vb="196 10 372 350" if crop else None)


# ---------- iceberg ----------
ICE_DEFS = ('<defs>'
            '<linearGradient id="ic-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#081A1D"/><stop offset="1" stop-color="#153C3D"/></linearGradient>'
            '<linearGradient id="ic-water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#136269"/><stop offset=".45" stop-color="#0B3F46"/><stop offset="1" stop-color="#051D22"/></linearGradient>'
            '<linearGradient id="ic-mass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8BE6DB" stop-opacity=".62"/><stop offset="1" stop-color="#2D9AA0" stop-opacity=".1"/></linearGradient>'
            '<linearGradient id="ic-f1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D6EFF0"/></linearGradient>'
            '<linearGradient id="ic-f2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C3E8EA"/><stop offset="1" stop-color="#7DB8BE"/></linearGradient>'
            '<linearGradient id="ic-f3" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E4F5F6"/><stop offset="1" stop-color="#A3D2D7"/></linearGradient>'
            '<linearGradient id="ic-f4" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9BCFD4"/><stop offset="1" stop-color="#6FA7AD"/></linearGradient>'
            '<linearGradient id="ic-ray" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#BFF4EA" stop-opacity=".28"/><stop offset="1" stop-color="#BFF4EA" stop-opacity="0"/></linearGradient>'
            '<radialGradient id="ic-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#E4FFF8" stop-opacity=".95"/><stop offset="1" stop-color="#6FE3C5" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="ic-soft" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#BFF4EA" stop-opacity=".38"/><stop offset="1" stop-color="#BFF4EA" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="ic-vg" cx=".5" cy=".5" r=".78"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".42"/></radialGradient>'
            '</defs>')
TIP = ('<polygon points="225,172 275,97 300,117 355,47 420,172" fill="url(#ic-f3)"/><polygon points="355,47 300,117 285,172 345,172" fill="url(#ic-f1)"/>'
       '<polygon points="355,47 345,172 420,172" fill="url(#ic-f2)"/><polygon points="275,97 300,117 285,172 225,172" fill="url(#ic-f3)"/>'
       '<polygon points="300,117 322,130 312,172 285,172" fill="url(#ic-f4)"/>'
       '<polyline points="225,172 275,97 300,117 355,47 420,172" fill="none" stroke="#FFFFFF" stroke-opacity=".6" stroke-width="1.4" stroke-linejoin="round"/>'
       '<ellipse cx="322" cy="176" rx="150" ry="11" fill="url(#ic-soft)"/>'
       '<rect x="0" y="172" width="680" height="2.5" fill="#BFF4EA" fill-opacity=".7"/>'
       '<g fill="#BFF4EA" fill-opacity=".35"><rect x="120" y="182" width="80" height="2"/><rect x="470" y="184" width="100" height="2"/><rect x="200" y="192" width="50" height="2"/><rect x="500" y="196" width="60" height="2"/></g>')


def iceberg_scene(deco=True):
    bub = [(250, 215, 4), (310, 238, 3), (360, 205, 4), (420, 232, 3), (465, 250, 4), (215, 262, 3), (290, 290, 4), (345, 272, 3), (410, 300, 4), (320, 320, 3), (380, 228, 3), (270, 248, 3)]
    b = (ICE_DEFS + '<rect x="0" y="0" width="680" height="400" rx="12" fill="url(#ic-sky)"/>'
         '<g fill="#E9EDEA" fill-opacity=".55">' + "".join(f'<circle cx="{x}" cy="{y}" r="1.6"/>' for x, y in [(40, 30), (110, 70), (180, 24), (520, 36), (600, 80), (640, 30), (70, 120)]) + '</g>'
         '<circle cx="560" cy="64" r="60" fill="url(#ic-soft)"/><circle cx="560" cy="64" r="15" fill="#EAF7F3"/>'
         '<rect x="0" y="172" width="680" height="228" fill="url(#ic-water)"/>'
         '<polygon points="300,174 340,174 250,360 170,360" fill="url(#ic-ray)"/><polygon points="360,174 400,174 470,360 400,360" fill="url(#ic-ray)" fill-opacity=".8"/>'
         '<polygon points="200,174 445,174 500,217 485,292 380,337 250,344 175,292 160,217" fill="url(#ic-mass)"/>'
         '<polygon points="300,174 445,174 500,217 380,252" fill="#9FEEE3" fill-opacity=".2"/><polygon points="160,217 200,174 300,174 250,262" fill="#5FD0C9" fill-opacity=".16"/>'
         '<polygon points="250,344 380,337 380,252 250,262 175,292" fill="#1E7F84" fill-opacity=".22"/>'
         '<polyline points="200,174 160,217 175,292 250,344 380,337 485,292 500,217 445,174" fill="none" stroke="#BFF4EA" stroke-opacity=".28" stroke-width="1.2" stroke-linejoin="round"/>'
         + "".join(f'<g><circle cx="{x}" cy="{y}" r="{r*3.2:.1f}" fill="url(#ic-glow)" opacity=".5"/><circle cx="{x}" cy="{y}" r="{r}" fill="#E4FFF8" fill-opacity=".85"/></g>' for x, y, r in bub) + TIP
         + '<g fill="none" stroke="#FFFFFF" stroke-opacity=".16" stroke-width="1.2" stroke-linecap="round"><polyline points="318,176 332,230 318,262"/><polyline points="372,178 360,236 382,284"/><polyline points="250,190 262,226"/></g>'
         '<polyline points="355,47 346,86 352,112" fill="none" stroke="#FFFFFF" stroke-opacity=".7" stroke-width="1.6" stroke-linecap="round"/>'
         '<rect x="0" y="0" width="680" height="400" rx="12" fill="url(#ic-vg)" pointer-events="none"/>')
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
    b = (ICE_DEFS + '<rect x="0" y="0" width="680" height="572" rx="12" fill="url(#ic-sky)"/><rect x="0" y="172" width="680" height="400" fill="url(#ic-water)"/>'
         '<polygon points="150,174 530,174 640,230 650,430 560,512 130,522 30,440 40,230" fill="url(#ic-mass)"/>'
         '<polygon points="300,174 530,174 640,230 450,290" fill="#9FEEE3" fill-opacity=".18"/><polygon points="40,230 150,174 300,174 240,300" fill="#5FD0C9" fill-opacity=".14"/>'
         '<polygon points="130,522 560,512 450,290 240,300 30,440" fill="#1E7F84" fill-opacity=".2"/>'
         '<polyline points="150,174 40,230 30,440 130,522 560,512 650,430 640,230 530,174" fill="none" stroke="#BFF4EA" stroke-opacity=".28" stroke-width="1.2" stroke-linejoin="round"/>' + TIP)
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
    b = (MT_DEFS + '<rect x="0" y="0" width="680" height="330" rx="12" fill="url(#mt-sky)"/>' + _mountain_body())
    b += '<rect x="0" y="0" width="680" height="330" rx="12" fill="url(#mt-vg)" pointer-events="none"/>'
    return _svg(680, 330, b, "Montaña con camino y bandera", "Ilustración semirrealista de una montaña nevada con camino y campamentos.", deco)


MT_DEFS = ('<defs>'
           '<linearGradient id="mt-far" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#27504F"/><stop offset="1" stop-color="#112B2C"/></linearGradient>'
           '<linearGradient id="mt-lit" x1=".1" y1="0" x2=".9" y2="1"><stop offset="0" stop-color="#CBD6D1"/><stop offset=".55" stop-color="#8E9B96"/><stop offset="1" stop-color="#5B6864"/></linearGradient>'
           '<linearGradient id="mt-mid" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9AA7A2"/><stop offset="1" stop-color="#52605C"/></linearGradient>'
           '<linearGradient id="mt-shade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#586461"/><stop offset="1" stop-color="#232C2B"/></linearGradient>'
           '<linearGradient id="mt-snow" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D1E6E8"/></linearGradient>'
           '<linearGradient id="mt-snow2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C9DFE2"/><stop offset="1" stop-color="#86ADB4"/></linearGradient>'
           '<linearGradient id="mt-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#08171A"/><stop offset="1" stop-color="#123231"/></linearGradient>'
           '<radialGradient id="mt-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#A9F6E2" stop-opacity=".55"/><stop offset="1" stop-color="#6FE3C5" stop-opacity="0"/></radialGradient>'
           '<radialGradient id="mt-mist" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#E9FFF8" stop-opacity=".22"/><stop offset="1" stop-color="#E9FFF8" stop-opacity="0"/></radialGradient>'
           '<radialGradient id="mt-vg" cx=".5" cy=".5" r=".78"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".42"/></radialGradient>'
           '</defs>')


def _mountain_body():
    b = '<g fill="#E9EDEA" fill-opacity=".5">' + "".join(f'<circle cx="{x}" cy="{y}" r="1.8"/>' for x, y in [(40, 30), (120, 60), (210, 25), (300, 50), (420, 28), (640, 40), (600, 90), (70, 110)]) + "</g>"
    b += '<circle cx="570" cy="50" r="80" fill="url(#mt-glow)"/>'
    b += '<polygon points="0,300 80,205 150,255 225,170 310,300" fill="url(#mt-far)"/>'
    b += '<polygon points="0,300 60,272 110,245 170,215 230,190 300,165 340,150 400,120 450,100 500,78 540,58 570,50 520,160 470,235 380,300" fill="url(#mt-lit)"/>'
    b += '<polygon points="110,245 170,215 230,190 300,165 340,150 300,205 200,262 120,290 60,272" fill="url(#mt-mid)" fill-opacity=".85"/>'
    b += '<polygon points="570,50 612,112 650,190 680,262 680,300 380,300 470,235 520,160" fill="url(#mt-shade)"/>'
    b += '<polygon points="570,50 534,82 552,90 522,120 556,112 580,96 592,80" fill="url(#mt-snow)"/><polygon points="570,50 592,80 580,96 556,112 590,125 612,112" fill="url(#mt-snow2)"/>'
    b += '<polyline points="0,300 60,272 110,245 170,215 230,190 300,165 340,150 400,120 450,100 500,78 540,58 570,50" fill="none" stroke="#F1FFFA" stroke-opacity=".38" stroke-width="1.6" stroke-linejoin="round"/>'
    b += '<ellipse cx="210" cy="296" rx="230" ry="26" fill="url(#mt-mist)"/><ellipse cx="520" cy="298" rx="210" ry="20" fill="url(#mt-mist)"/>'
    b += '<polyline points="30,284 110,245 190,205 260,185 340,150 420,118 500,90 570,50" fill="none" stroke="#6FE3C5" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>'
    for cx, cy in ((110, 245), (340, 150)):
        b += f'<ellipse cx="{cx}" cy="{cy+12}" rx="14" ry="3" fill="#000" fill-opacity=".35"/><polygon points="{cx-13},{cy+10} {cx},{cy-14} {cx+13},{cy+10}" fill="#6FE3C5" stroke="#0F1E1F" stroke-width="2"/>'
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
    b = MT_DEFS + '<rect x="0" y="0" width="680" height="530" rx="12" fill="url(#mt-sky)"/>' + _mountain_body() + '<rect x="0" y="300" width="680" height="230" rx="12" fill="#0B1413"/><rect x="0" y="300" width="680" height="30" fill="#0B1413"/>'
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
BN_COLORS = {"y": ("#F5D65A", "#E3B72E", "#A9821F", "#FFE98A"), "b": ("#6B9BE6", "#3F73C4", "#2A4F8F", "#8DB6F2"),
             "g": ("#69C783", "#3E9A5A", "#2A6C3E", "#8EDCA3"), "k": ("#A9B3B5", "#7D8789", "#545E60", "#C6CFD1")}


def bins_scene(deco=True, crop=False):
    d = '<defs><linearGradient id="bn-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#08171A"/><stop offset="1" stop-color="#123231"/></linearGradient>'
    d += '<linearGradient id="bn-floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#112321"/><stop offset="1" stop-color="#091213"/></linearGradient>'
    d += '<radialGradient id="bn-ao" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".62"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
    d += '<radialGradient id="bn-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#A9F6E2" stop-opacity=".5"/><stop offset="1" stop-color="#6FE3C5" stop-opacity="0"/></radialGradient>'
    d += '<linearGradient id="bn-bottle" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".5" stop-color="#CFE9F5"/><stop offset="1" stop-color="#8DB6C9"/></linearGradient>'
    d += '<linearGradient id="bn-refl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".1"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
    for k, (light, main, shade, lid) in BN_COLORS.items():
        d += f'<linearGradient id="bn-{k}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{light}"/><stop offset=".45" stop-color="{main}"/><stop offset="1" stop-color="{shade}"/></linearGradient>'
        d += f'<linearGradient id="bn-{k}l" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{lid}"/><stop offset="1" stop-color="{main}"/></linearGradient>'
    d += '<linearGradient id="bn-spotg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9FFF8" stop-opacity=".0"/><stop offset="1" stop-color="#E9FFF8" stop-opacity=".1"/></linearGradient>'
    d += '<radialGradient id="bn-vg" cx=".5" cy=".5" r=".78"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".42"/></radialGradient>'
    d += '</defs>'
    b = d + '<rect x="0" y="0" width="680" height="370" rx="12" fill="url(#bn-sky)"/><polygon points="250,0 430,0 600,318 80,318" fill="url(#bn-spotg)"/>'
    b += '<g fill="#E9EDEA" fill-opacity=".5">' + "".join(f'<circle cx="{x}" cy="{y}" r="1.7"/>' for x, y in [(40, 30), (120, 60), (300, 26), (420, 40), (600, 34), (640, 90), (70, 120)]) + "</g>"
    b += '<rect x="0" y="318" width="680" height="52" rx="12" fill="url(#bn-floor)"/><rect x="0" y="318" width="680" height="14" fill="url(#bn-floor)"/><line x1="0" y1="318.5" x2="680" y2="318.5" stroke="#6FE3C5" stroke-opacity=".12"/>'
    b += '<circle cx="215" cy="70" r="62" fill="url(#bn-glow)"/><g stroke="#6FE3C5" stroke-opacity=".07" stroke-width="1"><line x1="0" y1="340" x2="680" y2="340"/><line x1="0" y1="356" x2="680" y2="356"/><line x1="170" y1="318" x2="60" y2="370"/><line x1="340" y1="318" x2="340" y2="370"/><line x1="510" y1="318" x2="620" y2="370"/></g>'
    for x, k in zip((105, 225, 345, 465), "ybgk"):
        b += f'<ellipse cx="{x+50}" cy="323" rx="66" ry="10" fill="url(#bn-ao)"/>'
        b += f'<polygon points="{x},160 {x+100},160 {x+92},316 {x+8},316" fill="url(#bn-{k})"/>'
        b += f'<polygon points="{x+6},166 {x+15},166 {x+21},310 {x+12},310" fill="#FFFFFF" fill-opacity=".2"/>'
        b += f'<line x1="{x+3}" y1="198" x2="{x+97}" y2="198" stroke="#000" stroke-opacity=".18" stroke-width="2"/><line x1="{x+6}" y1="262" x2="{x+94}" y2="262" stroke="#000" stroke-opacity=".14" stroke-width="2"/>'
        b += f'<rect x="{x+34}" y="129" width="32" height="13" rx="5" fill="url(#bn-{k}l)"/>'
        b += f'<rect x="{x-6}" y="140" width="112" height="22" rx="7" fill="url(#bn-{k}l)"/><rect x="{x-6}" y="140" width="112" height="3" rx="1.5" fill="#FFFFFF" fill-opacity=".35"/><rect x="{x-6}" y="156" width="112" height="6" rx="3" fill="#000" fill-opacity=".2"/>'
        b += f'<circle cx="{x+18}" cy="316" r="7" fill="#161B1A"/><circle cx="{x+82}" cy="316" r="7" fill="#161B1A"/><circle cx="{x+16}" cy="314" r="2" fill="#FFFFFF" fill-opacity=".25"/>'
        b += f'<rect x="{x-6}" y="326" width="112" height="22" fill="url(#bn-refl)" transform="scale(1 1)" opacity=".5"/>'
    ic = '#F4FBFA'
    b += f'<g fill="{ic}" fill-opacity=".94"><rect x="143" y="214" width="24" height="34" rx="3"/><ellipse cx="155" cy="214" rx="12" ry="3.5"/></g><rect x="146" y="222" width="5" height="22" rx="2.5" fill="#E3B72E" fill-opacity=".35"/>'
    b += f'<g fill="{ic}" fill-opacity=".94"><rect x="261" y="208" width="28" height="38" rx="3"/></g><g stroke="#3F73C4" stroke-width="2.5" stroke-linecap="round"><line x1="267" y1="219" x2="283" y2="219"/><line x1="267" y1="227" x2="283" y2="227"/><line x1="267" y1="235" x2="278" y2="235"/></g>'
    b += f'<g fill="{ic}" fill-opacity=".94"><rect x="385" y="224" width="20" height="28" rx="4"/><rect x="391" y="210" width="8" height="16" rx="2"/></g>'
    b += f'<g fill="{ic}" fill-opacity=".94"><rect x="501" y="216" width="28" height="32" rx="3"/></g><path d="M507 216 C507 204 523 204 523 216" fill="none" stroke="{ic}" stroke-opacity=".94" stroke-width="3"/>'
    b += '<path d="M214 34 C200 62 186 94 170 126" fill="none" stroke="#6FE3C5" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/><polygon points="170,128 163,114 177,116" fill="#6FE3C5"/>'
    b += '<g transform="rotate(24 160 80)"><rect x="152" y="62" width="16" height="36" rx="5" fill="url(#bn-bottle)" fill-opacity=".96"/><rect x="157" y="50" width="6" height="14" rx="2" fill="url(#bn-bottle)"/><rect x="156" y="46" width="8" height="5" rx="2" fill="#6FE3C5"/><rect x="155" y="68" width="3" height="24" rx="1.5" fill="#FFFFFF" fill-opacity=".7"/></g>'
    b += '<rect x="0" y="0" width="680" height="370" rx="12" fill="url(#bn-vg)" pointer-events="none"/>'
    return _svg(680, 370, b, "Cuatro contenedores de reciclaje: amarillo, azul, verde y gris", "Ilustración semirrealista de cuatro contenedores con una botella cayendo en el amarillo.", deco, vb="84 28 508 304" if crop else None)


# ---------- casa con porcentaje de match (cabecera del caso práctico) ----------
def casa_scene(deco=True):
    d = ('<defs>'
         '<linearGradient id="cs-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#08171A"/><stop offset="1" stop-color="#173D3C"/></linearGradient>'
         '<linearGradient id="cs-wall" x1=".1" y1="0" x2=".9" y2="1"><stop offset="0" stop-color="#E3E8E4"/><stop offset="1" stop-color="#9AA6A1"/></linearGradient>'
         '<linearGradient id="cs-side" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6E7B77"/><stop offset="1" stop-color="#3A4543"/></linearGradient>'
         '<linearGradient id="cs-roof" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E0704F"/><stop offset="1" stop-color="#8A3524"/></linearGradient>'
         '<linearGradient id="cs-roof2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B14E36"/><stop offset="1" stop-color="#5E241A"/></linearGradient>'
         '<linearGradient id="cs-win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFEDB8"/><stop offset="1" stop-color="#F2B94F"/></linearGradient>'
         '<linearGradient id="cs-ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#12302C"/><stop offset="1" stop-color="#091514"/></linearGradient>'
         '<linearGradient id="cs-card" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#26393A"/><stop offset="1" stop-color="#121D1E"/></linearGradient>'
         '<radialGradient id="cs-warm" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFD98A" stop-opacity=".55"/><stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></radialGradient>'
         '<radialGradient id="cs-moon" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#BFF4EA" stop-opacity=".35"/><stop offset="1" stop-color="#BFF4EA" stop-opacity="0"/></radialGradient>'
         '<radialGradient id="cs-vg" cx=".5" cy=".5" r=".78"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".42"/></radialGradient>'
         '</defs>')
    b = d + '<rect width="680" height="400" rx="12" fill="url(#cs-sky)"/>'
    b += '<g fill="#E9EDEA" fill-opacity=".5">' + "".join(f'<circle cx="{x}" cy="{y}" r="1.6"/>' for x, y in [(40, 36), (96, 80), (170, 30), (240, 14), (470, 22), (520, 60), (640, 30), (655, 110), (60, 130)]) + '</g>'
    b += '<circle cx="590" cy="76" r="64" fill="url(#cs-moon)"/><circle cx="590" cy="76" r="14" fill="#EAF7F3"/>'
    # casas lejanas
    b += ('<rect x="52" y="266" width="100" height="66" fill="#14302F"/><polygon points="42,268 102,226 162,268" fill="#102725"/>'
          '<rect x="70" y="284" width="16" height="18" rx="2" fill="#F2B94F" fill-opacity=".85"/><rect x="112" y="284" width="16" height="18" rx="2" fill="#F2B94F" fill-opacity=".55"/>'
          '<rect x="532" y="272" width="108" height="60" fill="#14302F"/><polygon points="522,274 586,234 650,274" fill="#102725"/>'
          '<rect x="552" y="290" width="16" height="18" rx="2" fill="#F2B94F" fill-opacity=".7"/><rect x="600" y="290" width="16" height="18" rx="2" fill="#F2B94F" fill-opacity=".9"/>')
    b += '<rect x="0" y="330" width="680" height="70" fill="url(#cs-ground)"/><polygon points="308,330 352,330 392,400 270,400" fill="#1E4541" fill-opacity=".75"/>'
    # casa principal
    b += '<circle cx="320" cy="262" r="150" fill="url(#cs-warm)" fill-opacity=".45"/>'
    b += '<polygon points="410,212 468,200 468,318 410,330" fill="url(#cs-side)"/>'
    b += '<polygon points="230,212 410,212 410,330 230,330" fill="url(#cs-wall)"/>'
    b += '<polygon points="320,128 378,116 484,204 426,216" fill="url(#cs-roof2)"/><polygon points="214,216 320,128 426,216" fill="url(#cs-roof)"/>'
    b += '<polyline points="214,216 320,128 426,216" fill="none" stroke="#FFD9C6" stroke-opacity=".55" stroke-width="1.6" stroke-linejoin="round"/>'
    b += '<rect x="396" y="136" width="22" height="46" fill="#7D8A86"/><rect x="392" y="132" width="30" height="8" fill="#5E6B67"/>'
    for x in (252, 344):
        b += (f'<circle cx="{x+22}" cy="264" r="50" fill="url(#cs-warm)"/><rect x="{x}" y="240" width="44" height="48" rx="3" fill="url(#cs-win)" stroke="#6E7B77" stroke-width="3"/>'
              f'<line x1="{x+22}" y1="240" x2="{x+22}" y2="288" stroke="#6E7B77" stroke-width="2.4"/><line x1="{x}" y1="264" x2="{x+44}" y2="264" stroke="#6E7B77" stroke-width="2.4"/>')
    b += '<rect x="306" y="268" width="28" height="62" rx="3" fill="#1B3A38"/><circle cx="328" cy="300" r="2.4" fill="#F2B94F"/><rect x="298" y="330" width="44" height="6" fill="#6E7B77"/>'
    b += '<rect x="176" y="288" width="10" height="44" fill="#4A3A2E"/><circle cx="181" cy="270" r="26" fill="#1C4A3A"/><circle cx="166" cy="284" r="17" fill="#17402F"/><circle cx="197" cy="284" r="19" fill="#225541"/><circle cx="178" cy="262" r="9" fill="#2C6A52" fill-opacity=".7"/>'
    b += '<circle cx="500" cy="318" r="16" fill="#1E4B3B"/><circle cx="496" cy="313" r="7" fill="#2C6A52" fill-opacity=".7"/>'
    # tarjeta de match
    b += ('<polygon points="330,102 350,102 340,114" fill="#26393A" stroke="#6FE3C5" stroke-opacity=".7"/>'
          '<rect x="232" y="26" width="216" height="76" rx="16" fill="url(#cs-card)" stroke="#6FE3C5" stroke-opacity=".75" stroke-width="1.6"/>'
          '<circle cx="272" cy="64" r="24" fill="none" stroke="#2C3A3A" stroke-width="6"/>'
          '<circle cx="272" cy="64" r="24" fill="none" stroke="#6FE3C5" stroke-width="6" stroke-linecap="round" stroke-dasharray="138.7 150.8" transform="rotate(-90 272 64)"/>'
          f'<text x="312" y="76" fill="#E9EDEA" style="{DI};font-size:34px;font-weight:500">92 %</text>'
          '<circle cx="424" cy="64" r="11" fill="#6FE3C5"/><path d="M418.5 64 l4 4 7 -8" fill="none" stroke="#0F1E1F" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>')
    b += '<rect x="0" y="0" width="680" height="400" rx="12" fill="url(#cs-vg)" pointer-events="none"/>'
    return _svg(680, 400, b, "Casa con las ventanas encendidas y una tarjeta de coincidencia del 92 %", "Ilustración semirrealista de una casa nocturna con un porcentaje de match.", deco)


# ---------- esquema del agente de IA (caso práctico) ----------
def agente_diagram(lang):
    L = {"es": dict(izq="Quien busca casa", izq2=("Cuenta lo que busca,", "por voz o por texto"), cen="Agente de IA", cen2=("Escucha, entiende", "y recomienda"), der="Portales pequeños", der2=("Su oferta, unida", "en un solo catálogo"),
                    a1="lo que busca", a2="match explicado", a3="catálogo", a4="visitas", extra="Servicios extra: reformas · legal · financiación",
                    label="Esquema: la persona habla con un agente de IA, que recibe el catálogo de varios portales pequeños, devuelve un match explicado y envía visitas a los portales; debajo, servicios extra.",
                    cap="El agente hace de intermediario: escucha a quien busca, conoce el catálogo de los portales y devuelve viviendas a su medida."),
         "en": dict(izq="Home seeker", izq2=("Tells what they want,", "by voice or text"), cen="AI agent", cen2=("Listens, understands", "and recommends"), der="Small portals", der2=("Their listings, joined", "in a single catalogue"),
                    a1="what they want", a2="explained match", a3="catalogue", a4="viewings", extra="Extra services: renovation · legal · financing",
                    label="Diagram: the person talks to an AI agent, which receives the catalogue of several small portals, returns an explained match and sends viewings to the portals; below, extra services.",
                    cap="The agent acts as an intermediary: it listens to the person searching, knows the portals' catalogue and returns homes that suit them.")}[lang]
    b = ('<defs><linearGradient id="ag-bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1A1B"/><stop offset="1" stop-color="#112A2B"/></linearGradient>'
         '<radialGradient id="ag-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#B8FFEE" stop-opacity=".8"/><stop offset=".4" stop-color="#6FE3C5" stop-opacity=".3"/><stop offset="1" stop-color="#6FE3C5" stop-opacity="0"/></radialGradient></defs>'
         '<rect width="680" height="420" rx="12" fill="url(#ag-bg)"/>')
    # persona y burbuja
    b += ('<circle cx="100" cy="150" r="22" fill="#CFE3DD"/><path d="M62 226 Q62 186 100 186 Q138 186 138 226 Z" fill="#8FB5AC"/>'
          '<rect x="110" y="60" width="86" height="42" rx="14" fill="#1E3A38" stroke="#6FE3C5" stroke-opacity=".7"/><polygon points="122,102 130,102 120,118" fill="#1E3A38" stroke="#6FE3C5" stroke-opacity=".7"/>'
          '<circle cx="134" cy="81" r="4.5" fill="#6FE3C5"/><circle cx="153" cy="81" r="4.5" fill="#6FE3C5"/><circle cx="172" cy="81" r="4.5" fill="#6FE3C5"/>')
    # agente (esfera de puntos)
    ring = 'fill="none" stroke="#6FE3C5" stroke-linecap="round" stroke-width="3.4" stroke-dasharray="1 7.5"'
    b += ('<circle cx="340" cy="150" r="86" fill="url(#ag-glow)"/>'
          f'<circle cx="340" cy="150" r="54" {ring}/><ellipse cx="340" cy="150" rx="54" ry="19" {ring}/><ellipse cx="340" cy="150" rx="19" ry="54" {ring}/><ellipse cx="340" cy="150" rx="38" ry="54" {ring} stroke-opacity=".6"/>'
          '<circle cx="340" cy="150" r="7" fill="#CFFFF2"/>')
    # portales (tres casitas)
    for cx, h, rf in ((538, 26, "#D9674A"), (580, 34, "#E0704F"), (622, 26, "#B14E36")):
        b += (f'<rect x="{cx-16}" y="{196-h}" width="32" height="{h}" fill="#8FA29C"/><polygon points="{cx-21},{196-h} {cx},{196-h-24} {cx+21},{196-h}" fill="{rf}"/>'
              f'<rect x="{cx-5}" y="{196-h+8}" width="10" height="9" rx="1.5" fill="#F2B94F"/>')
    arr = lambda x1, x2, y: (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#6FE3C5" stroke-width="2.6" stroke-linecap="round"/>'
                             f'<polygon points="{x2},{y} {x2 - (10 if x2 > x1 else -10)},{y-6} {x2 - (10 if x2 > x1 else -10)},{y+6}" fill="#6FE3C5"/>')
    b += arr(158, 272, 142) + arr(272, 158, 190) + arr(522, 408, 142) + arr(408, 522, 190)
    lbl = lambda x, y, t: f'<text x="{x}" y="{y}" text-anchor="middle" fill="#98A39E" style="{UI};font-size:17px">{t}</text>'
    b += lbl(215, 128, L["a1"]) + lbl(215, 216, L["a2"]) + lbl(465, 128, L["a3"]) + lbl(465, 216, L["a4"])
    for cx, head, subs in ((100, L["izq"], L["izq2"]), (340, L["cen"], L["cen2"]), (580, L["der"], L["der2"])):
        b += f'<text x="{cx}" y="268" text-anchor="middle" fill="#6FE3C5" style="{DI};font-size:23px;font-weight:500">{head}</text>'
        b += "".join(f'<text x="{cx}" y="{296 + i * 22}" text-anchor="middle" fill="#E9EDEA" style="{UI};font-size:17px">{s}</text>' for i, s in enumerate(subs))
    b += ('<line x1="340" y1="338" x2="340" y2="356" stroke="#6FE3C5" stroke-opacity=".5" stroke-width="2" stroke-dasharray="3 5"/>'
          '<rect x="70" y="358" width="540" height="46" rx="12" fill="none" stroke="#6FE3C5" stroke-opacity=".5" stroke-dasharray="5 5"/>'
          f'<text x="340" y="388" text-anchor="middle" fill="#E9EDEA" style="{UI};font-size:19px">{L["extra"]}</text>')
    return f'<figure class="diagram"><svg viewBox="0 0 680 420" role="img" aria-label="{L["label"]}">{b}</svg><figcaption>{L["cap"]}</figcaption></figure>'


# ---------- representación de la pizarra del taller (con notas de relleno, sin texto) ----------
def lienzo_diagram(lang):
    L = {"es": dict(prob=("Problema",), alt=("Alternativas",), cand=("Soluciones", "candidatas"), sol=("Solución",), obj=("Objetivos clave",), ret=("Retos",), ing=("Ingresos",),
                    pu=("Propuesta", "única de valor"), para=("¿A quién va", "dirigida?"), conc=("Concepto", "general"), met=("Métricas", "clave"),
                    z=("Entender el problema", "Diseñar la solución", "Convertirla en negocio"),
                    label="Representación de la pizarra del taller: un lienzo en tres zonas numeradas, con bloques para problema, alternativas, solución, objetivos, valor, ingresos y métricas. Las notas son de relleno.",
                    cap="El lienzo del taller, en tres zonas. Las notas amarillas son de relleno: no reproducen las del equipo."),
         "en": dict(prob=("Problem",), alt=("Alternatives",), cand=("Candidate", "solutions"), sol=("Solution",), obj=("Key objectives",), ret=("Challenges",), ing=("Revenue",),
                    pu=("Unique value", "proposition"), para=("Who is", "it for?"), conc=("High-level", "concept"), met=("Key", "metrics"),
                    z=("Understand the problem", "Design the solution", "Turn it into a business"),
                    label="Representation of the workshop whiteboard: a canvas in three numbered zones, with blocks for problem, alternatives, solution, objectives, value, revenue and metrics. The notes are placeholders.",
                    cap="The workshop canvas, in three zones. The yellow notes are placeholders: they do not reproduce the team's.")}[lang]
    b = ('<defs><linearGradient id="lz-bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1A1B"/><stop offset="1" stop-color="#112A2B"/></linearGradient></defs>'
         '<rect width="680" height="400" rx="12" fill="url(#lz-bg)"/>'
         '<line x1="203" y1="24" x2="203" y2="300" stroke="#6FE3C5" stroke-opacity=".25" stroke-dasharray="3 6"/><line x1="403" y1="24" x2="403" y2="300" stroke="#6FE3C5" stroke-opacity=".25" stroke-dasharray="3 6"/>')
    def nota(x, y):
        return (f'<rect x="{x}" y="{y}" width="30" height="24" rx="3" fill="#F2D56B" fill-opacity=".92"/>'
                f'<rect x="{x+5}" y="{y+7}" width="20" height="2.6" rx="1.3" fill="#8C7A3A"/><rect x="{x+5}" y="{y+13}" width="14" height="2.6" rx="1.3" fill="#8C7A3A"/>')
    def caja(x, y, w, h, lines, n):
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#122D2E" stroke="#6FE3C5" stroke-opacity=".55"/>'
        s += "".join(f'<text x="{x+10}" y="{y+21+i*17}" fill="#E9EDEA" style="{UI};font-size:15px;font-weight:600">{t}</text>' for i, t in enumerate(lines))
        y0 = y + 21 + (len(lines) - 1) * 17 + 12
        cols = max(1, (w - 14) // 38)
        for i in range(n):
            nx, ny = x + 10 + (i % cols) * 38 + ((i // cols) % 2) * 5, y0 + (i // cols) * 30
            if ny + 24 > y + h - 6: break
            s += nota(nx, ny)
        return s
    bl = ((20, 24, 176, 150, "prob", 3), (20, 184, 176, 116, "alt", 3),
          (210, 24, 186, 100, "cand", 4), (210, 134, 186, 80, "sol", 3), (210, 224, 186, 76, "obj", 3),
          (410, 24, 124, 76, "ret", 2), (410, 110, 124, 94, "pu", 3), (410, 214, 124, 86, "para", 2),
          (544, 24, 116, 76, "ing", 2), (544, 110, 116, 94, "conc", 3), (544, 214, 116, 86, "met", 3))
    for x, y, w, h, k, n in bl:
        b += caja(x, y, w, h, L[k], n)
    for cx, num, name in ((108, 1, L["z"][0]), (303, 2, L["z"][1]), (535, 3, L["z"][2])):
        b += (f'<circle cx="{cx}" cy="334" r="16" fill="#6FE3C5"/><text x="{cx}" y="340" text-anchor="middle" fill="#0F1E1F" style="{UI};font-size:18px;font-weight:700">{num}</text>'
              f'<text x="{cx}" y="378" text-anchor="middle" fill="#6FE3C5" style="{DI};font-size:18px;font-weight:500">{name}</text>')
    return f'<figure class="diagram"><svg viewBox="0 0 680 400" role="img" aria-label="{L["label"]}">{b}</svg><figcaption>{L["cap"]}</figcaption></figure>'
