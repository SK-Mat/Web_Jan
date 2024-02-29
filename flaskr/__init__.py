from flask import Flask
from datetime import timedelta
app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=3)#session time（10分）
import flaskr.main
