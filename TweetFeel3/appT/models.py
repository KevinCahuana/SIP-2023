from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Blueprint
from datetime import datetime
#db = SQLAlchemy()

#bp = Blueprint("models", __name__)

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Blueprint

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))  # Almacena el hash de la contraseña

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        if password==self.password:
            return True
        else:
            return False
    @staticmethod
    def get(user_id):
        return User.query.get(int(user_id))



# Resto del código de tu archivo models.py






   # brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))  # Definir la clave foránea

    # Define la relación entre User y Brand
    #brand = db.relationship('Brand', back_populates='users')


class Tweet(db.Model):
    __tablename__ = "tweets"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_name = db.Column(db.Text)
    tweet_id = db.Column(db.BigInteger, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sentiment = db.Column(db.String(255))
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    reply_count = db.Column(db.Integer, default=0)
    retweet_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    quote_count = db.Column(db.Integer, default=0)
    
    
    #brand = db.relationship('Brand', back_populates='tweets')
    
class Brand(db.Model):
    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


    # Define la relación inversa entre Brand y User
    #users = db.relationship('User', back_populates='brand')
    
class UserBrand(db.Model):
    __tablename__ = "user_brands"
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    brand_id=db.Column(db.Integer, db.ForeignKey("brands.id"), primary_key=True)
    



bp = Blueprint("models", __name__)