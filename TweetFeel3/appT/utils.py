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
