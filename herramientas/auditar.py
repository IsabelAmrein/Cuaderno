#!/usr/bin/env python3
"""Herramienta del agente Auditor: revisa proyectos públicos antes de incorporarlos al Cuaderno.

Uso:
  python3 herramientas/auditar.py npm   thinking-orbs [--archivo assets/vendor/thinking-orbs.js]
  python3 herramientas/auditar.py pypi  markdown
  python3 herramientas/auditar.py github Jakubantalik/thinking-orbs
  python3 herramientas/auditar.py skill  emilkowalski/skills

Genera un informe en documentacion/auditorias/ con un semáforo por criterio.
No instala nada en el proyecto: trabaja en carpetas temporales.
"""
import argparse, datetime as dt, json, pathlib, re, shutil, subprocess, sys, tarfile, tempfile, urllib.request, zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "documentacion" / "auditorias"
LICENCIAS_OK = {"MIT", "ISC", "BSD-2-Clause", "BSD-3-Clause", "Apache-2.0", "OFL-1.1", "CC0-1.0", "Unlicense", "0BSD", "MIT-0", "HPND", "PSF-2.0", "MIT-CMU"}
LICENCIAS_FUERTES = ("GPL", "AGPL", "SSPL", "EUPL", "CC-BY-NC", "BUSL")
PERFIL = "sitio estático, sin framework (sin React), navegador moderno, generador en Python 3.12"

PATRONES = {
    "evaluación dinámica de código": r"\beval\s*\(|new\s+Function\s*\(",
    "peticiones de red": r"\bfetch\s*\(|XMLHttpRequest|WebSocket|sendBeacon|EventSource|urllib\.request|requests\.(get|post)|socket\.",
    "cookies o almacenamiento": r"document\.cookie|localStorage|sessionStorage|indexedDB",
    "ejecución de comandos": r"child_process|os\.system|subprocess|\bspawn\s*\(",
    "variables de entorno": r"process\.env|os\.environ",
    "texto codificado muy largo": r"[A-Za-z0-9+/]{300,}={0,2}",
}
PATRONES_SKILL = {
    "descarga y ejecuta": r"curl[^\n]*\|\s*(ba)?sh|wget[^\n]*\|\s*(ba)?sh|powershell[^\n]*iex",
    "borrado o permisos peligrosos": r"rm\s+-rf|chmod\s+777|\bsudo\b",
    "instrucciones para ocultar o ignorar": r"ignore (all )?(previous|prior) instructions|do not (tell|inform|mention)[^\n]*user|without (telling|informing) the user",
    "envío de datos o credenciales": r"exfiltrat|send[^\n]{0,40}(api[_ -]?key|token|password|credentials)|\.env\b",
    "codificado en base64": r"base64\s+(-d|--decode)|atob\(",
}
SEM = {"verde": "🟢", "ambar": "🟡", "rojo": "🔴"}


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "cuaderno-auditor", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8"))


def get_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "cuaderno-auditor"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read(300_000).decode("utf-8", "ignore")


def run(cmd, cwd=None, timeout=120):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


DEFENSIVO = re.compile(r"\bflag\b|data, not instructions|\binert\b|never follow|do not follow|don't follow|prompt injection|\binjection\b|untrusted|treat (file|repository)", re.I)


def escanear_skill(texto):
    """Cuenta coincidencias reales y, aparte, las menciones defensivas (ejemplos de lo que NO hay que obedecer)."""
    reales, defensivas = {}, 0
    for linea in texto.splitlines():
        for k, p in PATRONES_SKILL.items():
            if re.search(p, linea, re.I):
                if k == "instrucciones para ocultar o ignorar" and DEFENSIVO.search(linea):
                    defensivas += 1
                else:
                    reales[k] = reales.get(k, 0) + 1
    return reales, defensivas


def escanear(texto, patrones):
    return {k: len(re.findall(p, texto, re.I)) for k, p in patrones.items() if re.search(p, texto, re.I)}


def hace(m):
    n = int(round(m))
    return "hace menos de un mes" if n == 0 else f"hace {n} {'mes' if n == 1 else 'meses'}"


def meses(fecha_iso):
    d = dt.datetime.fromisoformat(fecha_iso.replace("Z", "+00:00")).replace(tzinfo=None)
    return (dt.datetime.now() - d).days / 30.4


def clasifica_licencia(lic):
    if not lic or str(lic).upper() in ("UNKNOWN", "NONE", "UNLICENSED"):
        return "rojo", "Sin licencia clara: no se puede reutilizar legalmente."
    if any(x in str(lic).upper() for x in LICENCIAS_FUERTES):
        return "rojo", f"Licencia {lic}: copyleft fuerte o restrictiva, incompatible con un sitio que se publica y se copia."
    if str(lic) in LICENCIAS_OK:
        return "verde", f"Licencia {lic}: permisiva. Hay que conservar el aviso de copyright."
    return "ambar", f"Licencia {lic}: no está en la lista habitual. Hay que leerla antes de usarla."


def auditar_npm(pkg, archivo):
    ev = {"tipo": "npm", "nombre": pkg, "detalle": [], "patrones": {}, "notas": []}
    r = run(["npm", "view", pkg, "--json"])
    if r.returncode != 0:
        sys.exit(f"No se encontró el paquete npm '{pkg}'.")
    m = json.loads(r.stdout)
    ver = m.get("version")
    lic = m.get("license")
    deps = list((m.get("dependencies") or {}).keys())
    peers = m.get("peerDependencies") or {}
    ev.update(version=ver, licencia=lic, autor=(m.get("author") or {}).get("name") if isinstance(m.get("author"), dict) else m.get("author"),
              repo=(m.get("repository") or {}).get("url") if isinstance(m.get("repository"), dict) else m.get("repository"),
              modificado=(m.get("time") or {}).get("modified"), creado=(m.get("time") or {}).get("created"), deprecated=m.get("deprecated"),
              mantenedores=len(m.get("maintainers") or []), pagina=m.get("homepage"))
    ev["detalle"] += [f"Versión analizada: {ver}", f"Creado: {(ev['creado'] or '?')[:10]}; última publicación: {(ev['modificado'] or '?')[:10]}; personas mantenedoras: {ev['mantenedores']}",
                       f"Página del proyecto: {ev['pagina']}", f"Dependencias directas: {deps or 'ninguna'}", f"Dependencias de pares (peer): {peers or 'ninguna'}"]
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        run(["npm", "pack", f"{pkg}@{ver}"], cwd=tmp, timeout=120)
        tgz = next(tmp.glob("*.tgz"))
        with tarfile.open(tgz) as t:
            t.extractall(tmp / "x")
        pk = tmp / "x" / "package"
        archivos = [f for f in pk.rglob("*") if f.is_file()]
        peso = sum(f.stat().st_size for f in archivos)
        js = [f for f in archivos if f.suffix in (".js", ".cjs", ".mjs")]
        ev["peso_kb"] = round(peso / 1024, 1)
        ev["detalle"] += [f"Archivos: {len(archivos)}; peso descomprimido: {ev['peso_kb']} KB; archivos JavaScript: {len(js)}"]
        pj = json.loads((pk / "package.json").read_text(encoding="utf-8"))
        scripts = {k: v for k, v in (pj.get("scripts") or {}).items() if k in ("preinstall", "install", "postinstall", "prepare")}
        ev["scripts_instalacion"] = scripts
        ev["detalle"].append(f"Scripts que se ejecutan al instalar: {scripts or 'ninguno'}")
        total = {}
        for f in js:
            for k, v in escanear(f.read_text(encoding="utf-8", errors="ignore"), PATRONES).items():
                total[k] = total.get(k, 0) + v
        ev["patrones"] = total
        # auditoría de vulnerabilidades conocidas
        aud = tmp / "aud"; aud.mkdir()
        run(["npm", "init", "-y"], cwd=aud)
        run(["npm", "install", "--package-lock-only", "--ignore-scripts", f"{pkg}@{ver}"], cwd=aud, timeout=150)
        a = run(["npm", "audit", "--json"], cwd=aud, timeout=120)
        try:
            vul = json.loads(a.stdout).get("metadata", {}).get("vulnerabilities", {})
            lock = json.loads((aud / "package-lock.json").read_text(encoding="utf-8"))
            ev["transitivas"] = max(0, len(lock.get("packages", {})) - 2)
        except Exception:
            vul, ev["transitivas"] = {}, None
        ev["vulnerabilidades"] = vul
        ev["detalle"].append(f"Vulnerabilidades conocidas (npm audit): {vul or 'no se pudo comprobar'}; dependencias transitivas: {ev['transitivas']}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if archivo:
        f = pathlib.Path(archivo)
        if f.exists():
            ev["archivo"] = {"ruta": str(archivo), "kb": round(f.stat().st_size / 1024, 1), "patrones": escanear(f.read_text(encoding="utf-8", errors="ignore"), PATRONES),
                             "menciona_react": bool(re.search(r"react", f.read_text(encoding="utf-8", errors="ignore"), re.I))}
    ev["peers"] = peers
    ev["n_deps"] = len(deps)
    return ev


def auditar_pypi(pkg):
    m = get_json(f"https://pypi.org/pypi/{pkg}/json")
    i = m["info"]; ver = i["version"]
    files = m["releases"].get(ver, [])
    clasif = next((c.split("::")[-1].strip() for c in i.get("classifiers", []) if c.startswith("License :: OSI Approved")), None)
    mapa = {"MIT License": "MIT", "BSD License": "BSD-3-Clause", "Apache Software License": "Apache-2.0", "Historical Permission Notice and Disclaimer (HPND)": "HPND", "ISC License (ISCL)": "ISC"}
    ev = {"tipo": "pypi", "nombre": pkg, "version": ver, "licencia": i.get("license_expression") or mapa.get(clasif, clasif),
          "autor": i.get("author") or i.get("maintainer"), "repo": next((u for u in list((i.get("project_urls") or {}).values()) + [i.get("home_page") or ""] if "github.com" in (u or "") or "gitlab" in (u or "")), None),
          "modificado": max((f["upload_time_iso_8601"] for f in files), default=None), "deprecated": any(f.get("yanked") for f in files),
          "peso_kb": round(min((f["size"] for f in files), default=0) / 1024, 1), "patrones": {}, "notas": [], "detalle": []}
    reqs = [r for r in (i.get("requires_dist") or []) if "extra ==" not in r]
    ev["n_deps"] = len(reqs)
    ev["detalle"] += [f"Versión analizada: {ver}", f"Requiere Python: {i.get('requires_python')}", f"Dependencias obligatorias: {reqs or 'ninguna'}"]
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        run([sys.executable, "-m", "pip", "download", f"{pkg}=={ver}", "--no-deps", "-d", str(tmp)], timeout=180)
        total = {}
        for f in tmp.iterdir():
            if f.suffix == ".whl":
                with zipfile.ZipFile(f) as z:
                    for n in z.namelist():
                        if n.endswith(".py"):
                            for k, v in escanear(z.read(n).decode("utf-8", "ignore"), PATRONES).items():
                                total[k] = total.get(k, 0) + v
        ev["patrones"] = total
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ev["peers"] = {}
    ev["vulnerabilidades"] = {}
    ev["scripts_instalacion"] = {}
    return ev


def api_opcional(slug):
    try:
        return get_json(f"https://api.github.com/repos/{slug}")
    except Exception:
        return None


def clonar(slug):
    tmp = pathlib.Path(tempfile.mkdtemp())
    r = run(["git", "clone", "--depth", "1", f"https://github.com/{slug}.git", str(tmp / "r")], timeout=240)
    if r.returncode != 0:
        shutil.rmtree(tmp, ignore_errors=True)
        sys.exit(f"No se pudo clonar https://github.com/{slug}: {r.stderr.strip()[:200]}")
    return tmp, tmp / "r"


def detectar_licencia(repo):
    for f in sorted(repo.glob("LICEN[SC]E*")) + sorted(repo.glob("COPYING*")):
        t = f.read_text(encoding="utf-8", errors="ignore")[:1500].lower()
        for clave, spdx in (("mit license", "MIT"), ("permission is hereby granted, free of charge", "MIT"), ("apache license", "Apache-2.0"), ("gnu affero", "AGPL-3.0"),
                            ("gnu general public", "GPL-3.0"), ("gnu lesser", "LGPL-3.0"), ("mozilla public", "MPL-2.0"), ("isc license", "ISC"), ("unlicense", "Unlicense"),
                            ("redistribution and use in source and binary", "BSD-3-Clause")):
            if clave in t:
                return spdx
        return f"texto de {f.name} no reconocido"
    return None


def auditar_github(slug, como_skill=False, solo=None):
    tmp, repo = clonar(slug)
    try:
        fecha = run(["git", "log", "-1", "--format=%cI"], cwd=repo).stdout.strip()
        api = api_opcional(slug)
        archivos = [p for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts]
        kb = round(sum(p.stat().st_size for p in archivos) / 1024, 1)
        ev = {"tipo": "skill" if como_skill else "github", "nombre": slug, "version": run(["git", "rev-parse", "--short", "HEAD"], cwd=repo).stdout.strip(),
              "licencia": (api or {}).get("license", {}) and api["license"].get("spdx_id") or detectar_licencia(repo), "autor": slug.split("/")[0], "repo": f"https://github.com/{slug}",
              "modificado": fecha, "creado": (api or {}).get("created_at"), "deprecated": (api or {}).get("archived", False), "peso_kb": kb, "patrones": {}, "peers": {},
              "vulnerabilidades": {}, "scripts_instalacion": {}, "n_deps": 0, "notas": [], "detalle": [f"Archivos: {len(archivos)}; peso total: {kb} KB; último cambio: {fecha[:10]}"]}
        if api:
            ev["detalle"].append(f"Estrellas: {api.get('stargazers_count')}; forks: {api.get('forks_count')}; incidencias abiertas: {api.get('open_issues_count')}; archivado: {api.get('archived')}")
        else:
            ev["detalle"].append("La API de GitHub no respondió (límite de peticiones): faltan estrellas y fecha de creación.")
        if como_skill:
            md = [p for p in archivos if p.name.lower() == "skill.md" and (not solo or p.parent.name in solo)]
            code = [p for p in archivos if p.suffix in (".sh", ".py", ".js", ".ts", ".ps1") and (not solo or any(x in solo for x in p.parts))]
            if solo:
                ev["detalle"].append(f"Revisión limitada a las skills elegidas: {sorted(solo)}")
            ev["detalle"] += [f"Skills encontradas (SKILL.md): {len(md)}", f"Scripts incluidos: {len(code)} {[str(p.relative_to(repo)) for p in code[:6]]}"]
            total, instal, defens = {}, set(), 0
            for p in (md + ([q for q in archivos if q.suffix == '.md' and q not in md] if not solo else []) + code)[:120]:
                txt = p.read_text(encoding="utf-8", errors="ignore")[:200_000]
                reales, d = escanear_skill(txt)
                defens += d
                for k, v in reales.items():
                    total[k] = total.get(k, 0) + v
                for m in re.findall(r"(?:npm i(?:nstall)?|npx|pip install|brew install)[^\n`]{0,80}", txt):
                    instal.add(m.strip())
            ev["patrones"] = total
            mayor = max((p.stat().st_size for p in md), default=0)
            ev["peso_kb"] = round(mayor / 1024, 1)
            ev["detalle"].append(f"SKILL.md más grande: {ev['peso_kb']} KB (es lo que se carga en la conversación; el resto del repositorio no cuenta); total de SKILL.md: {round(sum(p.stat().st_size for p in md) / 1024, 1)} KB")
            ev["detalle"].append(f"Frases defensivas que mencionan ataques de inyección como ejemplo (no son órdenes): {defens}")
            ev["detalle"].append(f"Instalaciones que pide en sus textos: {sorted(instal)[:8] or 'ninguna'}")
            ev["scripts_instalacion"] = {"scripts": len(code)} if code else {}
        return ev
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def auditar_skill(slug, solo=None):
    return auditar_github(slug, como_skill=True, solo=solo)


def semaforo(ev):
    c = {}
    c["Licencia"] = clasifica_licencia(ev.get("licencia"))
    # seguridad
    s, txt = "verde", "Sin vulnerabilidades conocidas ni patrones de riesgo."
    vul = ev.get("vulnerabilidades") or {}
    alto = (vul.get("high", 0) or 0) + (vul.get("critical", 0) or 0)
    riesgo = [k for k in ev.get("patrones", {}) if k in ("evaluación dinámica de código", "ejecución de comandos", "texto codificado muy largo", "descarga y ejecuta", "borrado o permisos peligrosos",
                                                             "instrucciones para ocultar o ignorar", "envío de datos o credenciales", "codificado en base64")]
    red = [k for k in ev.get("patrones", {}) if k in ("peticiones de red", "cookies o almacenamiento", "variables de entorno")]
    if alto or ev.get("tipo") == "skill" and riesgo:
        s, txt = "rojo", f"Hay {alto} vulnerabilidades altas o críticas." if alto else f"Patrones peligrosos: {', '.join(riesgo)}."
    elif ev.get("scripts_instalacion") or riesgo or red or (sum(vul.values()) if vul else 0):
        s, txt = "ambar", "Revisar: " + ", ".join(filter(None, [("scripts de instalación" if ev.get("scripts_instalacion") else ""), ", ".join(riesgo), ", ".join(red),
                                                               (f"{sum(vul.values())} vulnerabilidades menores" if vul and sum(vul.values()) else "")])) + "."
    c["Seguridad"] = (s, txt)
    # mantenimiento y madurez
    if ev.get("deprecated"):
        c["Mantenimiento"] = ("rojo", "Marcado como obsoleto o archivado.")
    elif ev.get("modificado"):
        mm = meses(ev["modificado"])
        est = "verde" if mm < 12 else "ambar" if mm < 30 else "rojo"
        txt = f"Última actividad {hace(mm)}."
        if ev.get("creado") and meses(ev["creado"]) < 6:
            est = "ambar" if est == "verde" else est
            txt += f" Proyecto joven: creado {hace(meses(ev['creado']))}."
        if ev.get("mantenedores") == 1:
            txt += " Lo mantiene una sola persona."
        c["Mantenimiento"] = (est, txt)
    else:
        c["Mantenimiento"] = ("ambar", "No se pudo determinar la última actividad.")
    if ev["tipo"] in ("npm", "pypi"):
        c["Procedencia"] = ("verde", f"Repositorio declarado: {ev.get('repo')}.") if ev.get("repo") else ("ambar", "No declara un repositorio de código: no se puede comprobar su origen.")
    # eficiencia
    kb = (ev.get("archivo") or {}).get("kb") or ev.get("peso_kb") or 0
    nd = ev.get("n_deps") or 0
    if ev["tipo"] == "skill":
        c["Eficiencia"] = ("verde" if kb < 30 else "ambar" if kb < 80 else "rojo", f"La SKILL.md más grande pesa {kb} KB: es el coste de contexto cada vez que se usa.")
    elif (ev.get("archivo") or {}).get("kb"):
        c["Eficiencia"] = ("verde" if kb < 100 and nd <= 3 else "ambar" if kb < 500 and nd <= 15 else "rojo", f"El archivo que se incorpora pesa {kb} KB; {nd} dependencias propias.")
    else:
        c["Eficiencia"] = ("verde" if kb < 100 and nd <= 3 else "ambar", f"Paquete completo: {kb} KB y {nd} dependencias propias. Si solo se incorpora una parte, indicar el archivo con --archivo para medir lo real.")
    # compatibilidad
    peers = ev.get("peers") or {}
    if peers:
        c["Compatibilidad"] = ("ambar", f"Declara dependencias de pares {list(peers)}; nuestro perfil es: {PERFIL}. Comprobar si se puede usar sin ellas.")
        if (ev.get("archivo") or {}).get("menciona_react") is False:
            c["Compatibilidad"] = ("verde", f"Declara {list(peers)}, pero el archivo que realmente usamos no los necesita. Perfil: {PERFIL}.")
    else:
        c["Compatibilidad"] = ("verde", f"Sin dependencias de pares. Perfil del proyecto: {PERFIL}.")
    peor = "rojo" if any(v[0] == "rojo" for v in c.values()) else "ambar" if any(v[0] == "ambar" for v in c.values()) else "verde"
    return c, peor


def informe(ev, nota):
    c, peor = semaforo(ev)
    dec = {"verde": "Se puede adoptar.", "ambar": "Se puede adoptar con condiciones (ver los criterios en ámbar y las condiciones de adopción).", "rojo": "No adoptar hasta resolver los puntos en rojo."}[peor]
    hoy = dt.date.today().isoformat()
    L = [f"# Revisión de {ev['nombre']}", "", f"- **Fecha:** {hoy}", f"- **Tipo:** {ev['tipo']}", f"- **Versión o rama:** {ev.get('version')}",
         f"- **Autoría:** {ev.get('autor')}", f"- **Repositorio:** {ev.get('repo')}", f"- **Veredicto:** {SEM[peor]} {dec}", "", "## Semáforo", "", "| Criterio | Estado | Por qué |", "|---|---|---|"]
    L += [f"| {k} | {SEM[v[0]]} | {v[1]} |" for k, v in c.items()]
    L += ["", "## Evidencias"] + [f"- {d}" for d in ev["detalle"]]
    if ev.get("patrones"):
        L += ["", "### Patrones detectados en el código", "Un patrón no es un fallo por sí solo: indica dónde mirar."] + [f"- {k}: {v} coincidencias" for k, v in ev["patrones"].items()]
    else:
        L += ["", "### Patrones detectados en el código", "- Ninguno de los patrones de riesgo buscados."]
    if ev.get("archivo"):
        a = ev["archivo"]
        L += ["", f"### Archivo que realmente se incorpora ({a['ruta']})", f"- Peso: {a['kb']} KB", f"- Patrones de riesgo: {a['patrones'] or 'ninguno'}", f"- Menciona React: {a['menciona_react']}"]
    if nota:
        L += ["", "## Notas del Auditor", nota]
    L += ["", "## Condiciones de adopción", "- [ ] Alojar el archivo en `assets/vendor` y fijar la versión.", "- [ ] Incluir el texto de la licencia junto al archivo.", "- [ ] Probar con `reducir movimiento` y sin JavaScript.",
          "- [ ] Anotar la decisión en `documentacion/DECISIONES.md` y la versión en `documentacion/DEPENDENCIAS.md`.", "", "## Cómo retirarlo", "Borrar el archivo de `assets/vendor`, quitar su `<script>` en `build.py` y la parte de `assets/main.js` que lo usa.", "",
          "> Esta herramienta busca señales conocidas. No sustituye a leer el código de lo que va a ejecutarse en tu web.", ""]
    return "\n".join(L), peor, c


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tipo", choices=["npm", "pypi", "github", "skill"])
    ap.add_argument("objetivo")
    ap.add_argument("--archivo", help="Archivo local que realmente se incorpora (para escanearlo)")
    ap.add_argument("--nota", default="", help="Notas del Auditor para añadir al informe")
    ap.add_argument("--solo", help="Solo para skills: lista de carpetas de skills a revisar, separadas por comas")
    ap.add_argument("--no-guardar", action="store_true")
    a = ap.parse_args()
    ev = {"npm": lambda: auditar_npm(a.objetivo, a.archivo), "pypi": lambda: auditar_pypi(a.objetivo), "github": lambda: auditar_github(a.objetivo), "skill": lambda: auditar_skill(a.objetivo, set(a.solo.split(",")) if a.solo else None)}[a.tipo]()
    texto, peor, c = informe(ev, a.nota)
    if not a.no_guardar:
        OUT.mkdir(parents=True, exist_ok=True)
        f = OUT / f"{dt.date.today().isoformat()}-{re.sub(r'[^a-z0-9]+', '-', a.objetivo.lower()).strip('-')}.md"
        f.write_text(texto, encoding="utf-8")
        print("Informe:", f.relative_to(ROOT))
    print(f"{ev['nombre']}: {SEM[peor]}  |  " + "  ".join(f"{k} {SEM[v[0]]}" for k, v in c.items()))


if __name__ == "__main__":
    main()
