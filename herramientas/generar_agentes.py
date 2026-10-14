#!/usr/bin/env python3
"""Genera documentacion/agentes/agentes.yaml a partir de las fichas de subagentes y lo valida."""
import pathlib, re, yaml
D = pathlib.Path(__file__).resolve().parents[1] / "documentacion" / "agentes"
subs = []
for f in sorted((D / "subagentes").glob("*.md")):
    t = f.read_text(encoding="utf-8")
    ident = f.stem.split("-", 1)[1]
    campo = lambda *ks: next((m.group(1).strip() for k in ks if (m := re.search(rf"^\*\*{re.escape(k)}\.\*\* (.+)$", t, re.M))), "")
    sec = t.split("## Cuánto tarda un mini objetivo")[1].split("\n> ")[0]
    est = [{"objetivo": a.strip(), "tiempo": b.strip()} for a, b in re.findall(r"^\| (?!Mini objetivo|---)(.+?) \| (.+?) \|$", sec, re.M)]
    subs.append({"id": ident, "nombre": re.search(r"^# Subagente \d+: (.+)$", t, re.M).group(1).strip(), "mision": campo("Misión"), "idioma": campo("Idioma de trabajo"),
                 "lenguajes": campo("Lenguajes", "Lenguajes y herramientas"), "documento": f"agentes/subagentes/{f.name}", "estimaciones": est})
data = {"arquitecto": {"nombre": "Arquitecto", "mision": "Coordinar el proyecto, descomponer objetivos en mini objetivos, asignarlos, controlar las reglas y aprobar cada versión.",
                       "idioma": "Español", "lenguajes": ["Markdown", "YAML", "tablas de planificación"], "limite_mini_objetivo_min": 60, "documento": "agentes/ARQUITECTO.md"},
        "subagentes": subs}
cab = "# Equipo de agentes del sitio. Se genera con herramientas/generar_agentes.py a partir de las fichas de subagentes/. No se edita a mano.\n"
(D / "agentes.yaml").write_text(cab + yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
chk = yaml.safe_load((D / "agentes.yaml").read_text(encoding="utf-8"))
print("agentes.yaml válido:", len(chk["subagentes"]), "subagentes")
