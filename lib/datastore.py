import os

from google.cloud import pubsub, datastore

PROJECT_ID = os.getenv('PROJECT_ID')
BUCKET_NAME = os.getenv('BUCKET_NAME')
publisher = pubsub.PublisherClient()


def search(kind, filter):
    entities = datastore.Client(PROJECT_ID).query(kind=kind)
    for i in filter:
        entities.add_filter(i)
    result = list(entities.fetch())
    return result
