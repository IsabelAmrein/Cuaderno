# Cómo publicar una versión

Hazlo siempre así para no dejar archivos que ya no valen en el repositorio.

Cada zip trae `documentacion/CHANGELOG.md` con lo que cambia en esa versión: léelo antes de publicar.

1. **Descomprime** `cuaderno.zip`.
2. **Abre tu carpeta `Cuaderno`** (la que tienes clonada de GitHub). Activa los archivos ocultos con `Cmd + Shift + .` en Finder y **no toques la carpeta `.git`**.
3. **Borra todo lo demás** de esa carpeta: `assets`, `content`, `docs`, `herramientas`, `linkedin`, `documentacion` y los archivos sueltos. Así se eliminan los restos de versiones anteriores.
4. **Copia dentro** todo el contenido del zip descomprimido.
5. En VS Code, abre **Source Control**. Verás archivos añadidos, modificados y borrados. Es lo esperado.
6. Escribe un mensaje de commit, pulsa **Commit** y después **Sync Changes**.
7. En GitHub, mira la pestaña **Actions** hasta que aparezca el tic verde (uno a tres minutos).
8. Abre la web en una **ventana privada** del navegador para saltarte la memoria guardada.
9. Pega la dirección del artículo en el **Post Inspector de LinkedIn** y publica el borrador de la carpeta `linkedin`.

## Si el repositorio ya tiene archivos antiguos
- Elimina `.DS_Store` (el archivo oculto de macOS). El `.gitignore` de este proyecto evita que vuelva a subirse.
- Si GitHub Pages mostrara algo antiguo, comprueba en **Settings, Pages** que la rama es `main` y la carpeta `/docs`.

## Qué no se sube
`.gitignore` excluye `__pycache__`, `node_modules` y archivos del sistema.
