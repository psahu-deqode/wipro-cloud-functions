import os

import requests
from google.cloud import dialogflow

from lib.datastore import PROJECT_ID

dialogflow.AgentsClient.agent_path(PROJECT_ID)

APP_LAUNCH_FUNCTION_URL = os.getenv('APP_LAUNCH_FUNCTION_URL')
INDICATOR_FUNCTION_URL = os.getenv('INDICATOR_FUNCTION_URL')


def router(request):
    request_body = request.get_json(silent=True)

    def handle_app_launch(request_body):
        return requests.post(APP_LAUNCH_FUNCTION_URL, json=request_body).text

    def handle_indicator(request_body):
        return requests.post(INDICATOR_FUNCTION_URL, json=request_body).text

    if request_body.get('queryResult').get('intent').get("displayName") == 'launchApplication':
        return handle_app_launch(request_body)

    if request_body.get('queryResult').get('intent').get("displayName") == 'indicator':
        return handle_indicator(request_body)
