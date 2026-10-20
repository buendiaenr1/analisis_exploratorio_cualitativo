
# Análisis exploratorio cualitativo
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
