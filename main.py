import os

from flask import Flask

app = Flask(__name__)

from importfunction.DataImport import import_funct
from queryfunction.Query import query


@app.route('/query/', methods=['POST'])
def query_entity(request):
    response = query(request)
    return response


@app.route('/main/', methods=['POST'])
def import_function(request):
    response = import_funct(request)
    return response


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
