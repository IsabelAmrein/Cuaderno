# Isabel Amrein

*Del dato al producto.* Sitio personal, estático y bilingüe (español e inglés) de Isabel Amrein De Luca, con proyectos y apuntes sobre datos, IA generativa y producto.

**Web:** https://isabelamrein.github.io/Cuaderno/

## Qué hay en este repositorio
| Carpeta o archivo | Qué es |
|---|---|
| `docs/` | La web ya generada. GitHub Pages publica esta carpeta |
| `content/` | El contenido: entradas, proyectos y Sobre mí, en español e inglés, y las ilustraciones |
| `build.py` y `site.json` | El generador (Python 3) y la configuración del sitio |
| `assets/` | Estilos, script, tipografías propias y librerías, cada una con su licencia |
| `herramientas/` | Scripts que dibujan las ilustraciones |

## Reconstruir la web
```
python3 herramientas/gen_diagrams.py && python3 herramientas/render_art.py && python3 build.py
```
Necesita Python 3 con `Pillow`, `PyYAML` y `playwright` (este, solo para convertir las ilustraciones a imagen).

© Isabel Amrein De Luca. Las tipografías y librerías conservan sus licencias (ver `assets/fonts/LICENSES.txt` y `assets/vendor/`).
