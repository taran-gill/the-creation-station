import cv2
import ffmpeg
import os
import sys
import tempfile

from packages.audio_intensity.audio_intensity import AudioIntensityAnalyzer
from packages.pose_estimation.classifier import PoseClassifier, PoseEstimator
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

        self._frame_rate = Runner.get_frame_rate(mp4_path)

        poses = self._get_poses(mp4_path)
        emphasized_chunks = self._get_audio_intensity(mp4_path)

        print('Number of poses: ', len(poses))
        print('Number of emphasized chunks: ', len(emphasized_chunks))

        print('Poses matched with chunks: ', list(zip(poses, emphasized_chunks)))

        percentage_spent_closed = (len([pose for pose in poses if pose == 'closed']) / len(poses)) * 100

        print('\nRESULTS:')
        print(f'\t- You spent {percentage_spent_closed}% of your time displaying unwelcoming body language!')

    def _get_poses(self, file_path):
        self._sampling_interval = self._frame_rate // 2 #  Number of frames before a computed frame
        i = 0

        cap = cv2.VideoCapture(file_path)
        ret = True

        # XXX while getting the poses, count the number of frames in one pass for efficiency
        # opencv's API is inconsistent on retrieving video metadata
        self._total_frames = 0

        poses = []

        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break

            i += 1
            if i != self._sampling_interval:
                continue
            i = 0

            self._total_frames += 1

            result = pose_estimator.get_frame_result(frame)
            if result['nose']['confidence'] == 0:
                poses.append(None)
                continue

            pose = PoseClassifier.predict(result)
            poses.append(pose[0])

        cap.release()
        cv2.destroyAllWindows()

        print('Total frames:', self._total_frames)
        print('Frame rate:', self._frame_rate)
        print('Calculated video duration:', (self._total_frames * self._sampling_interval) / self._frame_rate)

        return poses

    def _get_audio_intensity(self, file_path):
        THRESHOLD_QUANTILE = 0.75
        audio_intensity_analyzer = AudioIntensityAnalyzer(file_path)

        return audio_intensity_analyzer.get_emphasized_chunks(
            int(len(audio_intensity_analyzer._sound) / self._total_frames), 
            THRESHOLD_QUANTILE
        )

    @staticmethod
    def get_frame_rate(file_path):
        probe = ffmpeg.probe(file_path)
        video_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

        """
        The r_frame_rate is the lowest framerate with which all timestamps can be represented accurately
        (i.e. it is the least common multiple of all framerates in the stream)
        """
        frame_rate = video_info['r_frame_rate'].split('/')
        return float(frame_rate[0]) / float(frame_rate[1])


if __name__ == '__main__':
    file = 'trailer.webm' if len(sys.argv) < 2 else sys.argv[1]

    script_path = os.path.abspath(os.path.join(os.getcwd(), 'fixtures/'))
    webm_path = os.path.join(script_path, file)

    with tempfile.TemporaryDirectory() as temp_dir:
        mp4_path = os.path.join(temp_dir, 'presentation.mp4')
        os.system(f'ffmpeg -loglevel warning -i {webm_path} -ss 00:00:02 -ab 128k -ar 44100 {mp4_path}')

        wav_path = os.path.join(temp_dir, 'presentation.wav')
        os.system(f'ffmpeg -loglevel warning -i {webm_path} -ss 00:00:02 -ab 128k -ar 44100 {wav_path}')

        results = Runner(mp4_path=mp4_path)
