#!/usr/bin/python3
"""Create a new view for State objects that handles
 all default RestFul API actions"""


from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State
app = Flask(__name__)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all state objects"""
    state_list = []
    for state in storage.all('State').values():
        state_list.append(state.to_dict())
    return jsonify(state_list), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """Retrieves a State object with the id linked to it"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """Deletes a state object"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a state object"""
    json_file = request.get_json()
    if not json_file:
        abort(400, {"Not a JSON"})
    if 'name' not in json_file:
        abort(400, {"Missing name"})
    state = State(name=json_file['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """Updates a state object"""
    json_file = request.get_json()
    if not json_file:
        abort(400, {"Not a JSON"})
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    for key, value in json_file.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
