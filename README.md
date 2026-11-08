# Cómo funcionan las interfaces en Minecraft

Guía divulgativa para entender cómo se combinan las reglas de la partida, las funciones de Minecraft y un paquete de recursos para crear menús y HUD. La lectura principal explica la idea; los desplegables técnicos enlazan al código y a los archivos de una demo vanilla.

- [Leer la guía](https://javierloro.github.io/minecraft-ui-guide/).
- [Demo Taller: datapack y recursos](demo/README.md).
- [Descargar proyecto reutilizable](downloads/minecraft-ui-demo.zip).
- [Manual técnico en Markdown](GUIA-INTERFACES-MINECRAFT.md).
- [Entrada para agentes](AGENTS.md).

## Editar la guía

El relato principal está en `source/template.html`. El manual técnico está en `GUIA-INTERFACES-MINECRAFT.md`. El generador crea `index.html` y sincroniza `llms-full.txt`:

```sh
python -m pip install -r requirements.txt
python tools/build.py
python tools/check.py
```

## Preparar la demo

```sh
python demo/tools/make_assets.py
python demo/tools/build.py
python demo/tools/check_pack.py
python tools/package_demo.py
```

La demo usa Minecraft Java 26.3 y sus mecanismos vanilla. No contiene plugins ni el servidor de Mojang. Ver [instrucciones y alcance](demo/README.md) antes de arrancarla.

## Publicar

GitHub Pages sirve `main` desde la raíz. Mantener enlaces relativos, `.nojekyll`, los archivos generados y los descargables sincronizados. No publicar carpetas de ejecución, mundos o registros.

Para repetir la validación de los comandos y codecs con el JAR oficial, sin iniciar el servidor:

```sh
python tools/validate_demo_native.py --java-home RUTA_AL_JDK_25
```

Este diagnóstico del repositorio utiliza un JDK; no forma parte de la lógica del juego ni del proyecto descargable.

Las capturas deben proceder del cliente ejecutando la demo. No afirmar una prueba visual a partir de verificaciones de sintaxis.
