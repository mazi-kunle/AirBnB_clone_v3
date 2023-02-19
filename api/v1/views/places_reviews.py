#!/usr/bin/python3
'''This is a module'''


from api.v1.views import app_views
from flask import jsonify, request
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from flask import abort
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_reviews(place_id):
    '''retrieves the list of all review objects'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        reviews = []
        all_review = place.reviews
        for review in all_review:
            reviews.append(review.to_dict())

        return (jsonify(reviews))

    elif request.method == 'POST':
        if not request.json:
            abort(400, description="Not a JSON")
        if 'user_id' not in request.json:
            abort(400, description="Missing user_id")
        if 'text' not in request.json:
            abort(400, description="Missing text")

    data = request.get_json()
    if storage.get(User, data['user_id']) is None:
        abort(404)

    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return (jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_a_review(review_id):
    '''retrieves a review object'''
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    # handle GET requests
    if request.method == 'GET':
        return (jsonify(review.to_dict()))

    # handle DELETE requests
    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return (jsonify({}))

    # handle PUT requests
    elif request.method == 'PUT':
        if not request.json:
            abort(400, description="Not a JSON")

        data = request.get_json()
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
                pass
            else:
                setattr(review, key, value)

        review.save()
        return (jsonify(review.to_dict()))
