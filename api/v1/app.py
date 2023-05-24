#!/usr/bin/python3
"""Main Flask App"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)

CORS(app, resources={r"/*": {"origins": '0.0.0.0'}})


@app.errorhandler(404)
def not_found(e):
    """returns a JSON"reponse if there is an error 404"""
    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def close_session(self):
    """Close the SQLAlchemy session of the request or reload the json"""
    storage.close()


if (__name__ == "__main__"):
    ip = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')

    if (not ip):
        ip = '0.0.0.0'
    if (not port):
        port = '5000'

    app.run(host=ip, port=port, threaded=True, debug=True)  # Remove debug
