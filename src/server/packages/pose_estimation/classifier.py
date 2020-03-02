import json
import numpy as np
import pandas as pd
from os import path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from .estimator import PoseEstimator


dataset_path = path.join(path.dirname(path.realpath(__file__)), 'dataset.json')
with open(dataset_path, 'r', encoding='utf-8') as fd:
    dataset = json.load(fd)

FEATURES = [feature for feature in dataset[0] if feature != 'pose']


poses = pd.read_json(dataset_path)
poses.head()

X_train, X_test, y_train, y_test = train_test_split(poses[FEATURES], poses['pose'], random_state=0)

scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

N_NEIGHBORS = 1
knn = KNeighborsClassifier(n_neighbors=N_NEIGHBORS)
knn.fit(X_train, y_train)
print('Accuracy of K-NN (K={:d}) classifier on training set: {:.2f}'
     .format(N_NEIGHBORS, knn.score(X_train, y_train)))
print('Accuracy of K-NN (K={:d}) classifier on test set: {:.2f}'
     .format(N_NEIGHBORS, knn.score(X_test, y_test)))


class PoseClassifier:
    @staticmethod
    def predict(pose):
        data = [None] * len(FEATURES)

        data[0], data[1] = PoseEstimator.get_elbow_angles(pose, scaled=True)

        data[2], data[3] = \
            PoseEstimator.get_wrist_to_other_elbow_distances(pose, scaled=True)

        data[4] = PoseEstimator.get_ankle_distance(pose, scaled=True)

        return knn.predict([data])

def knn_predict(pose):
    data = [None] * 5

    data[0], data[1] = PoseEstimator.get_elbow_angles(pose, scaled=True)

    data[2], data[3] = \
        PoseEstimator.get_wrist_to_other_elbow_distances(pose, scaled=True)

    data[4] = PoseEstimator.get_ankle_distance(pose, scaled=True)

    print(knn.predict([data]))