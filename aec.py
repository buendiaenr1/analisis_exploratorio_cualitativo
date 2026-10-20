# -*- coding: utf-8 -*-
# VERSION: v2.2 - Multi-PDF con expansion de wildcards (Windows/PowerShell)
"""
Analisis Exploratorio Cualitativo de PDF (v2.2)
================================================
Uso:
  python aec.py                    -> todos los PDFs de la carpeta actual
  python aec.py *.pdf              -> todos los PDFs de la carpeta actual
  python aec.py carpeta/           -> todos los PDFs dentro de una carpeta
  python aec.py a.pdf b.pdf        -> varios PDFs especificos
  python aec.py dosel.pdf          -> un solo PDF
"""

import sys
import io
import re
import glob
from pathlib import Path
from collections import Counter

# Forzar UTF-8 en consola Windows (evita UnicodeEncodeError)
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
except Exception:
    pass

import pymupdf as fitz
import spacy
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from textblob import TextBlob
from spacy.lang.es.stop_words import STOP_WORDS as STOP_ES


# =========================================================
# CACHE DE MODELOS (se cargan UNA sola vez)
# =========================================================
_NLP = None
_ANALYZER = None
_ANALYZER_TRIED = False


def get_nlp():
    global _NLP
    if _NLP is None:
        print("[i] Cargando spaCy (una sola vez)...")
        _NLP = spacy.load("es_core_news_sm")
    return _NLP


def get_analyzer():
    global _ANALYZER, _ANALYZER_TRIED
    if not _ANALYZER_TRIED:
        _ANALYZER_TRIED = True
        try:
            from pysentimiento import create_analyzer
            print("[i] Cargando pysentimiento (una sola vez)...")
            _ANALYZER = create_analyzer(task="sentiment", lang="es")
        except Exception as e:
            print(f"[!] pysentimiento no disponible ({type(e).__name__}). Fallback a TextBlob.")
            _ANALYZER = None
    return _ANALYZER


# =========================================================
# EXTRACCION Y ESTADISTICAS
# =========================================================
def extraer_texto(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(p.get_text() for p in doc), len(doc)


def estadisticas_basicas(texto, n_paginas):
    palabras = re.findall(r"\b\w+\b", texto.lower())
    oraciones = [o for o in re.split(r"[.!?]+", texto) if o.strip()]
    return {
        "num_paginas": n_paginas,
        "num_caracteres": len(texto),
        "num_palabras": len(palabras),
        "num_oraciones": len(oraciones),
        "palabras_por_oracion_prom": round(len(palabras) / max(len(oraciones), 1), 2),
        "vocabulario_unico": len(set(palabras)),
    }


# =========================================================
# LIMPIEZA Y TOKENIZACION
# =========================================================
def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"\S+@\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúñü\s]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def limpiar_parrafo(p):
    p = p.lower()
    p = re.sub(r"http\S+|www\S+", "", p)
    p = re.sub(r"\S+@\S+", "", p)
    p = re.sub(r"[^a-záéíóúñü\s]", " ", p)
    return re.sub(r"\s+", " ", p).strip()


def tokenizar(texto_limpio):
    return [t for t in texto_limpio.split() if len(t) > 2 and t not in STOP_ES]


def dividir_documentos(texto, min_len=80):
    """Divide en unidades para LDA: parrafos -> lineas -> ventanas de ~80 palabras."""
    docs = [p.strip() for p in re.split(r"\n\s*\n", texto) if len(p.strip()) >= min_len]
    if len(docs) >= 5:
        return docs
    docs = [p.strip() for p in re.split(r"\n", texto) if len(p.strip()) >= min_len]
    if len(docs) >= 5:
        return docs
    oraciones = [s.strip() for s in re.split(r"[.!?]+", texto) if len(s.strip()) > 20]
    ventanas, buf = [], ""
    for o in oraciones:
        buf += " " + o
        if len(buf.split()) >= 80:
            ventanas.append(buf.strip())
            buf = ""
    if buf.strip():
        ventanas.append(buf.strip())
    return ventanas


# =========================================================
# FRECUENCIAS Y NUBE
# =========================================================
def frecuencias(tokens, n=20):
    f_pal = pd.DataFrame(Counter(tokens).most_common(n), columns=["palabra", "frecuencia"])
    bigramas = list(zip(tokens, tokens[1:]))
    f_big = pd.DataFrame(
        [(" ".join(k), v) for k, v in Counter(bigramas).most_common(n)],
        columns=["bigrama", "frecuencia"],
    )
    return f_pal, f_big


def generar_nube(tokens, salida):
    wc = WordCloud(
        width=1200, height=600, background_color="white",
        colormap="viridis", max_words=150,
    ).generate(" ".join(tokens))
    plt.figure(figsize=(14, 7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nube de palabras", fontsize=16)
    plt.tight_layout()
    plt.savefig(salida, dpi=150)
    plt.close()


# =========================================================
# NER (ENTIDADES)
# =========================================================
def extraer_entidades(texto):
    nlp = get_nlp()
    doc = nlp(texto[:1_000_000])
    ents = [
        (e.text.strip(), e.label_)
        for e in doc.ents
        if len(e.text.strip()) >= 2 and re.search(r"[A-Za-zÁÉÍÓÚÑÜáéíóúñü]", e.text)
    ]
    if not ents:
        return pd.DataFrame(columns=["entidad", "tipo", "frecuencia"])
    return (
        pd.DataFrame(ents, columns=["entidad", "tipo"])
        .value_counts()
        .reset_index(name="frecuencia")
        .head(30)
    )


# =========================================================
# MODELADO DE TOPICOS (LDA)
# =========================================================
def modelar_topicos(texto, n_topicos=5, n_palabras=8):
    docs = [limpiar_parrafo(d) for d in dividir_documentos(texto, min_len=80)]
    docs = [d for d in docs if len(d.split()) >= 5]
    if len(docs) < 2:
        return {}
    n_topicos = min(n_topicos, max(2, len(docs) // 2))
    max_df = 0.95 if len(docs) >= 20 else 1.0
    vec = CountVectorizer(
        max_df=max_df,
        min_df=1,
        stop_words=list(STOP_ES),
        token_pattern=r"(?u)\b[a-záéíóúñü]{3,}\b",
    )
    try:
        X = vec.fit_transform(docs)
    except ValueError:
        return {}
    if X.shape[1] == 0:
        return {}
    n_topicos = min(n_topicos, X.shape[1])
    lda = LatentDirichletAllocation(
        n_components=n_topicos, random_state=42, max_iter=20
    )
    lda.fit(X)
    vocab = vec.get_feature_names_out()
    return {
        f"Topico {i+1}": [vocab[j] for j in lda.components_[i].argsort()[-n_palabras:][::-1]]
        for i in range(n_topicos)
    }


# =========================================================
# SENTIMIENTO
# =========================================================
def analizar_sentimiento_oraciones(texto):
    analyzer = get_analyzer()
    oraciones = [o.strip() for o in re.split(r"[.!?]+", texto) if len(o.strip()) > 20]
    regs = []
    for o in oraciones:
        if analyzer is not None:
            try:
                res = analyzer.predict(o)
                et = {"POS": "positivo", "NEG": "negativo", "NEU": "neutro"}[res.output]
                regs.append(
                    {"oracion": o[:150], "sentimiento": et,
                     "prob": round(max(res.probas.values()), 3)}
                )
            except Exception:
                regs.append({"oracion": o[:150], "sentimiento": "error", "prob": None})
        else:
            pol = TextBlob(o).sentiment.polarity
            et = "positivo" if pol > 0.1 else ("negativo" if pol < -0.1 else "neutro")
            regs.append(
                {"oracion": o[:150], "polaridad": round(pol, 3), "sentimiento": et}
            )
    return pd.DataFrame(regs)


# =========================================================
# PIPELINE POR PDF
# =========================================================
def analizar_pdf(pdf_path, salida_dir):
    Path(salida_dir).mkdir(parents=True, exist_ok=True)
    texto, n_pag = extraer_texto(pdf_path)
    if not texto.strip():
        print("   [SKIP] sin texto seleccionable")
        return None

    stats = estadisticas_basicas(texto, n_pag)
    tokens = tokenizar(limpiar_texto(texto))

    f_pal, f_big = frecuencias(tokens, 20)
    f_pal.to_csv(f"{salida_dir}/frecuencia_palabras.csv", index=False)
    f_big.to_csv(f"{salida_dir}/frecuencia_bigramas.csv", index=False)

    generar_nube(tokens, f"{salida_dir}/nube_palabras.png")

    df_sent = analizar_sentimiento_oraciones(texto)
    df_sent.to_csv(f"{salida_dir}/sentimiento.csv", index=False)

    df_ent = extraer_entidades(texto)
    df_ent.to_csv(f"{salida_dir}/entidades.csv", index=False)

    topicos = modelar_topicos(texto, 5)

    with open(f"{salida_dir}/texto_extraido.txt", "w", encoding="utf-8") as f:
        f.write(texto)

    return {
        "archivo": Path(pdf_path).name,
        "paginas": n_pag,
        "palabras": stats["num_palabras"],
        "oraciones": stats["num_oraciones"],
        "top_palabra": f_pal.iloc[0]["palabra"] if len(f_pal) else "-",
        "sent_pos": int((df_sent["sentimiento"] == "positivo").sum()) if len(df_sent) else 0,
        "sent_neg": int((df_sent["sentimiento"] == "negativo").sum()) if len(df_sent) else 0,
        "sent_neu": int((df_sent["sentimiento"] == "neutro").sum()) if len(df_sent) else 0,
        "n_entidades": len(df_ent),
        "n_topicos": len(topicos),
    }


# =========================================================
# EXPANSION DE WILDCARDS (para PowerShell)
# =========================================================
def expandir_entradas(args):
    rutas = []
    for arg in args:
        p = Path(arg)
        # 1) carpeta -> todos sus .pdf
        if p.is_dir():
            rutas.extend(sorted(str(f) for f in p.glob("*.pdf")))
            continue
        # 2) contiene wildcard -> glob
        if any(c in arg for c in "*?["):
            coincidencias = sorted(glob.glob(arg))
            if not coincidencias:
                coincidencias = sorted(glob.glob(arg, recursive=True))
            if not coincidencias:
                print(f"[!] Sin coincidencias para: {arg}")
            rutas.extend(coincidencias)
            continue
        # 3) archivo explicito
        if p.exists():
            rutas.append(str(p))
        else:
            print(f"[!] No existe: {arg}")
    # deduplicar
    vistos, unicos = set(), []
    for r in rutas:
        ra = str(Path(r).resolve())
        if ra not in vistos:
            vistos.add(ra)
            unicos.append(r)
    return unicos


# =========================================================
# LOTE
# =========================================================
def analizar_lote(pdfs, salida_base="resultados"):
    Path(salida_base).mkdir(exist_ok=True)
    resumen = []
    for i, pdf in enumerate(pdfs, 1):
        print(f"\n{'=' * 60}\n[{i}/{len(pdfs)}] {pdf}\n{'=' * 60}")
        try:
            info = analizar_pdf(pdf, f"{salida_base}/{Path(pdf).stem}")
            if info:
                resumen.append(info)
                print(f"   [OK] {info['paginas']} pag, {info['palabras']} palabras")
        except Exception as e:
            print(f"   [ERROR] {type(e).__name__}: {e}")
    if resumen:
        df = pd.DataFrame(resumen)
        df.to_csv(f"{salida_base}/_resumen_lote.csv", index=False)
        print(f"\n{'=' * 60}\n[OK] {len(resumen)}/{len(pdfs)} PDFs procesados")
        print(f"[OK] Resumen: {salida_base}/_resumen_lote.csv\n{'=' * 60}")
        print(df.to_string(index=False))


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        pdfs_actuales = sorted(str(f) for f in Path(".").glob("*.pdf"))
        if pdfs_actuales:
            print(f"[i] Sin args. Procesando {len(pdfs_actuales)} PDF(s) de la carpeta actual.")
            analizar_lote(pdfs_actuales)
        else:
            print("Uso:")
            print("  python aec.py                    -> todos los PDFs de la carpeta")
            print("  python aec.py *.pdf              -> todos los PDFs")
            print("  python aec.py carpeta/           -> todos los PDFs de una carpeta")
            print("  python aec.py a.pdf b.pdf        -> varios")
            print("  python aec.py dosel.pdf          -> uno solo")
        sys.exit(0)

    pdfs = expandir_entradas(sys.argv[1:])

    if not pdfs:
        print("[ERROR] Ningun PDF para procesar.")
        sys.exit(1)

    print(f"[i] {len(pdfs)} PDF(s) a procesar:")
    for p in pdfs:
        print(f"    - {p}")

    analizar_lote(pdfs)


