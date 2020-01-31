#!/usr/bin/python3
"""Flask Module for a web application"""

from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": '0.0.0.0'}})

@app.teardown_appcontext
def teardown(self):
    """closes all storage sessions"""
    storage.close()


@app.errorhandler(404)
def page_404(self):
    """returns a message not found on 404 error"""
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST') or '0.0.0.0',
            port=getenv('HBNB_API_PORT') or 5000, threaded=True)
