#!/usr/bin/python3

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

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True, debug='true')
