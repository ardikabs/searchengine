
import json

from flask import Flask, request, jsonify, abort, url_for, session
from flask_cors import CORS

import config
APP_SETTINGS = config.DevelopmentConfig

app = Flask(__name__,static_folder='static')
app.config.from_object(APP_SETTINGS)
CORS(app)


@app.route('/')
def index():
    return jsonify({"message":"Search Engine API by ardikabs"})

from api.views import api
app.register_blueprint(api)