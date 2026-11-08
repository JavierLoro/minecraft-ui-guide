# Taller: demo de interfaces de Minecraft Java

Proyecto base ejecutable para **Minecraft Java 26.3, Paper build 244 y JDK 25**. Incluye plugin, paquete de recursos propio, compilación con Gradle Wrapper, pruebas y un arranque local reproducible.

[Descargar el proyecto con el plugin compilado](https://javierloro.github.io/minecraft-ui-guide/downloads/minecraft-ui-demo.zip) · [Guía de interfaces](https://javierloro.github.io/minecraft-ui-guide/)

## Probar sin compilar

Necesitas Minecraft Java 26.3, Python 3.10+ y un JDK 25. Descarga el ZIP, extráelo y abre una terminal en la carpeta extraída.

```sh
python tools/dev.py prepare
```

Descarga la versión fija de Paper y comprueba su SHA-256. No incluye ni redistribuye el servidor de Minecraft. Antes de iniciar, lee la [EULA de Minecraft](https://www.minecraft.net/eula). Si la aceptas personalmente:

```sh
python tools/dev.py start --accept-eula
```

El script usa `JAVA_HOME` o el Java de tu PATH y comprueba que sea Java 25. También puedes indicar `--java-home RUTA_A_TU_JDK_25`. Esa ruta pertenece a tu máquina y no debe guardarse en el repositorio.

En Minecraft 26.3, conéctate a **127.0.0.1:25585**, acepta el paquete de recursos de la demo y escribe **`/uidemo`**. El servidor y el servicio del paquete escuchan solo en tu propio equipo. Detén el servidor escribiendo `stop` en su consola.

## Recorrido

1. **Fabricar pieza:** aumenta el progreso del pedido de demostración.
2. **Cobrar 25:** aparece al completarlo; un pedido no puede cobrarse dos veces.
3. **Nuevo pedido:** conserva el saldo y reinicia el progreso.
4. **Mostrar / ocultar HUD:** alterna su visibilidad y guarda la preferencia.
5. **Ajustes:** cambia el nombre, el tamaño del pedido y la posición del HUD. Cambiar el tamaño empieza un pedido nuevo sin borrar el saldo.
6. Sal y vuelve a entrar: el pedido, el saldo y las preferencias se conservan.

El saldo pertenece exclusivamente a esta demo. Fabricar no entrega objetos ni modifica inventarios o economías de otros plugins.

El menú incorpora tooltips en sus botones. Los ajustes muestran los cuatro inputs nativos: texto, booleano, selección y rango. El HUD usa una bossbar, una fuente bitmap propia, avances negativos y sprites transparentes del color blanco.

## HUD centrado y anclado

La vista **centrada** es la inicial. Permite comprobar la composición gráfica sin depender de cambios de coordenadas. **Esquina izquierda** activa los marcadores del shader `text.vsh` específico de 26.3. También puedes usar `/uidemo nativo` y `/uidemo anclado`.

El contrato de esta demo reserva `#FA02F0` para blanco y `#FA02E0` para turquesa. No es el contrato RGB ilustrativo de la guía ni un estándar de Minecraft. El compositor completa exactamente 160 píxeles de avance; el shader parte de esa anchura y del origen de la bossbar. Cambiar fuentes, anchuras o versión requiere ajustar y volver a probar ese contrato.

La bossbar blanca se reserva para el HUD; el paquete también vuelve transparentes otras bossbars blancas de estilo continuo. El HUD es informativo: la interacción con cursor está en los diálogos.

## Compilar y modificar

```sh
# Windows
.\gradlew.bat clean build

# Linux / macOS
sh gradlew clean build
```

Los resultados son `build/libs/minecraft-ui-demo.jar` y `build/pack/taller-pack.zip`. El paquete queda además embebido en el plugin. Tras cambiar los gráficos procedurales:

```sh
python tools/make_assets.py
python tools/check_pack.py
```

Vuelve a compilar y ejecuta `python tools/dev.py prepare` con el servidor detenido para copiar el nuevo plugin. El wrapper y su distribución llevan checksum fijo; las versiones están en `versions.json`.

## Qué cambiar para tu proyecto

| Quieres cambiar | Empieza aquí |
|---|---|
| Pedidos, saldo y reglas | `src/main/java/io/github/javierloro/uidemo/WorkshopState.java` |
| Pantallas, botones, tooltips e inputs | `DemoDialogs.java`, en ese mismo paquete |
| Validación de sesiones y frecuencia | `SessionGate.java` |
| Archivos de preferencias por jugador | `ProfileStore.java` |
| Composición, avances y colores del HUD | `HudRenderer.java` |
| Pack HTTP y ciclo de vida | `PackServer.java` y `UiDemoPlugin.java` |
| Fuentes, texturas y shader | `pack/assets/` |

Sustituye el namespace `taller`, el paquete Java, `plugin.yml` y los identificadores del pack al crear un proyecto independiente. Separa tus servicios de economía o juego del compositor y mantén la validación en el servidor. El [AGENTS.md](AGENTS.md) sirve de entrada para otro agente.

## Otro equipo o un servidor público

El arranque incluido está pensado para desarrollo local. Para otros jugadores, aloja `build/pack/taller-pack.zip` en una URL accesible y configura `resource-pack.public-url` en `run/plugins/MinecraftUiDemo/config.yml`. Ajusta por separado la interfaz de escucha y los accesos del servidor; no publiques la carpeta `run/`.

## Verificación y capturas

La compilación ejecuta pruebas de pedidos, cobro idempotente, entradas inválidas, aislamiento por jugador, sesiones caducadas y clics repetidos. La comprobación dentro de Minecraft tiene su propio [recorrido de prueba y capturas](CAPTURAS.md).

Los tests de Java no verifican el renderizado del shader ni la geometría de los controles del cliente. Las capturas de la guía deben proceder del cliente ejecutando esta demo. No sustituyas esa comprobación por imágenes generadas.

Código propio y recursos `taller`: MIT. Atribuciones y archivos de terceros: [NOTICE](NOTICE).
