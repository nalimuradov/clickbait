import json
from sklearn.svm import SVR
import numpy
import pickle
from PIL import Image
import requests
from io import BytesIO

# INPUT: training data (rgb map)
# OUTPUT: trained model


def preprocess_data():
    with open('video_data.txt') as json_file:
        data = json.load(json_file)

    features = []
    labels = []

    for video in data:
        response = requests.get(data[video][2])
        img = numpy.asarray(Image.open(BytesIO(response.content)))
        features.append(img.flatten())
        ratio = int(data[video][3]) / int(data[video][1])
        labels.append(ratio)

    return features, labels


def train_model(features, labels):
    regr = SVR(kernel='linear')
    regr.fit(features, labels)
    pickle.dump(regr, open('models/img_model.sav', 'wb'))


def main():
    features, labels = preprocess_data()
    train_model(features, labels)


if __name__ == "__main__":
    main()
