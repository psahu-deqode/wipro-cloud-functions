import os
from flask import abort, make_response, jsonify
from google.cloud import datastore, storage

from lib import logger

PROJECT_ID = os.getenv('PROJECT_ID')
BUCKET_NAME = os.getenv('BUCKET_NAME')
storage_client = storage.Client()


def search(kind, filters=None):
    entities = datastore.Client(PROJECT_ID).query(kind=kind)
    if filters is not None:
        for i in filters:
            entities.add_filter(i["column"], i["operator"], i["key"])
    result = list(entities.fetch())
    return result


def create_entity(kind, data, key=None):
    if key is None:
        key = datastore.Client(PROJECT_ID).key(kind)
    imported_json = datastore.Entity(key=key)
    imported_json.update(data)
    datastore.Client(PROJECT_ID).put(imported_json)
    return


def create_blob(json_file):
    # get bucket with name
    bucket = storage_client.get_bucket(BUCKET_NAME)

    if not bucket.get_blob(json_file):
        logger.info('Invalid file name passed in the request')
        abort(make_response(jsonify(message='Please provide a valid filename'), 400))

    # get bucket data as blob
    blob = bucket.get_blob(json_file)
    return blob
