import google
from google.cloud import pubsub_v1
from google.auth.transport import requests


credentials, project_id = google.auth.default()
r = requests.Request()
credentials.refresh(r)

publisher = pubsub_v1.PublisherClient(credentials=credentials)


def send_message(topic_name, launch_app_json, vehicle_vin):
    #topic_path = publisher.topic_path(PROJECT_ID, topic_name)
    #topic_path = "projects/tripbot-cloud/topics/topic"
    future = publisher.publish(topic_name, data=str(launch_app_json).encode("utf-8"), vin=vehicle_vin)
    try:
        print(future.result())
    except Exception as e:
        print("Error publishing: " + str(e))
    return
