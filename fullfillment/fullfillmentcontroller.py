import json
import os

from flask import make_response, jsonify
from google.cloud import pubsub, datastore

PROJECT_ID = os.getenv('PROJECT_ID')
BUCKET_NAME = os.getenv('BUCKET_NAME')
publisher = pubsub.PublisherClient()


def process_handle_app_launch(request):
    try:
        req = request.get_json(silent=True, force=True)
        appName = req.get("queryResult").get("parameters").get("LaunchApplication").lower()
        if appName is None or appName == "":
            return {'fulfillmentText': "Requested activity cannot be fulfilled"}
        entities = datastore.Client(PROJECT_ID).query(kind="SupportedAppList")
        entities.add_filter("synonyms", ">=", appName)
        entities.add_filter("synonyms", "<=", appName + "z")
        result = list(entities.fetch())
        if len(result) == 0:
            return {'fulfillmentText': "Requested activity cannot be fulfilled."}
        r = make_response(jsonify({"fulfillmentText": "launching_app" + appName}, 200))
        vehicleVin = req.get("originalDetectIntentRequest").get("payload").get("vin")
        if vehicleVin is None:
            return {'fulfillmentText': "VIN not found in payload. Hence cannot send msg."}
        launchAppJson = {
            "category": "APPLAUNCH",
            "package_id": result[0].package,
            "name": appName
        }
        topicName = "topic_" + vehicleVin
        publisher.create_topic(topicName)
        publisher.publish(topicName, b'("launching_app" + appName)', launchAppJson)

    except:
        r = make_response(jsonify({'fulfillmentText': "Requested activity cannot be fulfilled."}, 200))
    r.headers['Content-Type'] = 'application/json'
    return r
