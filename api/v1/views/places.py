#!/usr/bin/python3
"""Initialize Blueprint places"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getPlacesByCities(city_id):
    """retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city:
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getPlace(place_id):
    """retrives a Place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    """deletes a Place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createPlace(city_id):
    """creates a Place object"""
    city = storage.get(City, city_id)
    kwargs = request.get_json()
    if not kwargs:
        abort(400, 'Not a JSON')
    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')
    user = storage.get(User, kwargs['user_id'])
    if city and user:
        if 'name' in kwargs:
            kwargs['city_id'] = city_id
            place = Place(**kwargs)
            place.save()
            return jsonify(place.to_dict()), 201
        abort(400, 'Missing name')
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updatePlace(place_id):
    """update a Place object"""
    place = storage.get(Place, place_id)
    if place:
        kwargs = request.get_json()
        if kwargs:
            ignore_keys = ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']
            for key, value in kwargs.items():
                if key not in ignore_keys:
                    setattr(place, key, value)
            place.save()
            return jsonify(place.to_dict()), 200
        abort(400, 'Not a JSON')
    abort(404)
