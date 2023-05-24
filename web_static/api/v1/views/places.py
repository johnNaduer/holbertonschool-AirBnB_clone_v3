#!/usr/bin/python3
"""route /places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models.city import City
from models.place import Place
from models import storage


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city_id(city_id):
    """Method that retrieve a list of all places by id"""
    city = storage.get(City, city_id)
    if (city is None):
        abort(404)

    places = city.places
    if (places is None):
        abort(404)

    itr_places = places

    result = [place.to_dict() for place in itr_places]

    return (jsonify(result))


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_id(place_id):
    """Method that retrieve a list of all places by id"""
    place = storage.get(Place, place_id)
    if (place is None):
        abort(404)
    result = place.to_dict()

    return (jsonify(result))


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Method that delete a place by id"""
    delete_place = storage.get(Place, place_id)
    if delete_place is None:
        abort(404)
    else:
        delete_place.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Method that post a new place"""
    if (not storage.get(City, city_id)):
        abort(404)

    data_place = request.get_json(silent=True)
    if (type(data_place) is dict):
        new_place = Place(**data_place)
        setattr(new_place, "city_id", city_id)

        user_id = new_place.to_dict().get('user_id', None)
        if (not user_id):
            return jsonify({'message': 'Missing user_id'}), 400
        if (not storage.get(User, user_id)):
            abort(404)

        if (not new_place.to_dict().get('name', None)):
            return jsonify({'message': 'Missing name'}), 400

        new_place.save()
        return (jsonify(new_place.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Method to update/put a place by id"""
    actual_place = storage.get(Place, place_id)
    if (actual_place is None):
        abort(404)

    update_place = request.get_json(silent=True)
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    if (type(update_place) is dict):
        for attr in ignore:
            update_place.pop(attr, None)

        for key, value in update_place.items():
            setattr(actual_place, key, value)
        actual_place.save()
        return (jsonify(actual_place.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)
