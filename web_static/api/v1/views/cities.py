#!/usr/bin/python3
"""route /cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_from_state(state_id):
    """Method that retrieve a list of all cities by id"""
    state = storage.get(State, state_id)
    if (state is None):
        abort(404)

    cities = state.cities

    result = [city.to_dict() for city in cities]

    return (jsonify(result))


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_id(city_id):
    """Method that retrieve a list of all cities by id"""
    city = storage.get(City, city_id)
    if (city is None):
        abort(404)
    result = city.to_dict()

    return (jsonify(result))


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Method that delete a city by id"""
    delete_city = storage.get(City, city_id)
    if delete_city is None:
        abort(404)
    else:
        delete_city.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Method that post a new city"""
    if (not storage.get(State, state_id)):
        abort(404)

    data_city = request.get_json(silent=True)

    if (type(data_city) is dict):
        new_city = City(**data_city)
        setattr(new_city, "state_id", state_id)

        if (not new_city.to_dict().get('name', None)):
            return jsonify({'message': 'Missing name'}), 400

        new_city.save()

        return (jsonify(new_city.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Method to update/put a city by id"""
    actual_city = storage.get(City, city_id)
    if (actual_city is None):
        abort(404)

    update_city = request.get_json(silent=True)
    ignore = ['id', 'created_at', 'updated_at', 'state_id']
    if (type(update_city) is dict):
        for attr in ignore:
            update_city.pop(attr, None)

        for key, value in update_city.items():
            setattr(actual_city, key, value)
        actual_city.save()
        return (jsonify(actual_city.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)
