from lib import logger
from lib.datastore import search
from lib.pubsub import send_message
from fullfillment.router import agent


def process_app_launch(request):
    try:
        if type(request) != dict:
            request_json_data = request.get_json(silent=True, force=True)
        else:
            request_json_data = request

        app_name = request_json_data.get("queryResult").get("parameters").get("LaunchApplication").lower()

        if app_name is None or app_name == "":
            logger.logging.info('app_name was not provided.')
            agent.add_message('Requested activity cannot be fulfilled.')
            return agent.get_response()

        filters = [
            {'column': "synonyms", 'operator': ">=", "key": app_name},
            {'column': "synonyms", 'operator': ">=", "key": app_name + "z"}]
        result = search("SupportedAppList", filters)

        if len(result) == 0:
            logger.logging.info('Records not found in Datastore')
            agent.add_message('Requested activity cannot be fulfilled.')
            return agent.get_response()

        vehicle_vin = request_json_data.get("originalDetectIntentRequest").get("payload").get("vin")

        if vehicle_vin is None:
            logger.logging.info('vehicle_vin not found in payload')
            agent.add_message('VIN not found in payload. Hence cannot send msg.')
            return agent.get_response()

        launch_app_json = {
            "category": "APPLAUNCH",
            "package_id": result[0].get("package"),
            "name": app_name
        }

        send_message(launch_app_json, vehicle_vin)

        agent.add_message(f'launching_app {app_name}')
        return agent.get_response()

    except:
        agent.add_message('Requested activity cannot be fulfilled.')
        return agent.get_response()
