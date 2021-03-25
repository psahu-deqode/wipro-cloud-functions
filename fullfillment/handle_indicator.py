from lib import logger
from lib.datastore import search
from lib.common import get_vehicle_vin
from flask import abort, make_response, jsonify


def process_handle_indicator(request):
    try:
        request_json_data = request.get_json(silent=True, force=True)
        indicator_color = request_json_data.get("queryResult").get("parameters").get("indicatorColor")
        indicator_status = request_json_data.get("queryResult").get("parameters").get("indicatorStatus")
        indicator_type = request_json_data.get("queryResult").get("parameters").get("indicatorType")
        logger.logging.info({'indicatorColor': indicator_color, 'indicatorStatus': indicator_status, 'indicatorType': indicator_type})
        vehicle_vin = get_vehicle_vin(request_json_data)

        filter = {"column": "vin", "operator": "=", "key": vehicle_vin}
        result = search('VehicleStatus', filter)

        if len(result) == 0:
            abort(make_response(jsonify(fulfilmentText="Could not find vehicle information"), 400))

        entity_row = result[0]

        if entity_row.yatch == "0":
            abort(make_response(jsonify(fulfilmentText="no_indicator"), 400))

        elif entity_row.yatch == "1":
            if entity_row.parked == "y":
                return make_response(jsonify(fulfillmentText="blue_indicator_parked"), 200)
            else:
                return make_response(jsonify(fulfillmentText="blue_indicator_driving"), 200)

        elif entity_row.yatch == "2":
            if entity_row.parked == "y":
                return make_response(jsonify(fulfillmentText="red_indicator_parked"), 200)
            else:
                return make_response(jsonify(fulfillmentText="red_indicator_driving"), 200)

        elif entity_row.yatch == "3":
            if entity_row.parked == "y":
                return make_response(jsonify(fulfillmentText="blinking_red_indicator_parked"), 200)
            else:
                return make_response(jsonify(fulfillmentText="blinking_red_indicator_driving"), 200)

    except:
        return make_response(jsonify(fulfillmentText="Could not search for vehicle."), 400)
