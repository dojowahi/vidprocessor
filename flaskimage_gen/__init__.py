from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '28209de4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youtube.db'
db = SQLAlchemy(app)

from flaskimage_gen import routes