import twscrape
import json
import scripts.FuncionesBusqueda as FB

def initi():
    FB.Reloggear()
    

def scrape_tweets(brand_name):
    tweets =  FB.BuscarPalabraFechas("+"+brand_name, "2023-01-01", "2023-11-11", 10)
    return tweets

def save_tweets_to_json(tweets, filename):
    with open(filename, "w") as f:
        json.dump(tweets, f)


