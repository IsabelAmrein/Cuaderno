# Revisión de Leonxlnx/taste-skill

- **Fecha:** 2026-10-12
- **Tipo:** skill
- **Versión o rama:** d237dd3
- **Autoría:** Leonxlnx
- **Repositorio:** https://github.com/Leonxlnx/taste-skill
- **Veredicto:** 🔴 No adoptar hasta resolver los puntos en rojo.

## Semáforo

| Criterio | Estado | Por qué |
|---|---|---|
| Licencia | 🟢 | Licencia MIT: permisiva. Hay que conservar el aviso de copyright. |
| Seguridad | 🟡 | Revisar: scripts de instalación. |
| Mantenimiento | 🟢 | Última actividad hace menos de un mes. |
| Eficiencia | 🔴 | La SKILL.md más grande pesa 87.4 KB: es el coste de contexto cada vez que se usa. |
| Compatibilidad | 🟢 | Sin dependencias de pares. Perfil del proyecto: sitio estático, sin framework (sin React), navegador moderno, generador en Python 3.12. |

## Evidencias
- Archivos: 67; peso total: 6396.0 KB; último cambio: 2026-10-11
- La API de GitHub no respondió (límite de peticiones): faltan estrellas y fecha de creación.
- Skills encontradas (SKILL.md): 13
- Scripts incluidos: 3 ['skill.sh', 'install.sh', 'tests/skill_test.sh']
- SKILL.md más grande: 87.4 KB (es lo que se carga en la conversación; el resto del repositorio no cuenta); total de SKILL.md: 302.4 KB
- Frases defensivas que mencionan ataques de inyección como ejemplo (no son órdenes): 0
- Instalaciones que pide en sus textos: ['npm install --save @primer/css', 'npm install @carbon/react @carbon/styles', 'npm install @fluentui/react-components', 'npm install @fluentui/web-components @fluentui/tokens', 'npm install @material/web', 'npm install @primer/react-brand', 'npm install @radix-ui/themes', 'npm install bootstrap']

### Patrones detectados en el código
- Ninguno de los patrones de riesgo buscados.

## Notas del Auditor
Lectura manual parcial: el install.sh solo crea enlaces simbólicos en la carpeta de skills (no descarga nada, no ejecuta comandos de red, no borra ni cambia permisos), así que el aviso de seguridad en ámbar se queda en un simple aviso. Los 6 MB del repositorio son imágenes de ejemplo, no las skills. EL ROJO DE EFICIENCIA ES REAL: la skill principal (taste-skill) pesa 88 KB, del orden de decenas de miles de tokens cada vez que se carga, y el conjunto de skills ronda los 300 KB. Si se quiere probar, usar las ligeras (redesign-skill 16 KB, stitch-skill 12 KB) o hacer un resumen propio de la principal. Hay muchas variantes de otras personas con el mismo nombre: usar solo el repositorio original. Algunas skills piden instalar librerías de interfaz en sus ejemplos (React, Bootstrap, etc.) que no aplican a un sitio sin framework. No he leído todas las skills enteras: leer la que se vaya a instalar antes de añadirla.

## Condiciones de adopción
- [ ] Alojar el archivo en `assets/vendor` y fijar la versión.
- [ ] Incluir el texto de la licencia junto al archivo.
- [ ] Probar con `reducir movimiento` y sin JavaScript.
- [ ] Anotar la decisión en `documentacion/DECISIONES.md` y la versión en `documentacion/DEPENDENCIAS.md`.

## Cómo retirarlo
Borrar el archivo de `assets/vendor`, quitar su `<script>` en `build.py` y la parte de `assets/main.js` que lo usa.

> Esta herramienta busca señales conocidas. No sustituye a leer el código de lo que va a ejecutarse en tu web.
