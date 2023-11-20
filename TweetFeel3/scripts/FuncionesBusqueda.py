

import json
from twscrape import API
import asyncio
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
def tweetTOjson(tweet):
    return ({
                        'content' : tweet.rawContent,
                        'user_name': tweet.user.username,
                        #'user_followers ': tweet.user.friendsCount,
                        #'user_following_count ': tweet.user.followersCount,
                        #'user_total_tweets ': tweet.user.statusesCount,
                        #'user_description ': tweet.user.rawDescription,
                        #'user_url ': tweet.user.url,
                        #'user_screen_name ': tweet.user.displayname.lower(),
                        #'user_image ': tweet.user.profileImageUrl.replace('_normal', '_bigger'),
                        #'user_ratio ': get_ratio(tweet.user.friendsCount, tweet.user.followersCount),
                        "created" : tweet.date,
                        'id_tweet': int(tweet.id),
                        'retweet_count': int(tweet.retweetCount),
                        'reply_count': int(tweet.replyCount),
                        'like_count': int(tweet.likeCount),
                        'quote_count': int(tweet.quoteCount),
                        #'favorite_count ': tweet.user.favouritesCount,
        })
def get_ratio(followers, following):
    try:
        ratio = followers/following
        return round(ratio, 2)
    except:
        return 0
async def relog_accounts(api):
    await api.pool.delete_accounts("EnzoElAuditor")
    await api.pool.delete_accounts("FitoElAuditor")
    await api.pool.delete_accounts("MaximoTpoSem")
    await api.pool.delete_accounts("tposeminario2023")
    await api.pool.delete_accounts("MaximoTpoSeminario")
    await api.pool.delete_accounts("FitoElAuditor")
    await api.pool.delete_accounts("kekogomez389008")
    await api.pool.add_account("MaximoTpoSem", "tposeminario2023", "maximotposeminario@gmail.com", "tposeminario2023")
    await api.pool.add_account("kekogomez389008", "A46538857a", "kekogomez302@gmail.com", "A446538857a")
    await api.pool.add_account("Daniela78982071", "TpSeminario1234", "danielatpseminario@gmail.com", "Abcd1234Abcd1")
    #pepetw0504@gmail.com ; pepe_123 : @pepetw0504 : pepe_123
    await api.pool.add_account("pepetw0504", "pepe_123","pepetw0504@gmail.com","pepe_123" )
    #danielatpseminario@gmail.com ; Abcd1234Abcd1 : Daniela78982071  : TpSeminario1234
    #await api.pool.add_account("EnzoElAuditor", "EA0715TCPJ", "EmpeladoAuditorEnzo@gmail.com", "EA0715CPJ")
    #await api.pool.add_account("FitoElAuditor", "EA0716TCPJ", "EmpeladoAuditorFito@gmail.com", "EA0716CPJ")
    await api.pool.login_all()
    print(await api.pool.accounts_info())
async def Buscar_Palabra_Perfil(api, keyword,fecha_i,fecha_f,perfil, max_tweets=000):
    tweets = []
    async for tweet in api.search(keyword+" from:"+perfil+" since:"+fecha_i+" until:"+fecha_f, limit=max_tweets): 
        tweets.append(tweetTOjson(tweet))
    return tweets
async def Buscar_Palabra_Fechas(api, keyword,fecha_i,fecha_f, max_tweets=10):
    tweets = []
    async for tweet in api.search(keyword+" since:"+fecha_i+" until:"+fecha_f+" filter:has_engagement lang:es OR lang:en", limit=max_tweets): 
        tweets.append(tweetTOjson(tweet))
    return tweets
async def Buscar_Querry(api, q, max_tweets=100):
    tweets = []
    async for tweet in api.search(q,limit=max_tweets):
        tweets.append(tweetTOjson(tweet))
    return tweets

async def search_recent_tweets(api, keyword, max_tweets=100):
    tweets = []
    async for tweet in api.search(keyword, limit=max_tweets):
        tweets.append(tweetTOjson(tweet))
    return tweets

def Reloggear():
    api = API()
    asyncio.run(relog_accounts(api))

def BuscarMasRecientes(keyword,max_tweets=100):
    api = API()
    tweets = asyncio.run(search_recent_tweets(api, keyword, max_tweets))
    return tweets

def BuscarPalabraFechas(keyword,fecha_i,fecha_f,max_tweets=10): # fecha_i,fecha_f formato 2023-05-31
    api = API()
    tweets = asyncio.run(Buscar_Palabra_Fechas(api, keyword,fecha_i,fecha_f, max_tweets))
    return tweets

def BuscarPalbraPerfil(keyword,fecha_i,fecha_f,perfil,max_tweets=100): # fecha_i,fecha_f formato 2023-05-31
    api = API()
    tweets = asyncio.run(Buscar_Palabra_Perfil(api, keyword,fecha_i,fecha_f,perfil, max_tweets))
    return tweets

#if __name__ == "__main__":
    Reloggear()
    dictionary =BuscarMasRecientes("Mucha Sangre",10)
    print(len(dictionary))
    json_object = json.dumps(dictionary, indent=12)
 
    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)





#BuscarPalabraFechas("Nike","2022-11-01","2023-11-11",["es"],max_tweets=10)