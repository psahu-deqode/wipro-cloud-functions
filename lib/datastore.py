import os

from google.cloud import datastore

PROJECT_ID = os.getenv('PROJECT_ID')
BUCKET_NAME = os.getenv('BUCKET_NAME')


def search(kind, filters):
    entities = datastore.Client(PROJECT_ID).query(kind=kind)
    for i in filters:
        entities.add_filter(i)
    result = list(entities.fetch())
    return result


def create_entity(kind, data):
    imported_json = datastore.Entity(key=datastore.Client(PROJECT_ID).key(kind))
    imported_json.update(data)
    datastore.Client(PROJECT_ID).put(imported_json)
    return
