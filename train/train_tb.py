import json
from sklearn import svm
import numpy
import pickle
from PIL import Image
import requests
from io import BytesIO
import math
import cv2

# load data and clean for model training
def preprocess_data():
    with open('data/video_data.txt') as json_file:
        data = json.load(json_file)

    features = []
    labels = []

    for video in data:
        response = requests.get(data[video][2])
        img = numpy.asarray(Image.open(BytesIO(response.content)))
        features.append(img)

        ratio = math.sqrt(int(data[video][3]) / int(data[video][1]))
        labels.append(ratio)

    return features, labels


# features extracted using transfer learning
def extract_features(x):
    resnet_features = []

    model = ResNet50(weights='imagenet')
    model_cut = Model(model.input, model.layers[-2].output)
    model_cut.save('resnet50.h5')

    for i in x:
        i = cv2.resize(i, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)
        i = numpy.asarray(i)
        resnet_features.append(i)

    resnet_features = numpy.asarray(resnet_features)
    resnet_features = model_cut.predict(resnet_features)

    return resnet_features


# classifying based on extracted features
def train_model(features, labels):
    regr = svm.SVR()
    regr.fit(features, labels)
    pickle.dump(regr, open('resnet_img_model.sav', 'wb'))


# run to train the model
def main():
    features, labels = preprocess_data()
    features = extract_features(features)
    train_model(features, labels)


if __name__ == "__main__":
    main()
