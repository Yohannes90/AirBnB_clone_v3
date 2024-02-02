#!/usr/bin/python3
"""Initialize Blueprint views"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def hbnbStatus():
    """hbnb status"""
    response = {"status": "OK"}
    return jsonify(response)


if __name__ == "__main__":
    pass
