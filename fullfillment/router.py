import os
import requests
from pylogflow import Agent, IntentMap


agent = Agent()
APP_LAUNCH_FUNCTION_URL = os.getenv('APP_LAUNCH_FUNCTION_URL')
INDICATOR_FUNCTION_URL = os.getenv('INDICATOR_FUNCTION_URL')


def route_app_launch(request):
    return requests.post(APP_LAUNCH_FUNCTION_URL, json=request).text


def route_indicator(request):
    result = requests.post(INDICATOR_FUNCTION_URL, json=request).text
    return result


intentMap = IntentMap()
intentMap.add('launchApplication', route_app_launch)
intentMap.add('indicator', route_indicator)
