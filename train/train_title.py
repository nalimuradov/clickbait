import json
import nltk
from nltk.corpus import stopwords
import nltk
from sklearn import linear_model, svm
import pickle
from gensim.models import Word2Vec
import math
import heapq
import statistics
import numpy


# dictionary of 22 most common POS tags
pos_tags = {
    "CC": 0, "CD": 1, "DT": 2, "IN": 3, "JJ": 4, "JJS": 5, "MD": 6, "NN": 7, "NNS": 8, "NNP": 9, "POS": 10, "PRP": 11,
    "PRP$": 12, "RB": 13, "RP": 14, "TO": 15, "VB": 16, "VBD": 17, "VBG": 18, "VBP": 19, "VBZ": 20, "WRB": 21
}


# function to remove stop words (eg. 'a', 'the')
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence


# returns tags given a sentence
def pos_tagging(sentence):
    tokens = nltk.word_tokenize(sentence.lower())
    tags = nltk.pos_tag(tokens)
    return tags


# after being tagged, create feature vector of the part-of-speech counts 
# this vector will be used to train the model
def vectorize_sentence(sentence):
    pos_count = [0]*(len(pos_tags)*(len(pos_tags) + 1))
    pos = pos_tagging(sentence)
    for word in pos:
        if word[1] in pos_tags.keys():
            pos_count[pos_tags[word[1]]] += 1

    # now we do squared part
    for i in range(len(pos) - 1):
        if pos[i][1] in pos_tags.keys():
            if pos[i+1][1] in pos_tags.keys():
                position_index = len(pos_tags) + len(pos_tags) * pos_tags[pos[i][1]] + pos_tags[pos[i+1][1]]
                pos_count[position_index] += 1
    # print(pos_count)
    return pos_count


# testing word2vec
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
    with open('data/video_data.txt') as json_file:
        data = json.load(json_file)

    features = []
    labels = []

    for video in data:
        video_title = data[video][0]
        features.append(vectorize_sentence(video_title))
        # features.append(video_title)
        ratio = math.sqrt(int(data[video][3]) / int(data[video][1]))
        labels.append(ratio)
    return features, labels


# classifying based on extracted features (vector of pos tags)
def train_model(features, labels):
    regr = svm.SVR()
    regr.fit(features, labels)
    pickle.dump(regr, open('nlp_model.sav', 'wb'))


# run to train the model
def main():
    features, labels = preprocess_data()
    train_model(features, labels)
    # run_word2vec()


if __name__ == "__main__":
    main()
