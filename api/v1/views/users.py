#!/usr/bin/python3
"""handles all default RESTFul API actions for User objects"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all user objects"""
    users = storage.all(User)
    user_list = []
    for user in users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    if data.get('email', None) is None:
        abort(400, 'Missing email')
    if data.get('password', None) is None:
        abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    for k, v in data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
