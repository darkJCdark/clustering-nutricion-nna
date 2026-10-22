# Diccionario de datos (preliminar)

Perfil hecho el 2026-10-21 con **agregados** (conteos, porcentajes, categorías), sin imprimir registros individuales. Los IDs de los NNA están seudonimizados (formato `xxx_xx_9999`). El diccionario definitivo se genera en el Paso 2 (`data/interim/02_diccionario.csv`).

Leyenda de **Uso**: **M** = entra al modelo (candidata), **V** = solo validación externa (no entra al modelo), **X** = se excluye, **K** = clave/auxiliar.

## A. Ficha nominal consolidada (`FichaNominal_consolidado_IDs_v2.txt`)

Archivo de texto delimitado por `|`, UTF-8, 2 667 filas, 33 columnas, 157 NNA distintos, 19 cortes mensuales (`2025_01` a `2026_07`). Por NNA hay entre 1 y 36 filas (mediana 19). Hay 17 filas con ID + periodo repetidos (duplicados parciales). Cada corte tiene 134–144 NNA. En `2026_07` quedan 134 NNA; 23 NNA tienen su último corte antes.

| Variable | Escala | Valores / vacíos (agregado) | Uso | Tratamiento propuesto |
|---|---|---|---|---|
| `periodo` | ordinal (fecha) | 19 valores | K | Clave temporal con el ID |
| `IDs_FichaNominal` | nominal | 157 | K | Clave de unión; nunca entra al modelo |
| `Sexo` | nominal | M 56 %, F 44 % | M | Binaria |
| `Fecha de nacimiento` | fecha | 4 % no interpretable | K | Derivar `edad_meses` y descartar la fecha; no publicar |
| `Departamento` | nominal | Lima 91 %, 7 más | X | Casi constante |
| `Provincia` | nominal | Lima 89 %, 11 más | X | Casi constante |
| `Distrito` | nominal | 32 valores, 7 % vacío | X | Riesgo de reidentificación |
| `Nacionalidad` | nominal | PERUANA/PERUANO (misma categoría) | X | Constante tras normalizar |
| `Fecha de ingreso` | fecha | 107 valores | K | Derivar `meses_permanencia`; descartar la fecha |
| `Observaciones… forma de ingreso` | nominal | 97 % "presunta desprotección familiar" | X | Casi constante |
| `Juzgado/UPE` | nominal | 99,9 % UPE | X | Casi constante |
| `Tipo de documento` | nominal | 5 valores con saltos de línea | X | Administrativa |
| `Fecha de la Resolución Administrativa` | fecha | 7 % vacío | X | Administrativa |
| `Situación Legal de la (NNA)` | nominal | 6 valores; 82 % provisional, 9 % definitiva | M | Normalizar texto; agrupar categorías raras |
| `Fecha del Oficio de Ingreso` | fecha | 2 % vacío | X | Administrativa |
| `Nombre de UPE /Juzgado` | nominal | 9 valores con variantes (`UPE-LIMA-SUR`) | X | Administrativa |
| `Comunicado_DGA` | booleana | 100 % verdadero | X | Constante |
| `FECHA ELABORACIÓN PTI`, `VIGENCIA DEL PTI` | fecha | 91 y 89 valores | X | Administrativas |
| `ESTADO DEL PTI` | nominal | Actual 40 %, No tiene 39 %, Vencido 22 % (variantes `no tiene`) | X | Administrativa; revisar en Paso 2 si aporta contexto |
| `Instancia que elabora el PTI` | nominal | 8 valores | X | Administrativa |
| `Grado de Instrucción` | ordinal | 37 textos libres | X | Redundante con edad y nivel; tratar solo si hace falta |
| `Último nivel educativo logrado` | ordinal | Primaria 46 %, Secundaria 30 %, Inicial 15 %, Ninguno 7 %, Técnico 2 % (`Tècnico`) | M | Orden: Ninguno < Inicial < Primaria < Secundaria < Técnico |
| `Tipo de Institución Educativa` | nominal | EBR 87 %, Ninguno 7 %, otros | X | Casi constante |
| `Acceso a capacitación técnico productiva` | nominal | 99 % "No aplica" | X | Casi constante |
| `La NNA actualmente estudia` | nominal | Sí 92 %, No 8 % (`Si`/`si`/`NO`) | M | Normalizar a binaria |
| `Estado de Salud Física Actual` | nominal | Saludable 95 %, Anemia 4,5 %, otros raros (con `\r`) | M | Normalizar; agrupar categorías raras |
| `Presenta Discapacidad` | nominal | 91 % "No tiene"; 8 tipos | M | Binaria (sí/no) y, si hace falta, nivel |
| `Nivel Nutricional` | nominal | 31 textos (Saludable 29 %, Obesidad 11 %, Riesgo de baja talla 10 %, combinaciones…) | **V** | **No entra al modelo**: es un diagnóstico previo; sirve para ARI en validación externa |
| `Soporte Psico-emocional` | nominal | 53 textos (No 40 %, Acompañamiento 31 %, Psicoterapia 7 %, combinaciones) | M | Normalizar y agrupar en pocas categorías |
| `Atenciones de salud psicológica` | nominal | NO 99 % | X | Casi constante |
| `Atención en Salud mental especializada` | nominal | NO 84 %, SI RECIBE 11 %, No aplica 5 % | M | Normalizar (`No aplicca`) |
| `Seguro de Salud (NNA)` | nominal | SIS 99,9 % | X | Casi constante |

Nota sobre privacidad: discapacidad, salud mental y situación legal son datos sensibles de menores. En el informe y los notebooks solo se publican **agregados** con celdas de al menos 5 casos.

## B. Evaluaciones nutricionales mensuales (`Nutricion_IDs_2026*.xlsx`)

Seis libros: enero (todos los hogares), febrero y marzo (solo Infantes), abril y junio (todos), agosto (solo Matogrosso mujeres y hombres). **141 NNA distintos**, todos presentes en la ficha. Filas por libro: enero 141, febrero 7, marzo 6, abril 108, junio 108, agosto 32. Cada libro tiene una hoja por hogar con **encabezados distintos**:

| Hogar | Columnas de medición | Columnas de diagnóstico |
|---|---|---|
| Infantes (<5 años aprox.) | Fecha de nacimiento, edad (texto), peso (kg), talla (cm), IMC | Dos bloques de 4 columnas (IMC, P/E, T/E, P/T): "según percentiles OMS" y "según tabla de diagnóstico rápido" |
| Miguel Echenique | Igual, más `PA` | T/E e IMC/E, dos bloques |
| Tomás Valle | Igual, más `P.A` y P/E | P/E, T/E, IMC/E, dos bloques |
| Matogrosso mujeres y hombres | Igual, sin PA | T/E e IMC/E |

Problemas observados (todos tratados en el Paso 3):

- El ID figura en la columna "APELLIDOS Y NOMBRES" y es seudónimo (11 caracteres).
- La fecha de nacimiento llega como fecha, texto (`12/04/2014`) o con hora.
- La edad es texto libre (`4 años 10 meses`, `7 año 5 meses`, `7años 7meses`).
- Peso y talla son numéricos (infantes 10,6–25,1 kg y 74–118 cm; escolares y adolescentes 18–89 kg y 112–168 cm). Vacíos de 17 % en algunas hojas de Matogrosso.
- Los diagnósticos son texto con espacios finales y un asterisco `*` que indica "no aplica / no se calcula". Categorías: NORMAL, RIESGO SOBREPESO, SOBREPESO, OBESIDAD (también `OBESIDAD III`), RIESGO TALLA BAJA, TALLA BAJA, TALLA BAJA SEVERA, RIESGO BAJO PESO, ALTO.
- Los encabezados de columnas no se repiten entre hojas: la unificación debe hacerse por hoja con un mapa explícito.

Qué hace falta que el código calcule (no hay puntajes z en los libros): `edad_meses` desde la fecha, IMC verificado desde peso y talla, y percentil o puntaje z de talla/edad e IMC/edad con tablas de referencia (OMS para menores de 5 años; CDC 2000 o referencia OMS 5–19 años según el CENAN). **Pendiente de decisión y verificación** (ver Paso 4): de dónde salen las tablas LMS, porque los PDF del repositorio son tablas rápidas y curvas, no los parámetros LMS.

## C. Referencias externas del repositorio

`CENAN-0079/0081/0082/0083.pdf` (tablas rápidas INS/CENAN, 5–19 años, CDC 2000) y `curvas_oms.pdf` (0–5 años). Revisión parcial hasta ahora; el Paso 2 debe leerlas completas y registrar qué valores contienen.
