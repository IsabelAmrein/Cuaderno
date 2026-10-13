# Revisión de emilkowalski/skills

- **Fecha:** 2026-10-12
- **Tipo:** skill
- **Versión o rama:** 2d22863
- **Autoría:** emilkowalski
- **Repositorio:** https://github.com/emilkowalski/skills
- **Veredicto:** 🟢 Se puede adoptar.

## Semáforo

| Criterio | Estado | Por qué |
|---|---|---|
| Licencia | 🟢 | Licencia MIT: permisiva. Hay que conservar el aviso de copyright. |
| Seguridad | 🟢 | Sin vulnerabilidades conocidas ni patrones de riesgo. |
| Mantenimiento | 🟢 | Última actividad hace menos de un mes. |
| Eficiencia | 🟢 | La SKILL.md más grande pesa 14.0 KB: es el coste de contexto cada vez que se usa. |
| Compatibilidad | 🟢 | Sin dependencias de pares. Perfil del proyecto: sitio estático, sin framework (sin React), navegador moderno, generador en Python 3.12. |

## Evidencias
- Archivos: 29; peso total: 292.3 KB; último cambio: 2026-10-11
- La API de GitHub no respondió (límite de peticiones): faltan estrellas y fecha de creación.
- Revisión limitada a las skills elegidas: ['animate', 'animation-performance', 'break-ui', 'find-animation-opportunities', 'improve-animations', 'review-animations']
- Skills encontradas (SKILL.md): 6
- Scripts incluidos: 0 []
- SKILL.md más grande: 14.0 KB (es lo que se carga en la conversación; el resto del repositorio no cuenta); total de SKILL.md: 65.1 KB
- Frases defensivas que mencionan ataques de inyección como ejemplo (no son órdenes): 3
- Instalaciones que pide en sus textos: ninguna

### Patrones detectados en el código
- Ninguno de los patrones de riesgo buscados.

## Notas del Auditor
El repositorio contiene 15 skills. La primera revisión salió en ámbar por una sola: write-swift (41,5 KB), de programación en Swift, que no sirve para nuestro sitio. Revisadas solo las seis que sí nos servirían (animate, review-animations, improve-animations, find-animation-opportunities, animation-performance y break-ui), no hay riesgos ni scripts y la mayor pesa 14 KB. No se han tenido en cuenta por no aplicarse a un sitio estático: write-swift, animate-expo (React Native), ask-sonner (toasts de React), mobile-native, apple-design (gestos), pick-ui-library y prototype. Lectura manual: las tres frases que parecían sospechosas en otras skills del repositorio son defensivas (ordenan señalar textos que intenten dar órdenes). Las skills no son código de la web: se instalan en la cuenta de Isabel. Su regla de oro encaja con el proyecto: no instalar una librería de movimiento para un simple desvanecimiento, y que reducir movimiento viaje con la animación. Aplicando a mano su lista de cosas que no se deben enviar, nuestras animaciones tendrían cuatro observaciones: la aparición al hacer scroll dura 600 ms con la curva ease por defecto (recomienda 150 a 250 ms y una curva más decidida), las cajitas entran con 140 ms de escalonado (recomienda 30 a 80 ms), la bandera de la brújula nace de escala 0 (recomienda empezar en 0,95 con transparencia) y con reducir movimiento quitamos todo en vez de dar una versión más suave (por ejemplo, solo un desvanecimiento breve).

## Condiciones de adopción
- [ ] Alojar el archivo en `assets/vendor` y fijar la versión.
- [ ] Incluir el texto de la licencia junto al archivo.
- [ ] Probar con `reducir movimiento` y sin JavaScript.
- [ ] Anotar la decisión en `documentacion/DECISIONES.md` y la versión en `documentacion/DEPENDENCIAS.md`.

## Cómo retirarlo
Borrar el archivo de `assets/vendor`, quitar su `<script>` en `build.py` y la parte de `assets/main.js` que lo usa.

> Esta herramienta busca señales conocidas. No sustituye a leer el código de lo que va a ejecutarse en tu web.
