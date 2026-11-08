# Interfaces y HUD en Minecraft Java

Manual interactivo y documentación Markdown para construir menús, botones, toggles, tooltips, formularios, HUD y transiciones mediante funciones nativas y paquetes de recursos.

## Publicar en GitHub Pages

### Publicación automática desde PowerShell

Con Git y GitHub CLI instalados, ejecutar desde esta carpeta:

```powershell
pwsh -NoProfile -File .\publicar.ps1
```

El script comprueba la cuenta `JavierLoro`, permite iniciar sesión, crea el repositorio público `minecraft-ui-guide`, sube los archivos y activa Pages desde `main`. Si necesitas otro propietario o nombre:

```powershell
pwsh -NoProfile -File .\publicar.ps1 -Owner TU_USUARIO -Repository NOMBRE_DEL_REPOSITORIO
```

Se detiene si la cuenta o el remoto local no coinciden; no sustituye repositorios ajenos. Si falla la activación de Pages tras la subida, se puede completar desde Settings.

### Publicación desde la web

1. Crear un repositorio en GitHub. Un repositorio público permite usar Pages con GitHub Free.
2. Subir **el contenido de esta carpeta a la raíz del repositorio**. `index.html`, `AGENTS.md` y `.nojekyll` deben quedar en la raíz, no dentro de otra carpeta. No subir el ZIP como único archivo.
3. En el repositorio, abrir **Settings → Pages**.
4. Elegir **Deploy from a branch**, la rama **main** y la carpeta **/(root)**. Guardar.
5. Esperar a que termine la publicación y abrir la dirección que muestre GitHub.

La dirección de un repositorio normal será `https://TU_USUARIO.github.io/TU_REPOSITORIO/`. No es necesario editar el HTML para añadir ese prefijo: todos los enlaces locales son relativos.

El sitio ya está generado: publicar no requiere Node, Python ni GitHub Actions personalizados. `.nojekyll` evita transformar los archivos Markdown y permite servirlos como archivos de lectura directa. Si la rama se llama de otra forma, seleccionarla en Pages.

[Instrucciones oficiales de GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Compartir con un agente

Para una lectura rápida, proporcionar la URL de `AGENTS.md`:

```text
Lee https://TU_USUARIO.github.io/TU_REPOSITORIO/AGENTS.md.
Después consulta los capítulos necesarios de la guía Markdown enlazada
antes de implementar un sistema de interfaces para Minecraft Java.
```

| Archivo | Uso |
|---|---|
| `index.html` | Lectura visual, diagramas y simulaciones |
| `AGENTS.md` | Contexto técnico breve y mapa de lectura |
| `GUIA-INTERFACES-MINECRAFT.md` | Fuente completa en Markdown |
| `llms.txt` | Índice de recursos de texto |
| `llms-full.txt` | Guía completa en texto, generada desde el Markdown |

`llms.txt` es una ayuda de descubrimiento, no un mecanismo que obligue a los agentes a leerlo. El acceso directo a `AGENTS.md` funciona sin ejecutar JavaScript.

## Editar y regenerar

Para leer y publicar los archivos no hay dependencias. Solo para regenerar el HTML tras cambios:

```sh
python -m pip install -r requirements.txt
python tools/build.py
python tools/check.py
```

Editar `GUIA-INTERFACES-MINECRAFT.md` y, si cambia la presentación, `source/template.html`. El generador actualiza `index.html` y `llms-full.txt`. Subir también estos archivos generados al repositorio para que Pages publique la versión actualizada.

Para probar el sitio localmente:

```sh
python -m http.server 8000
```

Abrir `http://localhost:8000/`. También se puede abrir `index.html` directamente.

## Alcance

Es una guía con ejemplos y demostraciones didácticas; no contiene un plugin compilado ni un servidor de Minecraft. Las APIs, shaders y formatos deben adaptarse a la versión que se vaya a implementar.
