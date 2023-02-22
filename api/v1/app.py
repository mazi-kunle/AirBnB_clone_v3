#!/usr/bin/python3
'''This is a module'''


from flask import Flask, jsonify
from flask import render_template
from models import storage
import api.v1.views
import os
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})
app_views = api.v1.views.app_views
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    '''closes the storage on teardown'''
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''handle error 404'''
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    if os.getenv('HBNB_API_HOST'):
        host = os.getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'

    if os.getenv('HBNB_API_PORT'):
        port = os.getenv('HBNB_API_PORT')
    else:
        port = 5000

    app.run(host=host, port=port, threaded=True)
