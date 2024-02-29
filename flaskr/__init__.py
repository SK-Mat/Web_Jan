from flask import Flask
app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedalta(minutes=3)#session time（10分）
import flaskr.main
