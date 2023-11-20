import twscrape
from appT.models import Tweet, Brand
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_tweets_by_brand(brand_id):
    """Obtiene todos los tweets asociados a una marca.

    Args:
        brand_id (int): El ID de la marca.

    Returns:
        list[Tweet]: Una lista de tweets.
    """

    brand = Brand.query.get(brand_id)
    tweets = Tweet.query.filter_by(brand_id=brand.id).all()
    return tweets

def analyze_sentiment(tweets):
    """Analiza el sentimiento en los tweets.

    Args:
        tweets (list[Tweet]): Una lista de tweets.

    Returns:
        dict[str, float]: Un diccionario que representa la distribución de los sentimientos en los tweets.
    """

    sentiment_analyzer = SentimentIntensityAnalyzer()
    sentiment_distribution = {}
    for tweet in tweets:
        sentiment = sentiment_analyzer.polarity_scores(tweet.text)
        for sentiment_type, score in sentiment.items():
            if sentiment_type not in sentiment_distribution:
                sentiment_distribution[sentiment_type] = 0.0
            sentiment_distribution[sentiment_type] += score

    # Normalizamos los valores de la distribución de sentimientos
    for sentiment_type in sentiment_distribution:
        sentiment_distribution[sentiment_type] /= len(tweets)

    return sentiment_distribution


def filter_tweets(tweets, start_date=None, end_date=None, sentiment=None):
    filtered_tweets = tweets

    if start_date and end_date:
        filtered_tweets = [tweet for tweet in filtered_tweets if start_date <= tweet.created_at <= end_date]

    if sentiment:
        filtered_tweets = [tweet for tweet in filtered_tweets if tweet.sentiment == sentiment]

    return filtered_tweets


from openai import OpenAI

def Filter_Tweet(tweet,NombreMarca,descripcion):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        #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 -key kevin
        #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 - key mia
        api_key="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",
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                Tu trabajo será filtrar tweets que no tienen que ver con una marca.
                Marca: {NombreMarca}.
                Descripción de la marca:  {descripcion}
                Determina si un tweet habla de alguna manera de la marca {NombreMarca}. 
                Tweet : “ {tweet}”.
                Menciones indirectas también cuentan como validas
                Si tiene que ver con {NombreMarca} responder SI.
                Si no tiene que ver con {NombreMarca} responder NO.
                Solo puedes responder SI o NO.
                Ninguna otra respuesta es aceptada.
                """,
            }
        ],
        model="gpt-3.5-turbo",
    )
    print("Tweet ")
    print(tweet)
    print("respuesta")
    print(chat_completion.choices[0].message.content)
    # Extract the sentiment from the response
    filtrado = chat_completion.choices[0].message.content.strip()

    if filtrado == "SI":
        return True
    else:
        return False

