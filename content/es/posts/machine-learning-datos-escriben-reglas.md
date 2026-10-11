---
id: ml-reglas
title: "Machine Learning: cuando los datos escriben las reglas"
date: 2026-10-11
accent: aqua
tags: [machine-learning, fundamentos, data-science]
summary: Qué es el Machine Learning, en qué se diferencia de programar con reglas y por qué lo difícil no es entrenar un modelo, sino mantenerlo funcionando.
linkedin: En mi primera clase de Data Science me quedé con una idea: en programación tradicional tú escribes las reglas; en Machine Learning, los datos las escriben por ti. Lo explico con ejemplos propios, el mini proyecto que voy a montar y por qué NO voy a construir un clasificador de setas.
---

Mi primera clase del máster respondió a una pregunta que parece obvia hasta que intentas explicarla: ¿qué es exactamente el Machine Learning? Estos son mis apuntes, reescritos con mis propios ejemplos, más un mini proyecto que voy a montar para ponerlo a prueba.

## Qué es y dónde encaja

La Inteligencia Artificial es el campo amplio: conseguir que las máquinas hagan cosas que asociamos con la inteligencia. El Machine Learning (ML) es una de sus ramas: en lugar de decirle al ordenador qué hacer paso a paso, le das ejemplos y dejas que descubra los patrones por su cuenta.

La Data Science es el oficio que lo rodea. Combina estadística, programación y conocimiento del problema para entender los datos, predecir y tomar mejores decisiones.

## La idea que más me quedó: darle la vuelta al esquema

En la programación tradicional escribes las reglas, el programa las aplica a los datos y obtiene respuestas. En ML el flujo se invierte: aportas los datos y las respuestas correctas, y el algoritmo deduce las reglas. Esas reglas aprendidas son lo que llamamos modelo.

| | Entradas | Resultado |
|---|---|---|
| Programación tradicional | Reglas y datos | Respuestas |
| Machine Learning | Datos y respuestas | Reglas (el modelo) |

Un ejemplo con el correo no deseado:

- **Con reglas:** escribes "si el mensaje contiene *premio* y *urgente*, es spam". Funciona hasta que los spammers cambian las palabras y hay que reescribir las reglas a mano.
- **Con ML:** le enseñas miles de correos que alguien ya marcó como spam o no spam. El modelo detecta qué combinaciones de rasgos suelen ir con cada etiqueta, y se adapta si le das ejemplos nuevos.

## Cuatro usos que se repiten

**Recomendación.** Imagina una cadena de cines. Si sé que a un cliente le gustan los estrenos de un género y suele ir los viernes, puedo avisarle de que esta semana llega una película de ese género, con asientos libres en la zona que suele elegir. Incluso podría destacar en el aviso al actor que más veces ha visto. Eso sí, con su permiso: personalizar bien también es respetar la privacidad.

**Estrategia de juegos.** Hay modelos que ajustan la dificultad al nivel de cada jugador para que el reto sea exigente pero nunca imposible. A veces la diferencia está en milímetros.

**Clasificación.** El filtro de spam es el ejemplo clásico. Otro, más serio: modelos que ayudan a detectar neumonía en radiografías de tórax, que se desplegaron en entornos clínicos durante la pandemia.

**Predicción.** [Flood Hub, de Google](https://blog.google/outreach-initiatives/sustainability/flood-hub-ai-flood-forecasting-more-countries/), pronostica crecidas de ríos hasta siete días antes combinando previsiones meteorológicas e imágenes de satélite. Empezó como piloto en India en 2018, con unas 48 horas de margen. Una semana de aviso permite que la gente se ponga a salvo.

## Cómo funciona un proyecto de ML, en cinco pasos

1. **Definir el problema:** qué quiero predecir y qué decisión voy a tomar con ello.
2. **Etiquetar los datos:** ejemplos junto con su respuesta correcta.
3. **Entrenar el modelo:** el algoritmo busca los patrones.
4. **Predecir:** usar el modelo con datos que no ha visto.
5. **Monitorizar:** comprobar que sigue acertando cuando el mundo cambia.

## La parte difícil no es el modelo

Lo que más me sorprendió es que entrenar el modelo suele ser lo más ligero del proyecto. La dificultad está alrededor:

- **Los datos.** Llegan incompletos, sin etiquetar o desequilibrados. Un modelo solo puede ser tan bueno como los datos con los que aprende.
- **El entrenamiento.** El gran riesgo es el sobreajuste: que el modelo se aprenda los ejemplos de memoria y falle con casos nuevos. Se vigila separando los datos en conjuntos de entrenamiento, validación y prueba.
- **El despliegue.** Integrar el modelo en sistemas reales y mantenerlo. Los modelos se degradan con el tiempo porque los datos cambian, así que hay que reentrenarlos.

Lanzar un modelo es la parte fácil. Mantenerlo útil es el trabajo de verdad.

## Mini proyecto: un clasificador de imágenes

[Teachable Machine](https://teachablemachine.withgoogle.com/) es una herramienta gratuita de Google que entrena modelos de clasificación desde el navegador, sin programar. Este es mi plan:

1. Elegir tres objetos de mi escritorio (por ejemplo, una taza, una libreta y unos auriculares).
2. Sacar unas 50 fotos de cada uno con la webcam, variando fondo, luz y ángulo.
3. Entrenar el modelo y probarlo con fotos nuevas que no haya usado al entrenar.
4. Anotar dónde falla y por qué.

Quiero comprobar cuánto depende el resultado de la variedad de los datos: si todas las fotos tienen el mismo fondo, ¿qué está aprendiendo realmente el modelo? Cuando lo tenga montado, actualizaré este artículo con mis resultados.

## Un proyecto que no voy a construir (y qué enseña)

Mi primera idea fue un clasificador de setas: comestible o venenosa. La he descartado como aplicación a propósito. Un modelo entrenado con unas cuantas fotos se equivocará, y en este problema los errores no cuestan lo mismo. Decir "comestible" de una seta tóxica puede ser mortal. Decir "tóxica" de una comestible solo cuesta una cena.

Por eso importa mirar algo más que el porcentaje total de aciertos. Aquí la métrica clave sería el *recall*: de todas las setas tóxicas, ¿cuántas consigue señalar el modelo como tóxicas? Además, muchas setas venenosas se parecen mucho a las comestibles y su identificación segura la hace una persona experta, no una foto.

La lección es de diseño: elegir la métrica adecuada y pensar en el contexto de uso forma parte de construir un modelo. Cuando hay riesgo real, el modelo asiste a una persona, no decide por ella. Y, por si acaso: nunca uses un modelo de fotos para decidir qué comer.

## Lo que me llevo

El Machine Learning no es magia ni algo reservado a expertos. Es una forma distinta de resolver problemas en la que pesan más la calidad de los datos y el mantenimiento que el algoritmo en sí. En el próximo artículo contaré cómo me ha ido con el clasificador.
