import json
import nltk
from nltk.corpus import stopwords
import nltk
from sklearn import linear_model
import pickle
from gensim.models import Word2Vec

# nltk.download('popular')

# INPUT: training data (dictionary)
# OUTPUT: trained model

pos_tags_old = {
    "CC": 0, "CD": 1, "DT": 2, "EX": 3, "FW": 4, "IN": 5, "JJ": 6, "JJR": 7, "JJS": 8, "LS": 9, "MD": 10, "NN": 11,
    "NNS": 12, "NNP": 13, "NNPS": 14, "PDT": 15, "POS": 16, "PRP": 17, "PRP$": 18, "RB": 19, "RBR": 20, "RBS": 21,
    "RP": 22, "SYM": 23, "TO": 24, "UH": 25, "VB": 26, "VBD": 27, "VBG": 28, "VBN": 29, "VBP": 30, "VBZ": 31, "WDT": 32,
    "WP": 33, "WPS": 34, "WRB": 35
}

pos_tags = {
    "CC": 0, "CD": 1, "DT": 2, "IN": 3, "JJ": 4, "JJS": 5, "MD": 6, "NN": 7, "NNS": 8, "NNP": 9, "POS": 10, "PRP": 11,
    "PRP$": 12, "RB": 13, "RP": 14, "TO": 15, "VB": 16, "VBD": 17, "VBG": 18, "VBP": 19, "VBZ": 20, "WRB": 21
}


# not necessary, many stop words are crucial so shouldn't filter them out
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence


def pos_tagging(sentence):
    tokens = nltk.word_tokenize(sentence.lower())
    tags = nltk.pos_tag(tokens)
    return tags


def vectorize_sentence(sentence):
    pos_count = [0]*len(pos_tags)
    pos = pos_tagging(sentence)
    # print(pos)
    for word in pos:
        if word[1] in pos_tags.keys():
            pos_count[pos_tags[word[1]]] += 1
    # print(pos_count)
    return pos_count


def run_word2vec():
    with open('data.txt') as json_file:
        data = json.load(json_file)

    sentences = []
    for video in data:
        sentences.append(data[video][0])

    # print(sentences)
    word2vec = Word2Vec(sentences)
    vocabulary = word2vec.wv.vocab
    print(word2vec.wv['artificial'])


# take text and turn it into a usable format
# remove non ascii characters, chunking (NER), lemmatization, stopwords
def preprocess_data():
    with open('video_data.txt') as json_file:
        data = json.load(json_file)

    features = []
    labels = []

    for video in data:
        video_title = data[video][0]
        features.append(vectorize_sentence(video_title))
        ratio = int(data[video][3]) / int(data[video][1])
        labels.append(ratio)

    return features, labels


# take processed text embeddings and fit to model
# transfer learning, decide which regressor to use (SVR or?)
def train_model(features, labels):
    regr = linear_model.LinearRegression()
    regr.fit(features, labels)
    pickle.dump(regr, open('models/nlp_model.sav', 'wb'))


def main():
    features, labels = preprocess_data()
    train_model(features, labels)
    # run_word2vec()


if __name__ == "__main__":
    main()
