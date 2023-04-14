#!/usr/bin/python3
"""create a variable app, instance of Flask"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

# Register the app_views blueprint to the app instance
app.register_blueprint(app_views)

# Declare a method to handle the teardown_appcontext event
@app.teardown_appcontext
def close_storage(error):
    """Close the storage connection after the app context is torn down."""
    storage.close()

@app.errorhandler(404)
    """404 Error"""
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")

    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5001'

    app.run(host=host, port=port, threaded=True, debug='true')
