import os
import requests
from pylogflow import Agent, IntentMap


agent = Agent()

APP_LAUNCH_FUNCTION_URL = os.getenv('APP_LAUNCH_FUNCTION_URL')
INDICATOR_FUNCTION_URL = os.getenv('INDICATOR_FUNCTION_URL')
AMB_LIGHT_FUNCTION_URL = os.getenv('AMB_LIGHT_FUNCTION_URL')
HUD_REL_FUNCTION_URL = os.getenv('HUD_REL_FUNCTION_URL')


def route_app_launch(request):
    return requests.post(APP_LAUNCH_FUNCTION_URL, json=request).text


def route_indicator(request):
    return requests.post(INDICATOR_FUNCTION_URL, json=request).text


def route_amb_light(request):
    return requests.post(AMB_LIGHT_FUNCTION_URL, json=request).text


def route_hud_rel(request):
    return requests.post(HUD_REL_FUNCTION_URL, json=request).text


intentMap = IntentMap()
intentMap.add('AmbRelIntent', route_amb_light)
intentMap.add('AmbNumIntent', route_amb_light)
intentMap.add('AmbPerIntent', route_amb_light)
intentMap.add('AmbSpecIntent', route_amb_light)
intentMap.add('AmbApproxIntent', route_amb_light)
intentMap.add('HUDRelIntent', route_hud_rel)
intentMap.add('HUDNumIntent', route_hud_rel)
intentMap.add('HUDSpecIntent', route_hud_rel)
intentMap.add('HUDApproxIntent', route_hud_rel)
intentMap.add('launchApplication', route_app_launch)
intentMap.add('indicator', route_indicator)

