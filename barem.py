import pandas as pd
import numpy as np
from scipy import stats

# ==========================================================
# 0. PREPARACIÓN DE DATOS (Simulación de la base de 200 docentes)
# ==========================================================
np.random.seed(42)
n_docentes = 200

# Generamos respuestas aleatorias del 1 al 9 para 12 ítems
# Factor 1: Estrategias (ítems 1-4)
# Factor 2: Manejo (ítems 5-8)
# Factor 3: Compromiso (ítems 9-12)
columnas = [f'item{i}' for i in range(1, 13)]
datos_simulados = np.random.randint(1, 10, size=(n_docentes, 12))
df = pd.DataFrame(datos_simulados, columns=columnas)

# Simulamos que el Ítem 2 está redactado en sentido inverso
df['item2_original'] = df['item2'] 

print(f"✅ Base de datos cargada: {df.shape[0]} docentes, {df.shape[1]} ítems.\n")

# ==========================================================
# PASO 1: Recodificar los ítems inversos
# ==========================================================
df['item2_recodificado'] = 10 - df['item2_original']

# ==========================================================
# PASO 2: Confirmar la confiabilidad (Alfa de Cronbach)
# ==========================================================
def calcular_alpha_cronbach(items_df):
    items = items_df.dropna(axis=1)
    k = len(items.columns)
    varianzas_items = items.var(ddof=1)
    varianza_total = items.sum(axis=1).var(ddof=1)
    alpha = (k / (k - 1)) * (1 - (varianzas_items.sum() / varianza_total))
    return alpha

alpha_f1 = calcular_alpha_cronbach(df[['item1', 'item2_recodificado', 'item3', 'item4']])
alpha_f2 = calcular_alpha_cronbach(df[['item5', 'item6', 'item7', 'item8']])
alpha_f3 = calcular_alpha_cronbach(df[['item9', 'item10', 'item11', 'item12']])

# ==========================================================
# PASO 3: Calcular el puntaje bruto
# ==========================================================
df['bruto_estrategias'] = df[['item1', 'item2_recodificado', 'item3', 'item4']].sum(axis=1)
df['bruto_manejo'] = df[['item5', 'item6', 'item7', 'item8']].sum(axis=1)
df['bruto_compromiso'] = df[['item9', 'item10', 'item11', 'item12']].sum(axis=1)

# ==========================================================
# PASO 4 y 5: Construir la norma y Transformar a Puntuación T
# ==========================================================
media_f1 = df['bruto_estrategias'].mean()
std_f1 = df['bruto_estrategias'].std()

df['z_estrategias'] = (df['bruto_estrategias'] - media_f1) / std_f1
df['T_estrategias'] = 50 + (10 * df['z_estrategias'])

# ==========================================================
# PASO 6: Calcular el Percentil
# ==========================================================
df['percentil_estrategias'] = df['bruto_estrategias'].apply(
    lambda x: stats.percentileofscore(df['bruto_estrategias'], x)
)

# ==========================================================
# 📊 MOSTRAR LA BASE DE DATOS (Primeras 5 filas)
# ==========================================================
print("📊 VISTA PREVIA DE LA BASE DE DATOS (Primeras 5 filas):")
print("--------------------------------------------------------------------------------")
# Seleccionamos columnas clave para que la vista sea limpia y legible
columnas_clave = ['item1', 'item2_recodificado', 'item3', 'item4', 'bruto_estrategias', 'z_estrategias', 'T_estrategias', 'percentil_estrategias']
print(df[columnas_clave].head().to_string())
print("--------------------------------------------------------------------------------\n")

# ==========================================================
# CASO PRÁCTICO DEL TEXTO: La maestra que sacó 35 puntos
# ==========================================================
puntaje_maestra = 35
t_maestra = 50 + 10 * ((puntaje_maestra - media_f1) / std_f1)
percentil_maestra = stats.percentileofscore(df['bruto_estrategias'], puntaje_maestra)

print("="*60)
print("📊 INTERPRETACIÓN DEL CASO (La maestra con puntaje 35)")
print("="*60)
print(f"• Puntaje Bruto: {puntaje_maestra} (de un máximo de 36)")
print(f"• Puntuación T:  {t_maestra:.1f} (Una T > 60 indica rendimiento alto)")
print(f"• Percentil:     {percentil_maestra:.0f}º (Superó al {percentil_maestra:.0f}% de su grupo)")
print("\n💡 Conclusión: La maestra muestra una autoeficacia alta en estrategias de")
print("instrucción en comparación con su grupo de referencia, tal como explica el texto.")


