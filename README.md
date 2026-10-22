# clustering-nutricion-nna

Proyecto de clustering de perfiles nutricionales de niñas, niños y adolescentes (NNA) en hogares de cuidado residencial.
Curso **1INF03 Análisis de Datos** (PUCP, 2026-2). Metodología: **KDD de 9 pasos** del curso.

> **Estado:** estructura creada el 2026-10-21. El informe y el análisis aún no se han redactado; esperan el material del curso y la aprobación de cada paso.

## Cómo está organizado

| Carpeta | Contenido |
|---|---|
| [`docs/`](docs/) | Reglas de trabajo, estructura, bitácora, decisiones pendientes, lo aprendido del curso y formato del informe |
| [`kdd/`](kdd/) | Un `.md` por cada uno de los 9 pasos KDD del curso: objetivo, entrada, salida, checklist y estado |
| [`data/`](data/) | Datos: `raw/` (originales), `interim/`, `processed/`, `external/` (tablas públicas OMS/CENAN) |
| [`fuentes/`](fuentes/) | Registro de fuentes científicas verificadas (2022–2026) |
| [`reports/informe/`](reports/informe/) | Informe en Markdown, estilo IEEE a doble columna |
| [`notebooks/`](notebooks/), [`src/`](src/) | Código por paso y módulos reutilizables |
| [`scripts/`](scripts/) | Descarga de fuentes, verificación de citas y reordenamiento del repo |

## Para empezar

1. Leer [`docs/00_reglas_de_trabajo.md`](docs/00_reglas_de_trabajo.md).
2. Ver [`docs/03_decisiones_y_pendientes.md`](docs/03_decisiones_y_pendientes.md) para saber qué falta decidir.
3. Revisar [`docs/02_bitacora.md`](docs/02_bitacora.md): qué se hizo y cómo.
4. Antes de programar: [`docs/09_lista_previa_al_codigo.md`](docs/09_lista_previa_al_codigo.md), con el diccionario ([`docs/07`](docs/07_diccionario_de_datos.md)) y las decisiones de datos ([`docs/08`](docs/08_perfil_y_cobertura.md)).
4. Seguir los pasos en [`kdd/`](kdd/) en orden.

## Aviso sobre los datos

Los datos describen menores bajo protección del Estado. Aunque los IDs están pseudonimizados, la fecha de nacimiento, el distrito y la fecha de ingreso permiten reidentificar. Ver [`data/README.md`](data/README.md).
