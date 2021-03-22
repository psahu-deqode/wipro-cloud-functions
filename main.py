import os
from flask import Flask

from search_data import query
from import_data import imports
from fullfillment import app_launch

app = Flask(__name__)


@app.route('/query/', methods=['POST'])
def query_entity(request):
    app.logger.info('Search data function is invoked')
    response = query.query(request)
    return response


@app.route('/main/', methods=['POST'])
def import_function(request):
    app.logger.info('Data import function is invoked')
    response = imports.import_funct(request)
    return response


@app.route('/webhook/', methods=['POST'])
def handle_app_launch(request):
    app.logger.info('Fulfillment app launch function is invoked')
    response = app_launch.app_launch(request)
    return response


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
