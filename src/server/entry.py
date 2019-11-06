import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        app.logger.debug('***On Windows, use your Docker-Machine IP!***')
        app.logger.debug('***Type `docker-machine ip` into Quickstart Terminal***')

    app.run(debug=True, host='0.0.0.0')
