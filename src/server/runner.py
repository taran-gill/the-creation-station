import cv2
import ffmpeg
import os
from packages.pose_estimation.classifier import PoseClassifier, PoseEstimator


# Don't bother showing info/warnings from TF (it clogs the logs)
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Disable info (1) and warnings (2)


pose_estimator = PoseEstimator()


class Runner:
    def __init__(self, file_path):
        self._file_path = file_path

        self.get_poses()

    def get_audio_intensity(self):
        pass

    def get_poses(self):
        cap = cv2.VideoCapture(self._file_path)
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

        probe = ffmpeg.probe(self._file_path)
        video_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

        """
        The r_frame_rate is the lowest framerate with which all timestamps can be represented accurately 
        (i.e. it is the least common multiple of all framerates in the stream)
        """
        frame_rate = video_info['r_frame_rate'].split('/')
        frame_rate = float(frame_rate[0]) / float(frame_rate[1])

        print('Total frames:', self._total_frames)
        print('Frame rate:', frame_rate)
        print('Duration:', self._total_frames / frame_rate)

        cap.release()
        cv2.destroyAllWindows()
