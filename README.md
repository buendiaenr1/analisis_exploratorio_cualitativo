
# Análisis exploratorio cualitativo

# para correr aec.py usar:     python aec.py
# para correr cod.py usar:     streamlit run cod.py
# para correr barem1.py usar:   python barem1.py (modificar codigo para leer archivo)

Imagina que aec.py (Análisis Exploratorio Cualitativo) es como un dron que sobrevuela un bosque.
Mientras que tú (con cod.py) eres el explorador caminando entre los árboles, leyendo cada hoja con una lupa (análisis micro), aec.py es el dron que te da una foto aérea de todo el bosque (análisis macro) en cuestión de segundos.
En palabras simples, es un script de Python que lee uno o varios archivos PDF y le aplica "inteligencia artificial" básica para responder a preguntas generales sobre el texto.
Aquí tienes sus 5 "superpoderes" explicados de forma sencilla:
1. 📊 El Contador (Estadísticas)
Te dice de un vistazo qué tan grande es tu corpus de datos: cuántas páginas, palabras y oraciones tiene en total.
2. ☁️ El Radar de Palabras (Frecuencias y Nube de Palabras)
Ignora las palabras aburridas (como "el", "la", "de") y te dice cuáles son los 20 términos más repetidos por los participantes. Además, genera una imagen (nube de palabras) donde las ideas más centrales se ven más grandes.
Ejemplo: Si en una nube de entrevistas sobre teletrabajo la palabra "cansancio" es gigante, ya sabes por dónde va la cosa.
3. 🕵️ El Buscador de Nombres (Entidades / NER)
El script identifica y extrae automáticamente nombres propios, organizaciones, lugares y fechas que aparecen en el texto.
Ejemplo: Te dice que en tus entrevistas se mencionó 45 veces a la "Universidad", 20 veces a "Madrid" y 10 veces a "Juan".
4. 🧩 El Detector de Temas Ocultos (Modelado de Tópicos / LDA)
Esta es la parte más "mágica". El algoritmo agrupa palabras que suelen aparecer juntas y te dice: "Oye, basándome en las palabras, creo que en este texto hay 5 grandes temas ocultos".
Ejemplo: La máquina te sugiere que el "Tópico 1" son las palabras: jefe, correo, noche, estrés. Tú, como investigador, lees eso y dices: "¡Ah! La máquina detectó el tema de la desconexión digital".
5. 🌡️ El Termómetro Emocional (Análisis de Sentimiento)
Lee oración por oración e intenta adivinar si el tono es positivo, negativo o neutro.
Ejemplo: Te entrega una tabla diciendo que el 60% de las oraciones sobre "la nueva política de la empresa" tuvieron un sentimiento negativo.
¿Para qué sirve esto en tu investigación? (El valor metodológico)
No sirve para concluir nada por sí solo (la máquina no entiende el contexto profundo, las ironías ni el dolor humano). Sirve para ahorrarte tiempo y guiarte:
Familiarización rápida: En lugar de leer 500 páginas a ciegas, el dron te dice dónde aterrizar.
Generar hipótesis: Si el análisis de sentimiento te muestra que las entrevistas son mayormente negativas, llegas a tu lectura profunda (cod.py) con esa pista en la cabeza.
Triangulación: En tu tesis puedes decir: "El análisis computacional (Figura 1) reveló que el término 'burnout' fue el más frecuente y con polaridad negativa, lo cual fue confirmado posteriormente en la codificación manual de las entrevistas".



# analisis_exploratorio_cualitativo
En resumen: aec.py es tu asistente robástico que hace el trabajo sucio de contar, agrupar y medir el tono general, para que tú puedas dedicar tu cerebro humano a lo que realmente importa: interpretar el significado profundo.

## Codificar con cod.py
Si aec.py era el dron que te daba una foto aérea del bosque (análisis macro), cod.py es tú, el explorador, caminando por el bosque con una lupa y un cuaderno de campo (análisis micro).
En palabras simples, cod.py es tu mesa de trabajo digital y cuaderno de notas para hacer el trabajo profundo, lento y humano de la investigación cualitativa: la codificación y la interpretación.
Aquí tienes sus 4 "superpoderes" explicados de forma sencilla:
1. 🧩 El Reconstructor de Textos (Lectura limpia)
Los PDFs son terribles para leer en pantalla porque cortan las oraciones a la mitad con saltos de línea invisibles. cod.py lee el PDF, "arregla" esos saltos de línea y te presenta el texto en bloques o párrafos coherentes. Así puedes leer una idea completa sin que se corte a la mitad.
2. 🏷️ El Marcador de Categorías (Codificación)
En lugar de tener que imprimir 500 páginas y usar marcadores de colores de neón, la app te muestra un párrafo y te da un espacio para ponerle Códigos (etiquetas).
Ejemplo: Lees un párrafo donde un profesor dice que no puede desconectarse del correo, y le pones los códigos: difusion_fronteras, burnout, presion_digital.
3. 📝 El Diario de Campo Digital (Memorándums / Memos)
Esta es la función más importante para un cualitativista. Junto a cada párrafo, tienes un espacio para escribir Notas o Memos. Aquí es donde va tu cerebro: tus reflexiones, tus dudas, las conexiones con tu marco teórico o tus ideas brillantes que te dan a las 2 de la mañana.
Ejemplo: En el memo escribes: "Esto conecta con la teoría de la colonización del hogar de X autor. El espacio doméstico ya no es refugio."
4. 📦 La Caja de Exportación (Organización final)
Cuando terminas de leer y codificar, la app toma todo tu trabajo (el texto original + tus códigos + tus memos) y lo escupe en un archivo CSV (para Excel) o JSON. Ya no tienes un caos de notas sueltas, tienes una base de datos estructurada lista para buscar patrones, hacer matrices o escribir tu capítulo de resultados.
¿Para qué sirve esto en tu investigación? (El valor metodológico)
Mientras que la máquina (aec.py) cuenta palabras y detecta temas generales, la máquina no entiende el dolor, la ironía, el contexto cultural ni los silencios.
cod.py sirve para proteger y organizar tu pensamiento analítico humano. Te obliga a leer con calma, a enfrentar el texto, a asignarle significado (codificar) y a reflexionar sobre ese significado (memos). Es la herramienta que garantiza que tu tesis no sea solo un reporte estadístico, sino una interpretación hermenéutica profunda.
En resumen: cod.py es tu asistente de laboratorio que te limpia el texto, te pasa las "muestras" (párrafos) una por una, y te guarda meticulosamente todas las anotaciones que haces en tu cuaderno de campo.

# para correr la app usar:    streamlit run cod.py

# Baremación
Sí, este nuevo código no solo cumple con el texto, sino que es una versión significativamente mejor y más completa que el anterior.
La diferencia clave y más importante es que este código sí implementa explícitamente el "Paso 7: La tabla de baremo", el cual el texto describe como "el producto final", algo que el código anterior solo mencionaba en los comentarios pero no ejecutaba.
A continuación, te detallo punto por punto cómo este código se alinea perfectamente con la metodología del texto:
1. Correspondencia Exacta con los 7 Pasos del Texto
Paso 1 (Recodificación): El código aplica la fórmula exacta mencionada en el texto: (Máximo + Mínimo) - Respuesta, que en una escala de 1 a 9 se traduce correctamente como 10 - valor.
Paso 2 (Confiabilidad): Incluye la función matemática precisa del Alfa de Cronbach basada en las varianzas, y la aplica a los tres factores por separado, tal como exige el texto antes de proceder a sumar.
Paso 3 (Puntaje Bruto): Suma los 4 ítems de cada factor, generando los rangos esperados (de 4 a 36).
Pasos 4 y 5 (Norma y Puntuación T): Calcula la media y la desviación estándar de la muestra normativa. Luego aplica la transformación lineal exacta descrita:

  Z=(Bruto−Media)/DE y 
  T=50+(10∗Z)
  
Paso 6 (Percentil): Utiliza scipy.stats.percentileofscore, que es la implementación computacional correcta del concepto textual de "contar a los que quedaron detrás de ti".
Paso 7 (Tabla de Baremo): 🌟 Esta es la gran mejora. El código usa df.groupby('bruto_estrategias').agg(...) para generar una tabla de consulta real que asocia cada puntaje bruto con su Puntuación T y Percentil promedio. Esto materializa exactamente lo que el texto pide: "una tabla que convierte cada puntaje bruto en su percentil y su T, para que cualquier usuario del instrumento interprete un resultado sin recalcular nada".
Caso Práctico: Replica el ejemplo de la maestra con 35 puntos, calculando su T y percentil, e imprime la conclusión interpretativa ("autoeficacia alta... en comparación con su grupo") que cierra el texto.
3. Mejoras de Legibilidad y Buenas Prácticas (Respecto al código anterior)
Comentarios Didácticos: Incluye la fórmula comentada # Fórmula: (Máximo + Mínimo) - Respuesta, lo cual es excelente para la trazabilidad en investigación.
Salidas por Consola (Prints): Cada paso imprime un mensaje de confirmación (✅ Paso X:...), lo que hace que el script sea mucho más fácil de auditar y entender cuando se ejecuta.
Docstring en la función: La función de Cronbach ahora tiene una descripción ("""Calcula el Alfa..."""), siguiendo buenas prácticas de programación científica.
4. Única Observación Técnica (Menor)
El texto menciona de pasada la diferencia entre la Puntuación T lineal (la que usa el código) y la Puntuación T normalizada (que se deriva del percentil en una curva normal). El código implementa la T lineal, lo cual es correcto y suficiente, ya que el texto mismo indica que para distribuciones simétricas "las dos dan casi lo mismo" y utiliza la T lineal para el ejemplo principal de la maestra (dando 62.6 / 63).
Conclusión para tu Investigación
Dado que estás involucrado en la construcción de instrumentos de medición a nivel avanzado, este segundo script es el que debes usar como plantilla base. Es metodológicamente riguroso, está completamente alineado con la Teoría Clásica de los Tests descrita en el texto, y entrega el "producto final" real (la tabla de baremo) que necesitas para interpretar los datos de tus futuros participantes.
# para correr usar: python barem1.py

recuerde modificar para leer un archivo, este codigo solo simula las mediciones: ver video https://youtu.be/9WpN88VvF2s 

# Conversión  cualitativo a cuantitativo

Este código es un ejemplo perfecto y práctico de Métodos Mixtos Formales (específicamente, la estrategia de Conversión de datos cualitativos en cuantitativos, mencionada en la sección 6.4 del documento).
Su objetivo es tomar categorías que surgieron de tu análisis cualitativo (palabras) y transformarlas en números (0 y 1) para poder usarlas en una fórmula estadística y ver si predicen un resultado numérico.
A continuación, te explico el código paso a paso, desglosando qué hace la computadora y qué significa metodológicamente:

$\color{blue}{\text{1. Sección 0: Los Datos Originales
python
data original = {
    'docente': ['Docente 1', ...],
    'años_experiencia': [5, 20, 2, 15, 25, 8], # Variable Cuantitativa
    'estrategia_adaptacion': ['Integracion_Real', 'Cumplimiento_Aparente', ...] # Variable Cualitativa
}}$

Qué hace: Crea una tabla con datos simulados.
Significado metodológico: Representa el estado de tus datos después de usar tu herramienta cod.py. Tienes una variable numérica (años_experiencia) y una variable de texto (estrategia_adaptacion) que son las categorías o temas que tú mismo descubriste en las entrevistas.
2. Sección 1: La Conversión (Variables Dummy)
python
df_dummies = pd.get_dummies(df_original['estrategia_adaptacion'], prefix='cod', drop_first=False, dtype=int)
Qué hace: Toma la columna de texto y crea una columna nueva por cada categoría única que encuentra (cod_Cumplimiento_Aparente, cod_Integracion_Real, cod_Resistencia_Declarada). Si el docente pertenece a esa categoría, pone un 1; si no, pone un 0. El dtype=int asegura que sean números enteros (solucionando el error que vimos antes).
Significado metodológico: Esto se llama codificación en variables dummy (o indicadoras). Es el puente que permite que la estadística "entienda" las categorías cualitativas. La estadística no puede multiplicar la palabra "Resistencia", pero sí puede multiplicar un 1 o un 0.
3. Sección 2: Integración en el Modelo (El corazón del Método Mixto)
python
X = df_mixto[['cod_Cumplimiento_Aparente', 'cod_Resistencia_Declarada']]
y = df_mixto['años_experiencia']
X_const = sm.add_constant(X) 
modelo = sm.OLS(y, X_const).fit()
Qué hace: Configura una Regresión Lineal Ordinaria (OLS).
y es lo que queremos predecir (años de experiencia).
X son los predictores. Nota crucial: Observa que solo incluimos dos de las tres columnas dummy.
Significado metodológico (La Categoría de Referencia): Al dejar fuera cod_Integracion_Real de la variable X, la estamos convirtiendo automáticamente en el Grupo Base o de Referencia. El modelo estadístico no calculará un número para "Integración Real"; en su lugar, calculará cuántos años de experiencia más o menos tienen los otros grupos en comparación con este grupo base. Es como establecer el "nivel del mar" (cero) para medir la altura de las montañas.
4. Sección 3: Extracción e Interpretación Dinámica
python
coef_cump = modelo.params['cod_Cumplimiento_Aparente']
pval_cump = modelo.pvalues['cod_Cumplimiento_Aparente']
promedio_base = df_original[df_original['estrategia_adaptacion'] == 'Integracion_Real']['años_experiencia'].mean()
Qué hace: Saca los números crudos del modelo: los coeficientes (el efecto), los p-valores (la significancia) y calcula el promedio real del grupo base para tener contexto.
Significado metodológico: Traduce la "caja negra" de la estadística a lenguaje humano.
El coeficiente te dice la magnitud de la diferencia (ej. "+12.5 años").
El p-valor te dice si puedes confiar en ese número o si probablemente sea solo azar (en ciencias sociales, usualmente buscamos p < 0.05).
5. Sección 4: La Conclusión (Lista para tu Tesis)
python

1
Qué hace: Usa "f-strings" de Python para insertar los números calculados directamente en una frase con sentido.
Significado metodológico: Esto te ahorra tener que interpretar los números manualmente y evita errores humanos. Genera una frase de resultado lista para ser copiada, adaptada y defendida en tu capítulo de "Resultados Mixtos" o "Discusión".
💡 ¿Cómo leer el resultado que te dará este código?
Cuando lo ejecutes, verás algo como esto:
Coeficiente de 'Cumplimiento Aparente': 12.50 años (p-valor: 0.182)
Grupo de referencia (Base): 'Integracion_Real' (Promedio: 5.0 años)
Tu interpretación como investigador debe ser:
"Los docentes que mostraron una 'Integración Real' tienen en promedio 5 años de experiencia. En comparación con ellos, los docentes que mostraron un 'Cumplimiento Aparente' tienen 12.5 años más de experiencia (es decir, promedian 17.5 años). Sin embargo, el p-valor de 0.182 es mayor a 0.05, lo que indica que, en esta muestra tan pequeña (n=6), esta diferencia no es estadísticamente significativa y podría deberse al azar. Se requiere una muestra mayor para confirmar esta tendencia."
¿Por qué este código es una herramienta poderosa para tu investigación?
Porque materializa exactamente lo que pide el documento en el Nivel 6 (Métodos Mixtos): no te limitas a decir "algunos docentes se resisten y otros se integran". Ahora puedes afirmar (o refutar) con rigor estadístico si esa resistencia o integración está asociada sistemáticamente con variables como la antigüedad, la edad, el salario o el tamaño de la escuela. Eso eleva tu tesis de un nivel descriptivo a un nivel explicativo/predictivo.
