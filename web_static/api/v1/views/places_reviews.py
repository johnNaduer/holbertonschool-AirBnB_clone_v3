#!/usr/bin/python3
"""route /reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models.place import Place
from models.review import Review
from models import storage


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place_id(place_id):
    """Method that retrieve a list of all reviews by id"""
    place = storage.get(Place, place_id)
    if (place is None):
        abort(404)

    reviews = place.reviews
    if (reviews is None):
        abort(404)

    itr_reviews = reviews

    result = [review.to_dict() for review in itr_reviews]

    return (jsonify(result))


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_id(review_id):
    """Method that retrieve a list of all reviews by id"""
    review = storage.get(Review, review_id)
    if (review is None):
        abort(404)
    result = review.to_dict()

    return (jsonify(result))


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Method that delete a review by id"""
    delete_review = storage.get(Review, review_id)
    if delete_review is None:
        abort(404)
    else:
        delete_review.delete()
        storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Method that post a new review"""
    if (not storage.get(Place, place_id)):
        abort(404)

    data_review = request.get_json(silent=True)
    if (type(data_review) is dict):
        new_review = Review(**data_review)
        setattr(new_review, "place_id", place_id)

        user_id = new_review.to_dict().get('user_id', None)
        if (not user_id):
            return jsonify({'message': 'Missing user_id'}), 400
        if (not storage.get(User, user_id)):
            abort(404)

        if (not new_review.to_dict().get('text', None)):
            return jsonify({'message': 'Missing text'}), 400

        new_review.save()
        return (jsonify(new_review.to_dict()), 201)

    return (jsonify({'message': 'Not a JSON'}), 400)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Method to update/put a review by id"""
    actual_review = storage.get(Review, review_id)
    if (actual_review is None):
        abort(404)

    update_review = request.get_json(silent=True)
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    if (type(update_review) is dict):
        for attr in ignore:
            update_review.pop(attr, None)

        for key, value in update_review.items():
            setattr(actual_review, key, value)
        actual_review.save()
        return (jsonify(actual_review.to_dict()), 200)

    return (jsonify({'message': 'Not a JSON'}), 400)
