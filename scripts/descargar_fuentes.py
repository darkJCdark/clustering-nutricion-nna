#!/usr/bin/env python3
"""Verifica metadatos y descarga SOLO fuentes de acceso abierto.

Uso (desde la raiz del repo):
    set UNPAYWALL_EMAIL=tu_correo@dominio     (Windows)  /  export UNPAYWALL_EMAIL=...
    python scripts/descargar_fuentes.py [--entrada fuentes/fuentes.csv] [--salida fuentes]

Entrada: fuentes/fuentes.csv con columnas clave,doi,arxiv,nota.
Salida : fuentes/pdf/<clave>.pdf (solo acceso abierto) y fuentes/registro.csv.

Reglas:
- Crossref confirma titulo, anio y revista del DOI (no se acepta lo que no resuelva).
- Unpaywall (requiere UNPAYWALL_EMAIL) indica si hay PDF legal de acceso abierto.
- Si la fuente es de pago, NO se descarga: se deja el enlace para bajarla con la
  biblioteca PUCP. No se redistribuyen PDFs de pago.
- La indexacion (Scopus/IEEE) NO se puede confirmar por API abierta: queda
  'no confirmada' hasta que un integrante la verifique y la edite en el registro.
Solo biblioteca estandar de Python.
"""
import argparse, csv, hashlib, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import date

UA = "clustering-nutricion-nna/1.0 (trabajo academico PUCP)"
CAMPOS = ["clave", "doi", "arxiv", "titulo", "anio", "revista", "en_ventana_2022_2026",
          "acceso", "licencia", "url_origen", "archivo", "sha256", "fecha_consulta",
          "indexacion", "estado_verificacion", "observaciones"]
MANUALES = ("indexacion", "estado_verificacion", "observaciones")


def get(url, binario=False, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        datos = r.read()
    return datos if binario else json.loads(datos.decode("utf-8"))


def crossref(doi):
    d = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
    titulo = (d.get("title") or [""])[0]
    revista = (d.get("container-title") or [""])[0]
    partes = (d.get("issued", {}).get("date-parts") or [[None]])[0]
    return titulo, (partes[0] if partes else None), revista


def unpaywall(doi, email):
    d = get("https://api.unpaywall.org/v2/%s?email=%s" % (urllib.parse.quote(doi), urllib.parse.quote(email)))
    loc = d.get("best_oa_location") or {}
    return bool(d.get("is_oa")), loc.get("url_for_pdf"), loc.get("license") or ""


def arxiv_meta(aid):
    import xml.etree.ElementTree as ET
    xml = get("https://export.arxiv.org/api/query?id_list=" + aid, binario=True)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    e = ET.fromstring(xml).find("a:entry", ns)
    titulo = re.sub(r"\s+", " ", e.find("a:title", ns).text or "").strip()
    anio = int((e.find("a:published", ns).text or "0")[:4])
    return titulo, anio


def descargar_pdf(url, destino):
    datos = get(url, binario=True, timeout=90)
    if not datos.startswith(b"%PDF"):
        raise ValueError("la respuesta no es un PDF")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "wb") as f:
        f.write(datos)
    return hashlib.sha256(datos).hexdigest()


def leer_csv(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", default="fuentes/fuentes.csv")
    ap.add_argument("--salida", default="fuentes")
    a = ap.parse_args()
    email = os.environ.get("UNPAYWALL_EMAIL", "").strip()
    if not email:
        print("AVISO: sin UNPAYWALL_EMAIL no se consulta Unpaywall; solo se verifican metadatos y arXiv.")

    ruta_reg = os.path.join(a.salida, "registro.csv")
    previo = {r["clave"]: r for r in leer_csv(ruta_reg)}
    filas = []
    for src in leer_csv(a.entrada):
        clave, doi, aid = src["clave"].strip(), (src.get("doi") or "").strip(), (src.get("arxiv") or "").strip()
        fila = {c: "" for c in CAMPOS}
        fila.update(clave=clave, doi=doi, arxiv=aid, fecha_consulta=date.today().isoformat(),
                    indexacion="no confirmada", estado_verificacion="pendiente", acceso="cerrado/desconocido")
        for k in MANUALES:                      # conserva lo editado a mano
            if clave in previo and previo[clave].get(k):
                fila[k] = previo[clave][k]
        obs = []
        try:
            if doi:
                fila["titulo"], fila["anio"], fila["revista"] = crossref(doi)
                fila["url_origen"] = "https://doi.org/" + doi
            elif aid:
                fila["titulo"], fila["anio"] = arxiv_meta(aid)
                fila["revista"] = "arXiv (preprint)"
                fila["url_origen"] = "https://arxiv.org/abs/" + aid
            else:
                obs.append("sin doi ni arxiv")
        except Exception as e:                  # no se inventan metadatos
            obs.append("metadatos NO verificados: %s" % e)
        try:
            fila["en_ventana_2022_2026"] = "si" if 2022 <= int(fila["anio"]) <= 2026 else "NO"
        except (TypeError, ValueError):
            fila["en_ventana_2022_2026"] = "desconocido"

        pdf_url, lic = "", ""
        try:
            if aid and not doi:
                pdf_url, fila["acceso"] = "https://arxiv.org/pdf/" + aid, "arxiv"
                lic = "revisar licencia en la pagina del preprint"
            elif doi and email:
                es_oa, pdf_url, lic = unpaywall(doi, email)
                fila["acceso"] = "abierto" if es_oa else "cerrado"
        except Exception as e:
            obs.append("Unpaywall fallo: %s" % e)
        fila["licencia"] = lic
        if pdf_url:
            destino = os.path.join(a.salida, "pdf", clave + ".pdf")
            try:
                fila["sha256"] = descargar_pdf(pdf_url, destino)
                fila["archivo"] = destino.replace(os.sep, "/")
            except Exception as e:
                obs.append("descarga fallo: %s" % e)
        elif fila["acceso"].startswith("cerrado"):
            obs.append("descargar a mano con la biblioteca PUCP: " + fila["url_origen"])
        if obs:
            fila["observaciones"] = (fila["observaciones"] + " | " if fila["observaciones"] else "") + "; ".join(obs)
        filas.append(fila)
        print("[%s] %s | %s | %s" % (clave, fila["acceso"], fila["en_ventana_2022_2026"], fila["titulo"][:70]))
        time.sleep(1)

    os.makedirs(a.salida, exist_ok=True)
    with open(ruta_reg, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader(); w.writerows(filas)
    print("Registro escrito en", ruta_reg)


if __name__ == "__main__":
    sys.exit(main())
