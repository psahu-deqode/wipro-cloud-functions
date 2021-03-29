from fullfillment.router import agent

from lib.datastore import search
from lib.common import get_vehicle_vin


def process_handle_indicator(request):
    try:
        if type(request) != dict:
            request_json_data = request.get_json(silent=True, force=True)
        else:
            request_json_data = request

        vehicle_vin = get_vehicle_vin(request_json_data)

        filter = [{"column": "vin", "operator": "=", "key": vehicle_vin}]
        result = search('VehicleStatus', filter)

        if len(result) == 0:
            agent.add_message("Could not find vehicle information")
            return agent.get_response()

        entity_row = result[0]

        if entity_row.get("yatch") == "0":
            agent.add_message("no_indicator")

        elif entity_row.get("yatch") == "1":
            if entity_row.get("parked") == "y":
                agent.add_message("blue_indicator_parked")
            else:
                agent.add_message("blue_indicator_driving")

        elif entity_row.get("yatch") == "2":
            if entity_row.get("parked") == "y":
                agent.add_message("red_indicator_parked")
            else:
                agent.add_message("red_indicator_driving")

        elif entity_row.get("yatch") == "3":
            if entity_row.get("parked") == "y":
                agent.add_message("blinking_red_indicator_parked")
            else:
                agent.add_message("blinking_red_indicator_driving")
        return agent.get_response()

    except:
        agent.add_message(f"Could not search for vehicle.")
        return agent.get_response()