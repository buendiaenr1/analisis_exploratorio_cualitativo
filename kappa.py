from sklearn.metrics import cohen_kappa_score
import pandas as pd

# ==========================================================
# 0. DATOS SIMULADOS (Triangulación de Investigadores)
# ==========================================================
# Dos investigadores codifican las mismas 10 entrevistas de forma independiente (a ciegas)
datos = {
    'entrevista': [f'Entrevista {i}' for i in range(1, 11)],
    'codificador_1_tu': ['Imposicion', 'Delegacion', 'Cumplimiento', 'Imposicion', 'Resistencia',
                         'Integracion', 'Delegacion', 'Cumplimiento', 'Imposicion', 'Resistencia'],
    'codificador_2_par': ['Imposicion', 'Delegacion', 'Resistencia',  'Imposicion', 'Delegacion',
                          'Integracion', 'Delegacion', 'Cumplimiento', 'Imposicion', 'Integracion']
}
df_rigor = pd.DataFrame(datos)

# 🌟 MEJORA 1: Mostrar los datos y una columna de auditoría caso por caso
df_rigor['Acuerdo'] = df_rigor['codificador_1_tu'] == df_rigor['codificador_2_par']

print("📂 DATOS SIMULADOS: CODIFICACIÓN A CIEGAS")
print("-" * 70)
print(df_rigor.to_string(index=False))
print("-" * 70)
print(f"Acuerdos brutos: {df_rigor['Acuerdo'].sum()} de {len(df_rigor)} casos.\n")

# ==========================================================
# 1. CÁLCULO DEL KAPPA DE COHEN (CÓDIGO ORIGINAL INTACTO)
# ==========================================================
# Mide la concordancia corrigiendo el acuerdo que ocurre por puro azar
kappa = cohen_kappa_score(df_rigor['codificador_1_tu'], df_rigor['codificador_2_par'])

print("🛡️ RIGOR CUALITATIVO: TRIANGULACIÓN DE INVESTIGADORES")
print("=" * 60)
print(f"Kappa de Cohen calculado: {kappa:.2f}")
print("\n📖 INTERPRETACIÓN (Criterios de Landis & Koch):")

if kappa < 0.00: 
    print("• Pobre (Menor acuerdo que el azar)")
elif kappa <= 0.20: 
    print("• Leve")
elif kappa <= 0.40: 
    print("• Fair (Aceptable solo para fases muy exploratorias)")
elif kappa <= 0.60: 
    print("• Moderada (Buen nivel de acuerdo)")
elif kappa <= 0.80: 
    print("• Sustancial (Excelente para tesis y artículos Q1/Q2)")
else: 
    print("• Casi Perfecta (Acuerdo casi total)")

print("\n💡 Acción Metodológica (Nivel 5): Si el Kappa es bajo, no se publica.")
print("Se exige revisar el libro de códigos, redefinir las categorías ambiguas")
print("y volver a codificar hasta garantizar la 'Confirmabilidad' del dato.")

# ==========================================================
# 🌟 MEJORA 2: MATRIZ DE CONFUSIÓN (Diagnóstico de discrepancias)
# ==========================================================
# Esta mejora es fundamental para el "Nivel 5": no solo dice CUÁNTO falló, 
# sino DÓNDE falló, para que puedas redefinir las categorías ambiguas.
print("\n🔍 DIAGNÓSTICO DE DISCREPANCIAS (Matriz de Cruce)")
print("-" * 70)
print("Filas: Codificador 1 (Tú)  |  Columnas: Codificador 2 (Par)")
matriz = pd.crosstab(df_rigor['codificador_1_tu'], df_rigor['codificador_2_par'], 
                     rownames=['Tú'], colnames=['Par'], margins=False)
print(matriz)
print("\n💡 Interpretación de la matriz: Los valores en la diagonal principal (de arriba-izquierda")
print("a abajo-derecha) son acuerdos. Los valores FUERA de esa diagonal son las categorías")
print("que se están confundiendo (ej. Tú codificaste 'Resistencia' pero tu par 'Delegacion').")
print("Ahí es donde debes intervenir tu libro de códigos antes de continuar.")

