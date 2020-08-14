from bs4 import BeautifulSoup
import requests
import numpy as np

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

import networkx as nx
from PIL import Image, ImageDraw, ImageFont

SYMBOLS = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n,—'"
STOP_WORDS = stopwords.words('english')
LEMMATIZER = WordNetLemmatizer()
STEMMER = SnowballStemmer("english")

def get_text(url):
    r  = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    title = soup.find('h1').text
    summary = soup.find('p', {"class": "c-entry-summary p-dek"}).text
    data = ""
    for x in soup.find("div", {"class":"c-entry-content"}).find_all("p"):
        data += " "+x.text
    return title, summary, data

def remove_symbols(text):
    for symbol in SYMBOLS:
        text = text.replace(symbol, '')
    return text


def remove_stop_words(vocabulary):
    valid_words = [x for x in vocabulary if x not in STOP_WORDS and x.isalpha()]
    return valid_words


def stem_and_lemmatize(vocabulary):
    stemmed_lemmatized_words = [STEMMER.stem(LEMMATIZER.lemmatize(x)) for x in vocabulary]
    return stemmed_lemmatized_words

def clean_text(data):
    original_sentences = sent_tokenize(data)
    cleaned_sentences = []
    for sentence in original_sentences:
        sentence = sentence.lower()
        sentence = remove_symbols(sentence)
        vocabulary = word_tokenize(sentence)
        vocabulary = remove_stop_words(vocabulary)
        stemmed_lemmatized_words = stem_and_lemmatize(vocabulary)
        cleaned_sentences.append(" ".join(stemmed_lemmatized_words))
    return original_sentences, cleaned_sentences

def important_indices(cleaned_sentences):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(cleaned_sentences)
    cosines = cosine_similarity(X)
    np.fill_diagonal(cosines, 0)
    nx_graph = nx.from_numpy_array(cosines)
    scores = nx.pagerank(nx_graph)
    scores = np.array(list(scores.values()))
    best = np.where(scores > np.quantile(scores, 0.90))
    return best

def get_summary(url):
    title, summary, data = get_text(url)
    original_sentences, cleaned_sentences = clean_text(data)
    indeces = important_indices(cleaned_sentences)
    return title + ". " + summary + " " + " ".join(np.array(original_sentences)[indeces])

def create_TLDR(url):
    content = get_summary(url)
    f = ""
    count = 0
    for char in content:
        f += char
        if count >= 110 and char == " ":
            f += "\n"
            count = 0
        else:
            count += 1

    img = Image.new('RGB', (1200, 675), color = (255, 255, 255))

    fnt = ImageFont.truetype('./Arial.ttf', 20)
    d = ImageDraw.Draw(img)
    d.text((20,20), f, font=fnt, fill=(0, 0, 0))
    img.save('./pil_text_font.png')
