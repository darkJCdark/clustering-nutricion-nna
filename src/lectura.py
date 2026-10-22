"""Lectura de la ficha nominal y de los libros mensuales de nutrición."""
import re
import warnings
import pandas as pd
from . import config

ID_RE = re.compile(r"^[A-Za-z]{3}_[A-Za-z]{2}_\d{4}$")
MESES = {"ENERO": 1, "FEBRERO": 2, "MARZO": 3, "ABRIL": 4, "MAYO": 5, "JUNIO": 6,
         "JULIO": 7, "AGOSTO": 8, "SETIEMBRE": 9, "SEPTIEMBRE": 9, "OCTUBRE": 10}


def leer_ficha() -> pd.DataFrame:
    ruta = sorted(config.carpeta_ficha().glob("*.txt"))[0]
    return pd.read_csv(ruta, sep="|", encoding="utf-8", low_memory=False)


def _periodo_de_archivo(nombre: str) -> str:
    m = re.search(r"IDs_(\d{4})(\d{2})", nombre)
    return f"{m.group(1)}_{m.group(2)}"


def leer_nutricion_cruda() -> list[dict]:
    """Devuelve una lista de hojas: periodo, hogar, encabezados (texto) y filas con ID válido.

    No unifica columnas (eso es el Paso 3); solo localiza la fila de encabezado
    (la que está justo después de la fila 'DATOS') y las filas cuyo ID tiene formato válido.
    """
    hojas = []
    warnings.filterwarnings("ignore")
    for f in sorted(config.carpeta_nutricion().glob("*.xlsx")):
        per = _periodo_de_archivo(f.name)
        xl = pd.ExcelFile(f)
        for sn in xl.sheet_names:
            t = xl.parse(sn, header=None)
            col1 = t.iloc[:, 1].map(lambda v: str(v).strip() if isinstance(v, str) else "")
            filas = t[col1.map(lambda x: bool(ID_RE.match(x)))].copy()
            if filas.empty:
                continue
            # encabezado: última fila antes de la primera fila de datos que contenga 'PESO'
            primera = filas.index[0]
            enc_idx = [i for i in range(primera) if any("PESO" in str(v).upper() for v in t.iloc[i])]
            enc = [re.sub(r"\s+", " ", str(v)).strip() for v in t.iloc[enc_idx[-1]]] if enc_idx else []
            hojas.append({"periodo": per, "archivo": f.name, "hoja": sn.strip(),
                          "encabezado": enc, "filas": filas})
    return hojas
