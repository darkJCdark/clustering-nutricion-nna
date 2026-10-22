# Datos

| Carpeta | Contenido | ¿Se edita? |
|---|---|---|
| `raw/ficha_nominal/` | Ficha nominal consolidada (v1 y v2, `.xlsx` y `.txt`) | Nunca |
| `raw/nutricion_mensual/` | Evaluaciones nutricionales mensuales por hogar (`.xlsx`) | Nunca |
| `interim/` | Salidas de los pasos 2 y 3 (diccionario, datos limpios) | Las regenera el código |
| `processed/` | Salidas de los pasos 4 a 7 (variables, modelos, comparaciones) | Las regenera el código |
| `external/referencias_oms_cenan/` | Tablas CENAN (CDC 2000, 5–19 años) y curvas OMS (0–5 años): referencias públicas | Nunca |

## Contenido (estructura, sin datos individuales)

- **Ficha nominal:** una fila por NNA y mes (cortes `2025_01` a `2026_07`), 33 variables: sexo, fechas, ubicación, situación legal, educación, salud, soporte psico-emocional, nivel nutricional y seguro. Separador `|` en el `.txt`.
- **Evaluaciones mensuales:** una hoja por hogar y mes (Infantes, Miguel Echenique, Tomás Valle, Matogrosso mujeres y hombres). Edad, peso, talla, IMC y diagnósticos manuales según percentiles OMS y tablas rápidas INS/CENAN. Los infantes usan P/E, T/E, P/T e IMC; los adolescentes, T/E e IMC/E.

## Aviso de privacidad

Son datos de menores bajo protección del Estado. Los IDs (`PPA_FN_####`) están pseudonimizados, pero la **fecha de nacimiento, el distrito y la fecha de ingreso** permiten reidentificar. Por decisión del autor los originales se mantienen en el repositorio; el análisis **excluye** esas variables y los informes **no** muestran registros individuales.

Estado de la reubicación: ver `docs/01_estructura_del_repositorio.md` y `scripts/reordenar_repo.ps1`.
