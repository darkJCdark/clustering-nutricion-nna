#!/usr/bin/env python3
"""Revisa que cada parrafo de los .md del informe tenga una fuente.

Uso:
    python scripts/verificar_citas.py reports/informe [--registro fuentes/registro.csv]

Avisos que emite:
- Parrafo sin cita (Autor, anio) -> debe llevar fuente o marcarse como HIPOTESIS.
- Cita sin pagina (APA 7 con pagina: p. # / pp. #-#).
- Cita cuyo primer autor/anio no aparece en registro.csv.
- Cita fuera de 2022-2026.
Se omiten: titulos, tablas, bloques de codigo, citas en bloque y parrafos que
empiezan con 'HIPOTESIS:' o 'DECISION:' o contienen <!-- sin-fuente -->.
Termina con codigo 1 si hay avisos. Solo biblioteca estandar.
"""
import argparse, csv, glob, os, re, sys, unicodedata

CITA = re.compile(r"\(([^()]*?(?:19|20)\d{2}[a-z]?[^()]*?)\)|([A-ZÁÉÍÓÚÑ][\w\-ÁÉÍÓÚÑáéíóúñ]+(?: et al\.| y [A-ZÁÉÍÓÚÑ][\w\-ÁÉÍÓÚÑáéíóúñ]+)?) \(((?:19|20)\d{2}[a-z]?[^()]*)\)")
PAG = re.compile(r"\bpp?\.\s*\d+")
EXENTO = re.compile(r"^\s*(HIPOTESIS|HIPÓTESIS|DECISION|DECISIÓN)\s*:|<!--\s*sin-fuente\s*-->", re.I)


def norm(t):
    return unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()


def parrafos(texto):
    en_codigo = False
    buf, ini = [], 0
    for n, lin in enumerate(texto.splitlines(), 1):
        if lin.strip().startswith("```"):
            en_codigo = not en_codigo
            continue
        if en_codigo:
            continue
        if not lin.strip():
            if buf:
                yield ini, " ".join(buf); buf = []
        else:
            if not buf:
                ini = n
            buf.append(lin.strip())
    if buf:
        yield ini, " ".join(buf)


def registro(ruta):
    if not os.path.exists(ruta):
        return None
    with open(ruta, newline="", encoding="utf-8") as f:
        return [(norm(r.get("clave", "")), str(r.get("anio", ""))) for r in csv.DictReader(f)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ruta")
    ap.add_argument("--registro", default="fuentes/registro.csv")
    ap.add_argument("--min-caracteres", type=int, default=60)
    a = ap.parse_args()
    reg = registro(a.registro)
    if reg is None:
        print("AVISO: no existe %s; no se comparan citas con el registro." % a.registro)
    archivos = [a.ruta] if os.path.isfile(a.ruta) else sorted(glob.glob(os.path.join(a.ruta, "**", "*.md"), recursive=True))
    avisos = 0
    for ar in archivos:
        with open(ar, encoding="utf-8") as f:
            texto = f.read()
        for n, p in parrafos(texto):
            if p.startswith(("#", "|", ">", "![", "<!--")) or len(p) < a.min_caracteres or EXENTO.search(p):
                continue
            citas = [m.group(1) or m.group(2) + " (" + m.group(3) + ")" for m in CITA.finditer(p)]
            if not citas:
                print("%s:%d  SIN CITA: %s..." % (ar, n, p[:70])); avisos += 1; continue
            for c in citas:
                if not PAG.search(c):
                    print("%s:%d  SIN PAGINA: %s" % (ar, n, c)); avisos += 1
                ano = re.search(r"(?:19|20)\d{2}", c)
                if ano and not 2022 <= int(ano.group()) <= 2026:
                    print("%s:%d  FUERA DE 2022-2026: %s" % (ar, n, c)); avisos += 1
                if reg is not None and ano:
                    autor = norm(re.split(r"[ ,(]", c.strip("( "))[0])
                    if not any(autor in k and ano.group() == y for k, y in reg):
                        print("%s:%d  NO ESTA EN registro.csv: %s" % (ar, n, c)); avisos += 1
    print("Revision terminada: %d aviso(s) en %d archivo(s)." % (avisos, len(archivos)))
    return 1 if avisos else 0


if __name__ == "__main__":
    sys.exit(main())
