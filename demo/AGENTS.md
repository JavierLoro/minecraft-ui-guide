# Demo vanilla de interfaces

La instalación para servidores existentes está en `INSTALACION.md`: no requiere Python ni arrancar otro servidor. `DESARROLLO.md` separa las herramientas para modificar el proyecto.

Minecraft Java 26.3. Solo datapack y recursos; no reintroducir plugins ni APIs de Paper.

- Reglas: `datapack/data/taller/function/logic/`.
- Entrada: `/trigger taller.open` y `dialog/open.json`.
- Sesiones y validación: `function/ui/` y `function/input/`.
- HUD por jugador: `function/hud/` y `pack/assets/taller/`.
- Persistencia: objetivos `taller.*`; almacenamiento `taller:ctx` solo temporal y secuencial.
- `tools/build.py` genera los 48 formularios y los ZIP. `tools/make_assets.py` genera los gráficos propios.
- `function taller:test/run` ejecuta las reglas reales; consultar `storage taller:test report`.

Los números de sesión limitan el uso de botones antiguos; los permisos de administrador siguen siendo de confianza. El formulario solo transporta un entero acotado mediante `/trigger`. No prometer una ejecución de `minecraft:custom` en vanilla.

No publicar `run/`, `run-vanilla/`, mundos, perfiles, registros ni el JAR de Mojang. Las capturas deben proceder de esta demo ejecutada dentro de Minecraft. Los checks de sintaxis no equivalen a una prueba visual.
