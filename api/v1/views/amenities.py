#!/usr/bin/python3
"""Initialize Blueprint amenities"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getAllAmenities():
    """retrives list of all amenity objects"""
    amenities = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def getAmenity(amenity_id):
    """retrives specific Amenity object with its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createAmenity():
    """creates a Amenity object"""
    kwargs = request.get_json()
    if kwargs:
        if 'name' in kwargs:
            amenity = Amenity(**kwargs)
            amenity.save()
            return jsonify(amenity.to_dict()), 201
        abort(400, 'Missing name')
    abort(400, 'Not a JSON')


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def updateAmenity(amenity_id):
    """update a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        kwargs = request.get_json()
        if kwargs:
            ignore_keys = ['id', 'created_at', 'updated_at']
            for key, value in kwargs.items():
                if key not in ignore_keys:
                    setattr(amenity, key, value)
            amenity.save()
            return jsonify(amenity.to_dict()), 200
        abort(400, 'Not a JSON')
    abort(404)
