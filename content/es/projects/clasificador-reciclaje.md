---
id: reciclaje
title: Clasificador de reciclaje
subtitle: ¿En qué contenedor va esto? Una foto y una respuesta
date: 2026-10-12
status: en-marcha
accent: moss
hero: bins
stack: [Teachable Machine, Custom AI, Imágenes]
summary: Un modelo que, a partir de una foto, dice a qué contenedor va cada objeto. Pensado como un juego educativo para aprender a reciclar.
linkedin: Estoy construyendo un clasificador de reciclaje: una foto de un objeto y la respuesta de a qué contenedor va. Cuento el plan, cómo lo entreno y, sobre todo, dónde falla.
---

## Qué quiero resolver

Casi todos los niños tienen un móvil o una tablet en casa, y apuntar a un objeto y ver la respuesta es una forma de aprender a reciclar jugando. Este proyecto construye ese modelo con una herramienta sin programación, para entender cómo se entrena y dónde falla.

## Cómo lo construyo

1. **Definir las clases.** En España, cuatro: contenedor amarillo (envases de plástico, latas y briks), azul (papel y cartón), verde (vidrio) y resto. Las normas varían según el municipio, así que es un punto de partida.
2. **Reunir datos.** Unas 50 fotos por clase con objetos de mi casa, variando fondo, luz y ángulo.
3. **Entrenar y probar** el modelo con objetos nuevos que no haya fotografiado antes.
4. **Anotar dónde falla y por qué.**

## Qué quiero comprobar

- **Cuánto depende de los datos.** Si todas las fotos tienen el mismo fondo, ¿qué está aprendiendo realmente el modelo?
- **Qué casos le confunden.** Un brik parece cartón, pero va al contenedor amarillo.
- **Qué errores cuestan más.** Meter en el amarillo algo que no es reciclable puede estropear el reciclaje del resto, mientras que dejar un envase reciclable en "resto" simplemente lo pierde. Es la lección de diseño de la entrada sobre Machine Learning, con mucho menos riesgo.

## Con qué lo hago

Teachable Machine, una herramienta gratuita de Google que entrena modelos de clasificación de imágenes desde el navegador, sin programar. Corresponde al nivel *Custom AI* de la entrada sobre Machine Learning.

## Resultados

Los publicaré aquí cuando termine las pruebas: cuántas fotos usé por clase, la precisión por clase, los casos que fallan y lo que aprendí.

> Es una herramienta educativa pensada para usar con un adulto cerca. No sustituye las indicaciones oficiales de cada municipio.
