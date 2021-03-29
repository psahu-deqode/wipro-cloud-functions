from fullfillment.router import agent

from lib.datastore import search
from lib.common import get_vehicle_vin


def process_handle_indicator(request):
    try:
        request_json_data = request.get_json(silent=True, force=True)
        # print(request_json_data)
        # indicator_color = request_json_data.get("queryResult").get("parameters").get("indicatorColor")
        # indicator_status = request_json_data.get("queryResult").get("parameters").get("indicatorStatus")
        # indicator_type = request_json_data.get("queryResult").get("parameters").get("indicatorType")
        # logger.logging.info({'indicatorColor': indicator_color, 'indicatorStatus': indicator_status, 'indicatorType': indicator_type})
        vehicle_vin = get_vehicle_vin(request_json_data)

        filter = {"column": "vin", "operator": "=", "key": vehicle_vin}
        result = search('VehicleStatus', filter)

        if len(result) == 0:
            agent.add_message("Could not find vehicle information")
            return agent.get_response()

        entity_row = result[0]

        if entity_row.yatch == "0":
            agent.add_message("no_indicator")

        elif entity_row.yatch == "1":
            if entity_row.parked == "y":
                agent.add_message("blue_indicator_parked")
            else:
                agent.add_message("blue_indicator_driving")

        elif entity_row.yatch == "2":
            if entity_row.parked == "y":
                agent.add_message("red_indicator_parked")
            else:
                agent.add_message("red_indicator_driving")

        elif entity_row.yatch == "3":
            if entity_row.parked == "y":
                agent.add_message("blinking_red_indicator_parked")
            else:
                agent.add_message("blinking_red_indicator_driving")
        return agent.get_response()

    except:
        agent.add_message(f"Could not search for vehicle.")
        return agent.get_response()