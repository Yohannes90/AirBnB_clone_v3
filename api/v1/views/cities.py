#!/usr/bin/python3
"""Initialize Blueprint cities"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def getCitiesByState(state_id):
    """retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def getCity(city_id):
    """retrives a City object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def deleteCity(city_id):
    """deletes a City object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def createCity(state_id):
    """creates a City object"""
    state = storage.get(State, state_id)
    if state:
        kwargs = request.get_json()
        if kwargs:
            if 'name' in kwargs:
                kwargs['state_id'] = state_id
                city = City(**kwargs)
                city.save()
                return jsonify(state.to_dict()), 201
            abort(400, 'Missing name')
        abort(400, 'Not a JSON')
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def updateCity(city_id):
    """update a City object"""
    city = storage.get(City, city_id)
    if city:
        kwargs = request.get_json()
        if kwargs:
            ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
            for key, value in kwargs.items():
                if key not in ignore_keys:
                    setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200
        abort(400, 'Not a JSON')
    abort(404)
