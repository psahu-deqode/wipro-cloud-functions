import os
from flask import make_response, jsonify

from google.cloud import iot_v1


project_id = os.getenv("PROJECT_ID")
registry_id = os.getenv("REGISTRY_ID")
device_id = os.getenv("DEVICE_ID")
cloud_region = os.getenv("CLOUD_REGION")

client = iot_v1.DeviceManagerClient()
device_path = client.device_path(project_id, cloud_region, registry_id, device_id)


def send_command_to_device(request):
    request_json_data = request.get_json(silent=True, force=True)
    print("Sending command to device")
    command = request_json_data.get("data")
    data = command.encode("utf-8")
    client.send_command_to_device(
        request={"name": device_path, "binary_data": data}
    )
    return make_response(jsonify({'message': "Command sent to device successfully"}), 200)


def list_state_to_iotcore():

    device = client.get_device(request={"name": device_path})
    print("Last state: {}".format(device.state))

    print("State history")
    states = client.list_device_states(request={"name": device_path}).device_states
    for state in states:
        print("State: {}".format(state))

    return states


def update_device_config():
    # project_id = 'YOUR_PROJECT_ID'
    # cloud_region = 'us-central1'
    # registry_id = 'your-registry-id'
    # device_id = 'your-device-id'
    version = 0
    config = 'your-config-data1'
    print("Set device configuration")
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

    data = config.encode("utf-8")

    return client.modify_cloud_to_device_config(
        request={"name": device_path, "binary_data": data, "version_to_update": version}
    )


if __name__ == '__main__':
    list_state_to_iotcore()