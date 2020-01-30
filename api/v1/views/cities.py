#!/usr/bin/python3
"""Objects that handles all defaul RestFul API actions"""
from api.v1.views import app_views
from api.v1.views import *
from flask import jsonify, make_response, abort, request
from models import storage
from models.city import City

model = "City"
parent_model = "State"


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def get_cities(state_id):
    """GET /state api route"""
    return get_models(parent_model, state_id, "cities")


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """GET /city api route"""
    return get_model(model, city_id)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """DELETE /city api route"""
    return delete_model(model, city_id)



