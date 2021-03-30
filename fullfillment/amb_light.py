from fullfillment.router import agent
from lib.datastore import search, create_entity
from lib.common import get_vehicle_vin, new_vehicle_status_entity


def process_handle_amb_light(request):
    try:
        if type(request) != dict:
            request_json_data = request.get_json(silent=True, force=True)
        else:
            request_json_data = request

        direction = request_json_data.get("queryResult").get("parameters").get("level")
        by_approx = request_json_data.get("queryResult").get("parameters").get("approx")
        type = request_json_data.get("queryResult").get("parameters").get("hudval")
        by_how_much = int(request_json_data.get("queryResult").get("parameters").get("numval"))
        percentage = int(request_json_data.get("queryResult").get("parameters").get("per"))
        print({'Direction': direction, 'byApprox': by_approx, 'type': type, 'byHowMuch': by_how_much})

        ref_result = search('AmbLightRef')
        amb_light_ref_data = ref_result[0]
        print(f"AmbLight Ref: {amb_light_ref_data}")

        if percentage is None and (by_how_much is not None) and (
                by_how_much < amb_light_ref_data.get("minimum") or by_how_much > amb_light_ref_data.get("maximum")):
            agent.add_message(
                f"amb_light_not_in_range {amb_light_ref_data.get('minimum')} and  {amb_light_ref_data.get('maximum')}")
            return agent.get_response()

        vehicle_vin = get_vehicle_vin(request_json_data)
        filter = [{"column": "vin", "operator": "=", "key": vehicle_vin}]
        result = search("VehicleStatus", filter)

        if type is not None:
            by_how_much = amb_light_ref_data.get("type")
            print(f"Type: {type},by_how_much: {by_how_much}")

        if len(result) == 0:
            vehicle_data = new_vehicle_status_entity()
            vehicle_data.vin = vehicle_vin
            if by_how_much is None:
                vehicle_data.amb_light = amb_light_ref_data.get("small")
            else:
                vehicle_data.amb_light = by_how_much
            old_amb_light_data = vehicle_data.get("amb_light")
        else:
            vehicle_data = result[0]
            old_amb_light_data = vehicle_data.get("amb_light")
            if direction == "increase":
                if vehicle_data.get("amb_light") >= amb_light_ref_data.get("maximum"):
                    agent.add_message("amb_light_already_max")
                    return agent.get_response()
                if by_approx == "little":
                    vehicle_data.amb_light = vehicle_data.amb_light + amb_light_ref_data.get("small")
                elif by_approx == "lot":
                    vehicle_data.amb_light = vehicle_data.amb_light + amb_light_ref_data.get("big")
                else:
                    if 0 < percentage <= 100:
                        by_how_much = old_amb_light_data + (old_amb_light_data * percentage / 100)
                    else:
                        agent.add_message("amb_light_invalid_percentage")
                        return agent.get_response()
                    vehicle_data.amb_light = vehicle_data.amb_light + by_how_much

            elif direction == "decrease":
                if vehicle_data.amb_light <= amb_light_ref_data.get("minimum"):
                    agent.add_message("amb_light_already_min")
                    return agent.get_response()
                if by_approx == "little":
                    vehicle_data.amb_light = vehicle_data.amb_light - amb_light_ref_data.get("small")
                elif by_approx == "lot":
                    vehicle_data.amb_light = vehicle_data.amb_light - amb_light_ref_data.get("big")
                else:
                    if 0 < percentage <= 100:
                        by_how_much = old_amb_light_data - (old_amb_light_data * percentage / 100)
                    else:
                        agent.add_message("amb_light_invalid_percentage")
                        return agent.get_response()
                    vehicle_data.amb_light = vehicle_data.amb_light + by_how_much
            else:
                vehicle_data.amb_light = by_how_much
                old_amb_light_data = 0

            print("Existing vehicle found")

        if vehicle_data.amb_light is None:
            agent.add_message("hud_error")
            return agent.get_response()
        if vehicle_data.amb_light >= amb_light_ref_data.get("maximum"):
            vehicle_data.amb_light = amb_light_ref_data.get("maximum")
        elif vehicle_data.amb_light <= amb_light_ref_data.get("minimum"):
            vehicle_data.amb_light = amb_light_ref_data.get("minimum")
        try:

            result = create_entity("VehicleStatus", vehicle_vin, vehicle_data)

            if type is not None:
                if type == 'minimum':
                    agent.add_message("amb_light_min")
                if type == 'maximum':
                    agent.add_message("amb_light_max")
                else:
                    agent.add_message("amb_light_mid")

            elif old_amb_light_data == 0:
                if vehicle_data.amb_light == amb_light_ref_data.get("minimum"):
                    agent.add_message("amb_light_min")
                elif vehicle_data.amb_light == amb_light_ref_data.get("maximum"):
                    agent.add_message("amb_light_max")
                else:
                    agent.add_message(f"amb_light_set_to {vehicle_data.amb_light}")

            else:
                if old_amb_light_data <= vehicle_data.amb_light:
                    agent.add_message("raising")
                    agent.add_message("amb_light_changed")
                else:
                    agent.add_message("lowering")
                    agent.add_message("amb_light_changed")
            return agent.get_response()

        except:
            agent.add_message("Ambient Light info could not be inserted or updated.")
            return agent.get_response()

    except:
        agent.add_message("Error while trying to search vehicle.")
        return agent.get_response()
