import argparse
import datetime
import os
import ssl
import time
import jwt
import paho.mqtt.client as mqtt


algorithm = os.getenv("ALGORITHM")
ca_certs = os.getenv("CA_CERTS")
cloud_region = os.getenv("CLOUD_REGION")
listen_dur = int(os.getenv("LISTEN_DUR"))
mqtt_bridge_port = int(os.getenv("MQTT_BRIDGE_PORT"))
service_account_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.getenv("PROJECT_ID")
registry_id = os.getenv("REGISTRY_ID")
device_id = os.getenv("DEVICE_ID")
private_key_file = os.getenv("PRIVATE_KEY_FILE")
jwt_expires_minutes = int(os.getenv("JWT_EXPIRES_MINUTES"))
num_messages = int(os.getenv("NUM_MESSAGES"))


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Example Google Cloud IoT Core MQTT device connection code."
    )
    parser.add_argument(
        "--mqtt_bridge_hostname",
        default="mqtt.googleapis.com",
        help="MQTT bridge hostname.",
    )
    parser.add_argument("--gateway_id", required=False, help="Gateway identifier.")
    return parser.parse_args()


def create_jwt(project_id, private_key_file, algorithm):
    token = {
        # The time that the token was issued at
        "iat": datetime.datetime.utcnow(),
        # The time the token expires.
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=20),
        # The audience field should always be set to the GCP project id.
        "aud": project_id,
    }

    # Read the private key file.
    with open(private_key_file, "r") as f:
        private_key = f.read()

    print(
        "Creating JWT using {} from private key file {}".format(
            algorithm, private_key_file
        )
    )

    return jwt.encode(token, private_key, algorithm=algorithm)


# [START iot_mqtt_config]
def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return "{}: {}".format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print("on_connect", mqtt.connack_string(rc))


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print("on_disconnect", error_str(rc))


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print("on_publish")


def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload.decode("utf-8"))
    print(
        "Received message '{}' on topic '{}' with Qos {}".format(
            payload, message.topic, str(message.qos)
        )
    )


def get_client(args):
    """Create our MQTT client. The client_id is a unique string that identifies
    this device. For Google Cloud IoT Core, it must be in the format below."""
    client_id = "projects/{}/locations/{}/registries/{}/devices/{}".format(
        project_id, cloud_region, registry_id, device_id
    )
    print("Device client_id is '{}'".format(client_id))

    client = mqtt.Client(client_id=client_id)

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
        username="unused", password=create_jwt(project_id, private_key_file, algorithm)
    )

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to the Google MQTT bridge.
    client.connect(args.mqtt_bridge_hostname, mqtt_bridge_port)

    # This is the topic that the device will receive configuration updates on.
    mqtt_config_topic = "/devices/{}/config".format(device_id)

    # Subscribe to the config topic.
    client.subscribe(mqtt_config_topic, qos=1)

    # The topic that the device will receive commands on.
    mqtt_command_topic = "/devices/{}/commands/#".format(device_id)

    # Subscribe to the commands topic, QoS 1 enables message acknowledgement.
    print("Subscribing to {}".format(mqtt_command_topic))
    client.subscribe(mqtt_command_topic, qos=0)

    return client


def detach_device(client, device_id):
    """Detach the device from the gateway."""
    # [START iot_detach_device]
    detach_topic = "/devices/{}/detach".format(device_id)
    print("Detaching: {}".format(detach_topic))
    client.publish(detach_topic, "{}", qos=1)
    # [END iot_detach_device]


def attach_device(client, device_id, auth):
    """Attach the device to the gateway."""
    # [START iot_attach_device]
    attach_topic = "/devices/{}/attach".format(device_id)
    attach_payload = '{{"authorization" : "{}"}}'.format(auth)
    client.publish(attach_topic, attach_payload, qos=1)
    # [END iot_attach_device]


def send_data_from_bound_device():
    args = parse_command_line_args()

    # Publish to the events or state topic based on the flag.
    sub_topic = "state"

    client = get_client(args)

    # Publish num_messages messages to the MQTT bridge once per second.
    for i in range(1, num_messages + 1):
        # Process network events.
        client.loop()

        payload = "{}/{}-payload-{}".format(registry_id, device_id, i)
        print("Publishing message {}/{}: '{}'".format(i, num_messages, payload))

        device_topic = "/devices/{}/{}".format(device_id, "events")
        client.publish(device_topic, payload, qos=1)

        # Send events every second. State should not be updated as often
        for i in range(0, 60):
            time.sleep(1)
            client.loop()


if __name__ == "__main__":
    send_data_from_bound_device()
