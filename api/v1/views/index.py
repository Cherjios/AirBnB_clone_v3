#!/usr/bin/python3
"""status route"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

app = Flask(__name__)


@app_views.route('/status', methods=['GET'])
def status():
    """ return a JSON """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """ Retrives the number of each objects by type:"""
    o = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
        }
    o = {k: storage.count(v) for k, v in o.items()}
    return jsonify(o)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
