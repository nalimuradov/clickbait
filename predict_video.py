import pickle
import numpy
import requests
from PIL import Image
from io import BytesIO
from train import train_nlp_model
from flask import Flask, request, render_template
import cv2
import flask
import scipy.stats as st

# flask app setup
app = Flask(__name__)

# default route to templates/index.html on load
@app.route('/')
def home():
    return render_template('index.html')


# calculate results on request (submission of image and title)
@app.route('/', methods=['POST'])
def display():
    data = [x for x in request.form.values()]
    files = request.files.get('img_file')
    vid_title = data[0]
    thumbnail = cv2.imdecode(numpy.fromstring(files.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    thumbnail = Image.fromarray(thumbnail)
    thumbnail = thumbnail.convert('RGB')
    thumbnail = numpy.array(thumbnail)
    print(thumbnail.shape)
    prediction = predict(vid_title, thumbnail)

    # output on user submission
    pre_note = "Your title and thumbnail are better than..."
    post_note = "of the videos I trained on!"
    sub_post_note = "(in terms of views per subscribers)"
    return render_template('index.html', prediction_text='{}%'.format(prediction),
                           pre_note=pre_note, post_note=post_note, sub_post_note=sub_post_note)


# helper function to format output
def format_number(num):
    return '{:,}'.format(num).replace(',', ' ')


# use models to fit input given by the user - result is the view success of the video relative to training data
def predict(title, thumbnail):
    img_model = pickle.load(open('models/def_img_model.sav', 'rb'))
    nlp_model = pickle.load(open('models/nlp_model.sav', 'rb'))
    # model_cut = load_model('models/resnet50.h5', compile=False)

    img = [cv2.resize(thumbnail, dsize=(120, 90), interpolation=cv2.INTER_CUBIC).flatten()]
    title = [train_nlp_model.vectorize_sentence(title)]
    img_predict = img_model.predict(img)
    nlp_predict = nlp_model.predict(title)
    expected_view_ratio = float((img_predict[0] + nlp_predict[0]) / 2)

    # calculated mean and deviation of data - used for calculating relative success mentioned above
    mean = 0.774
    stdev = 0.645
    z_score = (expected_view_ratio - mean) / stdev
    final_view_score = st.norm.sf(z_score)
    final_view_score = float("{:.2f}".format(100*(1 - final_view_score)))
    print(final_view_score)

    return final_view_score


if __name__ == "__main__":
    app.run(debug=True)
