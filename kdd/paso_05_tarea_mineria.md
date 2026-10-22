# Paso 5 — Elegir la tarea de minería de datos

**Estado:** decidido (borrador de Claude)
**Salida que pide el curso:** Decisión documentada

| | |
|---|---|
| **Entrada** | `kdd/paso_01_entendimiento_negocio.md` |
| **Salida guardada** | Este `.md` |

## Decisión

**Tarea descriptiva no supervisada: clustering.**

Motivo (emparejamiento con el Paso 1): la pregunta busca **perfiles** y no predecir una etiqueta conocida; no existe una variable objetivo fiable (los diagnósticos manuales son resultado de tablas aplicadas a las mismas medidas, D4). Una tarea predictiva reproduciría las tablas. La optimización no aplica.

Qué **no** se hace: clasificación del `Nivel Nutricional` (circular), regresión de peso, series temporales (fase opcional D5).

## Checklist del curso

- [x] Tarea emparejada con los objetivos del Paso 1
- [x] Justificación de clustering frente a las otras tareas

## Registro de lo realizado

2026-10-21: decisión redactada. No requiere código.

## Fuentes

Los trabajos relacionados [1] (Szepannek) y [5] (Huang) y [4] (Heiskala) usan clustering para datos mixtos y trayectorias de IMC (ver `fuentes/registro.md` para alcance y población de cada uno).
