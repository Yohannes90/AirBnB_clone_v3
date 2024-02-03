#!/usr/bin/python3
"""Initialize Blueprint Review"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getReviewsByPlaces(place_id):
    """retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place:
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def getReview(review_id):
    """retrives a Review object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteReview(review_id):
    """deletes a Review object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def createReview(place_id):
    """creates a Review object"""
    place = storage.get(Place, place_id)
    kwargs = request.get_json()
    user = storage.get(User, kwargs['user_id'])
    if place and user:
        if kwargs:
            if 'user_id' in kwargs:
                if 'text' in kwargs:
                    kwargs['place_id'] = place_id
                    review = Review(**kwargs)
                    review.save()
                    return jsonify(review.to_dict()), 201
                abort(400, 'Missing text')
            abort(400, 'Missing user_id')
        abort(404, 'Not a JSON')
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updateReview(review_id):
    """update a Review object"""
    review = storage.get(Review, review_id)
    if review:
        kwargs = request.get_json()
        if kwargs:
            ignore_keys = ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']
            for key, value in kwargs.items():
                if key not in ignore_keys:
                    setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict()), 200
        abort(404, 'Not a JSON')
    abort(404)
