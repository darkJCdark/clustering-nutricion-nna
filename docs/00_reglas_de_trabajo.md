# Reglas de trabajo

## Alcance y permisos

- Claude trabaja **solo en este repositorio** (`clustering-nutricion-nna`). No toca otros repositorios ni carpetas.
- Tiene **autonomía completa para definir la estructura** del repositorio y organizar el contenido.
- **Nunca hace commits** ni push. Cambiar la historia de git y subir cambios es decisión exclusiva del autor.
- Todo el trabajo se deja en **archivos `.md`** (salvo código y datos).
- **Siempre indica qué hizo y cómo lo hizo** (ver `02_bitacora.md`).

## Forma de trabajo

- **Human-in-the-loop:** se consulta al autor antes de decidir variables, k, modelos, criterios de selección, descartes de datos y conclusiones.
- **Idioma y tono:** español neutro, directo, sin saludos ni relleno. El código va en bloques Markdown.
- **Proyecto individual:** lo trabaja una sola persona.
- **Primero el informe.** El autor adjuntará después el contenido del curso; hasta entonces no se redacta.
- **Cada paso del KDD guarda su salida en un archivo** que usa el paso siguiente. No se avanza sin aprobación.
- **Se aplica el método del curso** (ver `04_aprendido_en_el_curso.md`), no uno genérico.

## Fuentes

- **Nunca inventar fuentes.** Solo se cita lo que se pudo abrir y leer.
- Ventana **2022–2026**, indexadas en Scopus o IEEE Xplore, sin literatura gris.
- Cada fuente se registra en `fuentes/registro.md` con su estado de verificación. La indexación se marca como "no confirmada" hasta que el autor (o Claude, mediante el navegador con sesión iniciada) la compruebe.
- Cada párrafo de Introducción, Generalidades y Marco debe llevar al menos una fuente real que lo valide. Sin fuente: se marca `HIPOTESIS:` o `DECISION:`, o se elimina.
- Citas IEEE numéricas: [1], [1, p. 3].

## Uso de IA

El curso exige declarar y citar el uso de IA generativa; el docente puede pedir el reporte de prompts como anexo. Este proyecto declara el uso de Claude en `reports/informe/` y conserva la bitácora en `02_bitacora.md`.

## Datos

- Los datos originales se mantienen en el repositorio por decisión del autor. Se le advirtió del riesgo de reidentificación de menores.
- Para el análisis se excluyen la fecha de nacimiento exacta, el distrito y la fecha de ingreso.
- Los notebooks se guardan sin salidas que muestren registros.
