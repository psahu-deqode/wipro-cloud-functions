from google.cloud import pubsub_v1
from google.oauth2 import service_account

from lib.datastore import PROJECT_ID

credentials = service_account.Credentials
publisher = pubsub_v1.PublisherClient(credentials=credentials)


def send_message(topic_name, launch_app_json):
    topic_path = publisher.topic_path(PROJECT_ID, topic_name)
    publisher.publish(topic_path, str(launch_app_json).encode("utf-8"))
    return

