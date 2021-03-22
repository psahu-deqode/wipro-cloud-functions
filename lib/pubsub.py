from google import pubsub

from main import app

publisher = pubsub.PublisherClient()


def send_message(topic_name, message, launch_app_json):
    publisher.create_topic(topic_name)
    publisher.publish(topic_name, message, launch_app_json)
    app.logger.info('Message sent to Vehicle.')
    return
