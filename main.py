import os
from flask import Flask

from lib import logger
from search_data import queries as query_data
from import_data import imports as data_import
from fullfillment import app_launch as handle_app_launch
from fullfillment import router as router

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
    response = handle_app_launch.app_launch(request)
    return response


@app.route('/router/', methods=['POST'])
def routing(request):
    logger.logging.info('Fulfillment router function is called')
    response = router.router(request)
    return response


@app.route('/indicator/', methods=['POST'])
def handle_indicator(request):
    logger.logging.info('Fulfillment app launch function is invoked')
    response = handle_indicator.process_handle_indicator(request)
    return response


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
