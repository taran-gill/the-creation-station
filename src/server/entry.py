from flask import Flask, request
from flask_cors import CORS as cors
import os
import tempfile
import traceback

from runner import Runner


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
        webm_path = os.path.join(temp_dir, 'presentation.webm')
        video_file.save(webm_path)

        mp4_path = os.path.join(temp_dir, 'presentation.mp4')
        os.system(f'ffmpeg -nostdin -loglevel warning -i {webm_path} -ab 128k -ar 44100 {mp4_path}')

        wav_path = os.path.join(temp_dir, 'presentation.wav')
        os.system(f'ffmpeg -nostdin -loglevel warning -i {webm_path} -ab 128k -ar 44100 {wav_path}')

        try:
            results = Runner(mp4_path=mp4_path, wav_path=wav_path)
        except Exception as e:
            print(traceback.format_exc())

    return 'Upload successful!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')
