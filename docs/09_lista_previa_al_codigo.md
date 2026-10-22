# Lista previa al código

Estado al 2026-10-21. "Hecho" = documentado; el código aún no se escribió.

## Hecho

- [x] Estructura del repositorio (`docs/01`) y reglas (`docs/00`)
- [x] Método del curso (`docs/04`) y formato del informe (`docs/05`)
- [x] Diccionario y perfil de datos (`docs/07`, `docs/08`)
- [x] Los 9 pasos KDD documentados con entradas, salidas, criterios de salida y decisiones (`kdd/`)
- [x] Esqueleto del informe con árbol de problemas y objetivos en borrador (`reports/informe/informe.md`)
- [x] Fuentes iniciales verificadas en Scopus (`fuentes/registro.md`) y verificador de citas IEEE
- [x] Contrato de archivos entre pasos (tabla abajo)
- [x] Dependencias (`requirements.txt`) y convención de notebooks/módulos

## Pendiente antes o durante el código

| # | Pendiente | Quién | Bloquea |
|---|---|---|---|
| 1 | Ejecutar `scripts/reordenar_repo.ps1` (ensayo y luego `-Aplicar`) | Autor | Rutas de `data/raw/`; mientras tanto el código lee de las carpetas originales |
| 2 | Obtener tablas LMS (OMS 5–19 / CDC 2000) y registrar su fuente | Claude (Paso 4) / autor si requieren acceso | Z de referencia |
| 3 | ~~Umbrales de aceptación~~ fijados en `kdd/paso_06` (silhouette ≥ 0,20 según [4]; ARI relativo al control permutado) | hecho | — |
| 4 | Fecha de entrega y número de entregas del curso | Autor | Cronograma |
| 5 | Confirmar Chicco et al. en Scopus y sesión en IEEE Xplore | Autor / Claude | Fuentes del marco |
| 6 | Leer el texto completo de cada fuente y anotar páginas | Claude + autor | Citas con página |
| 7 | Instalar dependencias (no instalables desde el entorno de Claude) | Autor | Ejecutar notebooks |
| 8 | ~~Aprobar D1–D7~~ aprobadas el 2026-10-21 | hecho | — |

## Contrato de archivos (qué lee y qué escribe cada paso)

| Paso | Lee | Escribe |
|---|---|---|
| 1 | — | `kdd/paso_01…md` |
| 2 | `data/raw/*` | `data/interim/02_diccionario.csv`, `02_cobertura.csv` |
| 3 | `02_diccionario.csv`, `data/raw/*` | `data/interim/03_limpio.csv`, `03_log_limpieza.csv` |
| 4 | `03_limpio.csv` | `data/processed/04_features.csv`, `04_particion.csv`, `04_transformadores/` |
| 5 | Paso 1 | `kdd/paso_05…md` |
| 6 | `04_features.csv` | `data/processed/06_plan_experimentos.csv` |
| 7 | `04_features.csv`, `04_particion.csv`, `06_plan_experimentos.csv` | `data/processed/07_modelos/`, `07_comparacion.csv`, `07_etiquetas.csv`, `07_validacion.csv` |
| 8 | `07_etiquetas.csv`, `04_features.csv` | `reports/figures/`, `reports/tablas/08_perfiles.csv` |
| 9 | todo lo anterior | `reports/informe/informe.md` |

## Convenciones de código

- Notebooks numerados por paso; sin salidas que muestren filas individuales (limpiar salidas antes de guardar).
- Lógica reutilizable en `src/` (módulos propuestos: `lectura.py`, `limpieza.py`, `transformacion.py`, `gower.py`, `modelos.py`, `validacion.py`, `perfiles.py`).
- Semilla global `SEED = 42`, declarada en un solo lugar (`src/config.py`).
- Rutas relativas a la raíz del repositorio con `pathlib`.
- Cada notebook comienza con una celda "Entrada / Salida" que repite el contrato.
