import os
from flask import Flask, request
from flask_cors import CORS as cors

app = Flask(__name__)
cors(app)


@app.before_first_request
def activate():
    if os.environ.get('FLASK_ENV') == 'development':
        app.logger.debug('***On Windows, use your Docker-Machine IP!***')
        app.logger.debug('***Type `docker-machine ip` into Quickstart Terminal***')


@app.route('/ping')
def ping_pong():
    return 'pong'


@app.route('/upload', methods=['POST'])
def upload():
    app.logger.info('Received request ' + str(len(request.get_data())) + ' bytes long')

    return 'Upload successful!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')
