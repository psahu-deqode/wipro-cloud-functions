from flask import make_response
from flask import abort, jsonify

from lib import logger
from lib.datastore import search


def search_data(request):
    request_json_data = request.get_json(silent=True, force=True)
    list1 = []

    if request_json_data is None or request_json_data.get('key') is None:
        logger.logging.info('Query function is invoked without the key parameter')
        abort(make_response(jsonify(message='Please provide a valid key to search'), 400))

    key = request_json_data.get("key")
    filters = [{"column": "UnitName", "operator": "=", "key": key}]
    result = search("data", filters)

    if not result:
        data = "No result is returned"
    else:
        for i in result:
            list1.append(i)
        data = list1
    return make_response(jsonify(data=data), 200)
