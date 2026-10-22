# Estructura del repositorio

```
clustering-nutricion-nna/
├── README.md
├── docs/
│   ├── 00_reglas_de_trabajo.md
│   ├── 01_estructura_del_repositorio.md      (este archivo)
│   ├── 02_bitacora.md                         qué se hizo y cómo
│   ├── 03_decisiones_y_pendientes.md
│   ├── 04_aprendido_en_el_curso.md            método del curso aplicado al proyecto
│   ├── 05_formato_informe.md
│   ├── 06_contexto_sesion.md                  contexto acumulado de las sesiones
│   ├── 07_diccionario_de_datos.md             variables, escalas y uso
│   ├── 08_perfil_y_cobertura.md               cobertura y decisiones D1–D7
│   └── 09_lista_previa_al_codigo.md           pendientes y contrato de archivos
├── kdd/                                       un .md por paso del KDD (9 pasos)
│   ├── README.md
│   └── paso_01_… a paso_09_…
├── data/
│   ├── README.md
│   ├── raw/                                   originales, nunca se editan
│   │   ├── ficha_nominal/
│   │   └── nutricion_mensual/
│   ├── interim/                               salidas de pasos 2–3
│   ├── processed/                             salidas de pasos 4–7
│   └── external/
│       └── referencias_oms_cenan/             tablas CENAN y curvas OMS (públicas)
├── fuentes/
│   ├── README.md
│   ├── registro.md                            fuentes verificadas
│   └── fuentes.csv                            entrada de descargar_fuentes.py
├── reports/
│   └── informe/                               informe IEEE en Markdown
├── notebooks/                                 un notebook por paso (sin salidas con datos)
├── src/                                       módulos reutilizables
└── scripts/
    ├── descargar_fuentes.py
    ├── verificar_citas.py
    └── reordenar_repo.ps1                     mueve los datos a su lugar (sin commit)
```

## Por qué esta estructura

- **`kdd/` refleja los 9 pasos del curso** (ver `04_aprendido_en_el_curso.md`). Cada paso tiene su `.md` con la entrada, la salida y el checklist que el curso pide.
- **`data/raw/` no se modifica.** Cada paso escribe su salida en `interim/` o `processed/`, y el siguiente la lee.
- **Los PDF de OMS y CENAN van en `data/external/`**, separados de los datos personales: son referencias públicas.
- **`fuentes/`** concentra la verificación para cumplir la regla de "no inventar fuentes".
- **Todo el trabajo narrado va en `.md`**, de modo que el autor pueda revisarlo y aprobarlo paso a paso.

## Reubicación del contenido actual del repositorio

Estado al 2026-10-21: los datos están en la raíz con nombres de carpeta largos. Claude no tiene terminal en la computadora del autor, así que **no pudo mover ni borrar archivos**. Se preparó `scripts/reordenar_repo.ps1`, que los mueve sin tocar git.

| Ubicación actual | Ubicación nueva |
|---|---|
| `FichaNominal_consolidado_IDs.xlsx` (raíz) | `data/raw/ficha_nominal/FichaNominal_consolidado_IDs_v1.xlsx` |
| `Datos TA - Bloque 1 (…)/FichaNominal_consolidado_IDs_v2.txt` | `data/raw/ficha_nominal/FichaNominal_consolidado_IDs_v2.txt` |
| `Datos TA - Bloque 1 (…)/FichaNominal_consolidado_IDs_v2.xlsx` | `data/raw/ficha_nominal/FichaNominal_consolidado_IDs_v2.xlsx` |
| `Datos TA - Bloque 2 …/Nutricion_IDs_2026XX - … .xlsx` (6 archivos) | `data/raw/nutricion_mensual/` (mismo nombre) |
| `Datos TA - Bloque 2 …/CENAN-0079, 0081, 0082, 0083.pdf` | `data/external/referencias_oms_cenan/` |
| `Datos TA - Bloque 2 …/curvas_oms.pdf` | `data/external/referencias_oms_cenan/` |
| `README.md` | Se reemplaza por el nuevo |

Dudas abiertas sobre los datos: ver `03_decisiones_y_pendientes.md`.
