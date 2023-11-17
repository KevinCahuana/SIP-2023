from flask import Flask, Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from appT.utils import filter_tweets
from appT.models import User, Brand, Tweet, db,UserBrand
from appT.utils import get_tweets_by_brand, analyze_sentiment
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.login import login_user
from flask_login import login_user
from flask_login import LoginManager
import scripts.FuncionesBusqueda as FB
import scripts.sentimiento as sent
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
bp = Blueprint("routes", __name__)

from appT import app

login_manager = LoginManager()
login_manager.init_app(app)

# Configuración del login manager





@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Ruta de inicio de sesión
@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        #print(username)
        #print(password)

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('routes.brands'))
        else:
            error = "Invalid username or password."
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


# Ruta de registro
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        #load_user(user)
        #login_manager.user_loader(user)


        return redirect(url_for("routes.brands"))
    else:
        return render_template("register.html")

# Ruta de marcas
@bp.route("/brands")
def brands():
    #print('brands')
    #brands = UserBrand.query.filter_by(user_id=current_user.id).all()
    brands = Brand.query.join(UserBrand).filter(UserBrand.user_id == current_user.id).all()
    return render_template("brands.html", brands=brands)


# Ruta de cierre de sesión
@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("routes.login"))




# Ruta para agregar una marca
@bp.route("/add-brand", methods=["POST"])
def add_brand():
    
    from datetime import datetime, timedelta
    brand_name = request.form.get("brand_name")
    print(brand_name)

    # Verificar si la marca ya existe
    brand = Brand.query.filter_by(name=brand_name).first()
    if brand is None:

        brand = Brand(name=brand_name)
        db.session.add(brand)
        db.session.commit()
        #popular base de datos
        #FB.Reloggear()
        current_date = datetime.now()
        one_year_ago = current_date - timedelta(days=5)
        #current_date = current_date.strftime("%Y-%m-%d")
        #one_year_ago = one_year_ago.strftime("%Y-%m-%d")
        #current_date = str(current_date)
        #print(current_date)
        #one_year_ago = str(one_year_ago)
        #print(one_year_ago)
        tweets=[]
        
        for i in range(12, -1, -1):
            current_date = datetime.now()
            month_f= current_date - timedelta(days=i*30)
            month_i = current_date - timedelta(days=(i+1)*30)
            print("intervalo numero "+str(i))
            print(month_i)
            print(month_f)
            month_i = month_i.strftime("%Y-%m-%d")
            month_f = month_f.strftime("%Y-%m-%d")
            tweets = tweets+ FB.BuscarPalabraFechas("+"+brand_name, month_i, month_f, 5)

        #current_date = datetime.now()
        #five_ago = current_date - timedelta(days=5)
        #current_date = current_date.strftime("%Y-%m-%d")
        #five_ago = five_ago.strftime("%Y-%m-%d")
        #weets = tweets+ FB.BuscarPalabraFechas("+"+brand_name, five_ago, current_date, 3)



   
        for tweet in tweets:
            print('tweet')
            print(tweet)
            formato_deseado = "%Y-%m-%d %H:%M:%S %Z"  # Ejemplo: "2023-01-16 01:25:59 UTC"
            fecha_formateada = tweet['created'].strftime(formato_deseado)
            tweet = Tweet(
                text=tweet['content'],
                user_name=tweet['user_name'],
                tweet_id=int(tweet['id_tweet']),
                created_at=fecha_formateada,
                sentiment=sent.analizar_sentimiento(tweet['content']),
                brand_id=int(brand.id),
                #user_followers=tweet['user_followers'],
                reply_count=int(tweet['reply_count']),
                like_count=int(tweet['like_count']),
                quote_count=int(tweet['quote_count']), 
                retweet_count=int(tweet['retweet_count'])
            )
            print("contenido")
            print(tweet)
            db.session.add(tweet)
            db.session.commit()

    # Crear una relación entre la marca y el usuario
    #print(UserBrand.query.all(),current_user.id,brand.id)
    #current_user.id!!!
    user_brands = UserBrand(user_id=current_user.id, brand_id=brand.id)
    db.session.add(user_brands)
    db.session.commit()

    # Redireccionar al usuario a su panel de marcas
    return redirect(url_for("routes.brands"))


from flask import  render_template, request
from appT.utils import filter_tweets






def get_pie_chart_data(tweets):
    positive_count = len(list(filter(lambda tweet: tweet.sentiment == "Positivo", tweets)))
    negative_count = len(list(filter(lambda tweet: tweet.sentiment == "Negativo", tweets)))
    neutral_count = len(list(filter(lambda tweet: tweet.sentiment == "Neutral", tweets)))

    return {
        "datasets": [{"data": [positive_count, negative_count, neutral_count]}],
        "labels": ["Positivos", "Negativos", "Neutros"]
        
    }

def get_line_chart_data(tweets):
    dates = list(set(tweet.created_at.strftime('%Y-%m-%d') for tweet in tweets))
    dates.sort()

    positive_counts = []
    negative_counts = []
    neutral_counts = []

    for date in dates:
        positive_count = len(list(filter(lambda tweet: tweet.sentiment == 'Positivo' and tweet.created_at.strftime('%Y-%m-%d') == date, tweets)))
        negative_count = len(list(filter(lambda tweet: tweet.sentiment == 'Negativo' and tweet.created_at.strftime('%Y-%m-%d') == date, tweets)))
        neutral_count = len(list(filter(lambda tweet: tweet.sentiment == 'Neutral' and tweet.created_at.strftime('%Y-%m-%d') == date, tweets)))

        positive_counts.append(positive_count)
        negative_counts.append(negative_count)
        neutral_counts.append(neutral_count)

    return {
        "labels": dates,
        "datasets": [{
            "label": "Positivos",
            "data": positive_counts,
        }, {
            "label": "Negativos",
            "data": negative_counts,
        }, {
            "label": "Neutros",
            "data": neutral_counts,
        }],
    }



from datetime import datetime, timedelta
from flask import request

# ...

def apply_filters(tweets, start_date, end_date, selected_sentiments, priority_filter):
    filtered_tweets = tweets

    # Apply Date Range Filter
    if start_date and end_date:
        if type(start_date) is str:
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        if type(end_date) is str:  
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        print("dates")
        print(type(start_date))
        print(end_date)
        filtered_tweets = [tweet for tweet in filtered_tweets if start_date <= tweet.created_at <= end_date]

    # Apply Sentiment Filter
    if selected_sentiments:
        filtered_tweets = [tweet for tweet in filtered_tweets if tweet.sentiment in selected_sentiments]

    # Apply Priority Filter
    if priority_filter == "recent":
        filtered_tweets = sorted(filtered_tweets, key=lambda tweet: tweet.created_at, reverse=True)
    elif priority_filter == "popular":
        filtered_tweets = sorted(filtered_tweets, key=lambda tweet: tweet.like_count + tweet.retweet_count, reverse=True)

    return filtered_tweets

@bp.route('/brands/<int:brand_id>', methods=['GET', 'POST'])
def brand_tweets(brand_id):
    tweets = Tweet.query.filter_by(brand_id=brand_id).all()
    num_tweets=5
    if request.method == 'POST':
        # Get filter parameters from the form
        start_date = request.form.get('start_date') + " 00:00:00"
        end_date = request.form.get('end_date') + " 00:00:00"
        print(type(start_date))
        print(start_date)

        num_tweets = request.form.get('num_tweets') 
        
        print(type(start_date))
        if start_date == " 00:00:00":
            
            start_date =  (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            print(type(start_date))
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")

        if end_date == " 00:00:00":
            end_date =datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        # Convertir el string a un objeto datetime
        
        
        selected_sentiments = request.form.getlist('sentiments')
        if selected_sentiments == []:
            selected_sentiments = ['Positivo', 'Negativo', 'Neutral']

        priority_filter = request.form.get('priority_filter')
        if priority_filter == None:
            priority_filter = "popular"

        # Apply filters
        tweets = apply_filters(tweets, start_date, end_date, selected_sentiments, priority_filter)

    pie_chart_data = get_pie_chart_data(tweets)
    line_chart_data = get_line_chart_data(tweets)

    pie_chart_data = json.dumps(pie_chart_data)
    line_chart_data = json.dumps(line_chart_data)
    tweets = tweets[:int(num_tweets)]
    return render_template('tweets.html', tweets=tweets, pie_chart_data=pie_chart_data, line_chart_data=line_chart_data,brand_id=brand_id)

if __name__ == '__main__':
    app.run(debug=True)
