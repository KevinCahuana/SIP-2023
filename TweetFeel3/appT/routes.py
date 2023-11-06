from flask import Flask, Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user

from appT.models import User, Brand, Tweet, db,UserBrand
from appT.utils import get_tweets_by_brand, analyze_sentiment
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.login import login_user
from flask_login import login_user
from flask_login import LoginManager


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
    #brands = UserBrand.query.filter_by(user_id=current_user.id).all()
    brands = Brand.query.join(UserBrand).filter(UserBrand.user_id == current_user.id).all()
    return render_template("brands.html", brands=brands)

# Ruta de tweets
@bp.route("/tweets/<int:brand_id>")
def tweets(brand_id):
    tweets = get_tweets_by_brand(brand_id)
    sentiment_distribution = analyze_sentiment(tweets)
    return render_template("tweets.html", tweets=tweets, sentiment_distribution=sentiment_distribution)

# Ruta de cierre de sesión
@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("routes.login"))

# Ruta para agregar una marca
@bp.route("/add-brand", methods=["POST"])
def add_brand():
    brand_name = request.form.get("brand_name")
    print(brand_name)

    # Verificar si la marca ya existe
    brand = Brand.query.filter_by(name=brand_name).first()
    if brand is None:
        brand = Brand(name=brand_name)
        db.session.add(brand)
        db.session.commit()

    # Crear una relación entre la marca y el usuario
    #print(UserBrand.query.all(),current_user.id,brand.id)
    #current_user.id!!!
    user_brands = UserBrand(user_id=current_user.id, brand_id=brand.id)
    db.session.add(user_brands)
    db.session.commit()

    # Redireccionar al usuario a su panel de marcas
    return redirect(url_for("routes.brands"))
