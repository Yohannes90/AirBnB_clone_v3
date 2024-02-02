#!/usr/bin/python3
"""Initialize Blueprint views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def hbnbStatus():
    """hbnb status"""
    response = {"status": "OK"}
    return jsonify(response)

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def hbnbStats():
    """hbnb stats retrieves the number of each objects by type"""
    stats = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(stats)


if __name__ == "__main__":
    pass
