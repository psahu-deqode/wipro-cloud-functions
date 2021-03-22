from flask import abort, jsonify
from flask import make_response
import json
from google.cloud import storage

from lib import logger
from lib.datastore import BUCKET_NAME, create_entity


def import_funct(request):
    # create storage client
    storage_client = storage.Client()
    # get bucket with name
    bucket = storage_client.get_bucket(BUCKET_NAME)
    # validate if a filename is provided or not
    request_json_data = request.get_json(silent=True, force=True)

    if request_json_data is None:
        logger.info('Invalid request in Import data function')
        abort(make_response(jsonify(message='Please provide a filename'), 400))

    if request_json_data.get("filename") is None or not request_json_data.get("filename"):
        logger.info('Invalid filename  in Import data function request')
        abort(make_response(jsonify(message='Please provide a filename'), 400))

    json_file = request_json_data.get("filename")
    # Validate the existence of the file in the bucket

    if not bucket.get_blob(json_file):
        logger.info('Invalid file name passed in the request')
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
        kind = "data"
        data = i
        create_entity(kind, data)

    return make_response(jsonify({'message': "Json uploaded successfully to Datastore"}), 201)
