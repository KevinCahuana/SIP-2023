import twscrape
import json
import scripts.FuncionesBusqueda as FB

def initi():
    FB.Reloggear()
    

def scrape_tweets(brand_name):
    tweets =  FB.BuscarPalabraFechas("+manaos", "2023-01-01", "2023-09-29_02:00:00_UTC", 200)
    return tweets

def save_tweets_to_json(tweets, filename):
    with open(filename, "w") as f:
        json.dump(tweets, f)

if __name__ == "__main__":
    brand_name = input("Enter the brand name to scrape tweets for: ")

    tweets = scrape_tweets(brand_name)

    filename = f"tweets/{brand_name}.json"
    save_tweets_to_json(tweets, filename)

    print(f"Successfully saved tweets to {filename}")
