---
id: caso-buscar-casa
title: "Del problema al match: cómo plantearíamos buscar casa con IA"
seo_title: "Del problema al match: buscar casa con IA"
date: 2026-10-19
order: 3
accent: sand
projects: [master]
hero: casa
teacher: David Rey
tags: [caso-de-uso, innovacion, propuesta-de-valor]
module: Business Data and AI Strategy
kind: caso
case: buscar-casa-ia
summary: Un caso práctico de clase: cómo pasar de un problema real, buscar casa, a una idea con valor basada en datos e IA, con modelo de negocio y métricas.
linkedin: Mi tercera clase de Data Science e IA generativa fue un taller de casos de uso con IA. Partimos de un problema real, buscar casa, y lo convertimos en una idea con valor basada en datos - un agente conversacional, un porcentaje de match y un modelo de negocio. Cuento los tres pasos del lienzo y lo que me llevo.
---

Esta clase fue distinta de las anteriores: en vez de escuchar, nos tocó construir. Forma parte del módulo *Business Data and AI Strategy* y fue un **taller de casos de uso con IA**, la sesión de innovación del módulo. Este artículo cuenta el caso desde el problema hasta la propuesta de valor. Es la parte práctica que acompaña a la teoría: el caso seguirá creciendo con las siguientes clases y lo iré enlazando con la teoría que lo explica.

## El caso

El profesor nos planteó un caso realista: una empresa dedicada a la búsqueda de viviendas, que funciona como agencia inmobiliaria. En equipo y sobre una pizarra colaborativa teníamos que levantar el problema, valorar alternativas, proponer una solución con una <span class="hl">propuesta de valor basada en el dato</span> y perfilar un plan: cómo lo haríamos y cómo mediríamos el éxito. Terminamos con un mini pitch de cuatro minutos por equipo.

Trabajamos con una versión adaptada del *Lean Canvas*, un lienzo para ordenar una idea de negocio. Se recorre en tres pasos, y me parece una buena forma de ordenar cualquier idea:

{{include:vista}}

## Paso 1: entender el problema

Partimos del recorrido de una persona que quiere comprar una casa, de la idea a la firma: piensa en comprar, investiga la zona, busca en portales, contacta y concierta visitas, negocia el precio, firma las arras, busca financiación y formaliza la compra ante notario y banco. El profesor señaló dos tramos como el foco del caso: la búsqueda en portales y el contacto para concertar visitas.

{{include:recorrido}}

El material planteaba dos puntos de vista: el de quien busca casa y el de la agencia, que pierde contactos de calidad porque no puede atender todas las llamadas y no distingue quién tiene un interés real. Nos quedamos con el primero. A lo largo del recorrido, quien busca se hace preguntas como dónde buscar, cuánto se puede gastar o cuál es el precio justo; los filtros no responden a lo que de verdad quiere saber, la información está repartida entre imágenes y textos, y todo es un proceso manual y reactivo, con una negociación y un papeleo que exigen mucha dedicación. Además, por lo que nos contaron compañeros, buscar casa puede ser una experiencia agotadora: horas comparando y peleando con otras personas por las mismas viviendas. En el lienzo lo resumimos en tres líneas: no hay un portal único de oferta y de información, se pierde mucho tiempo buscando y la experiencia de uso es mala.

¿Y qué hace hoy la gente? Buscar en portales individuales. Es la alternativa que existe, y tiene costes claros: se pierde tiempo, las viviendas aparecen repetidas y hay que llamar una por una.

## Paso 2: diseñar la solución

Nuestra idea fue crear un modelo centralizado que unifique la búsqueda. Algo parecido a esos comparadores que reúnen a muchas empresas y te dan el mejor precio para un billete de tren, pero con las viviendas de varios portales.

La pieza clave es un <span class="hl">agente conversacional</span>. En vez de rellenar filtros, la persona habla con él, también por voz, y le cuenta qué busca y cómo vive. Esa conversación es dato no estructurado: el agente lo convierte en variables, las cruza con el catálogo de viviendas y devuelve un **porcentaje de match** con cada una, explicando por qué encaja: «creo que este piso es para ti por esto y esto, y te vas a sentir bien por esto otro».

{{include:agente}}

Las viviendas llegarían por conexiones API con las plataformas o, si no fuera posible, mediante un modelo de extracción de datos (*scraping*).

Los **objetivos clave** que nos marcamos fueron cuatro:

- Conseguir la confianza del cliente.
- Modernizar el proceso de búsqueda.
- Ofrecer un modelo conversacional que dé las alternativas por voz.
- Convencer de que los pisos ofrecidos están escogidos a su medida.

## La pregunta incómoda del profesor

Aquí llegó el reto: ¿por qué la empresa más grande del sector, que ya tiene herramientas parecidas, querría contratarnos o enviarnos su tráfico? Nuestra respuesta fue darle la vuelta: no íbamos a vendérselo a ella. Como domina casi todo el mercado, nos pusimos del lado de las pequeñas: juntarlas en una plataforma donde todas pudieran convivir y competir con más fuerza.

## Paso 3: convertirla en negocio

### La propuesta de valor

Ahorrar tiempo y mejorar la experiencia de búsqueda con una <span class="hl">hiperpersonalización unificada y con servicios extra</span>. Son tres ideas:

- **Hiperpersonalización.** Con las fotos de las plataformas generamos un render 3D realista y lo ambientamos según lo que la persona nos ha contado. Si busca casa para vivir con hijos, perro y su suegra, la vivienda se adapta a esas necesidades para que se imagine viviendo allí; si es soltera y quiere compartir con amigos, el render muestra otro uso. Verse en la casa aumenta el interés.
- **Unificación.** Reunimos la oferta y damos el porcentaje de match. Además, gestionamos el contacto: si alguien ve una vivienda a través de nuestra aplicación, enviamos nosotros un mensaje ya preparado a la plataforma, a la inmobiliaria o al particular para pedir una visita.
- **Servicios extra.** Cuando alguien ya está decidido y le ha gustado su render, podemos ofrecerle una empresa de reformas que le dé buen precio según el estilo de la casa, orientación legal y financiera (cuánto va a costar de verdad, qué conviene saber de las arras o de los seguros de hipoteca) y enlace con brokers de hipotecas.

### A quién va dirigida

A dos públicos: personas que buscan piso para comprar, porque la idea es para venta, y los pequeños portales inmobiliarios que quieran unirse para dar un servicio conjunto.

### Dos retos

Nos planteamos dos preguntas difíciles. La primera, **cómo agrupar la oferta**: con acuerdos con plataformas, brokers y publicidad, un modelo B2B. La segunda, **cómo rentabilizarlo**. Por un lado, ingresos de reformas, brokers y servicios legales; por otro, una suscripción para quien busca casa. Una búsqueda dura unos tres o cuatro meses, hasta que se compra, y mucha gente se suscribe a un asistente de IA para un trabajo concreto y luego se da de baja. Aquí sería igual: se paga mientras dura la búsqueda y se obtiene todo el servicio personalizado. Con los portales, los acuerdos serían por el tráfico que les enviamos, por contactos o por suscripción; eso quedó por definir.

### El concepto general

En una línea: un pacto con los pequeños portales y un agente de IA multimodal que habla con el cliente y trae toda la información. Detrás hay un sistema de recomendación, conexión por API con los portales, los datos del usuario compilados, los datos de cada portal y un modelo de IA que aprende de las búsquedas que acaban bien. En la pizarra apuntamos una idea más: un asistente formado por subagentes, según la fase en la que se encuentre quien compra.

### Cómo mediríamos el éxito

El profesor nos dio tres miradas de partida: la de la persona que busca (tiempo de búsqueda, número de visitas físicas y satisfacción), la de la agencia (contactos de calidad y operaciones cerradas) y la de la empresa (ingresos y base de usuarios). Nosotros nos quedamos con tres métricas:

- **Tráfico de clientes**, orgánico y de pago: cómo conseguimos que la gente entre en la plataforma.
- **Conversión vía API**: de las personas con las que hablamos y a las que damos matches, cuántas enviamos a una plataforma y cierran una visita en persona. Como estamos conectados por API, los portales nos informan; esa visita es nuestra conversión, y la compra sería un extra.
- **Satisfacción**: una encuesta al terminar la conversación.

## La pieza que falta: partir también del dato

En los anexos de la presentación había una idea que me pareció útil para este caso. El diseño de producto tradicional empieza por la persona y su problema, que es justo lo que hicimos. Pero hay otra puerta de entrada: empezar por el **dato como activo** y buscar dónde encaja. Se resume en unas pocas preguntas: qué datos tenemos y de qué calidad son, si son únicos o nos darían un posicionamiento diferencial, en qué procesos de nuestro cliente podrían serle útiles y si pueden producir una experiencia diferente a la actual. Y un aviso importante: el proceso no es lineal, se va y se vuelve entre explorar, encajar, idear, ejecutar y evaluar. La fuente que citaba la presentación es *The Design Thinking Playbook*.

Si lo aplico a nuestro caso, los activos serían las conversaciones con las personas que buscan, el catálogo de las plataformas y sus fotografías: con ellos se hacen el match y el render.

## Lo que me llevo

- **Primero el problema, después la tecnología.** La idea solo tiene sentido porque el dolor es real: las horas que se pierden buscando casa.
- **Una buena pregunta cambia el enfoque.** «¿Por qué la grande querría trabajar con vosotros?» nos hizo pasar de competir con ella a unir a las pequeñas.
- **Se puede empezar por el problema o por el dato.** Conviene hacer las dos cosas, porque el camino no es lineal.
- **Una idea de IA es también una idea de negocio.** Sin ingresos y sin métricas, se queda en un prototipo. Y todo se apoya en el dato: de la conversación a las variables, de las variables al match y del match a la conversión.

El caso continúa en las siguientes clases.
