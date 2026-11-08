# Instalar Taller en tu servidor

Para un servidor **Minecraft Java 26.3** que ya está funcionando.

[Descargar el paquete de instalación](https://javierloro.github.io/minecraft-ui-guide/downloads/taller-instalacion.zip). Contiene los dos ZIP y un fragmento de configuración; no incluye un servidor nuevo.

1. **Copia el datapack.** Coloca `taller-datapack.zip`, sin descomprimir, en `<tu-mundo>/datapacks/` del servidor.
2. **Configura los recursos.** Si tu servidor aún no distribuye un paquete propio, añade estas líneas a su `server.properties`:

```properties
resource-pack={{PACK_URL}}
resource-pack-sha1={{PACK_SHA1}}
```

3. **Reinicia el servidor** con tu procedimiento habitual para cargar el datapack y la configuración.
4. **Entra y abre el taller.** Acepta el paquete de recursos y escribe `/trigger taller.open`. Los jugadores no necesitan OP para usarlo.

Si ya envías un paquete de recursos propio, integra los archivos de Taller en el tuyo, conserva su URL y actualiza el SHA-1 del ZIP combinado. [Cómo combinar los recursos](https://github.com/JavierLoro/minecraft-ui-guide/blob/main/demo/DESARROLLO.md#combinar-con-otros-recursos).

Los ZIP están preparados para instalarse directamente. Python solo se usa para desarrollar y regenerar el proyecto.

**Comprobación:** en Ajustes puedes ocultar el HUD, cambiar el tamaño del pedido y volver al menú. La vista centrada es la inicial; el anclaje requiere comprobar su posición en el cliente.
