# Guía de interfaces y demo vanilla

## Decisión de producto

La web es primero divulgativa: cualquier persona interesada debe entender la idea sin programar ni abrir los desplegables. Los detalles técnicos, comandos y referencias de archivos van en desplegables junto a cada concepto. No convertir la portada en un tutorial de instalación.

La implementación de referencia es Minecraft Java vanilla: datapack y paquete de recursos. No reintroducir Paper ni un plugin. La demo es un ejemplo concreto; no presentar ampliaciones todavía inexistentes como funciones implementadas.

## Fuentes y comandos

- Relato público y presentación: `source/template.html`.
- Manual técnico: `GUIA-INTERFACES-MINECRAFT.md`.
- `python tools/build.py` genera `index.html` y `llms-full.txt`.
- `python tools/check.py` comprueba enlaces, anclas y sincronización.
- Demo: [demo/README.md](demo/README.md) y [demo/AGENTS.md](demo/AGENTS.md).
- `python demo/tools/build.py` genera formularios y paquetes; `python demo/tools/check_pack.py` verifica sus recursos.
- `python tools/package_demo.py` prepara el proyecto descargable. No incluir mundos, datos de jugadores, cachés ni el JAR de Mojang.

## Mapa de la implementación

El datapack conserva estado en scoreboards, recibe `/trigger` y valida las acciones. Las funciones `logic/` aplican reglas; `ui/` muestra diálogos; `hud/` compone una bossbar por jugador. El paquete aporta fuentes, texturas y un shader específico de 26.3.

La sesión del menú se incluye en los botones. El formulario transporta solo un entero validado. `minecraft:custom` no ejecuta una función de datapack automáticamente. El almacén `taller:ctx` es temporal y secuencial, no persistencia de jugadores.

## Evidencia

Distinguir validación de formatos, pruebas ejecutadas en vanilla y prueba visual en cliente. No generar imágenes para simular capturas. Consultar [demo/CAPTURAS.md](demo/CAPTURAS.md). Mantener relativos los enlaces internos y el sitio independiente de servidores ajenos.
