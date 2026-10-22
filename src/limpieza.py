"""Funciones de limpieza del Paso 3 (ficha nominal y libros de nutrición)."""
import re
import unicodedata
import numpy as np
import pandas as pd

DX_BASE = {"P/E": "pe", "T/E": "te", "P/T": "pt", "IMC/E": "imce", "IMC": "imce"}


def _txt(v) -> str:
    return re.sub(r"\s+", " ", str(v)).strip() if isinstance(v, str) else ""


def sin_tildes(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def norm_cat(v) -> str:
    """minúsculas, sin tildes ni saltos de línea; vacío -> ''."""
    return sin_tildes(_txt(v)).lower()


def parsear_fecha(v):
    """Acepta datetime, dd/mm/aaaa (con espacios), aaaa-mm-dd; devuelve Timestamp o NaT."""
    if isinstance(v, (pd.Timestamp, np.datetime64)):
        return pd.Timestamp(v)
    if hasattr(v, "year") and hasattr(v, "month"):
        return pd.Timestamp(v)
    if isinstance(v, str):
        s = v.strip()
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y", "%Y-%m-%d %H:%M:%S"):
            try:
                return pd.to_datetime(s, format=fmt)
            except (ValueError, TypeError):
                continue
    return pd.NaT


def periodo_a_fecha(p: str) -> pd.Timestamp:
    """'2026_01' -> 15 de enero de 2026 (día 15 como fecha de medición asumida)."""
    a, m = p.split("_")
    return pd.Timestamp(int(a), int(m), 15)


def meses_entre(f0, f1):
    if pd.isna(f0) or pd.isna(f1):
        return np.nan
    return (f1 - f0).days / 30.4375


def dx_texto(v):
    """Diagnóstico manual en texto limpio; '*' -> NaN (no aplica)."""
    s = _txt(v).upper()
    if s in ("", "*", "NAN"):
        return np.nan
    for a, b in (("NORNAL", "NORMAL"), ("RIESGO DE ", "RIESGO "), ("SOBRE PESO", "SOBREPESO"), ("BAJO DE PESO", "BAJO PESO"),
                 ("OBEESIDAD", "OBESIDAD"), ("RIEGO", "RIESGO"), ("RIESO ", "RIESGO "), (" TALA ", " TALLA ")):
        s = s.replace(a, b)
    if s == "ALTA":
        s = "ALTO"
    return s


def mapear_columnas(encabezado: list[str]) -> dict:
    """Devuelve {nombre_estandar: posicion} a partir del encabezado de una hoja.

    Reglas: fecha/edad/peso/talla por texto; 'IMC' numérico = primer IMC antes de cualquier
    diagnóstico; P/E, T/E, P/T, IMC/E: primera aparición = bloque A (percentil/z OMS),
    segunda = bloque B (tabla de diagnóstico rápido).
    """
    pos = {}
    visto = {}
    primer_dx = None
    for j, h in enumerate(encabezado):
        u = h.upper()
        if j == 1:
            pos["id"] = j
        elif u.startswith("FECHA") and "fecha_nac" not in pos:
            pos["fecha_nac"] = j
        elif u == "EDAD":
            pos["edad_txt"] = j
        elif u.startswith("PESO"):
            pos["peso_kg"] = j
        elif u.startswith("TALLA"):
            pos["talla_cm"] = j
        elif u in ("P/E", "T/E", "P/T", "IMC/E", "IMC"):
            if u == "IMC" and primer_dx is None:
                pos["imc_rep"] = j
                continue
            if primer_dx is None:
                primer_dx = j
            base = DX_BASE[u]
            visto[base] = visto.get(base, 0) + 1
            bloque = "a" if visto[base] == 1 else "b"
            pos[f"dx_{bloque}_{base}"] = j
    return pos
