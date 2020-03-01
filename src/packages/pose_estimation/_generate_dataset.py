from estimator import PoseEstimator
import json
import os


if __name__ == '__main__':
    pose_estimator = PoseEstimator()

    filenames = [f.path for f in os.scandir('./images') if f.is_file()]

    dataset = []

    for f in filenames:
        print('\n')
        print(f)
        result = pose_estimator.get_frame_result(f)

        pose = f.split('./images/')[1].split('_')[0]

        data = {'pose': f.split('./images/')[1].split('_')[0]}

        data['left_elbow_angle'] = PoseEstimator.get_elbow_angle(
            result['leftShoulder']['coordinates'],
            result['leftElbow']['coordinates'],
            result['leftWrist']['coordinates']
        ) / 360
        data['right_elbow_angle'] = PoseEstimator.get_elbow_angle(
            result['rightShoulder']['coordinates'],
            result['rightElbow']['coordinates'],
            result['rightWrist']['coordinates']
        ) / 360

        data['left_wrist_right_elbow_distance'] = PoseEstimator.get_wrist_to_other_elbow_distance(
            result['leftWrist']['coordinates'],
            result['rightElbow']['coordinates'],
            result['leftShoulder']['coordinates'],
            result['rightShoulder']['coordinates']
        ) / 3.6
        data['right_wrist_left_elbow_distance'] = PoseEstimator.get_wrist_to_other_elbow_distance(
            result['rightWrist']['coordinates'],
            result['leftElbow']['coordinates'],
            result['leftShoulder']['coordinates'],
            result['rightShoulder']['coordinates']
        ) / 3.6

        data['ankle_distance'] = 0.9
        if result['leftAnkle']['confidence'] > 0.5 and result['leftAnkle']['confidence'] > 0.5:
            data['ankle_distance'] = PoseEstimator.get_wrist_to_other_elbow_distance(
                result['leftAnkle']['coordinates'],
                result['rightAnkle']['coordinates'],
                result['leftHip']['coordinates'],
                result['rightHip']['coordinates']
            )
        print(data['ankle_distance'])

        dataset.append(data)

    with open('dataset.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)
