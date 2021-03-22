import os
import logging
from flask import Flask

from search_data.query import query
from import_data.imports import import_funct
from fullfillment.app_launch import app_launch

app = Flask(__name__)


logging.basicConfig(filename='wipro_cloud_functions.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/query/', methods=['POST'])
def query_entity(request):
    app.logger.info('Search data function is invoked')
    response = query(request)
    return response


@app.route('/main/', methods=['POST'])
def import_function(request):
    app.logger.info('Data import function is invoked')
    response = import_funct(request)
    return response


@app.route('/webhook/', methods=['POST'])
def handle_app_launch(request):
    app.logger.info('Fulfillment app launch function is invoked')
    response = app_launch(request)
    return response


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
