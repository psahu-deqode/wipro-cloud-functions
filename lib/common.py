

def get_vehicle_vin(request_json_data):

    if request_json_data.get("originalDetectIntentRequest").get("payload").get("vin") is None:
        vehicle_vin = "888"
    else:
        vehicle_vin = request_json_data.get("originalDetectIntentRequest").get("payload").get("vin")
    return vehicle_vin