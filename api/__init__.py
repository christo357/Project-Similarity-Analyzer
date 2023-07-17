from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = '1640a705d17ca214dbd13336c7ca6f18f006c2c4'
app.config["MONGO_URI"] ='mongodb+srv://u2003060:AsEnfAyD8e8mbcTm@cluster0.y21rmtn.mongodb.net/College'

#setup mongodb
mongodb_client = PyMongo(app)
db = mongodb_client.db

from api import routes