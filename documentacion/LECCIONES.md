# Lecciones aprendidas

Cada error o confusión que tuvimos y la regla que salió de él. Sirve para no repetirlos.

| Qué pasó | Qué aprendimos | Regla |
|---|---|---|
| Se generó un zip antes de enseñar el resultado | Isabel quiere ver y aprobar antes | **Previsualizar antes de generar el zip** |
| Se generó un zip sin la documentación al día | El repositorio debe explicar lo que contiene | **Documentación al día antes de cada zip** |
| La ilustración de la galleta resultó "rara" | Decidir sin alternativas es arriesgado | Ofrecer **varias opciones** antes de implementar un diseño nuevo |
| Una captura de pantalla se confundió con una animación que sí se movía | Una foto fija no demuestra movimiento | Para enseñar movimiento, **mostrar un GIF** |
| El dictado "Mussen" era en realidad otra cosa (Motion) | Los nombres dictados pueden transcribirse mal | **Buscar y confirmar** el nombre antes de actuar |
| Al regenerar la brújula se perdió el reflejo del cristal | Reescribir un dibujo puede borrar detalles | **Revisar visualmente** cada ilustración tras regenerarla |
| El generador de la receta de galletas no estaba guardado como archivo | Lo que no se guarda no se puede repetir | **Todo generador vive en `herramientas/`** |
| El Auditor marcó en rojo frases defensivas de una skill y paquetes de fuentes enteros | Una herramienta busca señales, no entiende intenciones | **Lectura manual siempre**, y medir lo que se incorpora, no el paquete entero |
| El Auditor aprobó una librería "joven" sin avisar | La madurez y el número de mantenedores importan | El semáforo incluye **edad y mantenedores** |
| Una regla antigua de CSS anulaba la versión suave de `reducir movimiento` | Una regla global puede deshacer una nueva | **Probar con la preferencia activada** cada vez que se toque movimiento |
| Se dijo que las skills "pesaban hasta 41 KB" y era una skill irrelevante | Una cifra sin contexto confunde | **Medir solo lo que se usará** y decir qué se ha excluido |
| Se subían archivos viejos a GitHub | Copiar encima no borra | **Borrar lo antiguo** (salvo `.git`) antes de pegar la versión nueva |
| El archivo `agentes.yaml`, presentado como legible por programas, no era un YAML válido | Lo que se declara válido hay que **validarlo** | Los archivos de datos se **validan con un programa** y se generan desde su fuente, no a mano |
| Todo se organizó como «artículos» hasta que Isabel explicó que lo construido y los apuntes son cosas distintas | Los tipos de contenido condicionan toda la estructura | **Preguntar qué tipos de contenido habrá** antes de diseñar el menú y las páginas |
| Una captura de página completa dejó secciones vacías porque las animaciones ocultan lo que aún no se ha visto | Una captura no hace scroll | **Bajar por la página** antes de capturar, y comprobar el HTML cuando algo parezca faltar |
| Quien abrió el sitio sin conocerlo no entendía quién eras ni qué era, aunque todo estaba bien hecho | Quien construye el sitio ya sabe lo que hay | **Probar la portada con alguien que no te conozca:** si en cinco segundos no sabe quién eres y qué haces, hay que cambiarla |
| La vista previa en móvil parecía correcta, pero una auditoría automática encontró textos de diagramas de 7 a 10 px y botones de 24 px | Ver no es medir | **Auditar con números** (anchos de 320 a 1024 px, texto mínimo y zonas táctiles de 44 px), no solo con una captura |
| La primera animación explicaba la idea, pero se veía plana y los cambios de escena eran secos | Comunicar no basta: lo que se mira tiene que estar trabajado | **Escribir un guion** (escenas, transiciones y un detalle de cierre), **mirarlo fotograma a fotograma** y renderizarlo a vídeo antes de darlo por bueno |
| El guion de la animación resumía el trabajo de Isabel en "datos y modelos" y dejaba fuera el análisis, el Machine Learning, el producto y la medición | Quien escribe el guion no vive el trabajo | **Validar el mensaje con quien lo vive** antes de pulir la forma |
| El nombre «Rumbo» no decía quién eres y sonaba raro, aunque a mí me parecía poético | Un nombre de marca personal debe responder a «¿quién eres?» antes que a «¿qué metáfora uso?» | **Para un sitio personal, el nombre es el de la persona**; la metáfora va en el lema o en la ilustración |

