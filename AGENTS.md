# Interfaces de Minecraft Java: lectura rápida para agentes

Este repositorio reúne una guía técnica independiente y una demo reutilizable de Paper en `demo/`. La guía explica el sistema; la demo aporta un plugin compilable, recursos propios y un arranque local. Usa este archivo para orientarte y consulta [la guía completa](GUIA-INTERFACES-MINECRAFT.md) para implementar. El [HTML interactivo](index.html) explica visualmente la misma arquitectura.

## Modelo mental

```text
Datos del servidor → compositor de componentes → canal nativo → cliente
                                                          + paquete de recursos
Clic del cliente → router del servidor → validar → cambiar estado → renderizar
```

El servidor mantiene las reglas y el estado autorizado. Minecraft transporta y presenta componentes. El paquete aporta fuentes, imágenes y shaders. Una imagen o un shader no implementa economía, electricidad ni producción.

## Mapa de mecanismos

| Necesidad | Mecanismo | Responsabilidad de la aplicación |
|---|---|---|
| Menú modal | Diálogo, por ejemplo `NoticeDialog` | Pantalla, navegación y cierre |
| Imagen en el texto | Fuente bitmap: carácter privado → PNG | Catálogo de glifos y métricas |
| Posición dentro del diálogo | Avances positivos/negativos, saltos de línea y `ascent` | Compositor de layout |
| Botón | Evento de clic en un componente | Acción y validación de sesión |
| Tooltip | Evento de hover `show_text` | Contenido explicativo |
| Toggle gráfico | Dos glifos on/off con una acción | Estado del servidor y nuevo diálogo |
| Formulario | Inputs nativos de texto, booleano, opciones y rango | Validación y procesamiento |
| HUD durante el juego | Nombre de una bossbar | Texto compuesto y actualización por jugador |
| HUD repartido por la pantalla | Shader de texto del paquete | Protocolo de marcadores y anclajes |
| Quitar la barra estándar | Sprites transparentes del color reservado | Compatibilidad con otras bossbars |
| Transición gráfica | Glifo por títulos y shader de fragmentos | Efecto, duración, cancelación y limpieza |
| Idioma y visibilidad | Preferencias en el servidor | Persistencia y sincronización |

## Flujo mínimo de un toggle

1. El servidor compone un diálogo con el glifo adecuado al estado actual.
2. El componente del icono y su etiqueta llevan la acción `hud.toggle_player`.
3. El cliente devuelve el identificador y la generación de sesión.
4. El router valida jugador, sesión, permisos y frecuencia.
5. El servidor cambia y persiste la preferencia.
6. Envía el diálogo actualizado y cambia el HUD si corresponde.

Los nombres de acción, namespace `miui`, caracteres privados y codificación RGB de esta guía son ejemplos de contrato propio. No son un protocolo oficial de Minecraft.

## Precauciones que afectan a la implementación

- Fijar la versión exacta de cliente, servidor, API y paquete. Los diálogos existen desde Java 1.21.6; eso no garantiza que un shader de una versión funcione en otra.
- Un shader desplaza píxeles, no las zonas donde Minecraft detecta el ratón. Verificar la alineación visual y clicable en los diálogos.
- Las bossbars no ofrecen botones ni tooltips interactivos durante el juego normal. Usar diálogos para interacción con cursor.
- Los colores del HUD pueden actuar como instrucciones que el shader descodifica; reservarlos para evitar modificar texto normal.
- Cambiar sprites de bossbar afecta a otras barras del mismo color/estilo.
- Actualizar por cambios y liberar barras, sesiones y tareas al desconectar. Evitar reenviar todo cada tick.
- Validar acciones en el servidor y hacer idempotentes las operaciones económicas.
- El cliente debe cargar el paquete antes de mostrar la interfaz gráfica. Preparar una alternativa si no está disponible.

## Dónde ampliar

La [guía completa](GUIA-INTERFACES-MINECRAFT.md) está numerada para facilitar su búsqueda:

- Capítulos 3–7: versiones, estructura, paquete, fuentes y composición.
- Capítulos 8–14: diálogos, clics, tooltips, toggles, formularios y router.
- Capítulos 15–19: bossbars, transparencia, shaders, adaptación y progreso.
- Capítulos 20–24: mascota, notificaciones, efectos, preferencias y datos de máquinas.
- Capítulos 25–28: rendimiento, implementación por fases, pruebas y diagnóstico.
- Capítulo 29: alcance y documentación primaria.

## Trabajo en este repositorio

- La fuente de contenido es `GUIA-INTERFACES-MINECRAFT.md`; la presentación está en `source/template.html`.
- Tras editar cualquiera, ejecutar `python tools/build.py` y `python tools/check.py`.
- El generador actualiza `index.html` y `llms-full.txt`. No mantener esas copias manualmente.
- Conservar enlaces relativos para funcionar tanto en un dominio como en `usuario.github.io/repositorio/`.
- Mantener el sitio independiente de servidores concretos y sin registros ni rutas personales.

`llms.txt` sirve como índice de descubrimiento. No garantiza que un agente lo lea automáticamente: compartir directamente la URL de este archivo cuando se necesite una incorporación rápida.

## Demo ejecutable

- Entrada del proyecto y comandos: [demo/README.md](demo/README.md).
- Arquitectura para agentes: [demo/AGENTS.md](demo/AGENTS.md).
- Paper 26.3 build 244, JDK 25, Gradle Wrapper 9.2.1; versiones fijadas en `demo/versions.json`.
- En `demo/`: `gradlew.bat build` / `sh gradlew build`, y `python tools/check_pack.py`.
- Después de compilar: `python tools/package_demo.py` desde la raíz regenera los descargables. Nunca incluir `demo/run/`, cachés, mundos, perfiles ni registros.
- `demo/CAPTURAS.md` define las pruebas en el cliente. No afirmar que el shader o la interfaz han sido comprobados visualmente solo porque compile Java.
