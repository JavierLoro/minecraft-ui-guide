# Cómo funcionan las interfaces en Minecraft

Un menú con botones, una barra de progreso o un panel que sigue visible mientras juegas pueden construirse combinando funciones que Minecraft ya tiene. El juego pone la pantalla, un paquete de recursos cambia su aspecto y las reglas de la partida deciden qué información mostrar y qué ocurre al pulsar.

No necesitas programar para seguir la explicación de [la web](index.html). Allí se cuenta la idea con imágenes y ejemplos; los desplegables permiten entrar en el detalle técnico cuando te interese. Este documento amplía esa segunda lectura.

![El juego, las reglas de la partida y los recursos forman la interfaz.](assets/images/interface-overview.png)

Ilustración conceptual generada con IA; no es una captura de la demo.

Nuestra [demo Taller](demo/README.md) implementa la idea con un datapack y un paquete de recursos para Minecraft Java 26.3. Puedes instalarla en vanilla y usar sus archivos como base. [Descargar proyecto](downloads/minecraft-ui-demo.zip).


## 1. Qué permite construir la idea

Un menú abre una pantalla para elegir acciones. El HUD muestra información durante el juego. Un botón puede mostrar una explicación al pasar el ratón; un interruptor cambia una preferencia y actualiza lo que ves.

Taller implementa pedidos, cobro único, botones, tooltips, ajustes y HUD. Las mascotas y las transiciones complejas son ampliaciones posibles, no funciones ya incluidas.

## 2. Las tres piezas

- **Reglas:** el datapack conserva progreso y preferencias y valida las acciones.
- **Minecraft:** presenta diálogos, recibe comandos y transporta el HUD mediante una bossbar.
- **Recursos:** fuentes, texturas y shader dan forma a la presentación.

En una partida individual las funciones también se ejecutan en el servidor interno del juego. En la demo, el código de las reglas está en [logic/](https://github.com/JavierLoro/minecraft-ui-guide/tree/main/demo/datapack/data/taller/function/logic/).

## 3. Versión de referencia

La demo está fijada a Minecraft Java **26.3**, datapack **121.0** y recursos **97.1**. El servidor oficial requiere Java 25. Las versiones y el origen verificable de su JAR están en [versions.json](demo/versions.json).

Los formatos cambian entre versiones. No presentar este shader como compatible con cualquier cliente. [Notas oficiales de 26.3](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3).

## 4. Estructura de la demo

```text
demo/
  datapack/data/taller/
    function/player/   entrada y ciclo por jugador
    function/ui/       composición y navegación
    function/input/    validación de mensajes
    function/logic/    pedidos y preferencias
    function/hud/      bossbar y dibujo
    function/test/     autopruebas nativas
    dialog/            pantallas registradas
  pack/assets/         fuentes, texturas y shader
  tools/               generación, comprobación y arranque
```

No hay un plugin ni una API de servidor externa. Los [archivos del proyecto](demo/README.md) son el punto de partida para implementar.

## 5. Cargar el paquete de recursos

El cliente debe cargar las imágenes y las fuentes para dibujar el aspecto previsto. En un mundo individual, instala y activa [taller-resources.zip](downloads/taller-resources.zip). El servidor local preparado por [dev.py](demo/tools/dev.py) sirve ese ZIP y lo requiere al conectar.

El datapack no detecta por sí solo el estado de la descarga. El servidor de Minecraft no se incluye en el descargable; se obtiene desde Mojang y se verifica su hash.

## 6. Imágenes que se comportan como letras

Una fuente bitmap relaciona un carácter con una imagen. Cuando Minecraft dibuja ese carácter, aparece el gráfico. Así se pueden combinar iconos, marcos y texto en una composición.

Referencias: [hud.json](demo/pack/assets/taller/font/hud.json), [icons.json](demo/pack/assets/taller/font/icons.json) y [generador de gráficos](demo/tools/make_assets.py). Los caracteres privados elegidos son un contrato de la demo.

## 7. Colocar las piezas

El avance de una letra determina dónde empieza la siguiente. Los espacios de anchura positiva y negativa permiten avanzar y retroceder; distintas líneas base sitúan elementos a diferentes alturas.

Taller termina su composición con **160 píxeles de avance**. El panel aporta 161; los desplazamientos compensan los textos y la barra. Referencias: [space.json](demo/pack/assets/taller/font/space.json), [label.json](demo/pack/assets/taller/font/label.json), [value.json](demo/pack/assets/taller/font/value.json) y [hud/apply.mcfunction](demo/datapack/data/taller/function/hud/apply.mcfunction).

## 8. Abrir una pantalla

Los diálogos son pantallas nativas de Minecraft. El datapack registra un acceso en el menú de pausa; `/trigger taller.open` solicita abrir el menú de Taller.

[open.json](demo/datapack/data/taller/dialog/open.json) define la entrada. [ui/main.mcfunction](demo/datapack/data/taller/function/ui/main.mcfunction) prepara sus valores y [ui/show.mcfunction](demo/datapack/data/taller/function/ui/show.mcfunction) envía el diálogo personalizado a ese jugador.

## 9. Botones sin permisos de operador

Los botones de la demo ejecutan `trigger taller.action set <número>`. El jugador solo puede utilizar un objetivo trigger habilitado para él. La función del datapack interpreta ese número y decide qué hacer.

El menú incluye una sesión y un código de acción en el mensaje. [input/action.mcfunction](demo/datapack/data/taller/function/input/action.mcfunction) comprueba sesión, caducidad, frecuencia y estado antes de llamar a las reglas. No se aceptan comandos arbitrarios.

## 10. Explicaciones al pasar el ratón

Un botón de diálogo puede incluir `tooltip`. Minecraft muestra ese componente al pasar el ratón o enfocar el control; el datapack no necesita recibir continuamente la posición del cursor.

Los tooltips del taller se definen en [ui/show.mcfunction](demo/datapack/data/taller/function/ui/show.mcfunction). Las acciones esenciales conservan una etiqueta visible.

## 11. Interruptores con estado

Un interruptor representa una preferencia. Al pulsar, cambia el valor guardado y se vuelve a dibujar el resultado. La imagen no guarda ese estado.

[logic/toggle.mcfunction](demo/datapack/data/taller/function/logic/toggle.mcfunction) alterna `taller.hud`; [hud/update.mcfunction](demo/datapack/data/taller/function/hud/update.mcfunction) muestra u oculta el panel del jugador.

## 12. Ajustes y formularios

Taller utiliza checkbox, selector y deslizador para visibilidad, posición y tamaño del pedido. [tools/build.py](demo/tools/build.py) genera las pantallas de [dialog/settings/](https://github.com/JavierLoro/minecraft-ui-guide/tree/main/demo/datapack/data/taller/dialog/settings/) con los valores actuales.

La acción `minecraft:dynamic/run_command` crea `trigger taller.form set $(goal)$(hud)$(anchor)`. Las dos últimas cifras son banderas; las anteriores, el objetivo. El mensaje equivale a `objetivo × 100 + visible × 10 + anclado`.

[logic/settings.mcfunction](demo/datapack/data/taller/function/logic/settings.mcfunction) acepta únicamente objetivos de 1 a 12 y banderas de 0 a 1. La demo no persiste un campo de nombre libre. `minecraft:dynamic/custom` no llama por sí solo a funciones de datapack.

## 13. Navegar y cerrar

Cada menú nuevo renueva la sesión; una acción aceptada vuelve a mostrar el estado actual. Ajustes tiene su propio modo y tiempo de validez.

Referencias: [ui/main.mcfunction](demo/datapack/data/taller/function/ui/main.mcfunction), [ui/settings.mcfunction](demo/datapack/data/taller/function/ui/settings.mcfunction) y [ui/close.mcfunction](demo/datapack/data/taller/function/ui/close.mcfunction). Los diálogos no pausan la partida, de modo que el datapack puede responder mientras están abiertos.

## 14. Validar en el datapack

El cliente solicita una acción; no decide cuánto saldo recibe. Se comparan los datos del jugador, se comprueba que el pedido está completo y se impide pagar de nuevo uno ya cobrado.

La validación de entrada está en [input/](https://github.com/JavierLoro/minecraft-ui-guide/tree/main/demo/datapack/data/taller/function/input/). Las reglas reales están en [logic/craft.mcfunction](demo/datapack/data/taller/function/logic/craft.mcfunction), [claim.mcfunction](demo/datapack/data/taller/function/logic/claim.mcfunction) y [next.mcfunction](demo/datapack/data/taller/function/logic/next.mcfunction).

## 15. Usar una bossbar para el HUD

Una barra de jefe tiene un nombre que Minecraft ya sabe mostrar durante el juego. Ese nombre puede contener la composición gráfica del panel.

![Capas conceptuales de un HUD.](assets/images/hud-layers.png)

Ilustración conceptual generada con IA, no captura del motor.

Taller asigna un identificador persistente a cada jugador y crea `taller:player_<id>`. [hud/create.mcfunction](demo/datapack/data/taller/function/hud/create.mcfunction) prepara su barra; [hud/apply.mcfunction](demo/datapack/data/taller/function/hud/apply.mcfunction) actualiza su nombre y destinatario. No se comparte una sola barra mutable entre todos los jugadores.

## 16. Ocultar la barra estándar

El paquete vuelve transparentes `white_background.png` y `white_progress.png`, de 182 × 5 píxeles para esta versión. Así permanece el nombre compuesto, sin la barra blanca de fondo.

Archivos: [sprites de bossbar](https://github.com/JavierLoro/minecraft-ui-guide/tree/main/demo/pack/assets/minecraft/textures/gui/sprites/boss_bar/). El reemplazo afecta también a otras barras blancas de estilo continuo; hay que reservar ese uso o coordinarlo.

## 17. Recolocar el HUD mediante shader

El modo centrado usa el origen habitual de la bossbar. El modo anclado marca sus componentes con `#FA02F0` y `#FA02E0`; el [shader de texto](demo/pack/assets/minecraft/shaders/core/text.vsh) reconoce esos valores y desplaza el dibujo.

Ese contrato depende de la anchura de 160 píxeles y del shader de 26.3. No es un estándar del juego ni el contrato RGB genérico de otras implementaciones. El código conserva la base de la versión objetivo y distingue también la sombra del texto.

## 18. Escala y resolución

La interfaz se mide en coordenadas lógicas de GUI. Debe comprobarse con varias escalas y tamaños de ventana; mover píxeles no cambia automáticamente las zonas de clic.

El HUD de esta demo es informativo. Los botones están en los diálogos, donde Minecraft ya gestiona cursor y foco. El [recorrido de comprobación](demo/CAPTURAS.md) incluye el HUD anclado y el resto de textos del juego.

## 19. Progreso y estadísticas

El datapack conserva piezas y objetivo por jugador. Selecciona uno de seis gráficos de barra a partir de `piezas × 5 / objetivo` y recompone el nombre cuando cambia el estado.

[Hud/update.mcfunction](demo/datapack/data/taller/function/hud/update.mcfunction) elige la imagen y los desplazamientos. [Make_assets.py](demo/tools/make_assets.py) genera las seis texturas. El saldo de la demo no modifica inventarios.

## 20. Personajes y bocadillos

Una mascota dibujada en la interfaz puede combinar imágenes de fuente, texto y sonidos. Su comportamiento debe programarse por separado y requiere probar los anclajes y las preferencias.

Esta ampliación no está implementada en Taller. La ilustración de capas muestra posibilidades de la técnica, no funciones ya verificadas de la demo.

## 21. Notificaciones y alternativas

Un sistema puede utilizar títulos, barra de acción o chat para avisar de un cambio. Elige un canal que no estorbe a la partida y permite ocultar lo accesorio.

La demo conserva una entrada de chat clicable y un acceso desde el menú de pausa. Su implementación está en [player/init.mcfunction](demo/datapack/data/taller/function/player/init.mcfunction) y [open.json](demo/datapack/data/taller/dialog/open.json).

## 22. Transiciones visuales

Un título con un glifo y un shader puede formar parte de una transición. El efecto necesita sus propios tiempos y limpieza al interrumpirse.

Taller no implementa todavía transiciones complejas. No confundir la capacidad de la técnica con el alcance comprobado de este proyecto.

## 23. Guardar las preferencias

Progreso, saldo, objetivo y preferencias están en los scoreboards del mundo. Al volver a entrar, se conserva el identificador del jugador y se refresca su HUD.

[Player/rejoin.mcfunction](demo/datapack/data/taller/function/player/rejoin.mcfunction) invalida la sesión anterior. El almacenamiento `taller:ctx` solo prepara temporalmente la siguiente operación, ejecutada de forma secuencial; no es el archivo persistente de un jugador.

## 24. Conectar la interfaz con un juego

Sustituye las reglas de pedido por las de tu proyecto y conserva la separación entre estado, validación y dibujo. Un dibujo de máquina no produce objetos por sí mismo.

La demo permite practicar ese recorrido sin tocar una economía real. Su [carpeta logic/](https://github.com/JavierLoro/minecraft-ui-guide/tree/main/demo/datapack/data/taller/function/logic/) es el punto de sustitución.

## 25. Actualizar sin redibujar todo continuamente

El ciclo por jugador atiende solicitudes y temporizadores. El HUD se recompone al entrar o cambiar sus datos; no se vuelve a enviar completo cada tick por rutina.

[Player/tick.mcfunction](demo/datapack/data/taller/function/player/tick.mcfunction) administra la cola, el enfriamiento y la habilitación de triggers. Cada bossbar pertenece a su identificador de jugador.

## 26. Partir del proyecto base

1. Instala el datapack y los recursos en un mundo de pruebas de 26.3.
2. Abre `/trigger taller.open` sin OP y recorre las acciones.
3. Cambia una regla en `logic/` y comprueba su efecto.
4. Modifica una textura o una fuente y revisa las métricas del HUD.
5. Cambia el namespace y los objetivos al crear tu propio proyecto.

[Instrucciones de Taller](demo/README.md) y [mapa para agentes](demo/AGENTS.md). No requiere Gradle ni compilar Java.

## 27. Comprobar las reglas y el resultado visual

Las autopruebas son funciones reales del datapack:

```mcfunction
function taller:test/run
data get storage taller:test report
```

El informe debe tener `errors: 0`. [Test/run.mcfunction](demo/datapack/data/taller/function/test/run.mcfunction) prueba límites del pedido, pago único, separación de datos y rangos de ajustes.

Validar JSON y comandos con el código del juego comprueba sus formatos, no la experiencia visual. Las [capturas y pruebas del cliente](demo/CAPTURAS.md) deben realizarse aparte.

## 28. Encontrar un problema

- **No se abre:** comprobar que el datapack está habilitado y que se usa `/trigger taller.open`.
- **Faltan dibujos:** comprobar que el paquete de recursos está activo y es el de la misma versión.
- **No cobra:** comprobar objetivo, progreso y marca de cobro; no modificar solo la etiqueta.
- **El anclaje falla:** volver al modo centrado y revisar versión, escala y shader.
- **Cambios sin actualizar:** ejecutar `python demo/tools/build.py` y recargar el datapack o reiniciar el mundo de pruebas.

No publicar registros con datos de jugadores. No utilizar mundos importantes para las primeras pruebas.

## 29. Alcance y referencias

La lectura principal de la web explica la idea. Sus desplegables y este manual enlazan a una implementación vanilla concreta. Las ilustraciones no sustituyen las capturas ni la prueba dentro del cliente.

- [Diálogos de Minecraft Java 1.21.6](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21-6).
- [Cambios y formatos de Minecraft Java 26.3](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3).
- [Proyecto y alcance de la demo](demo/README.md).
- [Versiones fijadas](demo/versions.json) y [pruebas visuales](demo/CAPTURAS.md).
