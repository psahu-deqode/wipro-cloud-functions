from flask import make_response
from flask import abort, jsonify
from google.cloud import datastore

from main import app
from lib.datastore import PROJECT_ID


def query(request):
    request_json_data = request.get_json(silent=True, force=True)
    list1 = []

    if request_json_data is None or request_json_data.get('key') is None:
        app.logger.info('Query function is invoked without the key parameter')
        abort(make_response(jsonify(message='Please provide a valid key to search'), 400))

    key = request_json_data.get("key")
    entities = datastore.Client(PROJECT_ID).query(kind="data")
    entities.add_filter("UnitName", "=", key)
    entities_list = list(entities.fetch())

    if not entities_list:
        data = "No result is returned"
    else:
        for i in entities_list:
            list1.append(i)
        data = list1

    return make_response(jsonify({"data": data}), 200)
