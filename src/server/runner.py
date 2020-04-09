import cv2
import ffmpeg
import numpy as np
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
    _mp4_path = None
    _wav_path = None

    _total_frames = None
    _frame_rate = None

    _audio_intensity_analyzer = None
    _chunk_length = None

    def __init__(self, **kwargs):
        self._mp4_path = kwargs.get('mp4_path')
        self._wav_path = kwargs.get('wav_path')

        self._frame_rate = Runner.get_frame_rate(self._mp4_path)

        self._audio_intensity_analyzer = AudioIntensityAnalyzer(self._mp4_path)

        self._print_results()

    def _print_results(self):
        poses = self._get_poses()
        self._chunk_length = int(len(self._audio_intensity_analyzer._sound) / self._total_frames) # needs the total frames determined within _get_poses

        emphasized_chunks = self._get_audio_intensity(threshold_quantile=0.7)
        print('Poses matched with chunks: ', list(zip(poses, emphasized_chunks)))

        print('\nRESULTS:')

        percentage_spent_closed = (len([pose for pose in poses if pose == 'closed']) / len(poses)) * 100
        print(f'\t- You spent {percentage_spent_closed}% of your time displaying unwelcoming body language!')

        percentage_spent_open = (len([pose for pose in poses if pose == 'open']) / len(poses)) * 100
        print(f'\t- You spent {percentage_spent_open}% of your time displaying welcoming body language!')

        poses_matched = [int(pose == 'open') for pose in poses]
        if len(emphasized_chunks) > len(poses_matched):
            emphasized_chunks = emphasized_chunks[:len(poses_matched)]

        corrcoef = np.corrcoef(poses_matched, emphasized_chunks)[0][1]
        print(f'\t- You had a correlation of {round(corrcoef, 1)} between your emphasized words and your body language!')

        """
        Cannot use a quantile to determine what counts as silence because we don't know how much silent time is actually in the file.
        Therefore, we take a percentage of the maximum loudness recorded.
        """
        silence_threshold = max([s.rms for s in self._audio_intensity_analyzer._sound]) * 0.1
        speech_rms_values = [s.rms for s in self._audio_intensity_analyzer._sound if s.rms > silence_threshold]

        speech_rms_average = sum(speech_rms_values) / len(speech_rms_values)
        speech_rms_std_dev = np.std(speech_rms_values)
        print(f'\t- {round(100 * (speech_rms_std_dev / speech_rms_average), 1)}% of your enunciation volume was within one standard deviation!')

    def _get_poses(self):
        self._sampling_interval = self._frame_rate // 2 #  Number of frames before a computed frame
        i = 0

        cap = cv2.VideoCapture(self._mp4_path)
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

    def _get_audio_intensity(self, **kwargs):
        return self._audio_intensity_analyzer.get_emphasized_chunks(
            self._chunk_length, 
            kwargs.get('threshold_quantile')
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
        os.system(f'ffmpeg -i {webm_path} -ab 128k -ar 44100 {mp4_path}')

        wav_path = os.path.join(temp_dir, 'presentation.wav')
        os.system(f'ffmpeg -i {webm_path} -ab 128k -ar 44100 {wav_path}')

        results = Runner(mp4_path=mp4_path, wav_path=wav_path)
