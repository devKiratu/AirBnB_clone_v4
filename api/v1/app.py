#!/usr/bin/python3
""" Web server endpoint """
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from os import environ
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# Global strict slashes
# app.url_map.strict_slashes = False


@app.teardown_appcontext
def tear_down(error=None):
    """ Close storage connection """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    # Define host and port environment variables
    host = environ.get('HBNB_API_HOST', "0.0.0.0")
    port = environ.get('HBNB_API_PORT', 5000)

    app.run(host=host, port=port, threaded=True)
