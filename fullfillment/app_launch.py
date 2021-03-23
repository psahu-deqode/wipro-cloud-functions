from flask import make_response, jsonify, abort

from lib import logger
from lib.datastore import search
from lib.pubsub import send_message


def app_launch(request):
    # try:
    request_json_data = request.get_json(silent=True, force=True)
    app_name = request_json_data.get("queryResult").get("parameters").get("LaunchApplication").lower()

    if app_name is None or app_name == "":
        logger.logging.info('app_name was not provided.')
        abort(make_response(jsonify(fulfilmentText='Requested activity cannot be fulfilled.'), 400))

    filters = [
        {'column': "synonyms", 'operator': ">=", "key": app_name},
        {'column': "synonyms", 'operator': ">=", "key": app_name + "z"}]
    result = search("SupportedAppList", filters)

    if len(result) == 0:
        logger.logging.info('Records not found in Datastore')
        abort(make_response(jsonify(fulfilmentText='Requested activity cannot be fulfilled.'), 400))

    vehicle_vin = request_json_data.get("originalDetectIntentRequest").get("payload").get("vin")

    if vehicle_vin is None:
        logger.logging.info('vehicle_vin not found in payload')
        abort(make_response(jsonify(fulfilmentText='VIN not found in payload. Hence cannot send msg.'), 400))

    launch_app_json = {
        "category": "APPLAUNCH",
        "package_id": result[0].get("package"),
        "name": app_name
    }
    # topic_name = "topic_" + vehicle_vin
    topic_name = "projects/tripbot-cloud/topics/topic"
    send_message(topic_name, launch_app_json, vehicle_vin)

    return make_response(jsonify(fulfillmentText=f'launching_app {app_name}'), 200)

    # except:
    #     abort(make_response(jsonify(fulfillmentText='Requested activity cannot be fulfilled.'), 400))
