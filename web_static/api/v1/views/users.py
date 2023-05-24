#!/usr/bin/python3
"""route /users"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Method that retrieve a list of all users by id"""
    users = storage.all(User)
    if (users is None):
        abort(404)

    itr_users = users.values()

    result = [user.to_dict() for user in itr_users]

    return (jsonify(result))


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_id(user_id):
    """Method that retrieve a list of all users by id"""
    user = storage.get(User, user_id)
    if (user is None):
        abort(404)
    result = user.to_dict()

    return (jsonify(result))


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Method that delete a user by id"""
    delete_user = storage.get(User, user_id)
    if delete_user is None:
        abort(404)
    else:
        delete_user.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Method that post a new user"""
    data_user = request.get_json(silent=True)

    if (type(data_user) is dict):
        new_user = User(**data_user)
        if (not new_user.to_dict().get('email', None)):
            return jsonify({'message': 'Missing email'}), 400
        if (not new_user.to_dict().get('password', None)):
            return jsonify({'message': 'Missing password'}), 400

        new_user.save()
        return (jsonify(new_user.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Method to update/put a user by id"""
    actual_user = storage.get(User, user_id)
    if (actual_user is None):
        abort(404)

    update_user = request.get_json(silent=True)
    ignore = ['id', 'created_at', 'updated_at']
    if (type(update_user) is dict):
        for attr in ignore:
            update_user.pop(attr, None)

        for key, value in update_user.items():
            setattr(actual_user, key, value)
        actual_user.save()
        return (jsonify(actual_user.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)
