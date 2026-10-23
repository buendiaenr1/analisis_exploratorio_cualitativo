import pandas as pd
import statsmodels.api as sm

# ==========================================================
# 0. DATOS ORIGINALES (Tal como salen de tu análisis cualitativo)
# ==========================================================
data_original = {
    'docente': ['Docente 1', 'Docente 2', 'Docente 3', 'Docente 4', 'Docente 5', 'Docente 6'],
    'años_experiencia': [5, 20, 2, 15, 25, 8], # Variable Cuantitativa
    # Variable Cualitativa (Categorías emergentes de cod.py)
    'estrategia_adaptacion': ['Integracion_Real', 'Cumplimiento_Aparente', 'Integracion_Real', 
                              'Cumplimiento_Aparente', 'Resistencia_Declarada', 'Integracion_Real']
}
df_original = pd.DataFrame(data_original)

print("📂 DATOS ORIGINALES (Antes de la conversión)")
print("-" * 65)
print(df_original.to_string(index=False))
print("\n💡 Aquí vemos la variable cualitativa 'estrategia_adaptacion' tal como")
print("emergió del análisis, lista para ser transformada.\n")

# ==========================================================
# 1. CONVERSIÓN CUALI -> CUANTI (Variables Dummy)
# ==========================================================
# Se mantiene 'dtype=int' para garantizar que sean 0 y 1, no True/False
df_dummies = pd.get_dummies(df_original['estrategia_adaptacion'], prefix='cod', drop_first=False, dtype=int)
df_mixto = pd.concat([df_original[['docente', 'años_experiencia']], df_dummies], axis=1)

print("🔄 CONVERSIÓN MIXTA (Variables Dummy)")
print("-" * 65)
print(df_mixto.to_string(index=False))
print("\n💡 Interpretación: Ahora las variables dummy son numéricas (0 y 1)")
print("y pueden usarse en cualquier fórmula estadística.\n")

# ==========================================================
# 2. INTEGRACIÓN EN MODELO (Regresión Lineal)
# ==========================================================
X = df_mixto[['cod_Cumplimiento_Aparente', 'cod_Resistencia_Declarada']]
y = df_mixto['años_experiencia']
X_const = sm.add_constant(X) # Añade el intercepto (la constante)

modelo = sm.OLS(y, X_const).fit()

# Extraemos los valores para hacer la conclusión dinámica y precisa
coef_cump = modelo.params['cod_Cumplimiento_Aparente']
coef_resis = modelo.params['cod_Resistencia_Declarada']
pval_cump = modelo.pvalues['cod_Cumplimiento_Aparente']
pval_resis = modelo.pvalues['cod_Resistencia_Declarada']

# Calculamos el promedio del grupo base para la interpretación
promedio_base = df_original[df_original['estrategia_adaptacion'] == 'Integracion_Real']['años_experiencia'].mean()

print("📊 MODELO ESTADÍSTICO CON DATOS CUALITATIVOS CONVERTIDOS")
print("-" * 65)
print(f"Coeficiente de 'Cumplimiento Aparente':   {coef_cump:>5.2f} años (p-valor: {pval_cump:.3f})")
print(f"Coeficiente de 'Resistencia Declarada':   {coef_resis:>5.2f} años (p-valor: {pval_resis:.3f})")
print(f"Grupo de referencia (Base):               'Integracion_Real' (Promedio: {promedio_base:.1f} años)")

print("\n💡 CONCLUSIÓN MIXTA (Interpretación de los coeficientes):")
print(f"Respecto al grupo base ('Integración Real'):")
print(f"  • Los docentes con 'Cumplimiento Aparente' tienen, en promedio, {abs(coef_cump):.1f} años {'más' if coef_cump > 0 else 'menos'} de experiencia.")
print(f"  • Los docentes con 'Resistencia Declarada' tienen, en promedio, {abs(coef_resis):.1f} años {'más' if coef_resis > 0 else 'menos'} de experiencia.")

print("\n⚠️ Nota de Rigor Metodológico:")
print("Los p-valores indican la significancia estadística. En esta muestra simulada (n=6),")
print("los p-valores son altos (>0.05), lo que significa que la diferencia podría deberse al azar.")
print("En tu investigación real, con una muestra mayor, este modelo te dirá si la categoría")
print("cualitativa predice significativamente la variable cuantitativa.")

