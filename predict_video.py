import pickle
import numpy
import requests
from PIL import Image
from io import BytesIO
from train import train_nlp_model
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/', methods=['POST'])
def display():
    data = [x for x in request.form.values()]
    print(data[0])
    prediction = predict(data[0])
    return render_template('index.html', prediction_text='Proportion: {}'.format(prediction))


def predict(title):
    img_model = pickle.load(open('models/img_model.sav', 'rb'))
    nlp_model = pickle.load(open('models/nlp_model.sav', 'rb'))

    response = requests.get('https://i.ytimg.com/vi/xfQBkdLa6fo/default.jpg')
    img = [numpy.asarray(Image.open(BytesIO(response.content))).flatten()]

    title = [train_nlp_model.vectorize_sentence(title)]

    img_predict = img_model.predict(img)
    nlp_predict = nlp_model.predict(title)

    expected_view_ratio = "{:.2f}".format((img_predict[0] + nlp_predict[0]) / 2)
    print(expected_view_ratio)
    return expected_view_ratio


if __name__ == "__main__":
    app.run(debug=True)
