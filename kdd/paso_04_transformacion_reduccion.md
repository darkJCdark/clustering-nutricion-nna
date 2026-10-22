# Paso 4 — Transformación y reducción de dimensiones

**Estado:** documentado; pendiente de ejecutar; **bloqueo conocido: tablas de referencia LMS**
**Salida que pide el curso:** Archivo con variables transformadas (y componentes/factores si se reduce)

| | |
|---|---|
| **Entrada** | `data/interim/03_limpio.csv` |
| **Salida guardada** | `data/processed/04_features.csv`, `data/processed/04_particion.csv` (NNA → train/test), `data/processed/04_transformadores/` y este `.md` |
| **Notebook** | `notebooks/04_transformacion.ipynb` |

## Orden de operaciones (importa por la fuga de información)

1. **Partición train/test por NNA** (D3: 70/30, `random_state` fijo, estratificada por tramo etario o sexo si el tamaño lo permite). Se guarda en `04_particion.csv` **antes** de ajustar cualquier transformador.
2. Derivar variables: `edad_meses`, `imc` (recalculado), `meses_permanencia`.
3. Medidas antropométricas relativas a la edad: **puntaje z** de talla/edad e IMC/edad (5–19 años). Los transformadores/tablas se ajustan **solo con train** si dependen de los datos; las tablas de referencia son externas y no se ajustan.
4. Escalado de las numéricas: Z-score si la distribución es simétrica; robusta (mediana/RIC) si es asimétrica o con atípicos; decidir **variable por variable**, no de forma masiva. Normalizar ≠ estandarizar.
5. Codificación: las categóricas se mantienen como categorías para Gower y K-Prototypes (no one-hot); `Último nivel educativo` como ordinal (Ninguno < Inicial < Primaria < Secundaria < Técnico); dummies solo para K-Means línea base.
6. Reducción de dimensiones: **opcional**. Bartlett (y KMO si EFA) sobre las numéricas antes de decidir. Con 3–6 numéricas se espera no reducir; DECISION: no reducir salvo que Bartlett y KMO lo justifiquen.
7. Guardar cada transformador (por ejemplo con `joblib`) y el diccionario de columnas finales.

## Bloqueo: referencias de crecimiento

Los libros traen diagnósticos en texto, no puntajes z. Para el z se necesitan los parámetros LMS (OMS 2007 para 5–19 años, o CDC 2000 como usa el CENAN). Los PDF del repositorio son tablas rápidas y curvas. Opciones, por orden de preferencia:
1. Usar los parámetros LMS publicados (OMS/CDC), registrando la fuente exacta y fecha de consulta.
2. Si no se pueden obtener: usar IMC y talla **crudos estandarizados por edad y sexo dentro de la muestra** (z interno), declarándolo como limitación.
3. Usar las categorías de los diagnósticos manuales como variable ordinal de **validación**, no de entrada.
DECISION: se intenta 1 en el Paso 4; si no es posible, se documenta 2 y se avisa al autor.

## Checklist del curso

- [ ] Partición hecha antes de ajustar transformadores
- [ ] Z o percentiles de referencia calculados y verificados (muestra de comprobación contra los diagnósticos manuales, solo en agregado)
- [ ] Escala elegida por variable con su justificación
- [ ] Codificación acorde a cada algoritmo
- [ ] Bartlett/KMO calculados; reducción decidida
- [ ] Transformadores guardados

## Criterios de salida

- `04_features.csv` tiene una fila por NNA, columnas tipadas (numéricas/categóricas/ordinales) y la columna `conjunto` (train/test).
- La concordancia de las categorías derivadas del z con los diagnósticos manuales se reporta (si es baja, se investiga antes de seguir).

## Registro de lo realizado

*(Se completa al ejecutar.)*

## Fuentes

OMS/CDC (por registrar tras obtenerlas, con fuente indexada o institucional pública: DECISION si no es 2022–2026). Resto: reglas del curso.
