
# Análisis exploratorio cualitativo
# para correr cod.py usar:     streamlit run cod.py

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

