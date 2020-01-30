#!/usr/bin/python3
"""Create a new view for Amenity objects that handles
 all default RestFul API actions"""


from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity

app = Flask(__name__)


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all amenity objects"""
    amenity_list = []
    for amenity in storage.all('Amenity').values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id=None):
    """Retrieves a State object with the id linked to it"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Deletes a state object"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an amenity object"""
    json_file = request.get_json()
    if not json_file:
        abort(400, {"Not a JSON"})
    if 'name' not in json_file:
        abort(400, {"Missing name"})
    amenity = Amenity(name=json_file['name'])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id=None):
    """Updates a state object"""
    json_file = request.get_json()
    if not json_file:
        abort(400, {"Not a JSON"})
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    for key, value in json_file.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
