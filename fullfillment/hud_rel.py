from lib import logger
from fullfillment.router import agent
from lib.datastore import search, create_entity
from lib.common import get_vehicle_vin, new_vehicle_status_entity


def process_handle_hud_rel(request):
    try:

        if type(request) != dict:
            request_json_data = request.get_json(silent=True, force=True)
        else:
            request_json_data = request

        direction = request_json_data.get("queryResult").get("parameters").get("level")
        by_approx = request_json_data.get("queryResult").get("parameters").get("approx")
        type = request_json_data.get("queryResult").get("parameters").get("hudval")
        by_how_much = int(request_json_data.get("queryResult").get("parameters").get("numval"))
        print({'Direction': direction, 'byApprox': by_approx, 'type': type, 'byHowMuch': by_how_much})

        hud_data = search('HudRef')
        hud_ref_data = hud_data[0]

        if by_how_much is not None and (
                by_how_much < hud_ref_data.get("minimum") or by_how_much < hud_ref_data.get("maximum")):
            agent.add_message(
                f"hud_angle_not_in_range of  {hud_ref_data.get('minimum')} and {hud_ref_data.get('maximum')}")
        vehicle_vin = get_vehicle_vin(request_json_data)
        filter = [{"column": "vin", "operator": "=", "key": vehicle_vin}]

        result = search('VehicleStatus', filter)
        if type is not None:
            by_how_much = hud_ref_data.get("type")
            logger.logging.info({'type': type, 'by_how_much': by_how_much})
        if len(result) == 0:
            vehicle_data = new_vehicle_status_entity()
            vehicle_data.vin = vehicle_vin
            if by_how_much is None:
                vehicle_data.hud_angle = hud_ref_data.get('small')
            else:
                vehicle_data.hud_angle = by_how_much
            old_hud_angle_data = vehicle_data.hud_angle
        else:
            vehicle_data = result[0]
            old_hud_angle_data = vehicle_data.hud_angle

            if direction == 'increase':
                if vehicle_data.hud_angle >= hud_ref_data.get('maximum'):
                    agent.add_message("hud_angle_already_max")
                if by_approx == "little":
                    vehicle_data.hud_angle = vehicle_data.hud_angle + hud_ref_data.small
                elif by_approx == "lot":
                    vehicle_data.hud_angle = vehicle_data.hud_angle + hud_ref_data.big
                else:
                    vehicle_data.hud_angle = vehicle_data.hud_angle + by_how_much

            elif direction == "decrease":
                if vehicle_data.hud_angle <= hud_ref_data.get('minimum'):
                    agent.add_message("hud_angle_already_min")
                if by_approx == "little":
                    vehicle_data.hud_angle = vehicle_data.hud_angle - hud_ref_data.small
                elif by_approx == "lot":
                    vehicle_data.hud_angle = vehicle_data.hud_angle - hud_ref_data.big
                else:
                    vehicle_data.hud_angle = vehicle_data.hud_angle - by_how_much
            else:
                vehicle_data.hud_angle = by_how_much
                old_hud_angle_data = 0

            logger.logging.info("Existing vehicle found.")

            if vehicle_data.hud_angle is None:
                agent.add_message("hud_error")

            if vehicle_data.hud_angle >= hud_ref_data.maximum:
                vehicle_data.hud_angle = hud_ref_data.maximum
            elif vehicle_data.hud_angle <= hud_ref_data.minimum:
                vehicle_data.hud_angle = hud_ref_data.minimum

        try:
            result = create_entity("VehicleStatus", vehicle_vin, vehicle_data)

            if type is not None:
                if type == 'minimum':
                    agent.add_message("hud_angle_min")
                if type == 'maximum':
                    agent.add_message("hud_angle_max")
                else:
                    agent.add_message("hud_angle_mid")

            elif old_hud_angle_data == 0:
                if vehicle_data.hud_angle == hud_ref_data.minimum:
                    agent.add_message("hud_angle_min")
                elif vehicle_data.hud_angle == hud_ref_data.maximum:
                    agent.add_message("hud_angle_max")
                else:
                    agent.add_message(f"hud_angle_set_to {vehicle_data.hud_angle}")
            else:
                if old_hud_angle_data <= vehicle_data.hud_angle:
                    agent.add_message("raising")
                else:
                    agent.add_message("lowering")
                    if old_hud_angle_data <= vehicle_data.hud_angle:
                        agent.add_message("raising")
                        agent.add_message("hud_angle_changed")
                    else:
                        agent.add_message("lowering")
                        agent.add_message("hud_angle_changed")

            return agent.get_response()

        except:
            agent.add_message("HUD info could not be inserted or updated")
            return agent.get_response()

    except:
        agent.add_message("Error while trying to search vehicle.")
        return agent.get_response()
