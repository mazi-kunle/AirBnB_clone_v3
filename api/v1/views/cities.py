#!/usr/bin/python3
'''This is a module'''


from api.v1.views import app_views
from flask import jsonify, request
from models.state import State
from models.city import City
from flask import abort
from models import storage


@app_views.route('/states<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_cities(state_id):
    '''retrieves the list of all city objects'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        cities = []
        all_city = state.cities
        for city in all_city:
            cities.append(city.to_dict())

        return (jsonify(cities))

    elif request.method == 'POST':
        if not request.json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")

    new_city = City(**request.get_json())
    new_city.save()
    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_a_city(city_id):
    '''retrieves a city object'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    # handle GET requests
    if request.method == 'GET':
        return (jsonify(city.to_dict()))

    # handle DELETE requests
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return (jsonify({}))

    # handle PUT requests
    elif request.method == 'PUT':
        if not request.json:
            abort(400, description="Not a JSON")

        data = request.get_json()
        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(city, key, value)

        city.save()
        return (jsonify(city.to_dict()))
