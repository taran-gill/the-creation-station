import numpy as np
import posenet
import os
import tensorflow as tf


MODEL = 101
SCALE = 1


class PoseEstimator:
    def __init__(self):
        self._config = tf.ConfigProto()
        self._config.gpu_options.allow_growth = True

        self._session = tf.Session(config=self._config)
        model_cfg, self._model_outputs = posenet.load_model(MODEL, self._session)
        self._output_stride = model_cfg['output_stride']


    def get_frame_result(self, image_path):
        input_image, draw_image, output_scale = posenet.read_imgfile(
            image_path,
            scale_factor=SCALE,
            output_stride=self._output_stride
        )

        heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = self._session.run(
            self._model_outputs,
            feed_dict={'image:0': input_image}
        )

        pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
            heatmaps_result.squeeze(axis=0),
            offsets_result.squeeze(axis=0),
            displacement_fwd_result.squeeze(axis=0),
            displacement_bwd_result.squeeze(axis=0),
            output_stride=self._output_stride,
            max_pose_detections=10,
            min_pose_score=0.25
        )

        keypoint_coords *= output_scale
        keypoint_coords = keypoint_coords[0]
        keypoint_scores = keypoint_scores[0]

        results = {}
        for i, (confidence, coordinates) in enumerate(zip(keypoint_scores, keypoint_coords)):
            # Coordinates are given in (Y, X) so we change them
            results[posenet.PART_NAMES[i]] = { 'confidence': confidence, 'coordinates': (coordinates[1], coordinates[0]) }
            print(posenet.PART_NAMES[i], confidence, coordinates)

        return results


    @staticmethod
    def get_elbow_angle(shoulder, elbow, wrist):
        shoulder, elbow, wrist = np.array(shoulder), np.array(elbow), np.array(wrist)

        ba, bc = shoulder - elbow, wrist - elbow

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        return np.rad2deg(angle)


    @staticmethod
    def get_wrist_to_other_elbow_distance(wrist, other_elbow, left_shoulder, right_shoulder):
        """
        If distance of the wrist to the other elbow is small relative to the distance between shoulders,
        the arms are crossed. If the distance is large, the arms are likely outstretched.
        """
        wrist_other_elbow_distance = np.linalg.norm(np.array(wrist) - np.array(other_elbow))
        shoulder_distance = np.linalg.norm(np.array(left_shoulder) - np.array(right_shoulder))

        return wrist_other_elbow_distance / shoulder_distance


    @staticmethod
    def get_ankle_distance(left_ankle, right_ankle, left_hip, right_hip):
        """
        Crossed legs tend to indicate untrustworthiness, while open legs indicate confidence.
        """
        ankle_distance = np.linalg.norm(np.array(left_ankle) - np.array(right_ankle))
        hip_distance = np.linalg.norm(np.array(left_hip) - np.array(right_hip))

        return ankle_distance / hip_distance

