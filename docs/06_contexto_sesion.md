> **Nota de actualización (2026-10-21):** este contexto se escribió antes de revisar la teoría del curso. Donde habla de **7 pasos KDD** y de `reports/0X_*.md`, rige ahora el **KDD de 9 pasos** documentado en `kdd/` y `docs/04_aprendido_en_el_curso.md`. Donde dice "Claude no tiene acceso a Scopus ni IEEE", ver `docs/02_bitacora.md` sobre el navegador con sesión. Donde dice que el informe usa APA 7, rige **IEEE numérico**.

# Contexto del proyecto: clustering nutricional en NNA y ciclo KDD

Curso: 1INF03 Análisis de Datos (PUCP, 2026-2). Repositorio de GitHub: `darkJCdark/clustering-nutricion-nna`. Repo local del curso: `pucp-2026-2-1inf03-data-analysis`.
Elaborado el 2026-10-21 a partir de la sesión de trabajo. Es un resumen para retomar el proyecto sin perder contexto.

## 1. Reglas de trabajo acordadas

- **Idioma y tono:** español neutro, directo, sin saludos ni relleno. El código va en bloques Markdown.
- **Human-in-the-loop:** siempre consultar antes de decidir variables, k, modelos, criterios, descartes de datos o conclusiones.
- **Nunca hacer commits** ni empujar al repositorio. El usuario decide qué y cuándo se sube.
- **No inventar fuentes.** Solo citar lo que se pudo abrir y verificar.
- **Fuentes:** 2022–2026, Scopus o IEEE Xplore. Claude no tiene acceso a esas bases: toda fuente queda como "indexación no confirmada" hasta que el usuario la verifique con la biblioteca PUCP.
- **Cada paso del ciclo KDD guarda una salida en archivo** que el siguiente paso usa. No se avanza sin aprobación.
- **Orden de trabajo:** primero el informe. El usuario adjuntará después el contenido del curso; hasta entonces no se redacta.
- **Proyecto individual:** lo trabaja solo (lo planteó antes como grupal).
- **Tarea pausada:** completar `step7b_modelossupervisados_clasificación.py` y `.ipynb` de la semana 10. Se identificaron 4 tareas (variables `department`/`region`, atípicos, imputación, educación dummies vs ordinal). Se acordó alcance con comparación con regresión logística y orden Below Secondary < Bachelor's < Master's & above. No se modificó ningún archivo.

## 2. Datos del proyecto

- **Ficha nominal consolidada:** una fila por NNA y mes (cortes mensuales de 2025_01 a 2026_07), 33 variables: sexo, fechas, ubicación, situación legal, educación, salud, soporte psico-emocional, nivel nutricional y seguro.
- **Evaluaciones nutricionales mensuales (Excel):** una hoja por hogar y mes (Infantes, Miguel Echenique, Tomás Valle, Matogrosso mujeres y hombres). Traen edad, peso, talla, IMC y diagnósticos manuales según percentiles OMS y según tablas rápidas INS/CENAN.
- **Layouts heterogéneos:** infantes usan P/E, T/E, P/T e IMC; adolescentes usan T/E e IMC/E.
- **Problemas de calidad observados:** categorías inconsistentes (mayúsculas, saltos de línea), fechas en dos formatos, tildes rotas, hojas con columnas distintas.
- **Referencias del material:** tablas CENAN (CDC 2000, 5 a 19 años) y curvas OMS (0 a 5 años). Revisión parcial: solo se abrió parte del PDF 0079 y las 2 primeras páginas de las curvas.
- **Datos originales en el repo:** el usuario decidió mantenerlos publicados. Riesgo advertido: fecha de nacimiento, distrito y fecha de ingreso de menores bajo protección permiten reidentificación, aunque los IDs estén pseudonimizados. El usuario mantuvo su decisión.

## 3. Diseño de clustering acordado (a validar)

- **Segmentar por tramo:** menores de 5 años (indicadores OMS) y 5 a 19 años (CDC/CENAN). El usuario dejó la decisión final al criterio justificado con fuentes y datos.
- **Variables:** nutrición (edad, peso, talla, IMC, percentiles o puntaje z) más contexto de la ficha (salud, educación, soporte psicológico, situación legal, permanencia). Excluir fecha de nacimiento exacta, distrito y fecha de ingreso.
- **Comparar 3 o más modelos y luego optimizar el mejor:** K-Means (línea base), Gower + PAM, K-Prototypes (variante Gower), jerárquico con Gower, KAMILA o clases latentes. DBSCAN opcional para atípicos.
- **Validación:** Silhouette y Davies-Bouldin (juntos), Calinski-Harabasz como apoyo, estabilidad con varias semillas e inicializaciones, ARI frente a los diagnósticos manuales.
- **Fase opcional:** clustering de trayectorias mensuales de IMC o percentil.
- **Advertencia:** con ~157 NNA distintos, un tramo puede quedar chico para 4 o 5 modelos.

## 4. Ciclo KDD y archivos de salida (propuesta)

| Paso | Salida guardada |
|---|---|
| 1 Entendimiento del negocio | `reports/01_negocio.md` |
| 2 Selección y entendimiento de datos | `data/interim/02_diccionario.csv`, `reports/02_calidad.md` |
| 3 Preprocesamiento | `data/interim/03_limpio.parquet`, `reports/03_decisiones.md` |
| 4 Transformación | `data/processed/04_features.parquet` y encoders guardados |
| 5 Reducción de dimensiones | `data/processed/05_reducido.parquet`, `reports/05_variables.md` |
| 6 Clustering (≥3 modelos) | `reports/06_comparacion.csv` |
| 7 Validación y optimización | `reports/07_validacion.md` y figuras |

Estructura de repo sugerida: `data/{raw,interim,processed,external}`, `notebooks/` numerados por paso, `src/` para código reutilizable, `reports/informe`, `scripts/`, `fuentes/`, `docs/`. Notebooks sin salidas que muestren registros. Se recomienda combinar `.ipynb` y `.py`.

## 5. Informe

- **Formato:** Markdown en `reports/informe/`, estilo **IEEE a doble columna**, sin guía de TA del curso (no existe). Extensión sin límite oficial.
- **Cambio pendiente por IEEE:** las citas pasan a numéricas ([1], [1, p. 3]). `FORMATO.md`, `verificar_citas.py` y la skill de fuentes están hechos para APA 7 y hay que adaptarlos; todavía no se hizo.
- **Estructura (`FORMATO.md` v2):** resumen ≤12 líneas; Generalidades (contexto, árbol de problemas, problema seleccionado, limitaciones; objetivo general y específicos SMART, resultados, tabla causa → objetivo → resultado → medio de verificación → IOV); marco conceptual; trabajos relacionados (mínimo 3, con tabla comparativa); metodología KDD; experimentación y resultados; conclusiones; ética; repositorio; contribuciones y declaración de uso de IA; referencias.
- **Se quitó:** formulario de extracción, plan de proyecto y PRISMA completo (no es una tesis).
- **Árbol de problemas:** 2–3 efectos, 1 problema central, 3–5 causas con correspondencia 1 a 1 con los objetivos específicos. Cada causa y efecto con fuente o marcado `HIPOTESIS:`. Los umbrales de IOV se acuerdan con el usuario, no se inventan.
- **Regla de sustento:** cada párrafo de Introducción, Generalidades y Marco lleva al menos una fuente real que lo valide.
- **Pendiente de decidir:** si aplica la excepción Ortegón et al. (2005) para el árbol de problemas.

## 6. Fuentes verificadas hasta ahora (indexación NO confirmada)

| Clave | Referencia | DOI / ID | Aporte |
|---|---|---|---|
| szepannek2024 | Szepannek, Aschenbruck y Wilhelm (2024). Clustering large mixed-type data with ordinal variables. *Advances in Data Analysis and Classification*, 19(3), 749–767. | 10.1007/s11634-024-00595-5 | K-Prototypes con Gower, comparado con Gower+PAM, KAMILA y otros; recomienda varias inicializaciones |
| ghattas2025 | Ghattas y Sanchez San-Benito (2025). Clustering Approaches for Mixed-Type Data: A Comparative Study. arXiv (preprint). | arXiv:2511.19755 | KAMILA, LCM y K-Prototypes mejores por ARI; fallan con interacciones fuertes |
| chicco2025 | Chicco et al. (2025). *PeerJ Computer Science*. | 10.7717/peerj-cs.3309 | Silhouette y Davies-Bouldin como índices internos más fiables (para clústeres convexos con k-means, k=2) |
| heiskala2025 | Heiskala et al. (2025). Timing based clustering of childhood BMI trajectories. *Int J Obes*, 49(5), 872–880. | 10.1038/s41366-025-01714-8 | K-medoids sobre trayectorias de IMC; silhouette ≈ 0,20; k=3 |
| huang2023 | Huang et al. (2023). Defining longitudinal trajectory of BMI percentile… *Precision Nutrition*, 2(2). | 10.1097/PN9.0000000000000037 | K-Means de series temporales con BIC, 4 trayectorias; Boston Birth Cohort |

Notas de alcance: Chicco et al. evaluaron k=2 con k-means y datos de historias clínicas; no generalizar a datos mixtos. No se encontró ninguna fuente IEEE verificable ni estudios de clustering en niños en cuidado residencial. Existen artículos de clustering nutricional infantil de revistas indonesias que no se abrieron ni validaron. Una fuente de PubMed (hybrid AI para clasificación nutricional) no se pudo abrir y no se usa.

## 7. Scripts y entregables preparados (en la computadora de Claude, no en el repo)

- `FORMATO.md` (v2), `scripts/descargar_fuentes.py`, `scripts/verificar_citas.py`, `fuentes/fuentes.csv`.
- `descargar_fuentes.py`: valida metadatos con Crossref, comprueba acceso abierto con Unpaywall (requiere `UNPAYWALL_EMAIL`), descarga solo PDFs de acceso abierto y escribe `fuentes/registro.csv`. **No se pudo probar con las APIs reales** desde el contenedor (red bloqueada); solo se comprobó que compila y que no inventa datos.
- `verificar_citas.py`: avisa de párrafos sin cita, citas sin página, fuera de 2022–2026 o ausentes del registro. Probado con un texto de ejemplo. Está pensado para APA 7.
- Los PDFs de pago no se descargan ni se suben.

## 8. Skills propuestas (el usuario las revisa y las guarda)

1. `fuentes-verificadas-2022-2026`: búsqueda, ficha y verificación de fuentes.
2. `problematica-objetivos-smart`: árbol de problemas y objetivos SMART con tabla causa–objetivo–IOV.
3. `kdd-clustering-nutricion`: ciclo KDD con salida guardada por paso, modelos y validación, privacidad.

Pendiente: ajustar la tercera, que dice "nunca subir datos al repo", porque el usuario decidió mantener los originales publicados.

## 9. Limitaciones del entorno de Claude

- El contenedor no puede instalar paquetes desde PyPI (por ejemplo `imbalanced-learn`); las pruebas de código que lo requieran las ejecuta el usuario.
- No hay acceso a Scopus ni a IEEE Xplore.
- El acceso a la computadora del usuario a veces no está disponible; reintentar y, si no responde, avisar.

## 10. Pendientes abiertos

1. Adaptar `FORMATO.md`, `verificar_citas.py` y la skill de fuentes a citas IEEE numéricas.
2. Decidir la excepción Ortegón et al. (2005).
3. Esperar el contenido del curso que adjuntará el usuario y luego empezar por el paso 1 y el árbol de problemas (evidencia del problema central primero).
4. Ajustar la skill KDD según la decisión sobre los datos.
5. Retomar o no la tarea de `step7b` (semana 10).
6. Si los originales siguen en el repo público, reconsiderar la advertencia de reidentificación.
