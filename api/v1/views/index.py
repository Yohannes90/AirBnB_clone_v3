#!/usr/bin/python3
"""Initialize Blueprint views"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify


@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    """hbnb status"""
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    pass
