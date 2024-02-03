#!/usr/bin/python3
"""Initialize Blueprint users"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getAllUsers():
    """retrives list of all User objects"""
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def getUser(user_id):
    """retrives specific User object with its id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteUser(user_id):
    """deletes a User object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createUser():
    """creates a User object"""
    kwargs = request.get_json()
    if kwargs:
        if 'email' in kwargs:
            if 'password' not in kwargs:
                user = User(**kwargs)
                user.save()
                return jsonify(user.to_dict()), 201
            abort(400, 'Missing password')
        abort(400, 'Missing email')
    abort(404, 'Not a JSON')


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def updateUser(user_id):
    """update a User object"""
    user = storage.get(User, user_id)
    if user:
        kwargs = request.get_json()
        if kwargs:
            ignore_keys = ['id', 'email', 'created_at', 'updated_at']
            for key, value in kwargs.items():
                if key not in ignore_keys:
                    setattr(user, key, value)
            user.save()
            return jsonify(user.to_dict()), 200
        abort(404, 'Not a JSON')
    abort(404)
