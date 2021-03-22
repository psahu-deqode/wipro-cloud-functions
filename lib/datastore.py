import os
from google.cloud import pubsub


PROJECT_ID = os.getenv('PROJECT_ID')
BUCKET_NAME = os.getenv('BUCKET_NAME')
publisher = pubsub.PublisherClient()
