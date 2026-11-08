# Comprobar y capturar la demo

Usa Minecraft Java 26.3 con el paquete de esta demo. Conserva las capturas originales tomadas con F2; se seleccionan y publican después de comprobar que no contienen información privada.

## Recorrido de prueba

1. Conéctate a `127.0.0.1:25585` y acepta el paquete. Comprueba que no hay avisos de carga fallida ni glifos ausentes.
2. Abre `/uidemo`. Fabrica hasta completar un pedido, cobra y comprueba que otro clic o una pantalla anterior no añade un segundo cobro.
3. Abre Ajustes. Cambia el nombre, el tamaño del pedido, la visibilidad y la posición del HUD. Guarda y vuelve a abrir la pantalla.
4. Desconéctate y vuelve a entrar; comprueba que se mantienen el saldo y las preferencias.
5. Prueba la vista centrada y la anclada, con dos escalas de interfaz. Comprueba además que chat, nombres y otros textos no cambian de posición o color.
6. Oculta el HUD y verifica que desaparece. Rechaza el paquete en una conexión nueva y comprueba la alternativa nativa sin glifos privados.

## Capturas para la guía

- `taller-menu.png`: menú principal con el pedido y los botones; deja un tooltip visible si F2 lo permite en esa pantalla.
- `taller-ajustes.png`: los cuatro controles de Ajustes.
- `taller-hud.png`: durante el juego, fuera del diálogo, con un pedido a medio completar.
- `taller-hud-anclado.png`: la variante anclada, solo si se ha comprobado su posición y lectura.

Las capturas seleccionadas irán en `assets/screenshots/` de la guía. La documentación debe indicar qué demuestra cada una y enlazar al archivo de código correspondiente. Una captura no demuestra por sí sola persistencia ni validación: esas comprobaciones se registran por separado.
