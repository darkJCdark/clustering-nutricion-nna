# Perfiles nutricionales de niñas, niños y adolescentes en hogares de cuidado residencial mediante clustering de datos mixtos

**Autor:** Jorge Chamorro · Pontificia Universidad Católica del Perú · Curso 1INF03 Análisis de Datos, 2026-2

> **BORRADOR (2026-10-21).** Solo contiene lo que se puede sostener antes de codificar. Los resultados, el resumen y las conclusiones se completan después. Estilo IEEE a doble columna: al exportar (Pandoc/Word) aplicar la plantilla IEEE de dos columnas. Las citas usan el N.º de `fuentes/registro.md` y se renumeran al final. Las páginas de cada cita faltan hasta leer el texto completo.

## Resumen

*(≤12 líneas, sin citas ni siglas. Se redacta al final.)*

## 1. Generalidades

### 1.1 Contexto del problema

Las instituciones residenciales para niños y adolescentes enfrentan un riesgo nutricional mayor que el de sus pares fuera de ellas. En un estudio transversal en Nigeria con cuatro residencias y 48 escuelas, la prevalencia de talla baja fue 37,5 % frente a 17,1 %, y la de emaciación 24,3 % frente a 13,8 % [6]. Los autores recomiendan evaluar periódicamente el estado nutricional de estos niños [6]. Este hallazgo se refiere a Nigeria y no se extrapola al Perú.

El IMC por sí solo puede ocultar carencias. En 248 adolescentes de residencias de Taiwán, la ingesta de energía y proteínas fue menor que la de la población general, aunque su IMC fue comparable [7]. Esto respalda combinar medidas antropométricas con otras variables al describir el estado nutricional.

En los hogares que estudia este trabajo, cada mes se evalúa el estado nutricional de cada NNA con percentiles de la OMS y tablas rápidas del CENAN, y los resultados se registran en libros con formatos distintos y en una ficha nominal consolidada. HIPOTESIS: esa práctica produce diagnósticos individuales, pero no una visión agrupada de perfiles. (Observación propia sobre los datos; ver `docs/07`.)

### 1.2 Árbol de problemas (borrador)

| Nivel | ID | Enunciado | Fuente o marca |
|---|---|---|---|
| Efecto | E1 | Mayor prevalencia de malnutrición en niños institucionalizados que en no institucionalizados | [6] (Nigeria) |
| Efecto | E2 | Carencias nutricionales no visibles cuando se usa solo el IMC | [7] (Taiwán) |
| Efecto | E3 | Seguimiento poco focalizado entre NNA con necesidades distintas | HIPOTESIS: sin fuente |
| **Problema central** | PC | No existe una segmentación de los NNA de los hogares por perfil nutricional-contextual que complemente los diagnósticos manuales | DECISION: observación sobre los datos y práctica descrita en 1.1; sin fuente que lo afirme para el Perú |
| Causa | C1 | Los registros nutricionales tienen formatos heterogéneos y categorías inconsistentes que impiden analizarlos en conjunto | DECISION: evidencia en `docs/07` (encabezados distintos por hoja, texto libre, `*`) |
| Causa | C2 | El diagnóstico se basa en indicadores antropométricos aislados, sin combinarlos con el contexto de salud, educación y soporte | [7] respalda la limitación de usar solo antropometría |
| Causa | C3 | No se ha comparado qué métodos de clustering sirven para esta mezcla de variables numéricas, ordinales y categóricas con tamaño de muestra pequeño | HIPOTESIS: ver [1] para métodos de datos mixtos |
| Causa | C4 | No hay un criterio de validación (test y estabilidad) que indique si un agrupamiento es confiable | HIPOTESIS: ver validación del curso |

Cada causa debe resolverse con herramientas informáticas y tener un objetivo específico (1.5). La figura del árbol se agrega al final.

### 1.3 Problema seleccionado y alcance

Segmentar a los NNA de 5 a 19 años de los hogares Infantes, Miguel Echenique, Tomás Valle y Matogrosso con datos de enero de 2026 (decisiones D1 y D2 de `docs/08`). Los menores de 5 años se describen aparte por tamaño de muestra (19 con medida válida en enero de 2026).

### 1.4 Limitaciones

- DECISION: 112 NNA de 5 a 19 años con medida válida en enero de 2026, el único corte con todos los hogares.
- DECISION: sin verdad terreno clínica; los diagnósticos manuales provienen de las mismas medidas.
- DECISION: formatos heterogéneos; z de referencia sujeto a obtener tablas LMS (Paso 4).
- DECISION: los estudios [6], [7] y [8] corresponden a Nigeria, Taiwán y Tailandia.

### 1.5 Objetivos

**Objetivo general (SMART, borrador).** Segmentar, mediante clustering de datos mixtos con al menos tres algoritmos comparados, los perfiles nutricionales de los NNA de 5 a 19 años de los hogares residenciales a partir de las evaluaciones de enero de 2026 y la ficha nominal, alcanzando una solución validada en test y estable, antes de la fecha de entrega del curso (por confirmar).

**Objetivos específicos (uno por causa).**

| Causa | Objetivo específico | Resultado esperado | Medio de verificación | IOV (umbrales de `kdd/paso_06`) |
|---|---|---|---|---|
| C1 | OE1. Integrar y limpiar los registros en una tabla maestra por NNA | RE1.1 `03_limpio.csv` y log de limpieza | Notebooks 02–03, `03_log_limpieza.csv` | 0 duplicados ID+mes; ≤20 % vacíos por columna del modelo |
| C2 | OE2. Construir variables antropométricas relativas a la edad y variables de contexto | RE2.1 `04_features.csv` | Notebook 04 | Concordancia del z derivado con diagnósticos manuales reportada |
| C3 | OE3. Comparar ≥3 algoritmos de clustering de datos mixtos y elegir el mejor | RE3.1 `07_comparacion.csv` | Notebook 07a | ≥3 algoritmos con ≥2 escenarios cada uno; silhouette ≥ 0,20 (referencia de [4]) |
| C4 | OE4. Validar el modelo elegido con test y estabilidad | RE4.1 `07_validacion.csv` | Notebooks 07b–07c | ARI de test y de estabilidad claramente sobre el control permutado (sin cifra de la literatura) |

## 2. Marco conceptual

*(Por redactar con fuente por párrafo: indicadores antropométricos (P/E, T/E, P/T, IMC/E), puntaje z y percentiles (OMS, CDC), clustering de datos mixtos, distancia de Gower, validación de clustering.)*

## 3. Trabajos relacionados

Candidatos registrados (alcance y población en `fuentes/registro.md`): [1] clustering de datos mixtos con ordinales; [4] y [5] trayectorias de IMC infantil con k-medoids y K-Means de series; [2] comparativa de datos mixtos (preprint, antecedente). Falta la tabla comparativa y leer los textos completos. Búsqueda en Scopus con términos en inglés, 2026-10-21; IEEE Xplore pendiente (sin sesión).

## 4. Metodología (KDD de 9 pasos)

Resumen por paso en `kdd/`. Diagrama de flujo pendiente.

## 5. Experimentación y resultados

*(Se completa tras el Paso 7–8.)*

## 6. Conclusiones y trabajos futuros

*(Se completa tras el Paso 9.)*

## 7. Implicancias éticas

Reidentificación (fecha de nacimiento, distrito, fecha de ingreso, discapacidad y situación legal de menores), estigmatización por perfiles, uso como apoyo y no como diagnóstico, y datos originales publicados en un repositorio público por decisión del autor (riesgo advertido).

## 8. Repositorio

`https://github.com/darkJCdark/clustering-nutricion-nna` (ver `README.md` para reproducir).

## 9. Declaraciones

**Uso de IA:** Claude (Anthropic) asistió en la organización del repositorio, la búsqueda de fuentes en Scopus y la redacción de borradores. Todas las fuentes se verificaron por título y resumen en Scopus; el autor es responsable del contenido final. (Completar con el reporte de prompts si el curso lo pide.)

## Referencias

*(IEEE, numeradas por orden de aparición. Provisional: usar `fuentes/registro.md`.)*
