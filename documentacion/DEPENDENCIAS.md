# Inventario de dependencias

Todo lo que no escribimos nosotros. Revisado con la herramienta del [Auditor](agentes/subagentes/09-auditor.md) el 2026-10-12.

| Componente | Tipo | Versión | Licencia | Para qué se usa | ¿Llega a la web? | Estado |
|---|---|---|---|---|---|---|
| markdown | Python (PyPI) | 3.11 | BSD-3-Clause | `build.py`: convierte los artículos de Markdown en HTML | No, solo al generar | 🟡 |
| Pillow | Python (PyPI) | 12.3.0 | MIT-CMU | `build.py`: imágenes para compartir en LinkedIn | No, solo al generar | 🟡 |
| playwright | Python (PyPI) | 1.63.0 | Apache-2.0 | `herramientas/render_art.py` y pruebas de calidad | No, solo para pruebas y arte | 🟡 |
| esbuild | npm | 0.28.2 | MIT | Empaquetó una vez el motor de los orbes | No, ya no se usa en el proyecto | 🟡 |
| thinking-orbs | npm | 0.3.2 | MIT | `assets/vendor/thinking-orbs.js`: indicador "pensando" y orbes de los proyectos en marcha | Sí (15,5 KB) | 🟡 |
| Newsreader | npm (fuente) | 5.3.0 | OFL-1.1 | `assets/fonts`: títulos | Sí (solo latín y latín extendido) | 🟡 |
| Figtree | npm (fuente) | 5.3.0 | OFL-1.1 | `assets/fonts`: texto | Sí (solo latín y latín extendido) | 🟢 |
| JetBrains Mono | npm (fuente) | 5.3.0 | OFL-1.1 | `assets/fonts`: fechas y código | Sí (solo latín y latín extendido) | 🟡 |

**Cómo leer el estado:** 🟢 sin reservas, 🟡 se puede usar con condiciones, 🔴 no adoptar, ⚪ no se pudo revisar.

## Notas
- Los **ámbar de Eficiencia** de los paquetes de fuentes se deben a que el paquete completo trae muchos alfabetos. Nosotros solo copiamos el latín y el latín extendido (unos 180 KB en total).
- **Pillow** aparece en ámbar en Seguridad porque incluye utilidades que abren programas externos (por ejemplo, para mostrar una imagen). Nosotros solo la usamos para crear y guardar imágenes, y solo en la generación, nunca en la web.
- **thinking-orbs** está en ámbar por ser un proyecto joven mantenido por una sola persona. La mitigación es tener una copia alojada con la versión fijada. Informe completo en [`auditorias`](auditorias/2026-10-12-thinking-orbs.md).
- Los componentes de la web (fuentes y orbes) llevan su licencia en `assets/fonts/LICENSES.txt` y `assets/vendor/thinking-orbs-LICENSE.txt`.

## Revisadas y no adoptadas
| Proyecto | Veredicto | Por qué no |
|---|---|---|
| [Motion](auditorias/2026-10-12-motion.md) (librería de animación) | 🟡 | Pesa unos 757 KB y no hace falta: nuestras animaciones se resuelven con CSS y 15 KB propios |
| [taste-skill](auditorias/2026-10-12-leonxlnx-taste-skill.md) | 🔴 | Segura, pero su skill principal pesa 88 KB de contexto |

## Skills pendientes de decidir por Isabel
Seis de las skills de [Emil Kowalski](auditorias/2026-10-12-emilkowalski-skills.md) (🟢). No son parte del sitio: se instalan en la cuenta. Ver [`agentes/SKILLS.md`](agentes/SKILLS.md).

