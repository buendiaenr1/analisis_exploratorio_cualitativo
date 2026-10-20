import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import json
import re

# Configuración de la página
st.set_page_config(page_title="Codificador Cualitativo PDF", layout="wide", page_icon="📄")

def extraer_parrafos_inteligentes(archivo_pdf):
    """
    Extrae texto del PDF y reconstruye los párrafos correctamente,
    ignorando los saltos de línea arbitrarios que suelen tener los PDFs.
    """
    doc = fitz.open(stream=archivo_pdf.read(), filetype="pdf")
    texto_completo = ""
    for pagina in doc:
        texto_completo += pagina.get_text()
    
    # Dividir por saltos de línea simples para procesar línea por línea
    lineas = texto_completo.split('\n')
    parrafos_unidos = []
    parrafo_actual = ""
    
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        
        if not parrafo_actual:
            parrafo_actual = linea
        else:
            # Verificar si el párrafo actual termina en un signo de puntuación que indique final de idea
            # (Punto, interrogación, exclamación, dos puntos, o cierre de paréntesis/comillas)
            termina_en_puntuacion = re.search(r'[.!?:"\)]\s*$', parrafo_actual)
            
            if termina_en_puntuacion:
                # Es un nuevo párrafo
                parrafos_unidos.append(parrafo_actual)
                parrafo_actual = linea
            else:
                # Es continuación del mismo párrafo, unir con un espacio
                parrafo_actual += " " + linea
    
    # Agregar el último párrafo si existe
    if parrafo_actual:
        parrafos_unidos.append(parrafo_actual)
        
    # Filtrar bloques demasiado cortos (ruido, números de página, encabezados sueltos)
    parrafos_limpios = [p for p in parrafos_unidos if len(p) > 60]
    
    return parrafos_limpios

def main():
    st.title("📄 Herramienta de Codificación Cualitativa para PDF")
    st.markdown("""
    **Instrucciones:**
    1. Sube tu PDF con tus datos (entrevistas, documentos, etc.).
    2. El sistema reconstruirá automáticamente los párrafos completos.
    3. Asigna **Códigos** (temas/categorías) y **Notas/Memos** (reflexiones) a cada bloque.
    4. Exporta los datos al finalizar (CSV o JSON).
    """)

    archivo_subido = st.file_uploader("Sube tu archivo PDF", type=["pdf"])

    if archivo_subido is not None:
        # Inicializar estado de la sesión
        if 'parrafos' not in st.session_state:
            with st.spinner("🧠 Procesando y reconstruyendo párrafos del PDF..."):
                st.session_state.parrafos = extraer_parrafos_inteligentes(archivo_subido)
                st.session_state.codificaciones = {} 

        parrafos = st.session_state.parrafos
        st.success(f"✅ Texto procesado. Se han identificado **{len(parrafos)}** bloques de texto coherentes para codificar.")

        st.markdown("---")
        
        for i, parrafo in enumerate(parrafos):
            if i not in st.session_state.codificaciones:
                st.session_state.codificaciones[i] = {"codigos": "", "memo": ""}

            st.markdown(f"#### 📌 Bloque {i+1}")
            
            # Texto legible y no editable
            st.markdown(f"<div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff; font-family: sans-serif; line-height: 1.6;'>{parrafo}</div>", unsafe_allow_html=True)

            col1, col2 = st.columns([1, 2])
            
            with col1:
                codigos_input = st.text_input(
                    "🏷️ Códigos (separados por comas)",
                    value=st.session_state.codificaciones[i]["codigos"],
                    key=f"codigos_input_{i}",
                    help="Ej: Barrera_economica, Falta_apoyo_familiar"
                )
            with col2:
                memo_input = st.text_area(
                    "📝 Notas / Memos analíticos",
                    value=st.session_state.codificaciones[i]["memo"],
                    height=80,
                    key=f"memo_input_{i}",
                    help="Reflexiones, dudas o conexiones teóricas."
                )

            # Guardar en el estado de la sesión
            st.session_state.codificaciones[i]["codigos"] = codigos_input
            st.session_state.codificaciones[i]["memo"] = memo_input
            
            st.markdown("---")

        # Sección de Exportación
        st.subheader("💾 Exportar Datos Codificados")
        
        datos_para_exportar = []
        for i, parrafo in enumerate(parrafos):
            codigos_str = st.session_state.codificaciones[i]["codigos"]
            memo_str = st.session_state.codificaciones[i]["memo"]
            
            if codigos_str.strip() or memo_str.strip():
                datos_para_exportar.append({
                    "Bloque_ID": i + 1,
                    "Texto_Original": parrafo,
                    "Códigos": codigos_str,
                    "Notas_Memos": memo_str
                })

        if datos_para_exportar:
            df = pd.DataFrame(datos_para_exportar)
            
            col_exp1, col_exp2, col_exp3 = st.columns(3)
            
            with col_exp1:
                csv = df.to_csv(index=False).encode('utf-8-sig') # utf-8-sig para que Excel lo abra bien con tildes
                st.download_button(
                    label="📥 Descargar CSV (Excel)",
                    data=csv,
                    file_name="codificacion_cualitativa.csv",
                    mime="text/csv"
                )
            
            with col_exp2:
                json_data = json.dumps(datos_para_exportar, ensure_ascii=False, indent=4)
                st.download_button(
                    label="📥 Descargar JSON",
                    data=json_data,
                    file_name="codificacion_cualitativa.json",
                    mime="application/json"
                )
                
            with col_exp3:
                st.metric("Bloques Codificados", len(datos_para_exportar))
        else:
            st.info("ℹ️ Aún no has asignado códigos ni notas. ¡Empieza a leer y codificar!")

if __name__ == "__main__":
    main()




