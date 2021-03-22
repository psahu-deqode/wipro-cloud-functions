from import_data.imports import import_funct
from search_data.query import query
from fullfillment.app_launch import process_handle_app_launch
import os
from flask import Flask

app = Flask(__name__)


@app.route('/query/', methods=['POST'])
def query_entity(request):
    response = query(request)
    return response


@app.route('/main/', methods=['POST'])
def import_function(request):
    response = import_funct(request)
    return response


@app.route('/webhook/', methods=['POST'])
def webhook(request):
    response = process_handle_app_launch(request)
    return response


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
