#!/usr/bin/python3
'''This is a module'''


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    '''A status handler'''
    json_data = {
                    "status": "OK"
                }
    return json_data


@app_views.route('/stats')
def stats():
    '''retrieves the number of each object by type'''
    data = {
                "amenities": storage.count(Amenity),
                "cities": storage.count(City),
                "places": storage.count(Place),
                "reviews": storage.count(Review),
                "states": storage.count(State),
                "users": storage.count(User)
            }

    return(jsonify(data))
