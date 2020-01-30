#!/usr/bin/python3
"""Create a new view for Amenity objects that handles
 all default RestFul API actions"""


from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place

app = Flask(__name__)


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """ Returns all place objects """
    place_list = []
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    else:
        places = city.places
        for place in places:
            place_list.append(place.to_dict())
    return jsonify(place_list), 200


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id=None):
    """Retrieves a place object with the id linked to it"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id=None):
    """Deletes a place object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id=None):
    """Creates a Place"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    result = request.get_json()
    if result is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in result:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get('User', result['user_id'])
    if user is None:
        abort(404)
    if 'name' not in result:
        return jsonify({"error": "Missing name"}), 400
    place = Place(city_id=city_id)
    for key, value in result.items():
        setattr(place, key, value)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id=None):
    """Updates a state object"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    json_file = request.get_json()
    if json_file is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in json_file.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
