#!/usr/bin/python3
'''This is a module'''


from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
from flask import abort
from models import storage


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_users():
    '''retrieves the list of all user objects'''
    if request.method == 'GET':
        all_user = storage.all(User).values()
        users = []
        for user in all_user:
            users.append(user.to_dict())

        return (jsonify(users))

    elif request.method == 'POST':
        if not request.json:
            abort(400, description="Not a JSON")
        if 'email' not in request.json:
            abort(400, description="Missing email")
        if 'password' not in request.json:
            abort(400, description="Missing password")

    data = request.get_json()
    new_user = User(**data)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_an_user(user_id):
    '''retrieves a user object'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    # handle GET requests
    if request.method == 'GET':
        return (jsonify(user.to_dict()))

    # handle DELETE requests
    elif request.method == 'DELETE':
        storage.delete(user)
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
                setattr(user, key, value)

        user.save()
        return (jsonify(user.to_dict()))
