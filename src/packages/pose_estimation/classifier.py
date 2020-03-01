import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier


with open('dataset.json', 'r', encoding='utf-8') as fd:
    dataset = json.load(fd)

FEATURES = [feature for feature in dataset[0] if feature != 'pose']

poses = pd.read_json('dataset.json')
poses.head()

X_train, X_test, y_train, y_test = train_test_split(poses[FEATURES], poses['pose'], random_state=0)

scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

logreg = LogisticRegression()
logreg.fit(X_train, y_train)
print('Accuracy of Logistic regression classifier on training set: {:.2f}'
     .format(logreg.score(X_train, y_train)))
print('Accuracy of Logistic regression classifier on test set: {:.2f}'
     .format(logreg.score(X_test, y_test)))

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)
print('Accuracy of K-NN classifier on training set: {:.2f}'
     .format(knn.score(X_train, y_train)))
print('Accuracy of K-NN classifier on test set: {:.2f}'
     .format(knn.score(X_test, y_test)))

x = knn.predict([[0.17528203799986225, 0.22766950714831652, 0.27189179513486567, 0.22138988155591524, 0.9]])
print(x)