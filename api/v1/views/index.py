#!/usr/bin/python3
"""
Index view
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/status", methods=['GET'])
def status():
    """
    Get status of web server
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def count_objects():
    """
    An endpoint that retrieves the number of each objects by type
    """
    counts = {}
    objects = {'amenities': Amenity, 'cities': City, 'places': Place,
               'reviews': Review, 'states': State, 'users': User}

    for key, value in objects.items():
        obj_count = storage.count(value)
        counts[key] = obj_count

    return jsonify(counts)
