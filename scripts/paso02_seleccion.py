#!/usr/bin/env python3
"""Paso 2 KDD: selección y entendimiento de datos.

Entrada : ficha nominal (.txt) y libros de nutrición (.xlsx) en data/raw (o rutas originales).
Salida  : data/interim/02_diccionario.csv, data/interim/02_cobertura.csv, data/interim/02_estadisticos.csv
No imprime filas individuales; solo agregados.
Uso: python scripts/paso02_seleccion.py
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import config, lectura  # noqa: E402

# Uso por variable de la ficha (docs/07): M modelo, V validación, X excluida, K clave
USO = {
    "periodo": ("K", "ordinal", "clave temporal"), "IDs_FichaNominal": ("K", "nominal", "clave de unión"),
    "Sexo": ("M", "nominal", "binaria"), "Fecha de nacimiento": ("K", "fecha", "derivar edad_meses y descartar"),
    "Departamento": ("X", "nominal", "casi constante"), "Provincia": ("X", "nominal", "casi constante"),
    "Distrito": ("X", "nominal", "riesgo de reidentificación"), "Nacionalidad": ("X", "nominal", "constante tras normalizar"),
    "Fecha de ingreso": ("K", "fecha", "derivar meses_permanencia y descartar"),
    "Situación Legal de la (NNA)": ("M", "nominal", "agrupar categorías raras"),
    "Último nivel educativo logrado": ("M", "ordinal", "Ninguno<Inicial<Primaria<Secundaria<Técnico"),
    "La NNA actualmente estudia": ("M", "nominal", "binaria"),
    "Estado de Salud Física Actual": ("M", "nominal", "agrupar categorías raras"),
    "Presenta Discapacidad (Indicar tipo de discapacidad)": ("M", "nominal", "binaria sí/no"),
    "Nivel Nutricional": ("V", "nominal", "solo validación externa"),
    "Soporte Psico-emocional": ("M", "nominal", "normalizar y agrupar"),
    "Atención en Salud mental especializada": ("M", "nominal", "normalizar"),
}


def main():
    config.INTERIM.mkdir(parents=True, exist_ok=True)
    f = lectura.leer_ficha()
    filas = []
    for c in f.columns:
        s = f[c]
        uso, escala, motivo = USO.get(c, ("X", "nominal", "administrativa o casi constante"))
        filas.append(dict(fuente="ficha", variable=c, escala=escala, tipo_python=str(s.dtype), uso=uso,
                          motivo=motivo, vacios_pct=round(s.isna().mean() * 100, 1), n_unicos=int(s.nunique())))
    hojas = lectura.leer_nutricion_cruda()
    vistos = set()
    for h in hojas:
        for j, nombre in enumerate(h["encabezado"]):
            if j < 2 or (h["hoja"], nombre) in vistos:
                continue
            vistos.add((h["hoja"], nombre))
        filas.append(dict(fuente="nutricion", variable=f"[{h['periodo']}] {h['hoja']}", escala="mixta",
                          tipo_python="object", uso="M", motivo="columnas: " + " | ".join(h["encabezado"][2:]),
                          vacios_pct=np.nan, n_unicos=len(h["filas"])))
    pd.DataFrame(filas).to_csv(config.INTERIM / "02_diccionario.csv", index=False, encoding="utf-8")

    # cobertura: filas por periodo y hoja; unión con la ficha de enero 2026
    cob = [dict(periodo=h["periodo"], hoja=h["hoja"], n_nna=len(h["filas"])) for h in hojas]
    cob = pd.DataFrame(cob)
    ids_ene = set()
    for h in hojas:
        if h["periodo"] == "2026_01":
            ids_ene |= set(h["filas"].iloc[:, 1].astype(str).str.strip())
    ids_ficha = set(f.loc[f["periodo"] == "2026_01", "IDs_FichaNominal"])
    resumen = pd.DataFrame([
        dict(periodo="2026_01", hoja="(total libros)", n_nna=len(ids_ene)),
        dict(periodo="2026_01", hoja="(total ficha)", n_nna=len(ids_ficha)),
        dict(periodo="2026_01", hoja="(libros y ficha)", n_nna=len(ids_ene & ids_ficha)),
        dict(periodo="2026_01", hoja="(libros sin ficha ese mes)", n_nna=len(ids_ene - ids_ficha)),
    ])
    pd.concat([cob, resumen]).to_csv(config.INTERIM / "02_cobertura.csv", index=False, encoding="utf-8")

    # estadísticos de la ficha: categóricas (frecuencia agregada) y duplicados
    est = []
    for c in ["Sexo", "Situación Legal de la (NNA)", "Último nivel educativo logrado", "La NNA actualmente estudia",
              "Estado de Salud Física Actual", "Atención en Salud mental especializada"]:
        vc = f[c].astype(str).str.replace(r"\s+", " ", regex=True).str.strip().str.lower().value_counts()
        for k, v in vc.items():
            est.append(dict(variable=c, categoria=k if v >= 5 else 'otras (<5)', n=int(v), pct=round(v / len(f) * 100, 1)))
    e = pd.DataFrame(est).groupby(['variable', 'categoria'], as_index=False).agg(n=('n', 'sum'), pct=('pct', 'sum'))  # celdas <5 agrupadas
    e.to_csv(config.INTERIM / "02_estadisticos.csv", index=False, encoding="utf-8")
    print("duplicados ID+periodo:", int(f.duplicated(["IDs_FichaNominal", "periodo"]).sum()))
    print(resumen.to_string(index=False))
    print("hojas leídas:", len(hojas), "| variables en diccionario:", len(filas))


if __name__ == "__main__":
    main()
