import os
from flask import abort, jsonify
from flask import make_response
from google.cloud import datastore

PROJECT_ID = os.getenv('PROJECT_ID')
BUCKET_NAME = os.getenv('BUCKET_NAME')


def query(request):
    req = request.get_json(silent=True, force=True)
    list1 = []
    if req is None or req.get('key') is None:
        abort(make_response(jsonify(message='Please provide a valid key to search'), 400))
    key = req.get("key")
    entities = datastore.Client(PROJECT_ID).query(kind="data")
    entities.add_filter("UnitName", "=", key)
    entities_list = list(entities.fetch())
    if not entities_list:
        data = "No result is returned"
    else:
        for i in entities_list:
            list1.append(i)
        data = list1

    r = make_response(jsonify({"data": data}), 200)
    r.headers['Content-Type'] = 'application/json'
    return r
