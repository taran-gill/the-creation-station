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
            min_pose_score=0.25)

        keypoint_coords *= output_scale
        keypoint_coords = keypoint_coords[0]
        keypoint_scores = keypoint_scores[0]

        results = {}

        for i, (confidence, coordinates) in enumerate(zip(keypoint_scores, keypoint_coords)):
            results[posenet.PART_NAMES[i]] = { 'confidence': confidence, 'coordinates': coordinates }

        print(results)

        return results

        # print('KEYPOINT_SCORES', keypoint_scores)
        # print('KEYPOINT_COORDS', keypoint_coords)
        # print('POSE_SCORES', pose_scores)

        # print()
        # print("Results for image: %s" % image_path)
        # for pi in range(len(pose_scores)):
        #     if pose_scores[pi] == 0.:
        #         break
        #     print('Pose #%d, score = %f' % (pi, pose_scores[pi]))
        #     for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
        #         print('Keypoint %s, score = %f, coord = %s' % (posenet.PART_NAMES[ki], s, c))

if __name__ == "__main__":
    pose_estimator = PoseEstimator()
    pose_estimator.get_frame_result('./images/open_gesture.jpg')
