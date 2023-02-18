#!/usr/bin/python3
'''This is a module'''


from api.v1.views import app_views


@app_views.route('/status')
def status():
    '''A status handler'''
    json_data = {
                    "status": "OK"
                }
    return json_data
