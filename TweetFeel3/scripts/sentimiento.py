import nltk
from textblob import TextBlob
import langdetect
# Importar los clasificadores de sentimiento
 
from deep_translator import GoogleTranslator

# Use any translator you like, in this example GoogleTranslator

# Definir una función para analizar el sentimiento de un texto
def analizar_sentimiento(texto):
    if texto == None:
        texto=""
    texto = GoogleTranslator(source='auto', target='en').translate(texto)
    # Crear un objeto TextBlob
    blob = TextBlob(texto)

    # Obtener el sentimiento
    sentimiento = blob.sentiment.polarity

    # Determinar la polaridad del sentimiento
    if sentimiento > 0:
        resultado = "Positivo"
    elif sentimiento < 0:
        resultado = "Negativo"
    else:
        resultado = "Neutral"

    return resultado

