# Decisiones y pendientes

## Decisiones tomadas

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-21 | Proyecto individual | Autor |
| 2026-10-21 | Informe en Markdown, estilo IEEE a doble columna, sin guía de TA del curso | Autor |
| 2026-10-21 | Datos originales se mantienen en el repositorio (se advirtió el riesgo de reidentificación) | Autor |
| 2026-10-21 | Primero el informe; el contenido del curso se adjuntará después | Autor |
| 2026-10-21 | Claude trabaja solo en este repo, con autonomía para definir la estructura; nunca hace commits | Autor |
| 2026-10-21 | Ciclo KDD de **9 pasos** del curso, un `.md` por paso | Claude (según el curso) |
| 2026-10-21 | Reordenar los datos con un script que el autor ejecuta (Claude no tiene terminal) | Claude |
| 2026-10-21 | Se aplica la excepción Ortegón et al. (2005) solo a la técnica del árbol de problemas; se marca como excepción en el informe | Autor ("sí, a todo") |
| 2026-10-21 | Decisiones de datos D1–D7 (unidad NNA en enero 2026; análisis principal 5–19 años; partición por NNA; diagnósticos solo para validación) — borrador a aprobar, ver `docs/08` | Claude (borrador) |
| 2026-10-21 | Verificador de citas adaptado a IEEE numérico; skills a 9 pasos propuestas | Claude |

## Pendientes que requieren al autor

1. **Ejecutar `scripts/reordenar_repo.ps1`** (primero sin `-Aplicar` para ver el ensayo) y revisar el resultado en `git status`. No hay commit.
2. **Sesión en Scopus e IEEE:** confirmar que la sesión institucional está activa en el navegador del chat. En IEEE Xplore se ve "Institutional Sign In".
3. ~~Excepción Ortegón et al. (2005)~~: aprobada el 2026-10-21.
4. **¿Hay alguna guía de la Tarea Académica** (el curso dice que la TA es sobre un proyecto real con una institución aliada y hay 3 entregas)? El autor indicó que no existe; confirmar cuántas entregas habrá.
5. **Datos públicos:** el repositorio en GitHub es público y contiene los datos originales. Se mantiene por decisión del autor; reconsiderar antes de entregar.
6. **Contenido del curso** que el autor adjuntará, para completar el informe.

## Pendientes técnicos (de Claude, con aprobación)

- ~~Adaptar `verificar_citas.py` a IEEE~~ (hecho). `descargar_fuentes.py` no depende del estilo de cita.
- Confirmar Chicco et al. en Scopus por título exacto.
- Probar `descargar_fuentes.py` con red real (en el entorno de Claude la red está bloqueada).
- Completar el Paso 1 (ficha técnica) con el autor.
- Tarea de la semana 10 (`step7b`): el autor pidió retomarla; falta abrir los archivos del repositorio del curso en el navegador del chat y completarlos.

## Pendientes previos al código

Ver `docs/09_lista_previa_al_codigo.md` (8 puntos, con responsable y qué bloquea).

- Revisar con el hogar el NNA con edad calculada ≈ 28 años (probable error de fecha de nacimiento).
