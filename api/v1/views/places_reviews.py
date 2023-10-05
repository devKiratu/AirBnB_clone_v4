#!/usr/bin/python3
""" View for Review object that handles all default RESTful API """
from flask import jsonify, request, make_response, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """
    Retrieves list of all review objects of a place

    Args:
        place_id (str): Identifies a place

    Returns:
        List of all review objects of a place

    Raises:
        status 404: If the city_id is not linked to any city
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return (jsonify(reviews), 200)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """
    Retrieves a Review object

    Args:
        review_id (str): Review id

    Returns:
        Review object

    Raises:
        status 404: If the review_id is not linked to any review
    """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return (jsonify(review.to_dict()), 200)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place_review(review_id):
    """
    Deletes a Review object

    Args:
        review_id (str): ID of review to delete

    Returns:
        Empty dictionary if successful

    Raises:
        Status 200 if success
        Status 404 if review_id is not linked to any review
    """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    review.delete()
    storage.save()

    return (jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review object

    args:
        place_id (str): Place ID to create place

    Returns:
        New Review if success
        'Not a JSON': If the HTTP request body is not valid JSON
        'Missing user_id': If the dictionary doesn’t contain the key user_id
        'Missing text': If the dictionary doesn’t contain the key text

    Raises:
        Status 201 if success
        Status 404: If the place_id is not linked to any Place object
        Status 404: If the user_id is not linked to any User object
        Status 400: If the HTTP request body is not valid JSON
        Status 400: If the dictionary doesn’t contain the key user_id
        Status 400: If the dictionary doesn’t contain the key text
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    # Check if request body is valid JSON
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    review_data = request.get_json()

    # Check if dictionary contains key user_id
    user_id = review_data.get('user_id')

    if review_data.get('user_id') is None:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    # Ensure user_id is linked to User object
    if storage.get(User, user_id) is None:
        abort(404)

    # Check if request data has attribute text
    if review_data.get('text') is None:
        return make_response(jsonify({'error': 'Missing text'}), 400)

    new_review = Review(**review_data)
    new_review.save()

    return (jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a review object

    Args:
        review_id (str): ID of review to update

    Raises:
        Status 200: If success
        Status 404: If review_id is not linked to any Review object
        Status 400: If the HTTP request body is not valid JSON

    Returns:
        Review object if success
        'Not a JSON': If the HTTP request body is not valid JSON
    """
    review = storage.get(Review, review_id)

    if place is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    review_data = request.get_json()

    for k, v in review_data.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, v)

    review.save()

    return (jsonify(review.to_dict()), 200)
