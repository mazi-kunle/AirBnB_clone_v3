#!/usr/bin/python3
'''This is a module'''


from api.v1.views import app_views
from flask import jsonify, request
from models.place import Place
from models.city import City
from models.user import User
from flask import abort
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_places(city_id):
    '''retrieves the list of all place objects'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        places = []
        all_place = city.places
        for place in all_place:
            places.append(place.to_dict())

        return (jsonify(places))

    elif request.method == 'POST':
        if not request.json:
            abort(400, description="Not a JSON")
        if 'user_id' not in request.json:
            abort(400, description="Missing user_id")
        if 'name' not in request.json:
            abort(400, description="Missing name")

    data = request.get_json()
    if storage.get(User, data['user_id']) is None:
        abort(404)

    new_place = Place(**data)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_an_place(place_id):
    '''retrieves a place object'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # handle GET requests
    if request.method == 'GET':
        return (jsonify(place.to_dict()))

    # handle DELETE requests
    elif request.method == 'DELETE':
        storage.delete(place)
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
                setattr(user, key, value)

        place.save()
        return (jsonify(place.to_dict()))
