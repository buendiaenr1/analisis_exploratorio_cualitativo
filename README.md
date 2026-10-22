
# Análisis exploratorio cualitativo

# para correr aec.py usar:     python aec.py
# para correr cod.py usar:     streamlit run cod.py
# para correr barem.py usar:   python barem.py (modificar codigo para leer archivo)

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
Sí, el código en Python implementa de manera fiel y exacta la metodología descrita en el texto.
El script traduce a código los "Fundamentos de Baremación y Análisis de Instrumentos" paso a paso, aplicando la lógica de la Teoría Clásica de los Tests (TCT) sobre una escala tipo Likert tratada como variable de intervalo, tal como se explica en la transcripción.
A continuación, te detallo cómo el código refleja cada una de las secciones del texto:
1. Correspondencia Paso a Paso
Preparación (Simulación): El texto menciona trabajar con una "base de práctica de doscientos docentes" y la escala TSES de 12 ítems (agrupados en 3 factores, escala de 1 a 9). El código configura exactamente este escenario usando numpy y pandas (n_docentes = 200, 12 columnas, valores aleatorios del 1 al 9).
Paso 1: Recodificar ítems inversos: El texto explica la fórmula (máximo + mínimo) - respuesta. En una escala de 1 a 9, esto es 10 - respuesta. El código lo implementa correctamente (10 - df['item2_original']). Nota didáctica: Aunque el texto aclara que la escala TSES original no tiene ítems inversos, el código simula uno (el ítem 2) para dejar constancia de cómo se programa este paso, lo cual es una excelente práctica académica.
Paso 2: Confiabilidad (Alfa de Cronbach): El código incluye una función personalizada (calcular_alpha_cronbach) que aplica la fórmula matemática estándar del Alfa de Cronbach para los tres factores, cumpliendo con el requisito de confirmar la consistencia interna antes de sumar.
Paso 3: Puntaje Bruto: Tal como indica el texto ("Sumas los cuatro ítems de cada factor"), el código usa .sum(axis=1) para generar las columnas de puntajes brutos.
Pasos 4 y 5: Construir la norma, Zeta y T: El código calcula la media (mean()) y la desviación estándar (std()) de la muestra normativa. Luego aplica las fórmulas exactas mencionadas en el texto:
Zeta: (Bruto - Media) / Desviación
Puntuación T: 50 + (10 * Zeta)
Paso 6: Percentil: Utiliza scipy.stats.percentileofscore, que es la forma estándar en Python para calcular el rango percentil (el porcentaje de personas que quedaron por debajo de un puntaje).
2. El Caso Práctico (La maestra con puntaje 35)
El texto dedica una sección a interpretar el caso de una maestra que obtiene 35 puntos en Estrategias de Instrucción. El código tiene un bloque final (CASO PRÁCTICO DEL TEXTO) dedicado exclusivamente a esto:
Toma el puntaje bruto de 35.
Calcula su Puntuación T y su Percentil usando los parámetros de la muestra simulada.
Imprime una conclusión interpretativa que coincide con el mensaje del texto: "La maestra muestra una autoeficacia alta... en comparación con su grupo de referencia".
3. Pequeñas diferencias (Adaptaciones propias de la programación)
Hay dos detalles menores donde el código se adapta a la ejecución en Python, sin perder el rigor metodológico:
Valores dinámicos vs. valores del texto: El texto menciona cifras específicas para la muestra (ej. Media = 29.1, Desviación = 4.7). Como el código genera los datos aleatoriamente (aunque con una semilla fija np.random.seed(42) para que sea reproducible), los valores exactos de la media y la desviación estándar variarán ligeramente. Sin embargo, la lógica matemática es idéntica.
Enfoque en el Factor 1: El código aplica la transformación completa a Z, T y Percentil principalmente al Factor 1 (Estrategias) para la vista previa y el caso práctico. Esto es coherente con el guion del texto, que usa ese factor para explicar el ejemplo de la maestra de los 35 puntos.
Conclusión
Como investigador a nivel de doctorado que busca construir y validar instrumentos de medición, puedes tener la certeza de que este script es una plantilla metodológicamente sólida. Captura la esencia de la baremación normativa: demostrar que un puntaje crudo (35/36) solo cobra significado estadístico y práctico cuando se contrasta contra la distribución de una muestra de referencia mediante Puntuaciones T y Percentiles.

# para correr usar: python barem.py

recuerde modificar para leer un archivo, este codigo solo simula las mediciones: ver video https://youtu.be/9WpN88VvF2s 
