# Paso 1 — Entendimiento del dominio y objetivos (ficha técnica)

**Estado:** documentado, listo para codificar (borrador de Claude; el autor puede ajustar)
**Salida que pide el curso:** Ficha técnica del proyecto

| | |
|---|---|
| **Entrada** | Datos del repositorio (`docs/07`, `docs/08`), reglas de trabajo, fuentes 6–8 |
| **Salida guardada** | Esta ficha. Alimenta Pasos 2, 5 y 9 |

## Ficha técnica

**Dominio.** Evaluación nutricional mensual de niñas, niños y adolescentes (NNA) en hogares de cuidado residencial en Lima. Hoy el estado nutricional se diagnostica caso por caso con tablas manuales (percentiles OMS y tablas rápidas INS/CENAN) y se registra en una ficha nominal y en libros mensuales con formatos distintos.

**Pregunta de investigación.**
¿Qué perfiles nutricionales distintos se forman entre los NNA de 5 a 19 años de los hogares residenciales cuando se combinan sus medidas antropométricas con su contexto de salud, educación y soporte psico-emocional, y qué tan estables son esos perfiles?

**Objetivo del negocio.** Dar a los equipos de los hogares una segmentación de NNA por perfil nutricional-contextual que permita priorizar seguimiento (no sustituye el diagnóstico clínico).
**Objetivo de análisis de datos.** Agrupar a los NNA con clustering sobre variables mixtas, comparando al menos 3 algoritmos, y validar el mejor con test y estabilidad.

**Población.**
- Espacio: NNA de los hogares Infantes, Miguel Echenique, Tomás Valle y Matogrosso (mujeres y hombres).
- Tiempo: corte transversal de enero 2026 (decisión D1); trayectorias 2026 opcionales.
- Inclusión: NNA con peso, talla y fecha de nacimiento válidos en enero 2026 y edad de 5 a 19 años (D2).
- Exclusión: menores de 5 años (se describen aparte), registros sin peso o talla.
- Eliminación: duplicados ID + periodo (17 filas parciales; se conserva la fila más completa y se registra).

**Métricas de evaluación (definidas desde el inicio).**
- Interna: silhouette sobre la matriz Gower (criterio común), Davies-Bouldin como apoyo y tamaños de cluster.
- Validación con test: ARI, Rand y Jaccard entre las etiquetas de test y las predichas por KNN entrenado con train.
- Estabilidad: ARI medio bajo submuestreo (80 %), bootstrap, ruido y semillas.
- Externa (informativa): ARI contra los diagnósticos manuales.
- DECISION: los umbrales de aceptación se fijan en el Paso 6 antes de ver los resultados (ver `informe/informe.md`, tabla de IOV).

**Recursos y limitaciones.** Un solo estudiante; datos sensibles de menores; ~135 NNA en el tramo principal; formatos heterogéneos; sin verdad terreno clínica; tablas LMS por obtener (Paso 4). Datos originales publicados en el repositorio por decisión del autor (riesgo de reidentificación advertido).

**Ética.** Salidas solo en agregados; sin fechas exactas, distrito ni IDs en informes; los perfiles no son diagnósticos ni se usan para etiquetar a una persona.

**Plan y entregables.** Un notebook por paso (`notebooks/`), cada uno lee la salida del anterior; informe IEEE en `reports/informe/`. Fecha de entrega: DECISION: por confirmar con el curso (el sílabo no se pudo leer).

## Checklist del curso

- [x] Problema planteado como pregunta, que relaciona variables y permite prueba empírica
- [x] Objetivos del negocio y de análisis de datos separados
- [x] Métricas definidas desde el inicio
- [x] Población delimitada en espacio y tiempo, con inclusión, exclusión y eliminación
- [x] Recursos y limitaciones
- [ ] Validación de la ficha con el negocio (el autor decide si consulta a los hogares)

## Registro de lo realizado

2026-10-21: ficha redactada a partir del perfil de datos (`docs/08`). No requiere código.

## Fuentes que sustentan este paso

[6] y [7] respaldan que las instituciones residenciales presentan mayor malnutrición y que el IMC solo no basta para evaluar. [3] respalda el uso de Silhouette y Davies-Bouldin (indexación sin confirmar: no citar hasta confirmarla). Lo demás es DECISION del proyecto.
