# Registro de cambios

Cada versión corresponde a un zip. Se actualiza **antes** de generar el zip.

## En preparación: 1.4
- Resultados del clasificador de reciclaje, en la página de su proyecto.
- Foto de Isabel en Sobre mí (hay un monograma «IA» mientras tanto).
- Confirmar los textos de las seis etapas de la animación.
- Decisiones pendientes de Isabel: comprar un dominio (hasta entonces se mantiene `/Cuaderno/`) y qué skills instalar.

## 1.3 (14 de octubre de 2026)
Cambios a partir del feedback en audio de una persona que abrió el sitio sin conocerlo:
- **Nuevo nombre: Isabel Amrein.** «Rumbo» sonaba genérico y no decía quién eres. Ahora la cabecera, los títulos, las imágenes para LinkedIn, `llms.txt` y los datos estructurados llevan tu nombre; el lema *Del dato al producto* y la animación explican el resto. Nuevo favicon con el monograma «IA».
- **Más calidad visual:** la animación se rediseña con un guion que cuenta **el ciclo completo de trabajo**: trabajo con los datos, los analizo, creo modelos, creo modelos de Machine Learning, gestiono el producto y mido los resultados, y vuelta a empezar. Una luz recorre el anillo de seis etapas, con un dibujo propio en el centro de cada una, y al cerrar el ciclo aparece la montaña de proyectos. Todo sobre un fondo con auroras y estrellas. Todas las ilustraciones (iceberg, brújula, contenedores y montaña) llevan degradados, luz de borde, sombras de contacto y viñeteado.
- **La portada explica quién eres y qué haces de un vistazo:** nombre y cargo arriba, una presentación en primera persona y una **animación de 26 segundos en bucle** (el ciclo completo y la montaña de proyectos) con botón de pausa. Con «reducir movimiento» solo se ve la montaña.
- **Cabecera:** icono de globo con `ES ⇄ EN` para el idioma e icono de contraste para el tema claro u oscuro. Botones de 44 px y menú en una segunda fila en el móvil.
- **Miniaturas y etiquetas de tipo** (*Entrada* y *Proyecto*) en todas las listas, y una frase que define cada sección: «lo que construyo» y «lo que aprendo».
- **Sobre mí:** ficha con foto (un monograma hasta que haya foto), trayectoria, experiencia, formación y un botón directo al perfil de LinkedIn.
- **Idioma:** la raíz detecta el idioma del navegador y recuerda la elección; en cualquier página aparece una sugerencia discreta en lugar de redirigir a la fuerza.
- **Pantallas pequeñas:** los diagramas son legibles y se deslizan con un aviso, y todas las zonas táctiles miden al menos 44 px. Comprobado entre 320 y 1024 px.
- **SEO:** títulos de hasta 60 caracteres y descripciones de 120 a 160 en todas las páginas, `llms.txt` y `llms-full.txt`, `robots.txt` con referencia a ambos, datos estructurados (`ProfilePage`, `Person`, `BlogPosting`, `CreativeWork` y `BreadcrumbList`) y enlaces internos nuevos («Sigue leyendo», «Otros proyectos» y una caja de autoría con enlace a Sobre mí y a LinkedIn).

## 1.2 (12 de octubre de 2026)
- **Rediseño de la portada:** nuevo nombre **Rumbo** con el lema *Del dato al producto*, y una montaña con banderas (una por entrada) en lugar del gráfico con cuadrícula.
- **Nueva estructura de proyectos y entradas:** menú Proyectos, Entradas y Sobre mí; las banderas de la portada son proyectos; cada proyecto tiene su página con estado, herramientas, resultados y entradas relacionadas.
- Dos proyectos nuevos: **Formación en Data Science e IA** (agrupa los apuntes de cada clase) y **Clasificador de reciclaje** (con su propia ilustración de contenedores). El apartado del clasificador sale del artículo de Machine Learning, que ahora solo lo menciona y lo enlaza.
- **Orbes vivos:** los proyectos «en marcha» llevan un pequeño orbe en movimiento dentro de su etiqueta de estado (lista, portada y cabecera del proyecto). Combina la montaña de la portada con la idea de «laboratorio abierto».
- La palabra «máster» desaparece de la web para el programa actual.
- Nuevo script `herramientas/generar_agentes.py` que genera y valida `agentes.yaml`.
- Eliminado el artículo de bienvenida. Su idea pasa a «Cómo trabajo» en Sobre mí, que además deja de listar herramientas porque están en LinkedIn.
- Retirados: el gráfico interactivo de la portada, la cuadrícula de fondo (también en las imágenes para compartir) y el nombre «Cuaderno de Isabel».
- Nuevo favicon: montaña con bandera. La imagen social de la portada usa la misma montaña.
- Documentación puesta al día: arquitectura, roadmap, decisiones, dependencias, agentes y lecciones aprendidas.
- Sobre mí sin la sección «Algunos proyectos»: repetía LinkedIn, mencionaba datos del trabajo y chocaba con el menú Proyectos.
- Nuevo informe del Auditor sobre la librería Motion (no adoptada).
- Nueva regla: la documentación se actualiza antes de cada zip.
- Corregido: `agentes.yaml` no era un YAML válido; ahora se genera desde las fichas de los subagentes y se valida.
- Pendiente de contenido: resultados del clasificador de reciclaje en el artículo 1.

## 1.1 (12 de octubre de 2026)
- Indicador "Pensando…" con el orbe *composing* de `thinking-orbs`, alojado en `assets/vendor` (15,5 KB).
- Auditor de proyectos públicos (subagente 9) y su herramienta `herramientas/auditar.py`.
- Primeros informes: thinking-orbs, skills de Emil Kowalski y taste-skill. Inventario de dependencias.
- Reglas de movimiento (duraciones de 220 y 250 ms, curva decidida, escalonado de 60 ms, nada nace de escala cero).
- Versión suave de `reducir movimiento`: desvanecimientos breves en lugar de quitar todo.
- Corregido: una regla antigua anulaba la versión suave y dejaba invisibles las cajitas.

## 1.0 (12 de octubre de 2026)
- Animaciones suaves: aparición al hacer scroll, siete cajitas por partes y brújula orientándose a la meta.
- Arquitecto y ocho subagentes, con documentación de arquitectura, decisiones, roadmap y checklists.
- Limpieza de obsoletos, `.gitignore`, guía de publicación y herramientas movidas a `herramientas/`.

## 0.4 (12 de octubre de 2026)
- Ilustración semirrealista en todo el blog: cabeceras (iceberg y brújula), montaña, iceberg, receta de galletas y escalera.
- Tipografías propias Newsreader, Figtree y JetBrains Mono, sin Google Fonts.
- Ancho de lectura más estrecho y tamaños de títulos ajustados.
- Brújula con bandera y camino de puntos hacia la meta.
- Corregido: la página en español enlazaba al otro idioma con el texto equivocado.

## 0.3 (11 de octubre de 2026)
- Artículo 1 ampliado: montaña del proyecto, gobierno del modelo, iceberg y tres formas de construir un modelo.
- Artículo 2: Estrategia de datos, con siete cajitas, escalera de madurez y tarjetas de niveles.
- Subrayados en palabras clave, crédito al profesor y proyecto de reciclaje.
- Sobre mí revisado dos veces para ajustar el cargo y el alcance.

## 0.2 (11 de octubre de 2026)
- Diseño oscuro con aguamarina, página Sobre mí, primeros artículos y borradores de LinkedIn.
- Publicación en GitHub Pages.

## 0.1 (11 de octubre de 2026)
- Sitio estático bilingüe con tema claro y oscuro, generador en Python y artículo de bienvenida.
