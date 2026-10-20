# -*- coding: utf-8 -*-
"""
Análisis Exploratorio Cualitativo de PDF (v2.1)
-----------------------------------------------
Correcciones v2.1:
- LDA robusto: divide en párrafos -> líneas -> ventanas (nunca falla con textos cortos)
- max_df/min_df adaptativos según cantidad de documentos
- Filtra entidades que son solo signos de puntuación
- Preserva estructura del texto para modelado de tópicos
- Sentimiento: usa pysentimiento si está instalado (mucho mejor en español)
"""
# ## pip install pymupdf spacy pandas matplotlib wordcloud scikit-learn textblob pysentimiento --upgrade

import sys
import io
import re
from pathlib import Path
from collections import Counter

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
# 1. EXTRACCIÓN DEL TEXTO
# =========================================================
def extraer_texto(pdf_path: str) -> tuple[str, int]:
    doc = fitz.open(pdf_path)
    paginas = [pag.get_text() for pag in doc]
    return "\n".join(paginas), len(doc)


# =========================================================
# 2. ESTADÍSTICAS BÁSICAS
# =========================================================
def estadisticas_basicas(texto: str, n_paginas: int) -> dict:
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
# 3. LIMPIEZA Y TOKENIZACIÓN
# =========================================================
def limpiar_texto(texto: str) -> str:
    """Limpieza agresiva -> una sola línea. Para frecuencias y nube."""
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"\S+@\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúñü\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def limpiar_parrafo(p: str) -> str:
    """Limpieza suave -> conserva estructura. Para LDA."""
    p = p.lower()
    p = re.sub(r"http\S+|www\S+", "", p)
    p = re.sub(r"\S+@\S+", "", p)
    p = re.sub(r"[^a-záéíóúñü\s]", " ", p)
    p = re.sub(r"\s+", " ", p).strip()
    return p


def tokenizar(texto_limpio: str) -> list[str]:
    tokens = texto_limpio.split()
    return [t for t in tokens if len(t) > 2 and t not in STOP_ES]


def dividir_documentos(texto: str, min_len: int = 80) -> list[str]:
    """Divide el texto en unidades para LDA: párrafos -> líneas -> ventanas."""
    docs = [p.strip() for p in re.split(r"\n\s*\n", texto) if len(p.strip()) >= min_len]
    if len(docs) >= 5:
        return docs
    docs = [p.strip() for p in re.split(r"\n", texto) if len(p.strip()) >= min_len]
    if len(docs) >= 5:
        return docs
    oraciones = [s.strip() for s in re.split(r"[.!?]+", texto) if len(s.strip()) > 20]
    ventanas, buffer = [], ""
    for o in oraciones:
        buffer += " " + o
        if len(buffer.split()) >= 80:
            ventanas.append(buffer.strip())
            buffer = ""
    if buffer.strip():
        ventanas.append(buffer.strip())
    return ventanas


# =========================================================
# 4. FRECUENCIAS
# =========================================================
def frecuencias(tokens: list[str], n: int = 20):
    f_palabras = pd.DataFrame(
        Counter(tokens).most_common(n), columns=["palabra", "frecuencia"]
    )
    bigramas = list(zip(tokens, tokens[1:]))
    f_bigramas = pd.DataFrame(
        [(" ".join(k), v) for k, v in Counter(bigramas).most_common(n)],
        columns=["bigrama", "frecuencia"],
    )
    return f_palabras, f_bigramas


# =========================================================
# 5. NUBE DE PALABRAS
# =========================================================
def generar_nube(tokens: list[str], salida: str = "nube_palabras.png"):
    wc = WordCloud(
        width=1200, height=600, background_color="white",
        colormap="viridis", max_words=150
    ).generate(" ".join(tokens))
    plt.figure(figsize=(14, 7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nube de palabras", fontsize=16)
    plt.tight_layout()
    plt.savefig(salida, dpi=150)
    plt.close()
    print(f"[OK] Nube guardada en: {salida}")


# =========================================================
# 6. ANÁLISIS DE SENTIMIENTO
# =========================================================
def analisis_sentimiento(texto: str) -> pd.DataFrame:
    """Usa pysentimiento si se puede descargar/cargar el modelo.
    Ante CUALQUIER error (import, red, timeout, disco), cae a TextBlob."""
    oraciones = [o.strip() for o in re.split(r"[.!?]+", texto) if len(o.strip()) > 20]
    registros = []
    analyzer = None

    try:
        from pysentimiento import create_analyzer
        # Si ya está descargado, esto es instantáneo. Si no, descarga el modelo.
        analyzer = create_analyzer(task="sentiment", lang="es")
        print("[i] Sentimiento: usando pysentimiento (espanol)")
    except Exception as e:
        print(f"[!] pysentimiento no disponible ({type(e).__name__}: {e})")
        print("[i] Fallback a TextBlob (basico en espanol).")

    for o in oraciones:
        if analyzer is not None:
            try:
                res = analyzer.predict(o)
                etiqueta = {"POS": "positivo", "NEG": "negativo", "NEU": "neutro"}[res.output]
                registros.append({
                    "oracion": o[:150],
                    "sentimiento": etiqueta,
                    "prob": round(max(res.probas.values()), 3),
                })
            except Exception:
                # Si falla una oración puntual, no tumbo todo el análisis
                registros.append({
                    "oracion": o[:150],
                    "sentimiento": "error",
                    "prob": None,
                })
        else:
            pol = TextBlob(o).sentiment.polarity
            etiqueta = "positivo" if pol > 0.1 else ("negativo" if pol < -0.1 else "neutro")
            registros.append({
                "oracion": o[:150],
                "polaridad": round(pol, 3),
                "sentimiento": etiqueta,
            })
    return pd.DataFrame(registros)


# =========================================================
# 7. ENTIDADES NOMBRADAS (NER)
# =========================================================
def extraer_entidades(texto: str) -> pd.DataFrame:
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(texto[:1_000_000])
    entidades = [
        (e.text.strip(), e.label_)
        for e in doc.ents
        if len(e.text.strip()) >= 2 and re.search(r"[A-Za-zÁÉÍÓÚÑÜáéíóúñü]", e.text)
    ]
    if not entidades:
        return pd.DataFrame(columns=["entidad", "tipo", "frecuencia"])
    df = pd.DataFrame(entidades, columns=["entidad", "tipo"])
    return df.value_counts().reset_index(name="frecuencia").head(30)


# =========================================================
# 8. MODELADO DE TÓPICOS (LDA)
# =========================================================
def modelar_topicos(texto_original: str, n_topicos: int = 5, n_palabras: int = 8):
    docs = dividir_documentos(texto_original, min_len=80)
    docs = [limpiar_parrafo(d) for d in docs]
    docs = [d for d in docs if len(d.split()) >= 5]

    if len(docs) < 2:
        print("[!] Muy pocos fragmentos de texto para LDA. Se omite.")
        return {}

    n_topicos = min(n_topicos, max(2, len(docs) // 2))

    # max_df adaptativo: 0.95 solo si hay suficientes documentos
    max_df = 0.95 if len(docs) >= 20 else 1.0
    vectorizer = CountVectorizer(
        max_df=max_df,
        min_df=1,
        stop_words=list(STOP_ES),
        token_pattern=r"(?u)\b[a-záéíóúñü]{3,}\b",
    )
    try:
        X = vectorizer.fit_transform(docs)
    except ValueError as e:
        print(f"[!] LDA omitido: {e}")
        return {}

    if X.shape[1] == 0:
        print("[!] LDA omitido: vocabulario vacio tras filtros.")
        return {}

    n_topicos = min(n_topicos, X.shape[1])
    lda = LatentDirichletAllocation(
        n_components=n_topicos, random_state=42, max_iter=20
    )
    lda.fit(X)

    vocab = vectorizer.get_feature_names_out()
    topicos = {}
    for i, comp in enumerate(lda.components_):
        top = comp.argsort()[-n_palabras:][::-1]
        topicos[f"Topico {i+1}"] = [vocab[j] for j in top]
    return topicos


# =========================================================
# 9. PIPELINE PRINCIPAL
# =========================================================
def analizar_pdf(pdf_path: str, salida_dir: str = "resultados"):
    if not Path(pdf_path).exists():
        print(f"[ERROR] No se encuentra: {pdf_path}")
        print(f"        Ruta actual: {Path.cwd()}")
        sys.exit(1)

    Path(salida_dir).mkdir(exist_ok=True)
    print(f"\n[+] Analizando: {pdf_path}\n" + "=" * 60)

    texto, n_paginas = extraer_texto(pdf_path)
    print(f"[OK] Texto extraido ({n_paginas} paginas, {len(texto)} caracteres)")

    if not texto.strip():
        print("[ERROR] El PDF no contiene texto seleccionable (posible escaneado).")
        sys.exit(1)

    stats = estadisticas_basicas(texto, n_paginas)
    print("\n[ESTADISTICAS BASICAS]")
    for k, v in stats.items():
        print(f"   {k:.<35} {v}")

    texto_limpio = limpiar_texto(texto)
    tokens = tokenizar(texto_limpio)
    print(f"\n[OK] Tokens utiles (sin stopwords): {len(tokens)}")

    f_pal, f_big = frecuencias(tokens, n=20)
    print("\n[TOP 15 PALABRAS]")
    print(f_pal.head(15).to_string(index=False))
    f_pal.to_csv(f"{salida_dir}/frecuencia_palabras.csv", index=False)
    f_big.to_csv(f"{salida_dir}/frecuencia_bigramas.csv", index=False)

    generar_nube(tokens, f"{salida_dir}/nube_palabras.png")

    df_sent = analisis_sentimiento(texto)
    df_sent.to_csv(f"{salida_dir}/sentimiento.csv", index=False)
    print("\n[DISTRIBUCION DE SENTIMIENTO]")
    print(df_sent["sentimiento"].value_counts().to_string())

    print("\n[ENTIDADES DETECTADAS - top 15]")
    df_ent = extraer_entidades(texto)
    if not df_ent.empty:
        print(df_ent.head(15).to_string(index=False))
        df_ent.to_csv(f"{salida_dir}/entidades.csv", index=False)
    else:
        print("   (no se detectaron entidades)")

    print("\n[TOPICOS PRINCIPALES - LDA]")
    # OJO: se pasa el texto ORIGINAL (preserva \n), no el limpiado
    topicos = modelar_topicos(texto, n_topicos=5)
    if topicos:
        for t, palabras in topicos.items():
            print(f"   {t}: {', '.join(palabras)}")
    else:
        print("   (no se pudieron extraer topicos)")

    with open(f"{salida_dir}/texto_extraido.txt", "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"\n[OK] Analisis completo. Resultados en carpeta: ./{salida_dir}/")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python aec.py archivo.pdf")
        sys.exit(1)
    analizar_pdf(sys.argv[1])





# -*- coding: utf-8 -*-
"""
Análisis Exploratorio Cualitativo de PDF (v2.1)
-----------------------------------------------
Correcciones v2.1:
- LDA robusto: divide en párrafos -> líneas -> ventanas (nunca falla con textos cortos)
- max_df/min_df adaptativos según cantidad de documentos
- Filtra entidades que son solo signos de puntuación
- Preserva estructura del texto para modelado de tópicos
- Sentimiento: usa pysentimiento si está instalado (mucho mejor en español)
"""

import sys
import io
import re
from pathlib import Path
from collections import Counter

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
# 1. EXTRACCIÓN DEL TEXTO
# =========================================================
def extraer_texto(pdf_path: str) -> tuple[str, int]:
    doc = fitz.open(pdf_path)
    paginas = [pag.get_text() for pag in doc]
    return "\n".join(paginas), len(doc)


# =========================================================
# 2. ESTADÍSTICAS BÁSICAS
# =========================================================
def estadisticas_basicas(texto: str, n_paginas: int) -> dict:
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
# 3. LIMPIEZA Y TOKENIZACIÓN
# =========================================================
def limpiar_texto(texto: str) -> str:
    """Limpieza agresiva -> una sola línea. Para frecuencias y nube."""
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"\S+@\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúñü\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def limpiar_parrafo(p: str) -> str:
    """Limpieza suave -> conserva estructura. Para LDA."""
    p = p.lower()
    p = re.sub(r"http\S+|www\S+", "", p)
    p = re.sub(r"\S+@\S+", "", p)
    p = re.sub(r"[^a-záéíóúñü\s]", " ", p)
    p = re.sub(r"\s+", " ", p).strip()
    return p


def tokenizar(texto_limpio: str) -> list[str]:
    tokens = texto_limpio.split()
    return [t for t in tokens if len(t) > 2 and t not in STOP_ES]


def dividir_documentos(texto: str, min_len: int = 80) -> list[str]:
    """Divide el texto en unidades para LDA: párrafos -> líneas -> ventanas."""
    docs = [p.strip() for p in re.split(r"\n\s*\n", texto) if len(p.strip()) >= min_len]
    if len(docs) >= 5:
        return docs
    docs = [p.strip() for p in re.split(r"\n", texto) if len(p.strip()) >= min_len]
    if len(docs) >= 5:
        return docs
    oraciones = [s.strip() for s in re.split(r"[.!?]+", texto) if len(s.strip()) > 20]
    ventanas, buffer = [], ""
    for o in oraciones:
        buffer += " " + o
        if len(buffer.split()) >= 80:
            ventanas.append(buffer.strip())
            buffer = ""
    if buffer.strip():
        ventanas.append(buffer.strip())
    return ventanas


# =========================================================
# 4. FRECUENCIAS
# =========================================================
def frecuencias(tokens: list[str], n: int = 20):
    f_palabras = pd.DataFrame(
        Counter(tokens).most_common(n), columns=["palabra", "frecuencia"]
    )
    bigramas = list(zip(tokens, tokens[1:]))
    f_bigramas = pd.DataFrame(
        [(" ".join(k), v) for k, v in Counter(bigramas).most_common(n)],
        columns=["bigrama", "frecuencia"],
    )
    return f_palabras, f_bigramas


# =========================================================
# 5. NUBE DE PALABRAS
# =========================================================
def generar_nube(tokens: list[str], salida: str = "nube_palabras.png"):
    wc = WordCloud(
        width=1200, height=600, background_color="white",
        colormap="viridis", max_words=150
    ).generate(" ".join(tokens))
    plt.figure(figsize=(14, 7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nube de palabras", fontsize=16)
    plt.tight_layout()
    plt.savefig(salida, dpi=150)
    plt.close()
    print(f"[OK] Nube guardada en: {salida}")


# =========================================================
# 6. ANÁLISIS DE SENTIMIENTO
# =========================================================
def analisis_sentimiento(texto: str) -> pd.DataFrame:
    """Usa pysentimiento si está disponible (mejor en español).
    Si no, cae a TextBlob (inglés)."""
    oraciones = [o.strip() for o in re.split(r"[.!?]+", texto) if len(o.strip()) > 20]
    registros = []

    analyzer = None
    try:
        from pysentimiento import create_analyzer
        analyzer = create_analyzer(task="sentiment", lang="es")
        print("[i] Sentimiento: usando pysentimiento (espanol)")
    except ImportError:
        print("[i] Sentimiento: usando TextBlob (limitado en espanol; "
              "instala 'pysentimiento' para mejor precision)")

    for o in oraciones:
        if analyzer is not None:
            res = analyzer.predict(o)
            etiqueta = {"POS": "positivo", "NEG": "negativo", "NEU": "neutro"}[res.output]
            registros.append({
                "oracion": o[:150],
                "sentimiento": etiqueta,
                "prob": round(max(res.probas.values()), 3),
            })
        else:
            pol = TextBlob(o).sentiment.polarity
            etiqueta = "positivo" if pol > 0.1 else ("negativo" if pol < -0.1 else "neutro")
            registros.append({
                "oracion": o[:150],
                "polaridad": round(pol, 3),
                "sentimiento": etiqueta,
            })
    return pd.DataFrame(registros)


# =========================================================
# 7. ENTIDADES NOMBRADAS (NER)
# =========================================================
def extraer_entidades(texto: str) -> pd.DataFrame:
    nlp = spacy.load("es_core_news_sm")
    doc = nlp(texto[:1_000_000])
    entidades = [
        (e.text.strip(), e.label_)
        for e in doc.ents
        if len(e.text.strip()) >= 2 and re.search(r"[A-Za-zÁÉÍÓÚÑÜáéíóúñü]", e.text)
    ]
    if not entidades:
        return pd.DataFrame(columns=["entidad", "tipo", "frecuencia"])
    df = pd.DataFrame(entidades, columns=["entidad", "tipo"])
    return df.value_counts().reset_index(name="frecuencia").head(30)


# =========================================================
# 8. MODELADO DE TÓPICOS (LDA)
# =========================================================
def modelar_topicos(texto_original: str, n_topicos: int = 5, n_palabras: int = 8):
    docs = dividir_documentos(texto_original, min_len=80)
    docs = [limpiar_parrafo(d) for d in docs]
    docs = [d for d in docs if len(d.split()) >= 5]

    if len(docs) < 2:
        print("[!] Muy pocos fragmentos de texto para LDA. Se omite.")
        return {}

    n_topicos = min(n_topicos, max(2, len(docs) // 2))

    # max_df adaptativo: 0.95 solo si hay suficientes documentos
    max_df = 0.95 if len(docs) >= 20 else 1.0
    vectorizer = CountVectorizer(
        max_df=max_df,
        min_df=1,
        stop_words=list(STOP_ES),
        token_pattern=r"(?u)\b[a-záéíóúñü]{3,}\b",
    )
    try:
        X = vectorizer.fit_transform(docs)
    except ValueError as e:
        print(f"[!] LDA omitido: {e}")
        return {}

    if X.shape[1] == 0:
        print("[!] LDA omitido: vocabulario vacio tras filtros.")
        return {}

    n_topicos = min(n_topicos, X.shape[1])
    lda = LatentDirichletAllocation(
        n_components=n_topicos, random_state=42, max_iter=20
    )
    lda.fit(X)

    vocab = vectorizer.get_feature_names_out()
    topicos = {}
    for i, comp in enumerate(lda.components_):
        top = comp.argsort()[-n_palabras:][::-1]
        topicos[f"Topico {i+1}"] = [vocab[j] for j in top]
    return topicos


# =========================================================
# 9. PIPELINE PRINCIPAL
# =========================================================
def analizar_pdf(pdf_path: str, salida_dir: str = "resultados"):
    if not Path(pdf_path).exists():
        print(f"[ERROR] No se encuentra: {pdf_path}")
        print(f"        Ruta actual: {Path.cwd()}")
        sys.exit(1)

    Path(salida_dir).mkdir(exist_ok=True)
    print(f"\n[+] Analizando: {pdf_path}\n" + "=" * 60)

    texto, n_paginas = extraer_texto(pdf_path)
    print(f"[OK] Texto extraido ({n_paginas} paginas, {len(texto)} caracteres)")

    if not texto.strip():
        print("[ERROR] El PDF no contiene texto seleccionable (posible escaneado).")
        sys.exit(1)

    stats = estadisticas_basicas(texto, n_paginas)
    print("\n[ESTADISTICAS BASICAS]")
    for k, v in stats.items():
        print(f"   {k:.<35} {v}")

    texto_limpio = limpiar_texto(texto)
    tokens = tokenizar(texto_limpio)
    print(f"\n[OK] Tokens utiles (sin stopwords): {len(tokens)}")

    f_pal, f_big = frecuencias(tokens, n=20)
    print("\n[TOP 15 PALABRAS]")
    print(f_pal.head(15).to_string(index=False))
    f_pal.to_csv(f"{salida_dir}/frecuencia_palabras.csv", index=False)
    f_big.to_csv(f"{salida_dir}/frecuencia_bigramas.csv", index=False)

    generar_nube(tokens, f"{salida_dir}/nube_palabras.png")

    df_sent = analisis_sentimiento(texto)
    df_sent.to_csv(f"{salida_dir}/sentimiento.csv", index=False)
    print("\n[DISTRIBUCION DE SENTIMIENTO]")
    print(df_sent["sentimiento"].value_counts().to_string())

    print("\n[ENTIDADES DETECTADAS - top 15]")
    df_ent = extraer_entidades(texto)
    if not df_ent.empty:
        print(df_ent.head(15).to_string(index=False))
        df_ent.to_csv(f"{salida_dir}/entidades.csv", index=False)
    else:
        print("   (no se detectaron entidades)")

    print("\n[TOPICOS PRINCIPALES - LDA]")
    # OJO: se pasa el texto ORIGINAL (preserva \n), no el limpiado
    topicos = modelar_topicos(texto, n_topicos=5)
    if topicos:
        for t, palabras in topicos.items():
            print(f"   {t}: {', '.join(palabras)}")
    else:
        print("   (no se pudieron extraer topicos)")

    with open(f"{salida_dir}/texto_extraido.txt", "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"\n[OK] Analisis completo. Resultados en carpeta: ./{salida_dir}/")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python aec.py archivo.pdf")
        sys.exit(1)
    analizar_pdf(sys.argv[1])    


