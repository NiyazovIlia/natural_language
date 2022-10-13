import pandas as pd
import numpy as np
import re
import annoy
from stop_words import get_stop_words
from gensim.models import Word2Vec
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords
import warnings

warnings.filterwarnings("ignore")


def main(text_movie):
    df = pd.read_csv('kino_p2.csv')

    def tweets_preprocessing(example):
        # Заменим на нижний регистр
        example = example.lower()
        # Заменим пунктуацию на пробелы
        example = re.sub(r'[^\w\s]', ' ', example)
        # Заменим спец. символы на пробелы
        example = re.sub(r'[^a-zA-Zа-яёA-ЯЁ0-9]', ' ', example)
        # Заменим числа на пробелы
        example = re.sub(r'[^a-zA-Zа-яёA-ЯЁ]', ' ', example)
        # Удалим символы
        example = ' '.join([w for w in example.split() if len(w) > 1])
        # Удалим из текста слова длиной в 2 символа
        example = [w for w in example.split() if len(w) > 2]
        # Удалим стоп-слова
        stop_words = get_stop_words("ru") + stopwords.words('russian')
        example = [w for w in example if w not in stop_words]
        # Приведем к нормальной форме
        test_1 = []
        lematiz = WordNetLemmatizer()
        for i in test_1:
            test_1.append(lematiz.lemmatize(i))
        test_2 = []
        stemmer = SnowballStemmer(language="russian")
        for i in example:
            test_2.append(stemmer.stem(i))

        return test_2

    df['preprocessed'] = df.preprocessed.apply(tweets_preprocessing)

    def test_2(df):
        text_2 = [tweet for tweet in df['preprocessed'].values if len(tweet) > 2]
        return text_2

    text = test_2(df)

    modelW2V = Word2Vec(sentences=text, vector_size=250, window=5, min_count=1, workers=10, batch_words=10)

    w2v_index = annoy.AnnoyIndex(250, 'angular')

    index_map = {}
    counter = 0

    for line in df['preprocessed']:
        n_w2v = 0
        index_map[counter] = line

        vector_w2v = np.zeros(250)
        for word in line:
            if word in modelW2V.wv:
                vector_w2v += modelW2V.wv[word]
                n_w2v += 1
        if n_w2v > 0:
            vector_w2v = vector_w2v / n_w2v
        w2v_index.add_item(counter, vector_w2v)

        counter += 1

        if counter > 100000:
            break

    w2v_index.build(15)

    def get_response(tweet, index, model, index_map):
        tweet = tweets_preprocessing(tweet)
        vector = np.zeros(250)
        norm = 0
        for word in tweet:
            if word in model.wv:
                vector += model.wv[word]
                norm += 1
        if norm > 0:
            vector = vector / norm
        answers = index.get_nns_by_vector(vector, 5, )
        return [df.movie.values[i] for i in answers]

    return get_response(text_movie, w2v_index, modelW2V, index_map)
