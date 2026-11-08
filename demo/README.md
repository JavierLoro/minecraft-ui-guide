# Taller: demo de interfaces en Minecraft vanilla

Datapack y paquete de recursos para **Minecraft Java 26.3**. Los menús, las acciones, el progreso y las preferencias se ejecutan con funciones y comandos del juego. No utiliza Paper, plugins, mods ni compilación Java.

## Probar en un mundo individual

1. Descarga [el datapack](https://javierloro.github.io/minecraft-ui-guide/downloads/taller-datapack.zip) y [los recursos](https://javierloro.github.io/minecraft-ui-guide/downloads/taller-resources.zip).
2. Al crear un mundo de Minecraft Java 26.3, añade el datapack en la pantalla de paquetes de datos. También puedes colocarlo en `datapacks/` de un mundo de pruebas y recargar ese mundo.
3. Instala y activa el ZIP de recursos desde Opciones → Paquetes de recursos.
4. Dentro del mundo, escribe `/trigger taller.open` o abre Taller desde los diálogos del menú de pausa.

Un jugador normal puede usar los botones: solo ejecutan `/trigger`. La instalación y la recarga de un datapack en un servidor corresponden a su administrador.

## Servidor vanilla local

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

## Recorrido de la demo

- **Fabricar pieza:** añade una pieza al pedido.
- **Cobrar 25:** solo aparece cuando está completo; cada pedido se cobra una vez.
- **Nuevo pedido:** reinicia el progreso y conserva el saldo.
- **Mostrar u ocultar HUD:** guarda la preferencia.
- **Ajustes:** checkbox de visibilidad, selector de posición y deslizador de tamaño del pedido.
- Sal y vuelve a entrar: los scoreboards del mundo conservan los datos de cada jugador.

El saldo pertenece a la demostración; no entrega objetos ni altera ninguna economía externa. El HUD incluye fuentes propias, avances negativos y seis estados de progreso. La posición centrada es la inicial; la esquina izquierda activa el shader específico de 26.3 y debe comprobarse visualmente en el cliente.

## Archivos que puedes reutilizar

| Parte | Archivo o carpeta |
|---|---|
| Entrada y ciclo por jugador | `datapack/data/taller/function/player/` |
| Pantalla y tokens de botones | `datapack/data/taller/function/ui/` |
| Validación de entradas | `datapack/data/taller/function/input/` |
| Reglas del pedido y ajustes | `datapack/data/taller/function/logic/` |
| Bossbar individual y composición | `datapack/data/taller/function/hud/` |
| Formularios registrados | `datapack/data/taller/dialog/settings/` |
| Fuentes, texturas y shader | `pack/assets/` |
| Generación de formularios y ZIP | `tools/build.py` |

Las acciones del menú llevan un número de sesión. El datapack compara esa sesión, limita la frecuencia y valida el estado antes de ejecutar la operación. Los formularios solo aceptan tamaños de 1 a 12 y banderas booleanas. Su mensaje numérico es `objetivo × 100 + visible × 10 + anclado`; no acepta comandos ni texto arbitrario del cliente.

Cada jugador tiene un identificador y una bossbar propia. El almacenamiento `taller:ctx` es temporal y se usa secuencialmente; la persistencia está en los scoreboards. No reutilices ese almacenamiento desde tareas aplazadas como si perteneciese permanentemente a un jugador.

La demo no registra un manejador para `minecraft:custom`: esa acción no ejecuta funciones de datapack por sí sola. Utiliza los comandos `/trigger` que sí pueden usar jugadores sin OP.

## Construir y comprobar

```sh
python tools/make_assets.py
python tools/build.py
python tools/check_pack.py
```

Para ejecutar las autopruebas en el servidor vanilla preparado, usa su consola:

```mcfunction
function taller:test/run
data get storage taller:test report
```

El informe debe mostrar `errors: 0`. Estas pruebas ejecutan las funciones de pedidos y ajustes con perfiles ficticios propios de la prueba, no con datos de jugadores reales. Los comandos y JSON se validan además contra el parser y los codecs del JAR oficial de Minecraft 26.3 durante el desarrollo.

La comprobación visual y las [capturas del cliente](CAPTURAS.md) son una etapa distinta. No afirmar que un shader se ve bien porque el datapack se haya cargado o las pruebas de comandos pasen.

## Alcance

Esta base implementa pedidos, botones, tooltips, tres controles, preferencias y HUD. Mascotas, transiciones complejas y un campo de nombre libre no están implementados. Un shader mueve el dibujo, no crea zonas clicables nuevas.

Los gráficos del paquete deben estar cargados; el datapack no detecta por sí solo el resultado de esa descarga. El arranque local los requiere. Los sprites transparentes afectan también a otras bossbars blancas de estilo continuo.

Cambia el namespace `taller`, los objetivos y el contrato de fuentes y shader al adaptarlo a otro proyecto. [Entrada para agentes](AGENTS.md), [guía divulgativa](https://javierloro.github.io/minecraft-ui-guide/) y [atribuciones](NOTICE).
