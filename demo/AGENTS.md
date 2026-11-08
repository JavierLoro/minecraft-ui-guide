# Demo de interfaces de Minecraft Java

Proyecto base para Paper 26.3 build 244 y Java 25. Todo el contenido grafico de `pack/assets/taller/` es propio; el shader conserva la base de Minecraft 26.3.

- `WorkshopState`: reglas puras de la demostracion y preferencias.
- `SessionGate`: sesiones de pantalla por jugador; invalida acciones antiguas.
- `ProfileStore`: persistencia local por UUID.
- `DemoDialogs`: pantallas y formularios nativos de Paper.
- `HudRenderer`: glifos, metricas y composicion de la bossbar.
- `PackServer`: servicio HTTP local del paquete, sin acceso al resto del disco.
- `UiDemoPlugin`: ciclo de vida, comandos y coordinacion.

Ejecutar `python tools/make_assets.py` tras modificar el generador. Compilar y probar con `./gradlew clean build` (Windows: `gradlew.bat clean build`), usando Java 25.

No publicar `run/`, perfiles, logs, UUID de jugadores ni datos de autenticacion. Los comandos actuan solo sobre el estado de demo del jugador; no modifican su inventario ni su economia real. Las capturas documentales deben proceder de Minecraft ejecutando esta demo, nunca de imagenes generadas.
