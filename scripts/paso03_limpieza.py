#!/usr/bin/env python3
"""Paso 3 KDD: limpieza y pre-procesamiento.

Entrada : ficha nominal y libros de nutrición (data/raw o rutas originales); data/interim/02_diccionario.csv
Salida  : data/interim/03_limpio.csv (una fila por NNA y medición),
          data/interim/03_log_limpieza.csv, data/interim/03_atipicos.csv
No imprime filas individuales. Uso: python scripts/paso03_limpieza.py
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import config, lectura, limpieza as L  # noqa: E402

LOG = []


def log(regla, n, detalle=""):
    LOG.append(dict(regla=regla, filas_afectadas=int(n), detalle=detalle))


# ---------- ficha ----------
def limpiar_ficha(f: pd.DataFrame) -> pd.DataFrame:
    n0 = len(f)
    f = f.copy()
    f["_vacios"] = f.isna().sum(axis=1)
    f = f.sort_values(["IDs_FichaNominal", "periodo", "_vacios"]).drop_duplicates(["IDs_FichaNominal", "periodo"], keep="first")
    log("ficha: duplicados ID+periodo (se conserva la fila con menos vacíos)", n0 - len(f))
    out = pd.DataFrame({"id": f["IDs_FichaNominal"], "periodo_ficha": f["periodo"]})
    out["sexo"] = f["Sexo"].map(L.norm_cat).replace({"m": "M", "f": "F"})
    out["fecha_nac_ficha"] = f["Fecha de nacimiento"].map(L.parsear_fecha)
    log("ficha: fecha de nacimiento no interpretable", out["fecha_nac_ficha"].isna().sum())
    out["fecha_ingreso"] = f["Fecha de ingreso"].map(L.parsear_fecha)
    log("ficha: fecha de ingreso no interpretable", out["fecha_ingreso"].isna().sum())

    sl = f["Situación Legal de la (NNA)"].map(L.norm_cat)
    out["situacion_legal"] = np.select(
        [sl.str.startswith("desproteccion familiar provis"), sl.str.startswith("desproteccion familiar definit"),
         sl.str.startswith("acogimiento residencial")], ["provisional", "definitiva", "acogimiento"], default="otra")
    ed = f["Último nivel educativo logrado"].map(L.norm_cat)
    mapa_ed = {"ninguno": 0, "inicial": 1, "primaria": 2, "secundaria": 3, "tecnico": 4}
    out["nivel_educativo"] = ed.map(mapa_ed)
    log("ficha: nivel educativo sin mapa", out["nivel_educativo"].isna().sum())
    out["estudia"] = f["La NNA actualmente estudia"].map(L.norm_cat).map({"si": 1, "no": 0})
    sal = f["Estado de Salud Física Actual"].map(L.norm_cat)
    out["salud_fisica"] = np.select([sal == "saludable", sal == "anemia"], ["saludable", "anemia"], default="otra")
    dis = f["Presenta Discapacidad (Indicar tipo de discapacidad)"].map(L.norm_cat)
    out["discapacidad"] = np.where(dis.isin(["", "no tiene"]), 0, 1)
    sop = f["Soporte Psico-emocional"].map(L.norm_cat)
    out["soporte_psico"] = np.select(
        [sop.str.startswith("no"), sop.str.contains("psicoterapia"), sop.str.contains("estimul"), sop.str.contains("acompa")],
        ["sin_soporte", "psicoterapia", "estimulacion", "acompanamiento"], default="otro")
    sm = f["Atención en Salud mental especializada"].map(L.norm_cat)
    out["salud_mental_esp"] = np.select([sm.str.startswith("si"), sm.str.startswith("no aplic"), sm == "no"],
                                        ["si", "no_aplica", "no"], default="desconocido")
    out["nivel_nutricional_ficha"] = f["Nivel Nutricional"].map(L.norm_cat)  # solo validación
    for c in ["estudia"]:
        log(f"ficha: {c} vacío -> se deja vacío (moda no aplicada)", out[c].isna().sum())
    return out


# ---------- nutrición ----------
def limpiar_nutricion(hojas) -> pd.DataFrame:
    filas = []
    for h in hojas:
        pos = L.mapear_columnas(h["encabezado"])
        d = h["filas"]
        reg = pd.DataFrame({"id": d.iloc[:, 1].map(lambda v: str(v).strip())})
        reg["periodo"] = h["periodo"]
        reg["hogar"] = h["hoja"].upper()
        reg["fecha_nac_nut_raw"] = d.iloc[:, pos["fecha_nac"]].values
        reg["peso_kg"] = pd.to_numeric(d.iloc[:, pos["peso_kg"]], errors="coerce").values
        reg["talla_cm"] = pd.to_numeric(d.iloc[:, pos["talla_cm"]], errors="coerce").values
        for k, j in pos.items():
            if k.startswith("dx_"):
                reg[k] = d.iloc[:, j].map(L.dx_texto).values
        filas.append(reg)
    n = pd.concat(filas, ignore_index=True)
    n["fecha_nac_nut"] = n["fecha_nac_nut_raw"].map(L.parsear_fecha)
    log("nutrición: fecha de nacimiento no interpretable", n["fecha_nac_nut"].isna().sum())
    n = n.drop(columns="fecha_nac_nut_raw")
    n0 = len(n)
    n["_v"] = n.isna().sum(axis=1)
    n = n.sort_values(["id", "periodo", "_v"]).drop_duplicates(["id", "periodo"], keep="first").drop(columns="_v")
    log("nutrición: duplicados ID+periodo", n0 - len(n))
    return n


def unir(n: pd.DataFrame, f: pd.DataFrame) -> pd.DataFrame:
    """Une cada medición con la fila de ficha del mismo periodo; si falta, la más cercana del mismo NNA."""
    f = f.copy()
    f["_pf"] = f["periodo_ficha"].map(L.periodo_a_fecha)
    n = n.copy()
    n["_pn"] = n["periodo"].map(L.periodo_a_fecha)
    res = []
    for i, r in n.iterrows():
        g = f[f["id"] == r["id"]]
        if g.empty:
            res.append((i, None, "sin_ficha"))
            continue
        dif = (g["_pf"] - r["_pn"]).abs()
        j = dif.idxmin()
        res.append((i, j, "mismo_periodo" if dif[j].days == 0 else "periodo_cercano"))
    m = pd.DataFrame(res, columns=["i", "j", "union"]).set_index("i")
    out = n.join(m)
    base = f.drop(columns="_pf")
    out = out.merge(base, left_on="j", right_index=True, how="left", suffixes=("", "_f"))
    out = out.rename(columns={"id_f": "id_ficha"})
    log("unión: mediciones con ficha de otro periodo", (out["union"] == "periodo_cercano").sum())
    log("unión: mediciones sin ficha", (out["union"] == "sin_ficha").sum())
    return out.drop(columns=["j", "_pn"])


def derivar(m: pd.DataFrame) -> pd.DataFrame:
    m = m.copy()
    fn = m["fecha_nac_nut"].fillna(m["fecha_nac_ficha"])
    log("edad: fecha de nacimiento tomada de la ficha", (m["fecha_nac_nut"].isna() & m["fecha_nac_ficha"].notna()).sum())
    disc = (m["fecha_nac_nut"].notna() & m["fecha_nac_ficha"].notna() &
            ((m["fecha_nac_nut"] - m["fecha_nac_ficha"]).abs() > pd.Timedelta(days=31)))
    log("edad: fechas de nacimiento de nutrición y ficha discrepan >31 días", disc.sum(), "se usa la de nutrición")
    fm = m["periodo"].map(L.periodo_a_fecha)
    m["edad_meses"] = [L.meses_entre(a, b) for a, b in zip(fn, fm)]
    m["meses_permanencia"] = [L.meses_entre(a, b) for a, b in zip(m["fecha_ingreso"], fm)]
    m["imc"] = m["peso_kg"] / (m["talla_cm"] / 100) ** 2
    m["tramo"] = np.where(m["edad_meses"] < 60, "menor_5", np.where(m["edad_meses"] < 228, "5_19", "mayor_19"))
    m["sin_medida"] = m["peso_kg"].isna() | m["talla_cm"].isna() | m["edad_meses"].isna()
    log("exclusión: sin peso, talla o edad", m["sin_medida"].sum(), "no se imputa la medida base")
    m["plausible"] = m["peso_kg"].between(5, 150) & m["talla_cm"].between(40, 200)
    log("plausibilidad: peso o talla fuera de 5–150 kg / 40–200 cm", (~m["plausible"] & ~m["sin_medida"]).sum(), "solo bandera")
    return m.drop(columns=["fecha_nac_nut", "fecha_nac_ficha", "fecha_ingreso"])


def atipicos(m: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for tramo, g in m[~m["sin_medida"]].groupby("tramo"):
        for c in ["peso_kg", "talla_cm", "imc", "edad_meses"]:
            s = g[c].dropna()
            q1, q3 = s.quantile([.25, .75])
            iqr = q3 - q1
            lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            filas.append(dict(tramo=tramo, variable=c, n=len(s), media=round(s.mean(), 2), mediana=round(s.median(), 2),
                              desv=round(s.std(), 2), asimetria=round(s.skew(), 2), curtosis=round(s.kurt(), 2),
                              lim_inf_iqr=round(lo, 2), lim_sup_iqr=round(hi, 2), atipicos_iqr=int(((s < lo) | (s > hi)).sum()),
                              atipicos_z3=int((((s - s.mean()) / s.std()).abs() > 3).sum())))
    return pd.DataFrame(filas)


def main():
    config.INTERIM.mkdir(parents=True, exist_ok=True)
    f = limpiar_ficha(lectura.leer_ficha())
    n = limpiar_nutricion(lectura.leer_nutricion_cruda())
    m = derivar(unir(n, f))
    cat = ["situacion_legal", "salud_fisica", "soporte_psico", "salud_mental_esp", "sexo"]
    for c in cat:
        v = m[c].isna().sum()
        m[c] = m[c].fillna("desconocido")
        log(f"categórica {c}: vacío -> 'desconocido'", v)
    # concordancia IMC reportado vs recalculado no disponible de forma uniforme: se registra solo imc recalculado
    cols = ["id", "periodo", "hogar", "tramo", "sin_medida", "plausible", "edad_meses", "peso_kg", "talla_cm", "imc",
            "meses_permanencia", "sexo", "situacion_legal", "nivel_educativo", "estudia", "salud_fisica", "discapacidad",
            "soporte_psico", "salud_mental_esp", "nivel_nutricional_ficha", "union"] + sorted(c for c in m.columns if c.startswith("dx_"))
    m[cols].to_csv(config.INTERIM / "03_limpio.csv", index=False, encoding="utf-8")
    atipicos(m).to_csv(config.INTERIM / "03_atipicos.csv", index=False, encoding="utf-8")
    pd.DataFrame(LOG).to_csv(config.INTERIM / "03_log_limpieza.csv", index=False, encoding="utf-8")
    ok = m[~m["sin_medida"]]
    print("mediciones:", len(m), "| con medida válida:", len(ok), "| NNA:", m["id"].nunique())
    print(m.groupby(["periodo", "tramo"]).size().unstack(fill_value=0).to_string())
    print(pd.DataFrame(LOG).to_string(index=False))
    print("vacíos en columnas del modelo (% sobre medidas válidas):")
    print((ok[["edad_meses", "peso_kg", "talla_cm", "imc", "meses_permanencia", "sexo", "situacion_legal", "nivel_educativo",
               "estudia", "salud_fisica", "discapacidad", "soporte_psico", "salud_mental_esp"]].isna().mean() * 100).round(1).to_string())


if __name__ == "__main__":
    main()
