#!/usr/bin/python3
"""Initialize Blueprint states"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def getAllStates():
    """retrives list of all state objects"""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def getState(state_id):
    """retrives specific state object with its id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def deleteState(state_id):
    """deletes a State object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/', methods=['POST'])
def createState():
    """creates a State object"""
    kwargs = request.get_json()
    if kwargs:
        if 'name' in kwargs:
            state = State(**kwargs)
            state.save()
            return jsonify(state.to_dict()), 201
        abort(400, 'Missing name')
    abort(400, 'Not a JSON')


@app_views.route('/states/<state_id>', methods=['PUT'])
def updateState(state_id):
    """update a State object"""
    state = storage.get(State, state_id)
    if state:
        kwargs = request.get_json()
        if kwargs:
            ignore_keys = ['id', 'created_at', 'updated_at']
            for key, value in kwargs.items():
                if key not in ignore_keys:
                    setattr(state, key, value)
            state.save()
            return jsonify(state.to_dict()), 200
        abort(400, 'Not a JSON')
    abort(404)
