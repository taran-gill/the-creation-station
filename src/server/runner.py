import cv2
import ffmpeg
import os
import sys
import tempfile

from packages.pose_estimation.classifier import PoseClassifier, PoseEstimator
from packages.audio_intensity.audio_intensity import AudioIntensityAnalyzer
from utils.profiler import line_profile


# Don't bother showing info/warnings from TF (it clogs the logs)
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Disable info (1) and warnings (2)


pose_estimator = PoseEstimator()


class Runner:
    _total_frames = None
    _frame_rate = None

    def __init__(self, **kwargs):
        mp4_path = kwargs.get('mp4_path')
        wav_path = kwargs.get('wav_path')

        self.get_poses(mp4_path)

        print('Total frames: ', self._total_frames)

        audio_intensity_analyzer = AudioIntensityAnalyzer(mp4_path)
        THRESHOLD_QUANTILE = 0.75
        emphasized_chunks = \
            audio_intensity_analyzer.get_emphasized_chunks(int(len(audio_intensity_analyzer._sound) / self._total_frames), THRESHOLD_QUANTILE)
        print('Number of emphasized chunks: ', len(emphasized_chunks))

    def get_audio_intensity(self):
        pass

    def get_poses(self, file_path):
        cap = cv2.VideoCapture(file_path)
        ret = True

        print('Beginning video...')

        # XXX while getting the poses, count the number of frames in one pass for efficiency
        # opencv's API is inconsistent on retrieving video metadata
        self._total_frames = 0

        # TODO replace with list w/ each element being the frame's pose
        # NOTE when this happens, make sure to put "None" where confidence threshold not met
        poses_map = {'open': 0, 'closed': 0, 'neutral': 0}

        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break

            self._total_frames += 1

            result = pose_estimator.get_frame_result(frame)
            if result['nose']['confidence'] == 0:
                continue

            pose = PoseClassifier.predict(result)
            poses_map[pose[0]] += 1

        print('Video finished!')
        print('Pose counts:', poses_map)

        probe = ffmpeg.probe(file_path)
        video_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

        """
        The r_frame_rate is the lowest framerate with which all timestamps can be represented accurately
        (i.e. it is the least common multiple of all framerates in the stream)
        """
        frame_rate = video_info['r_frame_rate'].split('/')
        self._frame_rate = float(frame_rate[0]) / float(frame_rate[1])

        print('Total frames:', self._total_frames)
        print('Frame rate:', self._frame_rate)
        print('Duration:', self._total_frames / self._frame_rate)

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    file = 'trailer.webm' if len(sys.argv) < 2 else sys.argv[1]

    script_path = os.path.abspath(os.path.join(os.getcwd(), 'fixtures/'))
    webm_path = os.path.join(script_path, file)

    with tempfile.TemporaryDirectory() as temp_dir:
        mp4_path = os.path.join(temp_dir, 'presentation.mp4')
        os.system(f'ffmpeg -loglevel warning -i {webm_path} -ab 128k -ar 44100 {mp4_path}')

        wav_path = os.path.join(temp_dir, 'presentation.wav')
        os.system(f'ffmpeg -loglevel warning -i {webm_path} -ab 128k -ar 44100 {wav_path}')

        results = Runner(mp4_path=mp4_path)
