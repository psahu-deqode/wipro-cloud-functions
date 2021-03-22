import os

from flask import abort, jsonify
from flask import make_response
import json
from google.cloud import storage, datastore

PROJECT_ID = os.getenv('PROJECT_ID')
BUCKET_NAME = os.getenv('BUCKET_NAME')


def import_funct(request):
    # create storage client
    storage_client = storage.Client()
    # get bucket with name
    bucket = storage_client.get_bucket(BUCKET_NAME)
    # validate if a filename is provided or not
    request_json_data = request.get_json(silent=True, force=True)
    if request_json_data is None:
        abort(make_response(jsonify(message='Please provide a filename'), 400))
    if request_json_data.get("filename") is None or not req.get("filename"):
        abort(make_response(jsonify(message='Please provide a filename'), 400))
    json_file = request_json_data.get("filename")
    # Validate the existance of the file in the bucket
    if not bucket.get_blob(json_file):
        abort(make_response(jsonify(message='Please provide a valid filename'), 400))
    # get bucket data as blob
    blob = bucket.get_blob(json_file)
    data = json.loads(blob.download_as_string())
    for i in data['ContentsList']:
        # append details to each json in ContentsList
        i['DocumentNo'] = data['DocumentNo']
        i['LanguageCode'] = data['LanguageCode']
        i['Version'] = data['Version']
        # Converted comma separated unit names to Array so it will be easier to search
        i['UnitName'] = i['UnitName'].split(', ') if len(i['UnitName']) != 0 else i['UnitName']
        # create datastore entity
        imported_json = datastore.Entity(key=datastore.Client(PROJECT_ID).key("data"))
        # update datastore entity with the imported json
        imported_json.update(i)
        datastore.Client(PROJECT_ID).put(imported_json)

    r = make_response(jsonify({'message': "Json uploaded successfully to Datastore"}), 201)
    r.headers['Content-Type'] = 'application/json'
    return r
