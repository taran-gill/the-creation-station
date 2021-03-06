import json
import numpy as np
import os
from estimator import PoseEstimator


if __name__ == '__main__':
    pose_estimator = PoseEstimator()

    filenames = [f.path for f in os.scandir('./images') if f.is_file()]

    print('Generating dataset for', len(filenames), 'images')

    dataset = []

    for f in filenames:
        print(f)
        result = pose_estimator.get_image_file_result(f)

        pose = f.split('./images/')[1].split('_')[0]

        data = {'pose': f.split('./images/')[1].split('_')[0]}

        data['left_elbow_angle'], data['right_elbow_angle'] = PoseEstimator.get_elbow_angles(result, scaled=True)

        data['left_wrist_right_elbow_distance'], data['right_wrist_left_elbow_distance'] = \
            PoseEstimator.get_wrist_to_other_elbow_distances(result, scaled=True)

        data['ankle_distance'] = PoseEstimator.get_ankle_distance(result, scaled=True)

        if np.isnan(data['left_elbow_angle']) or np.isnan(data['right_elbow_angle']) or \
                np.isnan(data['left_wrist_right_elbow_distance']) or \
                np.isnan(data['right_wrist_left_elbow_distance']) or \
                np.isnan(data['ankle_distance']):
            print('ERROR: Unable to generate features for', f)
            continue

        print('Generated features for', f)
        dataset.append(data)

    with open(os.environ['POSE_DATASET_PATH'], 'w', encoding='utf-8') as f:
        print('Generated dataset', len(dataset), 'images')
        json.dump(dataset, f, ensure_ascii=False, indent=4)
