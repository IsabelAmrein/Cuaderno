# Skills opcionales de diseño y movimiento

Una *skill* es un conjunto de instrucciones que se añade a Claude para que trabaje de una forma concreta. Aquí hay dos opciones que Isabel ha mencionado.

> Estado: **no están instaladas** en el entorno donde se construyó este proyecto. Isabel puede añadirlas a su cuenta. Se anotan aquí para que el Arquitecto sepa que existen.

## Lo que ya se usa
- **`frontend-design`** (incluida en Claude): guía de diseño visual intencionado, con criterio tipográfico y de composición. Es la que respalda la identidad del Cuaderno.

## Movimiento: skills de Emil Kowalski
- Repositorio: `github.com/emilkowalski/skills`.
- Incluye, entre otras: `animate` (crear una animación decidiendo propósito, herramienta, curva y duración), `review-animations` (revisar el movimiento existente) e `improve-animations` (auditar una base de código).
- Idea que coincide con este proyecto: no instalar una librería de movimiento para un simple desvanecimiento, y que `reducir movimiento` forme parte del mismo cambio.

## Criterio de diseño: taste-skill
- Repositorio: `github.com/Leonxlnx/taste-skill` (existen también variantes de otras personas).
- Busca evitar interfaces genéricas: obliga a elegir una dirección visual y a pasar una revisión final.

## Lo que dice la revisión del Auditor (12 de octubre de 2026)
| Skill | Veredicto | Lectura |
|---|---|---|
| [emilkowalski/skills](../auditorias/2026-10-12-emilkowalski-skills.md) | 🟢 | Tiene 15 skills; nos sirven 6: `animate`, `review-animations`, `improve-animations`, `find-animation-opportunities`, `animation-performance` y `break-ui` (la mayor, 14 KB). Sin riesgos |
| [Leonxlnx/taste-skill](../auditorias/2026-10-12-leonxlnx-taste-skill.md) | 🔴 | Segura, pero la principal pesa 88 KB de contexto. Mejor probar las ligeras |

## Antes de instalar cualquiera
1. **Léela entera.** Una skill es contenido que Claude ejecutará como instrucciones.
2. **Comprueba el autor y la licencia.**
3. Después de instalarla, el Arquitecto la usará solo cuando encaje con el mini objetivo (por ejemplo, el Maquetador con las de movimiento).
4. Si el resultado choca con `BRAND.md` o con las reglas del proyecto, mandan `BRAND.md` y las reglas.
