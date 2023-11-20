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

import openai
import os






from openai import OpenAI

def analyze_sentiment(text):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key="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",
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                Marca: Adidas. Descripción de la marca: Adidas es reconocida por sus innovadoras zapatillas deportivas. Analiza el siguiente tweet: " @albitonto10 @adidas Nike Todas las camisetas de esta temporada son recicladas Puma Todas las camisetas visitantes que sacan tienen un calendario en el pecho Es mi humilde opinión". Tu tarea consiste en determinar si el tweet hace alguna alusión a la marca Adidas. No es necesario que la marca se mencione explícitamente; incluso referencias indirectas son relevantes. Examina cuidadosamente las menciones y verifica si hay alguna conexión con Adidas. Si el tweet está relacionado con Adidas, responde con un claro "SÍ". En caso contrario, si el tweet no guarda relación con Adidas, responde con un inequívoco "NO".
                """,
            }
        ],
        model="gpt-3.5-turbo",
    )

    # Extract the sentiment from the response
    sentiment = chat_completion.choices[0].message.content

    return sentiment
    



#print(analyze_sentiment("@javier Massa es un hijo de puta"))