import cv2
from flask import Flask, request
from flask_cors import CORS as cors
import os
import tempfile
from packages.pose_estimation.classifier import PoseClassifier, PoseEstimator


# Don't bother showing info/warnings from TF (it clogs the logs)
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Disable info (1) and warnings (2)


pose_estimator = PoseEstimator()

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
        file_path = os.path.join(temp_dir, 'presentation.webm')
        video_file.save(file_path)

        try:
            cap = cv2.VideoCapture(file_path)
            ret = True

            while(cap.isOpened()):
                ret, frame = cap.read()
                if not ret:
                    break

                result = pose_estimator.get_frame_result(frame)
                if result['nose']['confidence'] == 0:
                    continue

                print(PoseClassifier.predict(result))
            print('Video finished!')

            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print('Error: ', e)

    return 'Upload successful!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')
