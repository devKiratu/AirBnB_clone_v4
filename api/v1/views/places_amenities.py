#!/usr/bin/python3
"""
View for link between Place objects and Amenity
objects that handles all default RESTful API actions
"""
from flask import jsonify, abort
from os import getenv
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views

storage_type = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves list of all Amenity objects of a place

    Args:
        place_id (str): Identifies a place

    Returns:
        List of all Amenity objects

    Raises:
        status 404: If the place_id is not linked to any Place
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if storage_type == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, a_id).to_dict()
                     for a_id in place.amenity_ids]

    return (jsonify(amenities), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object

    Args:
        place_id (str): ID of Place with amenity
        amenity_id (str): ID of Amenity to remove

    Returns:
        Empty dictionary if successful

    Raises:
        Status 200 if success
        Status 404 if place_id is not linked to any Place object,
        or if the amenity_id is not linked to any Amenity object,
        or if the Amenity is not linked to the Place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if storage_type == "db":
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)

    amenity.delete()
    storage.save()

    return {}


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Links a Amenity object to a Place object

    Args:
        place_id (str): ID of Place to link to
        amenity_id (str): ID of Amenity to link

    Raises:
        Status 200: If amenity is already linked
        Status 201: If success
        Status 404 if place_id is not linked to any Place object,
        or if the amenity_id is not linked to any Amenity object,

    Returns:
        Amenity object if success
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if storage_type == "db":
        # Check if amenity already linked
        if amenity in place.amenities:
            return (jsonify(amenity.to_dict()), 200)
        else:
            # Link amenity
            place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_ids:
            return (jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity.id)

    storage.save()

    return (jsonify(amenity.to_dict()), 201)
