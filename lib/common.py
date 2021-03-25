def get_vehicle_vin(request_json_data):
    if request_json_data.get("originalDetectIntentRequest").get("payload").get("vin") is None:
        vehicle_vin = "888"
    else:
        vehicle_vin = request_json_data.get("originalDetectIntentRequest").get("payload").get("vin")
    return vehicle_vin


def new_vehicle_status_entity():
    return {'ign': "n",
            'parked': "y",
            'vin': "",
            'yatch': "1",
            'hud_angle': 0,
            'amb_light': 0
            }
