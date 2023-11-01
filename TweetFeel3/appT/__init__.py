from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#import models


app = Flask(__name__)

from flask_login import LoginManager
from flask import Flask
import appT.models as models
import appT.routes as routes
from appT.models import db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:luciotruco99@localhost:4200/tweetfeel2'
app.config['SECRET_KEY'] = "lacucaracha"
app.register_blueprint(models.bp)
app.register_blueprint(routes.bp)
db.init_app(app)




if __name__ == "__main__":
    app.run(debug=True)
