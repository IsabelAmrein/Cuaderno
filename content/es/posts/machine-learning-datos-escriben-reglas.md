---
id: ml-reglas
title: "Machine Learning: cuando los datos escriben las reglas"
date: 2026-10-11
accent: aqua
hero: iceberg
teacher: Daniel Sáenz
tags: [machine-learning, fundamentos, data-science]
summary: Qué es el Machine Learning, cómo se construye un proyecto de principio a fin y por qué entrenar el modelo es solo la punta del iceberg.
linkedin: En mi primera clase de Data Science me quedé con una idea: en programación tradicional tú escribes las reglas; en Machine Learning, los datos las escriben por ti. Resumo cómo se construye un proyecto (una montaña con tres tramos), las tres formas de crear un modelo, por qué entrenarlo es solo la punta del iceberg y el mini proyecto de reciclaje que voy a montar.
---

Mi primera clase del máster respondió a una pregunta que parece obvia hasta que intentas explicarla: ¿qué es exactamente el Machine Learning? Estos son mis apuntes, reescritos con mis propios ejemplos, más un mini proyecto que voy a montar para ponerlo a prueba.

## Qué es y dónde encaja

La Inteligencia Artificial es el campo amplio: conseguir que las máquinas hagan cosas que asociamos con la inteligencia. El Machine Learning (ML) es una de sus ramas: en lugar de decirle al ordenador qué hacer paso a paso, le das ejemplos y dejas que descubra los patrones por su cuenta.

La Data Science es el oficio que lo rodea. Combina estadística, programación y conocimiento del problema para entender los datos, predecir y tomar mejores decisiones.

## La idea que más me quedó: la receta de galletas

Mi profesor, Daniel Sáenz, lo explicó con una receta de galletas y es la imagen que más se me quedó. Imagina que quieres hacer galletas:

- **Programación tradicional:** tienes los ingredientes y escribes tú la receta, es decir, las reglas. Si sigues los pasos, salen las galletas, que son las respuestas.
- **Machine Learning:** tienes los ingredientes y también las galletas ya hechas. Es el algoritmo quien se inventa la receta que lleva de unos a otras. Esa receta, aprendida a partir de ejemplos, es el modelo.

{{include:galletas}}

La diferencia está en quién escribe las reglas. En el primer caso, tú. En el segundo, los datos.

Un ejemplo cotidiano en cualquier empresa: la bandeja de entrada de atención al cliente. Llegan cientos de correos al día y hay que repartirlos entre reclamaciones, consultas, solicitudes de documentación y bajas.

- **Con reglas:** escribes "si el correo contiene *reclamación*, va al equipo de reclamaciones". Funciona hasta que un cliente enfadado escribe sin usar esa palabra, o mezcla dos temas en un mismo mensaje. Cada excepción obliga a añadir otra regla a mano.
- **Con ML:** le enseñas miles de correos que los agentes ya clasificaron. El modelo aprende qué rasgos suelen acompañar a cada categoría (el vocabulario, el tono, lo que se pide) y se adapta si le das ejemplos nuevos.

Eso sí, esos correos contienen datos personales, así que antes de entrenar habría que anonimizarlos.

## Cuatro usos que se repiten

**Recomendación.** Imagina una cadena de cines. Si sé que a un cliente le gustan los estrenos de un género y suele ir los viernes, puedo avisarle de que esta semana llega una película de ese género, con asientos libres en la zona que suele elegir. Incluso podría destacar en el aviso al actor que más veces ha visto. Eso sí, con su permiso: personalizar bien también es respetar la privacidad.

**Estrategia de juegos.** Hay modelos que ajustan la dificultad al nivel de cada jugador para que el reto sea exigente pero nunca imposible. A veces la diferencia está en milímetros.

**Clasificación.** Volviendo a atención al cliente: un modelo que lee cada correo y lo envía al equipo adecuado, para que nadie pierda tiempo reenviando. Un ejemplo más serio son los modelos que ayudan a detectar neumonía en radiografías de tórax, que se desplegaron en entornos clínicos durante la pandemia.

**Predicción.** [Flood Hub, de Google](https://blog.google/outreach-initiatives/sustainability/flood-hub-ai-flood-forecasting-more-countries/), pronostica crecidas de ríos hasta siete días antes combinando previsiones meteorológicas e imágenes de satélite. Empezó como piloto en India en 2018, con unas 48 horas de margen. Una semana de aviso permite que la gente se ponga a salvo.

## Cómo se construye un proyecto: la montaña que hay que escalar

Antes de empezar a escalar hay que saber a dónde vas: qué quiero predecir y qué decisión voy a tomar con ello. A partir de ahí, el camino tiene tres tramos y el modelo ocupa solo el del medio. Este es mi mapa, con lo que hay que vigilar en cada uno:

{{include:montana}}

Y ahora, los obstáculos de cada tramo, contados como me los explicaría a mí misma.

### Primer tramo: los datos

Todo empieza con los datos, y casi nunca llegan listos. El primer problema que te encuentras es que están incompletos o son inconsistentes: huecos, duplicados, fechas escritas de tres formas distintas. Lo siguiente es que hay pocos ejemplos etiquetados, porque alguien tiene que ponerles a mano la respuesta correcta. Y por último, que suelen estar desequilibrados: en los correos de atención al cliente habrá muchas más consultas que reclamaciones, y el modelo puede acabar ignorando lo poco frecuente.

La solución es dedicar tiempo al preprocesamiento. Primero, perfilar los datos para entender qué hay. Después, limpiarlos, quedarse solo con lo que aporta, transformarlos a un formato que el modelo entienda, enriquecerlos con información extra y, al final, validar que el resultado tiene sentido. No es la parte más vistosa, pero de ella depende todo lo demás.

### Segundo tramo: construir y entrenar

Con los datos listos toca entrenar, y aquí aparecen cuatro problemas clásicos.

El primero es elegir el algoritmo. Hay muchos y ninguno es el mejor para todo, así que lo sensato es probar varios, comparar sus resultados con métricas como la precisión o el recall y tener en cuenta qué tipo de problema es: clasificar, predecir un número o agrupar.

El segundo es el sobreajuste: el modelo se aprende tan bien los ejemplos de entrenamiento que falla con los nuevos. Para evitarlo se separan los datos en entrenamiento, validación y prueba, se aplican técnicas que frenan la complejidad del modelo (la regularización) y, si se puede, se consiguen más datos.

El tercero son los hiperparámetros, los ajustes que el modelo no aprende por sí solo. Probarlos a mano es eterno, así que se automatiza la búsqueda con técnicas como Grid Search o Random Search.

Y el cuarto es la potencia de cálculo: entrenar modelos grandes pide mucha máquina. Se resuelve alquilando procesadores especializados en la nube y repartiendo el entrenamiento en lotes pequeños.

### Tercer tramo: desplegar y mantener

Cuando el modelo funciona en el portátil empieza lo difícil. El primer problema es integrarlo con los sistemas que ya existen, que hablan otros formatos y otras tecnologías. Lo habitual es ofrecerlo como un servicio al que otras aplicaciones puedan llamar, documentando bien qué entra y qué sale.

El segundo es que el rendimiento se degrada con el tiempo, porque el mundo cambia y los datos nuevos ya no se parecen a los de entrenamiento. La solución es monitorizar la precisión y el recall de forma continua, con alertas automáticas, y reentrenar el modelo con datos recientes.

Hay dos más que conviene no olvidar: aguantar un gran volumen de peticiones sin ir más lento (con servicios en la nube que escalan solos) y asegurarse de que el modelo no trata injustamente a ciertos grupos, que es justo el siguiente tema.

## Gobierno del modelo: lo que no se puede olvidar

Más allá de los problemas técnicos, hay tres pilares que sostienen un proyecto serio.

**Trazabilidad.** Dejar registrado cada paso, desde los datos hasta el despliegue, con herramientas como MLflow. Si el modelo empieza a fallar, permite volver atrás y ver qué cambió: ¿los datos?, ¿algún ajuste? Y también explicar por qué se tomó una decisión.

**Equidad (*fairness*).** Comprobar que el modelo no trata peor a ciertos grupos ni repite los sesgos de los datos. Si el modelo de correos atendiera antes a quien escribe con tono formal y dejara para el final a quien comete faltas de ortografía, sería injusto. Se mide con métricas específicas, auditorías periódicas y, en casos críticos, con una persona que revise.

**Monitorización continua.** Vigilar el modelo en producción para detectar cuándo los datos cambian y deja de acertar, lo que se conoce como *concept drift*. Un recomendador de películas se queda anticuado cuando cambian las modas.

## Entrenar el modelo es solo la punta del iceberg

Al empezar pensaba que el trabajo era sobre todo escribir el código del modelo, y es una parte pequeña. Alrededor hay que recoger y verificar los datos, extraer sus características, gestionar la configuración y los recursos de computación, tener herramientas de análisis, montar la infraestructura que sirve el modelo y vigilarlo cuando ya está en marcha.

{{include:iceberg}}

La idea viene de un conocido artículo de Google de 2015, [*Hidden Technical Debt in Machine Learning Systems*](https://proceedings.neurips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf), que advierte de que los sistemas de ML acumulan costes de mantenimiento a la larga. Por eso investigar y producir son mundos distintos: en investigación importa sobre todo el rendimiento del modelo, mientras que en producción pesan igual la velocidad de respuesta, que los datos no dejan de cambiar, la equidad y poder explicar las decisiones.

## Tres formas de construir un modelo

Por suerte no hace falta escalar toda la montaña desde cero en cada proyecto. En clase vimos tres niveles, de menos a más trabajo. Cuanto más abajo del iceberg te metes, más control tienes y más tienes que sostener.

{{include:niveles}}

Una API te ahorra casi todo lo que hay bajo el agua. Un proyecto end-to-end te lo pone todo en las manos.

## Mini proyecto: ¿en qué contenedor va esto?

Para practicar el nivel Custom AI voy a usar Teachable Machine, una herramienta gratuita de Google que entrena modelos de clasificación desde el navegador, sin programar. Quiero montar un clasificador de residuos que, a partir de una foto, diga a qué contenedor va cada objeto. Lo imagino como un juguete educativo: casi todos los niños tienen un móvil o una tablet en casa, y apuntar a un objeto y ver la respuesta es una forma de aprender a reciclar jugando.

Este es mi plan:

1. **Definir las clases.** En España, cuatro: contenedor amarillo (envases de plástico, latas y briks), azul (papel y cartón), verde (vidrio) y resto. Las normas varían según el municipio, así que es un punto de partida.
2. **Reunir datos.** Unas 50 fotos por clase con objetos de mi casa, variando fondo, luz y ángulo.
3. **Entrenar y probar** el modelo con objetos nuevos que no haya fotografiado antes.
4. **Anotar dónde falla y por qué.**

Quiero comprobar dos cosas. La primera, cuánto depende el resultado de la variedad de los datos: si todas las fotos tienen el mismo fondo, ¿qué está aprendiendo realmente el modelo? La segunda, qué casos le confunden: un brik parece cartón pero va al contenedor amarillo.

Aquí aparece, con mucho menos riesgo, la lección del siguiente apartado: los errores no cuestan lo mismo en los dos sentidos. Meter en el amarillo algo que no es reciclable puede estropear el reciclaje del resto, mientras que dejar un envase reciclable en "resto" simplemente lo pierde. Y como herramienta educativa, es para usar con un adulto cerca y no sustituye las indicaciones oficiales de cada municipio.

Cuando lo tenga montado, actualizaré este artículo con mis resultados.

## Un proyecto que no voy a construir (y qué enseña)

Mi primera idea fue un clasificador de setas: comestible o venenosa. La he descartado como aplicación a propósito. Un modelo entrenado con unas cuantas fotos se equivocará, y en este problema los errores no cuestan lo mismo. Decir "comestible" de una seta tóxica puede ser mortal. Decir "tóxica" de una comestible solo cuesta una cena.

Por eso importa mirar algo más que el porcentaje total de aciertos. Aquí la métrica clave sería el *recall*: de todas las setas tóxicas, ¿cuántas consigue señalar el modelo como tóxicas? Además, muchas setas venenosas se parecen mucho a las comestibles y su identificación segura la hace una persona experta, no una foto.

La lección es de diseño: elegir la métrica adecuada y pensar en el contexto de uso forma parte de construir un modelo. Cuando hay riesgo real, el modelo asiste a una persona, no decide por ella. Y, por si acaso: nunca uses un modelo de fotos para decidir qué comer.

## Lo que me llevo

El Machine Learning no es magia ni algo reservado a expertos. Es una forma distinta de resolver problemas en la que pesan más la calidad de los datos y el mantenimiento que el algoritmo en sí, y entrenar el modelo es solo la punta del iceberg. En el próximo artículo contaré cómo me ha ido con el clasificador.
