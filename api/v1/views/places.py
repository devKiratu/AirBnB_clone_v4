#!/usr/bin/python3
"""
View for Place objects that handles all default RESTful API
"""
from flask import jsonify, request, make_response, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """
    Retrieves all places for a given city

    Args:
        city_id (str): Identifies a city

    Returns:
        places JSON: All the places found in specified city

    Raises:
        status 404: If the `city_id` is not linked to any city
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return (jsonify(places), 200)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """
    Retrieves a Place object

    Args:
        place_id: String ID for a given place

    Returns:
        place JSON: The place

    Raises:
        status 404: If the `place_id` is not linked to any place
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return (jsonify(place.to_dict()), 200)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object

    Args:
        place_id: String ID of place to delete

    Returns:
        Empty dictionary if successful

    Raises:
        Status 200 if success
        Status 404 if `place_id` is not linked to any place
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    place.delete()
    storage.save()

    return (jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place object

    args:
        city_id: String ID for city within which to create place

    Returns:
        New place if success
        'Not a JSON': If the HTTP request body is not valid JSON
        'Missing user_id': If the dictionary doesn’t contain the key `user_id`
        'Missing name': If the dictionary doesn’t contain the key `name`

    Raises:
        Status 201 if success
        Status 404: If the `city_id` is not linked to any city
        Status 404: If the `user_id` is not linked to any User object
        Status 400: If the HTTP request body is not valid JSON
        Status 400: If the dictionary doesn’t contain the key `user_id`
        Status 400: If the dictionary doesn’t contain the key `name`
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    # Check if request body is valid JSON
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    place_data = request.get_json()

    # Check if dictionary contains key user_id
    if place_data.get('user_id') is None:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    # Ensure user_id is linked to User object
    user_id = place_data.get('user_id')

    if storage.get(User, user_id) is None:
        abort(404)

    # Check if request data has name attribute
    if place_data.get('name') is None:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new_place = Place(**place_data)
    # new_place.city_id = city.id
    new_place.save()

    return (jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates a place object

    Args:
        place_id (str): ID of place to update

    Raises:
        Status 200: If success
        Status 404: If `place_id` is not linked to any Place
        Status 400: If the HTTP request body is not valid JSON

    Returns:
        Place if success
        'Not a JSON': f the HTTP request body is not valid JSON
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    place_data = request.get_json()

    for key, value in place_data.items():
        options = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        if key not in options:
            setattr(place, key, value)

    storage.save()

    return (jsonify(place.to_dict()), 200)
