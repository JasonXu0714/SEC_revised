import re
import pandas as pd
import nltk
import ssl
from collections import Counter

ssl._create_default_https_context = ssl._create_unverified_context
# download once at initialization
# nltk.download("stopwords")
# nltk.download("punkt")

# use of nltk packages
bigrams = nltk.bigrams
word_tokens = nltk.word_tokenize
stop_words = nltk.corpus.stopwords.words("english")


def filter_words(data):
    if pd.isnull(data) or not isinstance(data, str):
        return []
    data = word_tokens(data)
    wordFiltered = [w for w in data if w not in stop_words]
    return wordFiltered


def produce_grams(list_of_string):
    merged_string = " ".join(list_of_string)
    # Convert to lowercase for processing
    x_lower = merged_string.lower()
    grams = []
    words = re.compile("\w+").findall(x_lower)
    bi = [" ".join(bigram) for bigram in list(bigrams(words))]
    grams.extend(words)
    grams.extend(bi)
    return grams
