import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import art
ROOT = pathlib.Path(__file__).resolve().parents[1]
UI = "font-family:var(--f-ui)"; DI = "font-family:var(--f-display)"

def mountain(lang):
    L = {"es": dict(cols=[("Datos", ["Reunir y etiquetar", "Limpiar y validar", "Cuidar la calidad"]),
                          ("Modelo", ["Elegir algoritmo", "Evitar sobreajuste", "Validar y probar"]),
                          ("Producción", ["Integrar en sistemas", "Vigilar rendimiento", "Reentrenar"])],
                loop="Cuando los datos cambian, vuelta a empezar",
                label="Mapa de un proyecto de Machine Learning como una montaña con tres tramos: datos, modelo y producción, con una flecha de vuelta a empezar cuando los datos cambian.",
                cap="Un proyecto de ML se sube por tramos, y no termina en la cima: hay que volver a empezar cuando cambian los datos."),
         "en": dict(cols=[("Data", ["Collect and label", "Clean and validate", "Protect quality"]),
                          ("Model", ["Choose algorithm", "Avoid overfitting", "Validate and test"]),
                          ("Production", ["Integrate systems", "Monitor performance", "Retrain"])],
                loop="When the data changes, start again",
                label="Map of a machine learning project as a mountain with three stages: data, model and production, with an arrow back to the start when the data changes.",
                cap="An ML project is climbed in stages, and it doesn't end at the summit: you start again when the data changes.")}[lang]
    s = ('<polygon points="0,262 190,150 300,262" fill="var(--line)" fill-opacity=".9"/>'
         '<polygon points="0,262 570,70 680,262" fill="var(--paper)" stroke="var(--mute)" stroke-opacity=".6" stroke-width="2"/>'
         '<line x1="20" y1="255" x2="570" y2="70" stroke="var(--accent)" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>')
    camps = [(110, 225), (340, 147), (570, 70)]
    for (cx, cy), (head, lines) in zip(camps, L["cols"]):
        s += f'<line x1="{cx}" y1="{cy+12}" x2="{cx}" y2="294" stroke="var(--line)" stroke-width="2" stroke-dasharray="3 6"/>'
        s += f'<circle cx="{cx}" cy="{cy}" r="11" fill="var(--accent)" stroke="var(--paper)" stroke-width="3"/>'
        s += f'<text x="{cx}" y="326" text-anchor="middle" fill="var(--accent)" style="{DI};font-size:30px;font-weight:500">{head}</text>'
        for i, ln in enumerate(lines):
            s += f'<text x="{cx}" y="{362+i*29}" text-anchor="middle" fill="var(--ink)" style="{UI};font-size:20px">{ln}</text>'
    s += ('<line x1="570" y1="70" x2="570" y2="36" stroke="var(--ink)" stroke-width="3" stroke-linecap="round"/>'
          '<polygon points="570,36 600,47 570,58" fill="var(--accent)"/>')
    s += ('<path d="M570 438 V450 Q570 468 552 468 H128 Q110 468 110 450 V446" fill="none" stroke="var(--mute)" stroke-width="2.5" stroke-linecap="round"/>'
          '<polygon points="110,436 102,450 118,450" fill="var(--mute)"/>'
          f'<text x="340" y="498" text-anchor="middle" fill="var(--mute)" style="{UI};font-size:19px">{L["loop"]}</text>')
    return f'<figure class="diagram"><svg viewBox="0 0 680 510" role="img" aria-label="{L["label"]}">{s}</svg><figcaption>{L["cap"]}</figcaption></figure>'

def iceberg(lang):
    L = {"es": dict(chips=["Recogida de datos", "Verificación de datos", "Extracción de características", "Configuración",
                           "Gestión de recursos", "Herramientas de análisis", "Infraestructura de servicio", "Monitorización"],
                    tip=("Código", "del modelo"), seen="Lo que se ve", below="Lo que hay que sostener",
                    label="Iceberg: sobre el agua, el código del modelo; bajo el agua, la recogida y verificación de datos, la extracción de características, la configuración, la gestión de recursos, las herramientas de análisis, la infraestructura de servicio y la monitorización.",
                    cap="Construir el modelo es solo la punta: casi todo el trabajo está bajo el agua."),
         "en": dict(chips=["Data collection", "Data verification", "Feature extraction", "Configuration",
                           "Resource management", "Analysis tools", "Serving infrastructure", "Monitoring"],
                    tip=("Model", "code"), seen="What you see", below="What has to be maintained",
                    label="Iceberg: above the water, the model code; below it, data collection and verification, feature extraction, configuration, resource management, analysis tools, serving infrastructure and monitoring.",
                    cap="Building the model is only the tip: most of the work is under the water.")}[lang]
    s = ('<rect x="0" y="170" width="680" height="375" fill="var(--accent)" fill-opacity=".07"/>'
         '<line x1="0" y1="170" x2="680" y2="170" stroke="var(--accent)" stroke-opacity=".6" stroke-width="2"/>'
         '<polygon points="235,170 300,98 325,114 372,42 450,170" fill="var(--accent)"/>'
         '<polygon points="150,170 530,170 660,225 660,470 580,505 100,505 20,470 20,225" fill="var(--surface)" stroke="var(--accent)" stroke-width="2"/>')
    s += f'<text x="470" y="98" fill="var(--accent)" style="{UI};font-size:26px;font-weight:600">{L["tip"][0]}</text>'
    s += f'<text x="470" y="128" fill="var(--accent)" style="{UI};font-size:26px;font-weight:600">{L["tip"][1]}</text>'
    s += f'<text x="20" y="156" fill="var(--mute)" style="{UI};font-size:19px">{L["seen"]}</text>'
    for i, c in enumerate(L["chips"]):
        x = 40 if i % 2 == 0 else 355
        y = 235 + (i // 2) * 60
        s += (f'<rect x="{x}" y="{y}" width="285" height="46" rx="10" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>'
              f'<text x="{x+142}" y="{y+30}" text-anchor="middle" fill="var(--ink)" style="{UI};font-size:19px">{c}</text>')
    s += f'<text x="340" y="535" text-anchor="middle" fill="var(--mute)" style="{UI};font-size:19px">{L["below"]}</text>'
    return f'<figure class="diagram"><svg viewBox="0 0 680 548" role="img" aria-label="{L["label"]}">{s}</svg><figcaption>{L["cap"]}</figcaption></figure>'

def levels(lang):
    L = {"es": [("APIs preentrenadas", "Cloud Vision API", "https://cloud.google.com/vision",
                 "Usas un modelo que otros ya entrenaron, sin datos propios ni mucha programación. Ideal para resultados rápidos: detectar texto, analizar imágenes o traducir.", 1, "Esfuerzo bajo"),
                ("Custom AI", "Teachable Machine", "https://teachablemachine.withgoogle.com/",
                 "Aportas tus propios datos y la herramienta entrena y ajusta el modelo por ti, sin programar. Encaja en equipos con datos pero sin un gran equipo técnico.", 2, "Esfuerzo medio"),
                ("End-to-End AI", "TensorFlow", "https://www.tensorflow.org/",
                 "Diseñas, entrenas, pruebas, despliegas y escalas el modelo por tu cuenta, con control total. Es lo que usan los equipos técnicos.", 3, "Esfuerzo alto")],
         "en": [("Pre-trained APIs", "Cloud Vision API", "https://cloud.google.com/vision",
                 "You use a model others have already trained, with no data of your own and little coding. Ideal for quick results: detecting text, analysing images or translating.", 1, "Low effort"),
                ("Custom AI", "Teachable Machine", "https://teachablemachine.withgoogle.com/",
                 "You bring your own data and the tool trains and tunes the model for you, no coding. Fits teams that have data but not a large technical team.", 2, "Medium effort"),
                ("End-to-End AI", "TensorFlow", "https://www.tensorflow.org/",
                 "You design, train, test, deploy and scale the model on your own, with full control. It's what technical teams use.", 3, "High effort")]}[lang]
    out = []
    for title, eg, url, desc, n, eff in L:
        meter = "".join(f'<i class="on"></i>' if i < n else "<i></i>" for i in range(3))
        out.append(f'<div><p class="lvl-title">{title}</p><p class="lvl-eg"><a href="{url}">{eg}</a></p><p class="lvl-desc">{desc}</p>'
                   f'<p class="lvl-effort"><span class="meter" aria-hidden="true">{meter}</span>{eff}</p></div>')
    return '<div class="levels">' + "".join(out) + '</div>'

for l in ("es", "en"):
    (ROOT / f"content/{l}/snippets/montana.html").write_text(mountain(l) + "\n", encoding="utf-8")
    (ROOT / f"content/{l}/snippets/niveles.html").write_text(levels(l) + "\n", encoding="utf-8")
    (ROOT / f"content/{l}/snippets/iceberg.html").write_text(iceberg(l) + "\n", encoding="utf-8")
print("snippets ok")


# ---------- artículo 2: siete cajitas, escalera y tarjeta de niveles ----------
def siete(lang):
    L = {"es": (["Stakeholders", "Valor", "KPIs"], ["Diagnóstico", "Diseño"], ["Ejecución", "Reevaluación"], "lo que vimos en clase",
                "Las siete paradas de una estrategia de datos, con diagnóstico y diseño destacadas"),
         "en": (["Stakeholders", "Value", "KPIs"], ["Diagnosis", "Design"], ["Execution", "Re-evaluation"], "what we covered in class",
                "The seven stops of a data strategy, with diagnosis and design highlighted")}[lang]
    pre, mid, post, cap, label = L
    sep = '<span class="sep">›</span>'
    box = lambda t: f'<span class="st">{t}</span>'
    k = [0]
    def nw(inner):
        k[0] += 1
        return f'<span class="nw" style="--d:{k[0]*0.06:.2f}s">{sep}{inner}</span>'
    s = f'<span class="st" style="--d:0s">{pre[0]}</span>' + "".join(nw(box(t)) for t in pre[1:])
    s += nw(f'<span class="focus"><span class="row">{box(mid[0])}{sep}{box(mid[1])}</span><small>{cap}</small></span>')
    s += "".join(nw(box(t)) for t in post)
    return f'<div class="steps" role="group" aria-label="{label}">{s}</div>'

def escalera(lang):
    L = {"es": dict(y="↑ Madurez analítica", x="Ambición y adopción del dato →",
                    t=("Control", "Optimización", "Transformación"),
                    q=(("¿Qué ha pasado?", "Proteger lo que hay"), ("¿Qué pasará y cómo", "lo hago mejor?"), ("¿Qué negocio nuevo", "puedo crear?")),
                    label="Escalera de tres escalones ascendentes: control, optimización y transformación, de menor a mayor madurez analítica.",
                    cap="Tres etapas de una estrategia de datos, de menor a mayor madurez: no son mejores o peores, cada una pide cosas distintas."),
         "en": dict(y="↑ Analytical maturity", x="Data ambition and adoption →",
                    t=("Control", "Optimization", "Transformation"),
                    q=(("What happened?", "Protect what we have"), ("What will happen and", "how do we do it better?"), ("What new business", "can we create?")),
                    label="Staircase with three rising steps: control, optimization and transformation, from lower to higher analytical maturity.",
                    cap="Three stages of a data strategy, from lower to higher maturity: none is better or worse, each asks for different things.")}[lang]
    s = f'<text x="20" y="28" fill="var(--mute)" style="{UI};font-size:19px">{L["y"]}</text>'
    geo = [(20, 210, 120, .45), (240, 130, 200, .7), (460, 50, 280, 1)]
    for i, ((x, y, h, op), title, (q1, q2)) in enumerate(zip(geo, L["t"], L["q"])):
        s += f'<polygon points="{x},{y} {x+200},{y} {x+216},{y-14} {x+16},{y-14}" fill="var(--accent)" fill-opacity=".35"/>'
        s += f'<polygon points="{x+200},{y} {x+216},{y-14} {x+216},{y+h-14} {x+200},{y+h}" fill="var(--line)"/>'
        s += f'<rect x="{x}" y="{y}" width="200" height="{h}" rx="4" fill="var(--paper)" stroke="var(--line)" stroke-width="1.5"/>'
        s += f'<rect x="{x}" y="{y}" width="200" height="6" rx="3" fill="var(--accent)" fill-opacity="{op}"/>'
        s += f'<text x="{x+16}" y="{y+42}" fill="var(--accent)" style="{DI};font-size:24px;font-weight:500">{title}</text>'
        col2 = "var(--mute)" if i == 0 else "var(--ink)"
        s += f'<text x="{x+16}" y="{y+74}" fill="var(--ink)" style="{UI};font-size:17px">{q1}</text>'
        s += f'<text x="{x+16}" y="{y+97}" fill="{col2}" style="{UI};font-size:17px">{q2}</text>'
    s += '<line x1="10" y1="330" x2="670" y2="330" stroke="var(--mute)" stroke-opacity=".5" stroke-width="1.5"/>'
    s += f'<text x="340" y="364" text-anchor="middle" fill="var(--mute)" style="{UI};font-size:19px">{L["x"]}</text>'
    return f'<figure class="diagram"><svg viewBox="0 0 680 384" role="img" aria-label="{L["label"]}">{s}</svg><figcaption>{L["cap"]}</figcaption></figure>'

def tarjeta(lang):
    L = {"es": [("Nivel 1: problema serio", "Sin lenguaje común", "No hay un diccionario común y se confunde el glosario de negocio con el técnico."),
                ("Nivel 2: avanzando", "Lenguaje a medias", "Hay primeros diccionarios por área y los términos se incluyen según su uso."),
                ("Nivel 3: bien alineado", "Lenguaje compartido", "Un glosario completo, coordinado por la dirección de datos y cuidado por los responsables de cada término.")],
         "en": [("Level 1: serious problem", "No common language", "There is no shared dictionary and the business glossary gets mixed up with the technical one."),
                ("Level 2: making progress", "Half a language", "First dictionaries exist by area, and terms are added according to how much they're used."),
                ("Level 3: well aligned", "Shared language", "A complete glossary, coordinated by data leadership and kept up by the owner of each term.")]}[lang]
    out = []
    for n, (lab, title, desc) in enumerate(L, 1):
        meter = "".join('<i class="on"></i>' if i < n else "<i></i>" for i in range(3))
        out.append(f'<div><p class="lvl-meter"><span class="meter" aria-hidden="true">{meter}</span>{lab}</p><p class="lvl-title">{title}</p><p class="lvl-desc">{desc}</p></div>')
    return '<div class="levels">' + "".join(out) + '</div>'

for l in ("es", "en"):
    (ROOT / f"content/{l}/snippets/siete.html").write_text(siete(l) + "\n", encoding="utf-8")
    (ROOT / f"content/{l}/snippets/escalera.html").write_text(escalera(l) + "\n", encoding="utf-8")
    (ROOT / f"content/{l}/snippets/tarjeta.html").write_text(tarjeta(l) + "\n", encoding="utf-8")
print("snippets artículo 2 ok")


for l in ("es", "en"):
    (ROOT / f"content/{l}/snippets/montana.html").write_text(art.mountain_diagram(l) + "\n", encoding="utf-8")
    (ROOT / f"content/{l}/snippets/iceberg.html").write_text(art.iceberg_diagram(l) + "\n", encoding="utf-8")
    (ROOT / f"content/{l}/snippets/galletas.html").write_text(art.galletas(l) + "\n", encoding="utf-8")

(ROOT / "content/art").mkdir(exist_ok=True)
for name, fn in (("compass", lambda d: art.compass_scene(d, crop=True)), ("iceberg", art.iceberg_scene), ("bins", lambda d: art.bins_scene(d, crop=True))):
    (ROOT / f"content/art/{name}.svg").write_text(fn(True), encoding="utf-8")
print("art ok")
