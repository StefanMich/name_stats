from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object('default_settings')

CORS(app)
