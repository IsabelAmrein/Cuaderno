# Revisión de thinking-orbs

- **Fecha:** 2026-10-12
- **Tipo:** npm
- **Versión o rama:** 0.3.2
- **Autoría:** Jakub Antalik
- **Repositorio:** git+https://github.com/Jakubantalik/Libraries.dev.git
- **Veredicto:** 🟡 Se puede adoptar con condiciones (ver los criterios en ámbar y las condiciones de adopción).

## Semáforo

| Criterio | Estado | Por qué |
|---|---|---|
| Licencia | 🟢 | Licencia MIT: permisiva. Hay que conservar el aviso de copyright. |
| Seguridad | 🟢 | Sin vulnerabilidades conocidas ni patrones de riesgo. |
| Mantenimiento | 🟡 | Última actividad hace 1 mes. Proyecto joven: creado hace 3 meses. Lo mantiene una sola persona. |
| Procedencia | 🟢 | Repositorio declarado: git+https://github.com/Jakubantalik/Libraries.dev.git. |
| Eficiencia | 🟢 | El archivo que se incorpora pesa 15.5 KB; 0 dependencias propias. |
| Compatibilidad | 🟢 | Declara ['react'], pero el archivo que realmente usamos no los necesita. Perfil: sitio estático, sin framework (sin React), navegador moderno, generador en Python 3.12. |

## Evidencias
- Versión analizada: 0.3.2
- Creado: 2026-07-21; última publicación: 2026-09-22; personas mantenedoras: 1
- Página del proyecto: https://libraries.dev/orbs
- Dependencias directas: ninguna
- Dependencias de pares (peer): {'react': '>=18.0.0'}
- Archivos: 26; peso descomprimido: 127.6 KB; archivos JavaScript: 6
- Scripts que se ejecutan al instalar: ninguno
- Vulnerabilidades conocidas (npm audit): {'info': 0, 'low': 0, 'moderate': 0, 'high': 0, 'critical': 0, 'total': 0}; dependencias transitivas: 1

### Patrones detectados en el código
- Ninguno de los patrones de riesgo buscados.

### Archivo que realmente se incorpora (assets/vendor/thinking-orbs.js)
- Peso: 15.5 KB
- Patrones de riesgo: ninguno
- Menciona React: False

## Notas del Auditor
Lectura manual: se usa solo el motor independiente (thinking-orbs/engine), empaquetado con esbuild en un único archivo. Ese archivo no contiene referencias a React, no hace peticiones de red, no usa cookies y solo dibuja en un canvas. El repositorio declarado en npm (Jakubantalik/Libraries.dev, carpeta packages/thinking-orbs) y el que cita su documentación (Jakubantalik/thinking-orbs) pertenecen a la misma cuenta. Riesgo principal: proyecto muy joven (julio de 2026) y mantenido por una sola persona. Mitigación aplicada: copia alojada en el propio sitio con la versión fijada, de modo que no depende de actualizaciones. El indicador solo aparece si la carga tarda más de 140 ms y respeta reducir movimiento.

## Condiciones de adopción
- [ ] Alojar el archivo en `assets/vendor` y fijar la versión.
- [ ] Incluir el texto de la licencia junto al archivo.
- [ ] Probar con `reducir movimiento` y sin JavaScript.
- [ ] Anotar la decisión en `documentacion/DECISIONES.md` y la versión en `documentacion/DEPENDENCIAS.md`.

## Cómo retirarlo
Borrar el archivo de `assets/vendor`, quitar su `<script>` en `build.py` y la parte de `assets/main.js` que lo usa.

> Esta herramienta busca señales conocidas. No sustituye a leer el código de lo que va a ejecutarse en tu web.
