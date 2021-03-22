import os

from flask import make_response, jsonify, abort
from google.cloud import pubsub, datastore

PROJECT_ID = os.getenv('PROJECT_ID')
BUCKET_NAME = os.getenv('BUCKET_NAME')
publisher = pubsub.PublisherClient()


def process_handle_app_launch(request):
    try:
        request_json_data = request.get_json(silent=True, force=True)
        app_name = request_json_data.get("queryResult").get("parameters").get("LaunchApplication").lower()
        if app_name is None or app_name == "":
            abort(make_response(jsonify(fulfilmentText='Requested activity cannot be fulfilled.'), 400))
        entities = datastore.Client(PROJECT_ID).query(kind="SupportedAppList")
        entities.add_filter("synonyms", ">=", app_name)
        entities.add_filter("synonyms", "<=", app_name + "z")
        result = list(entities.fetch())
        if len(result) == 0:
            abort(make_response(jsonify(fulfilmentText='Requested activity cannot be fulfilled.'), 400))
        vehicle_vin = request_json_data.get("originalDetectIntentRequest").get("payload").get("vin")
        if vehicle_vin is None:
            abort(make_response(jsonify(fulfilmentText='VIN not found in payload. Hence cannot send msg.'), 400))
        launch_app_json = {
            "category": "APPLAUNCH",
            "package_id": result[0].package,
            "name": app_name
        }
        topic_name = "topic_" + vehicle_vin
        publisher.create_topic(topic_name)
        publisher.publish(topic_name, b'("launching_app" + app_name)', launch_app_json)
        r = make_response(jsonify(fulfillmentText=f'launching_app + {app_name}'), 200)
        r.headers['Content-Type'] = 'application/json'
        return r
    except:
        abort(make_response(jsonify(fulfillmentText='Requested activity cannot be fulfilled.'), 400))
