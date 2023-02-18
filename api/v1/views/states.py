#!/usr/bin/python3
'''This is a module'''


from api.v1.views import app_views
from flask import jsonify, request
from models.state import State
from flask import abort
from models import storage


@app_views.route('/states', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_state():
    '''retrieves the list of all state objects'''
    if request.method == 'GET':
        states = []
        all_states = storage.all(State).values()
        for state in all_states:
            states.append(state.to_dict())

        return (jsonify(states))
    elif request.method == 'POST':
        if not request.json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")

    new_state = State(**request.get_json())
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_a_state(state_id):
    '''retrieves a state object'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    # handle GET requests
    if request.method == 'GET':
        return (jsonify(state.to_dict()))

    # handle DELETE requests
    elif request.method == 'DELETE':
        storage.delete(state)
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
                setattr(state, key, value)

        state.save()
        return (jsonify(state.to_dict()))
