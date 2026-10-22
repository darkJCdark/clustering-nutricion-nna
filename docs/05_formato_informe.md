# Formato del informe

Trabajo de curso (no tesis). Archivo del informe: `reports/informe/` en Markdown, **estilo IEEE a doble columna**. No existe guía de TA específica; este formato combina la estructura de informe de IA Aplicada (1INF62), el esquema de problemática y objetivos del Formato 2025 (FCI-PUCP) y el **KDD de 9 pasos de 1INF03**. Límite de páginas: sin definir (confirmar con la docente).

## Reglas transversales

1. **Citas IEEE numéricas:** [1], [1, p. 3]; la lista de referencias se numera por orden de aparición.
2. **Ventana de fuentes:** 2022–2026, Scopus o IEEE Xplore, sin literatura gris. Excepción aprobada el 2026-10-21: Ortegón et al. (2005) solo para la técnica del árbol de problemas, marcada como excepción.
3. **Regla de sustento:** cada párrafo de Introducción, Generalidades y Marco lleva al menos una fuente real que lo valide. Sin fuente: `HIPOTESIS:` / `DECISION:` o se elimina. Se comprueba con `scripts/verificar_citas.py` (adaptado a IEEE numérico: [n, p. #]).
4. **Alcance exacto:** no atribuir a una fuente algo que no dice; nombrar la población y el contexto del estudio.
5. **Verificación:** cada fuente se abre y se contrasta (cifra, página, población) antes de citarla; estado en `fuentes/registro.md`.
6. **Privacidad:** el informe no contiene datos personales de los NNA.
7. **Figuras:** título debajo, con fuente si no es propia. **Tablas:** título arriba. Todas se explican en el texto.

## Estructura

| Sección | Contenido | Pasos KDD que la alimentan |
|---|---|---|
| Resumen (≤12 líneas) | Contexto, problema, método, resultados y conclusión; sin citas ni siglas | Todos |
| 1. Generalidades | 1.1 Contexto · 1.2 Árbol de problemas (2–3 efectos, 1 problema central, 3–5 causas) · 1.3 Problema seleccionado y alcance · 1.4 Limitaciones · 1.5 Objetivo general y específicos **SMART** (uno por causa) · 1.6 Tabla causa → objetivo → resultado → medio de verificación → IOV | Paso 1 |
| 2. Marco conceptual | Indicadores antropométricos (P/E, T/E, P/T, IMC/E), percentiles y puntaje z (OMS, CDC), clustering con datos mixtos, distancia Gower, validación | Pasos 1, 4, 6 |
| 3. Trabajos relacionados | Mínimo 3 publicaciones con relación al proyecto y tabla comparativa | Paso 6 |
| 4. Metodología | Los 9 pasos KDD aplicados al problema, con notación formal | Pasos 2–7 |
| 5. Experimentación y resultados | Setup (datos, métricas, parámetros, semillas, validación), resultados interpretados | Pasos 7–8 |
| 6. Conclusiones y trabajos futuros | Ligadas a los objetivos | Paso 9 |
| 7. Implicancias éticas | Reidentificación, sesgos, estigmatización, seguridad, autorización | Pasos 1, 2 |
| 8. Repositorio | Enlace y pasos de reproducción | — |
| 9. Declaraciones | Uso de IA (herramienta, propósito, validación; reporte de prompts si se pide) | — |
| Referencias | IEEE | — |

## Árbol de problemas (plantilla; no rellenar sin fuente)

| Nivel | ID | Enunciado | Fuente [n, p.] o `HIPOTESIS:` |
|---|---|---|---|
| Efecto | E1 | … | … |
| Efecto | E2 | … | … |
| **Problema central** | PC | … | … |
| Causa | C1 | … | … |
| Causa | C2 | … | … |
| Causa | C3 | … | … |

Cada causa debe poder resolverse con herramientas informáticas y corresponder 1 a 1 con un objetivo específico. Los umbrales de los IOV se acuerdan con el autor; no se inventan.

## Objetivo general SMART (esquema)

*"[Verbo] mediante [técnica] ... los perfiles nutricionales de [población] a partir de [datos], alcanzando [métrica ≥ umbral], antes de [fecha]."* Específico, Medible, Alcanzable, Relevante, Temporal.

## Lista de verificación antes de entregar

- [ ] Resumen ≤12 líneas, sin citas ni siglas
- [ ] Árbol de problemas con figura; cada causa y efecto con fuente o marcada `HIPOTESIS:`
- [ ] Objetivo general y específicos SMART, con correspondencia 1 a 1 con las causas
- [ ] Cada párrafo de Introducción y Marco con una fuente real
- [ ] Fuentes 2022–2026, verificadas contra el original, citadas con página
- [ ] Mínimo 3 algoritmos comparados y elección justificada (Paso 6–7)
- [ ] Validación con test y estabilidad reportadas (Paso 7)
- [ ] Resultados interpretados en términos del negocio (Pasos 8–9)
- [ ] Sección ética y declaración de uso de IA
- [ ] Sin datos personales en el informe
