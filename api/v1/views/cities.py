#!/usr/bin/python3
"""View for handling default RESTful API actions for City objects"""
from flask import jsonify, request, make_response, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """Retrieves all cities for a given state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieves a City Object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    if data.get('name', None) is None:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    city = City(**data)
    city.state_id = state.id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    for k, v in data.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict())
