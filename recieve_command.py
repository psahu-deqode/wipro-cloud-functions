import argparse
import datetime
import os
import ssl
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


def main():
    args = parse_command_line_args()
    """Connects a device, sends data, and receives data."""

    client = get_client(args)

    for i in range(1, listen_dur):
        # Process network events.
        client.loop()


if __name__ == "__main__":
    main()
