#!/usr/bin/python3
"""
States module to interface with the API
"""
from api.v1.views import (app_views, City, Place, storage)
from flask import (request, jsonify, abort)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def places_by_city(city_id):
    """
    Access the api call on all state objects
    - POST: Adds a new Place object. Requires name parameter.
    - GET: Default, returns a list of all places within a city
    """
    if city_id not in storage.all('City'):
        print("ERROR: ID not found")
        abort(404)

    if request.method == 'POST':
        posted_obj = request.get_json()
        if posted_obj is None:
            return("Not a JSON", 400)
        if 'user_id' not in posted_obj:
            return("Missing user_id", 400)
        if posted_obj['user_id'] not in storage.all('User'):
            abort(404)
        if 'name' not in posted_obj:
            return("Missing name", 400)
        new_obj = Place(**posted_obj)
        new_obj.city_id = city_id
        new_obj.save()
        return(jsonify(new_obj.to_json()), 201)

    """ Default: GET"""
    all_obj = storage.get('City', city_id).places
    rtn_json = []
    for place in all_obj:
        rtn_json.append(place.to_json())
    return (jsonify(rtn_json))


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_by_id(place_id=None):
    """
    Access the api call with on a specific state object
    returns a 404 if not found.
    - DELETE: Removes the state object
    - PUT: Updates the state object
    - GET: Default, return the state object.
    """
    if place_id not in storage.all('Place'):
        abort(404)

    if request.method == 'DELETE':
        storage.delete(storage.get('Place', place_id))
        storage.save()
        return(jsonify({}))

    if request.method == 'PUT':
        put_obj = request.get_json()
        if put_obj is None:
            return("Not a JSON", 400)
        instance = storage.get('Place', place_id)
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for attrib in put_obj:
            if attrib not in ignore_keys:
                setattr(instance, attrib, put_obj[attrib])
        instance.save()
        return(jsonify(instance.to_json()))

    """ Default: GET"""
    instance = storage.get('Place', place_id)
    return(jsonify(instance.to_json()))
