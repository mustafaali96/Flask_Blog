from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
# from flask_bcrypt import flask_bcrypt
from flask_wtf.csrf import CSRFProtect



app=Flask(__name__)
app.config['SECRET_KEY'] =  '904fa3ab6c1f1f631645d7b62faf0f03'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flaskblog import routes
