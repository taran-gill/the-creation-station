import cv2
from flask import Flask, request
from flask_cors import CORS as cors
import os
import tempfile


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
    video_file = request.files['video-blob']

    with tempfile.TemporaryDirectory() as temp_dir:
        print('Created temporary directory', temp_dir)

        file_path = os.path.join(temp_dir, 'x.webm')
        print(file_path)
        video_file.save(file_path)
        try:
            cap = cv2.VideoCapture(file_path)
            ret = True

            while(ret and cap.isOpened()):
                ret, frame = cap.read()
                print(frame)
            print('Video finished!')

            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print('Error: ', e)

    return 'Upload successful!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')
