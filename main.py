import os
from flask import Flask

from lib import logger
from dom import search_in_dom
from IoTcore import iotcore_cloud_functions
from fullfillment.router import intentMap
from search_data import queries as query_data
from import_data import imports as data_import
from fullfillment import hud_rel as handle_hud_rel
from fullfillment import indicator as handle_indicator
from fullfillment import amb_light as handle_amb_light
from fullfillment import app_launch as handle_app_launch

app = Flask(__name__)


@app.route('/query/', methods=['POST'])
def search_data(request):
    logger.logging.info('Search data function is invoked')
    response = query_data.search_data(request)
    return response


@app.route('/main/', methods=['POST'])
def import_data(request):
    logger.logging.info('Data import function is invoked')
    response = data_import.import_data(request)
    return response


@app.route('/webhook/', methods=['POST'])
def app_launch(request):
    logger.logging.info('Fulfillment app launch function is invoked')
    response = handle_app_launch.process_app_launch(request)
    return response


@app.route('/indicator/', methods=['POST'])
def indicator(request):
    logger.logging.info('Fulfillment app launch function is invoked')
    response = handle_indicator.process_handle_indicator(request)
    return response


@app.route('/amblight/', methods=['POST'])
def amb_light(request):
    logger.logging.info('Fulfillment amb light function is invoked')
    response = handle_amb_light.process_handle_amb_light(request)
    return response


@app.route('/hudrel/', methods=['POST'])
def hud_rel(request):
    logger.logging.info('Fulfillment hud rel function is invoked')
    response = handle_hud_rel.process_handle_hud_rel(request)
    return response


@app.route('/router/', methods=['POST'])
def routing(request):
    logger.logging.info('Fulfillment router function is called')
    result = intentMap.execute_intent(request.json)
    return result


@app.route('/search/', methods=['POST'])
def dom_search(request):
    logger.logging.info('Dom search function is invoked')
    response = search_in_dom.search_in_dom(request)
    return response


@app.route('/command/', methods=['POST'])
def command_to_device(request):
    response = iotcore_cloud_functions.send_command_to_device(request)
    return response


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
