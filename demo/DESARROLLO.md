# Desarrollo de Taller

Estas herramientas sirven para modificar y comprobar la demo. Para incorporarla a un servidor existente, usa [INSTALACION.md](INSTALACION.md).

## Generar los paquetes

Desde la raíz del repositorio:

```sh
python demo/tools/make_assets.py
python demo/tools/build.py
python demo/tools/check_pack.py
python demo/tools/check_datapack.py
python tools/package_demo.py
```

`package_demo.py` genera los ZIP de instalación, las instrucciones y el fragmento de configuración con el hash real de los recursos. La copia pública del pack usa una URL identificada por contenido: una actualización de la demo no cambia el archivo que ya tiene configurado otro servidor.

## Mundo de desarrollo aislado

El siguiente arranque es opcional para quien desarrolla la demo; no forma parte de la instalación de la funcionalidad.

Necesitas Java 25 y Python 3.10+. Desde esta carpeta:

```sh
python tools/build.py
python tools/dev.py prepare
```

El script descarga el servidor **oficial y sin modificar** desde Mojang y verifica su SHA-1. No se redistribuye el servidor. Tras leer y aceptar personalmente la [EULA de Minecraft](https://www.minecraft.net/eula):

```sh
python tools/dev.py start --accept-eula
```

Usa `JAVA_HOME` o añade `--java-home RUTA_AL_JDK_25`. La partida escucha en `127.0.0.1:25585`; el lanzador sirve únicamente el ZIP de recursos en `127.0.0.1:8127/pack.zip`. Entra con Minecraft 26.3 y acepta el paquete requerido. Para detenerlo, escribe `stop` en su consola.

`run-vanilla/` es un mundo de desarrollo aislado. No se utilizan mundos existentes ni archivos de otras instancias.

## Validación

En la consola de un servidor vanilla de pruebas con el datapack cargado:

```mcfunction
function taller:test/run
data get storage taller:test report
```

El informe debe tener `errors: 0`. No ejecutar las pruebas como sustituto de comprobar los menús y el HUD dentro del cliente. Consultar [CAPTURAS.md](CAPTURAS.md).

La herramienta `tools/validate_demo_native.py` del repositorio valida los comandos y codecs sin iniciar una partida. Esa comprobación no ejecuta las reglas ni verifica el dibujo.

## Combinar con otros recursos

Si el servidor ya distribuye un paquete propio, integrar `pack/assets/taller/` en él y revisar los cambios de `pack/assets/minecraft/`. El shader `text.vsh` y los sprites de bossbar no se deben sustituir sin combinar su funcionalidad con la que ya use el servidor. Tras generar el ZIP combinado, configurar su propia URL y su SHA-1.
