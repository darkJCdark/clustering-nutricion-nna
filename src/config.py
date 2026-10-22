"""Configuración común del proyecto (rutas y semilla)."""
from pathlib import Path

SEED = 42
RAIZ = Path(__file__).resolve().parents[1]
RAW_FICHA = RAIZ / "data" / "raw" / "ficha_nominal"
RAW_NUTRICION = RAIZ / "data" / "raw" / "nutricion_mensual"
INTERIM = RAIZ / "data" / "interim"
PROCESSED = RAIZ / "data" / "processed"

# Rutas originales (antes de ejecutar scripts/reordenar_repo.ps1)
_B1 = "Datos TA - Bloque 1 (Columnas FECHA Actualizadas) FichaNominal_consolidado_IDs.xlsx-20261021"
_B2 = "Datos TA - Bloque 2  Nutricion_IDs_2026.xlsx-20261021"
ORIG_FICHA = RAIZ / _B1
ORIG_NUTRICION = RAIZ / _B2


def carpeta_ficha():
    """Devuelve la carpeta con la ficha: la nueva si existe, si no la original."""
    return RAW_FICHA if any(RAW_FICHA.glob("*.txt")) else ORIG_FICHA


def carpeta_nutricion():
    return RAW_NUTRICION if any(RAW_NUTRICION.glob("*.xlsx")) else ORIG_NUTRICION
