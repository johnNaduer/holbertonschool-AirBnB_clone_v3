#!/usr/bin/python3
"""route /amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Method that retrieve a list of all amenities by id"""
    amenities = storage.all(Amenity)
    if (amenities is None):
        abort(404)

    itr_amenities = amenities.values()

    result = [amenity.to_dict() for amenity in itr_amenities]

    return (jsonify(result))


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """Method that retrieve a list of all amenities by id"""
    amenity = storage.get(Amenity, amenity_id)
    if (amenity is None):
        abort(404)
    result = amenity.to_dict()

    return (jsonify(result))


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Method that delete a amenity by id"""
    delete_amenity = storage.get(Amenity, amenity_id)
    if delete_amenity is None:
        abort(404)
    else:
        delete_amenity.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Method that post a new amenity"""
    data_amenity = request.get_json(silent=True)

    if (type(data_amenity) is dict):
        new_amenity = Amenity(**data_amenity)
        if (not new_amenity.to_dict().get('name', None)):
            return jsonify({'message': 'Missing name'}), 400

        new_amenity.save()

        return (jsonify(new_amenity.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Method to update/put a amenity by id"""
    actual_amenity = storage.get(Amenity, amenity_id)
    if (actual_amenity is None):
        abort(404)

    update_amenity = request.get_json(silent=True)
    ignore = ['id', 'created_at', 'updated_at']
    if (type(update_amenity) is dict):
        for attr in ignore:
            update_amenity.pop(attr, None)

        for key, value in update_amenity.items():
            setattr(actual_amenity, key, value)
        actual_amenity.save()
        return (jsonify(actual_amenity.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)
