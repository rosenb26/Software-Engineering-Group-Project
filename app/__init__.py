from flask import Flask
from flask_bootstrap import Bootstrap5
from config import Config

app = Flask(__name__)  
app.config.from_object(Config)
bootstrap = Bootstrap5(app) 

from app import routes