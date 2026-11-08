# Taller para tu servidor vanilla

Añade menús, pedidos, ajustes y HUD a un servidor existente de **Minecraft Java 26.3**. La instalación utiliza un datapack y un paquete de recursos ya preparados.

**[Descargar instalación](https://javierloro.github.io/minecraft-ui-guide/downloads/taller-instalacion.zip)** · **[Pasos de instalación](INSTALACION.md)**

1. Copia el ZIP del datapack a `<tu-mundo>/datapacks/`.
2. Añade a `server.properties` las dos líneas de recursos incluidas en el descargable.
3. Reinicia el servidor con tu procedimiento habitual.
4. Entra, acepta los recursos y escribe `/trigger taller.open`.

Si ya distribuyes un paquete propio, integra los recursos en él, conserva su URL y actualiza el SHA-1 del ZIP combinado. La instalación usa el servidor que ya tienes: no hay que ejecutar scripts ni compilar.

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

## Modificar el proyecto

El [proyecto fuente](https://javierloro.github.io/minecraft-ui-guide/downloads/minecraft-ui-demo.zip) incluye los archivos editables y las herramientas de desarrollo. Consulta [DESARROLLO.md](DESARROLLO.md) para regenerar recursos o levantar un mundo de pruebas aislado.

La comprobación visual y las [capturas del cliente](CAPTURAS.md) siguen siendo una etapa distinta de la validación de formatos.

## Alcance

Esta base implementa pedidos, botones, tooltips, tres controles, preferencias y HUD. Mascotas, transiciones complejas y un campo de nombre libre no están implementados. Un shader mueve el dibujo, no crea zonas clicables nuevas.

Los gráficos del paquete deben estar cargados; el datapack no detecta por sí solo el resultado de esa descarga. Los jugadores deben aceptar el paquete configurado por el servidor. Los sprites transparentes afectan también a otras bossbars blancas de estilo continuo.

Cambia el namespace `taller`, los objetivos y el contrato de fuentes y shader al adaptarlo a otro proyecto. [Entrada para agentes](AGENTS.md), [guía divulgativa](https://javierloro.github.io/minecraft-ui-guide/) y [atribuciones](NOTICE).
