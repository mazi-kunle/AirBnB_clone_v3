#!/usr/bin/python3
'''This is a module'''


from api.v1.views import app_views
from flask import jsonify, request
from models.amenity import Amenity
from flask import abort
from models import storage


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_amenities():
    '''retrieves the list of all amenity objects'''
    if request.method == 'GET':
        all_amenity = storage.all(Amenity).values()
        amenities = []
        for amenity in all_amenity:
            amenities.append(amenity.to_dict())

        return (jsonify(amenities))

    elif request.method == 'POST':
        if not request.json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")

    data = request.get_json()
    new_amenity = Amenity(**data)
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_an_amenity(amenity_id):
    '''retrieves a city object'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    # handle GET requests
    if request.method == 'GET':
        return (jsonify(amenity.to_dict()))

    # handle DELETE requests
    elif request.method == 'DELETE':
        storage.delete(amenity)
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
                setattr(amenity, key, value)

        amenity.save()
        return (jsonify(amenity.to_dict()))
