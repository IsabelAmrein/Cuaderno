# Checklists maestras

Las checklists por subagente están en [`subagentes`](subagentes). Estas son las transversales.

## A. Nuevo artículo
- [ ] Objetivo y una idea central definidos
- [ ] Dictado recibido; material de clase solo como referencia
- [ ] Datos verificados (Investigador)
- [ ] Borrador en español y versión en inglés con el mismo `id`
- [ ] `summary`, `tags`, `teacher` y gancho de LinkedIn
- [ ] Cabecera e ilustraciones creadas y aprobadas
- [ ] Revisión de privacidad (Guardián)
- [ ] Pase de calidad (Calidad)
- [ ] Previsualización aprobada por Isabel

## B. Nueva ilustración o foto
- [ ] Estilo semirrealista y colores fijos en objetos
- [ ] Descripción accesible
- [ ] Probada en claro, oscuro y móvil
- [ ] Foto propia, sin terceros ni niños, sin ubicación, con peso razonable
- [ ] Imagen social de 1200 por 630

## C. Antes de generar el zip
- [ ] Isabel ha visto la previsualización y ha dicho que sí
- [ ] `python3 build.py` termina sin errores
- [ ] Calidad y Guardián en verde
- [ ] Documentación al día: `CHANGELOG`, `ROADMAP`, `DECISIONES` y `DEPENDENCIAS`
- [ ] `agentes.yaml` válido y generado a partir de las fichas
- [ ] Sin menciones prohibidas (empresa, cargos del profesor)

## D. Cierre de versión y limpieza
- [ ] Archivos obsoletos eliminados del proyecto
- [ ] Sin `__pycache__`, `.DS_Store` ni `node_modules`
- [ ] `docs/` regenerado desde cero
- [ ] Documentación y roadmap al día
- [ ] Nota de cambios y mensaje de commit

## G. Nuevo proyecto
- [ ] Mismo `id` en español e inglés
- [ ] Título, subtítulo y resumen claros
- [ ] Estado (`en-marcha`, `terminado` o `idea`) y herramientas
- [ ] Problema, proceso y resultado (o «Resultados» pendientes, dicho con honestidad)
- [ ] Cabecera ilustrada con el estilo de `BRAND.md`
- [ ] Entradas relacionadas con `projects:` y enlaces en ambos sentidos
- [ ] Revisión de privacidad (Guardián)
- [ ] Gancho de LinkedIn

## F. Incorporar un proyecto público
- [ ] Necesidad clara y alternativa propia valorada
- [ ] Informe del Auditor guardado en `documentacion/auditorias`
- [ ] Lectura manual del código o texto que se incorpora
- [ ] Licencia permisiva y su texto incluido junto al archivo
- [ ] Versión fijada y copia alojada en `assets/vendor`
- [ ] Inventario `DEPENDENCIAS.md` y `DECISIONES.md` actualizados
- [ ] Aprobación de Isabel

## E. Accesibilidad
- [ ] Texto alternativo en imágenes y gráficos
- [ ] Contraste suficiente
- [ ] Todo se puede usar con teclado y el foco se ve
- [ ] Con `reducir movimiento` todo se ve completo y solo hay desvanecimientos breves
- [ ] Tablas y diagramas legibles en móvil
