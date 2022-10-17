from collections import defaultdict, OrderedDict

import numpy as np
import pandas as pd
from main import main
import re
from nltk.stem import LancasterStemmer
from easygui import msgbox

ARTICLE_BLACKLIST = 11000


def text_lemmatiser(text: str = '', dict_words=None) -> [list]:
    if dict_words is None:
        dict_words = {}

    lemmatised_words = []
    lemmatised_dict = {}
    lancaster = LancasterStemmer()

    if str:
        # Remove the leading spaces and newline character
        line = text.strip()
        # Convert the characters in line to lowercase to avoid case mismatch
        line = line.lower()
        # Remove the punctuation marks from the line
        line = re.sub(r'[.,"\'-?:!;]', ' ', line)
        line = re.sub(r'[\([{})\]]', ' ', line)
        # Split the line into words
        words = line.split()

        # words lemmatisation
        lemmatised_words = list(map(lambda w: lancaster.stem(w), words))

    if dict_words:
        lemmatised_dict = defaultdict(int)
        for value in dict_words.items():
            key = lancaster.stem(str(value[0]))
            lemmatised_dict[key] += value[1]

    return lemmatised_words, lemmatised_dict


def count_words(text: str, d: dict) -> dict:
    words, _ = text_lemmatiser(text=text)

    # Iterate over each word in line
    for word in words:
        # Check if the word is already in dictionary
        if word in d:
            # Increment count of word by 1
            d[word] = d[word] + 1
        else:
            # Add the word to dictionary with count 1
            d[word] = 1
    return d


def count_words_perarticle(text: str) -> dict:
    d = dict()

    words, _ = text_lemmatiser(text=text)

    # Iterate over each word in line
    for word in words:
        # Check if the word is already in dictionary
        if word in d:
            # Increment count of word by 1
            d[word] = d[word] + 1
        else:
            # Add the word to dictionary with count 1
            d[word] = 1
    return d


def create_dict(wordlist: dict, threshold: float, size_df: int, blacklist: dict, string: str):
    wordlist = {k: v / size_df for k, v in wordlist.items()}
    dictionary = dict()

    _, blacklist = text_lemmatiser(dict_words=blacklist)

    for value in wordlist.items():
        if value[1] > threshold and value[1] > 4 * blacklist.get(value[0], 0) / ARTICLE_BLACKLIST:
            dictionary[value[0]] = value[1]

    if len(dictionary) != 0:
        return dictionary
    else:
        msgbox("the threshold you have selected for {} is too high. Please select another threshold".format(string),
               "Error")
        exit()


def score_attribution(article_dict: dict, gold_std: dict) -> float:
    count = 0
    for k, v in article_dict.items():
        if k in gold_std:
            count = count + v * gold_std[k]
    return count


def scaler(newMin: float, newMax: float, values: list, x: float):
    min_ = min(values)
    max_ = max(values)
    result = 1
    if min_ != max_:
        result = ((x - min_) * (newMax - newMin) / (max_ - min_) + newMin)
    return result


def compute_score(wordlist_list: list, dict_weights: dict):
    score = list()
    score_norm = list()
    for d in wordlist_list:
        score.append(score_attribution(d, dict_weights))

    for x in score:
        score_norm.append(scaler(0, 1, score, x))
    return score_norm


def matching_articles(score: list, threshold: float):
    matching = list((np.array(score) >= threshold) * 1)
    return matching


def order_and_select_words(dictionary, percentile):
    assert percentile <= 1.00
    assert percentile > 0.00

    # ordering dictionary by value
    dictionary = OrderedDict({k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)})

    # selecting the first (percentile)% elements -> if no elements is included the percentile increases of 0.01
    elements = 0
    while elements < 1:
        elements = int(percentile * len(dictionary))
        percentile += 0.01

    while len(dictionary) > elements:
        dictionary.popitem(last=True)

    return dictionary


def classification_alg(df: pd.DataFrame):
    # Getting the dataframe of articles
    df = df.fillna("None")
    wordlist_list_abs = [dict() for x in range(df.shape[0])]
    wordlist_list_ti = [dict() for x in range(df.shape[0])]
    wordlist_list_kw = [dict() for x in range(df.shape[0])]

    # Step1 - count occurrences of all words (minus black list)

    blacklist_df = pd.read_excel('blacklist_dict.xlsx', engine='openpyxl')
    blacklist = dict(blacklist_df.values)

    wordlist_abstract = dict()
    wordlist_title = dict()
    wordlist_keywords = dict()

    for i in range(df.shape[0]):
        wordlist_abstract = count_words(df.iloc[i]['Abstract'], wordlist_abstract)
        wordlist_title = count_words(df.iloc[i]['Article Title'], wordlist_title)
        wordlist_keywords = count_words(df.iloc[i]['Keywords'], wordlist_keywords)
        wordlist_list_abs[i] = count_words_perarticle(df.iloc[i]['Abstract'])
        wordlist_list_ti[i] = count_words_perarticle(df.iloc[i]['Article Title'])
        wordlist_list_kw[i] = count_words_perarticle(df.iloc[i]['Keywords'])

    # Step2 - create a dictionary based on a threshold
    threshold_dict_abs = 0.0
    threshold_dict_ti = 0.0
    threshold_dict_kw = 0.0

    dictionary_abstract = create_dict(wordlist_abstract, threshold_dict_abs, df.shape[0], blacklist, "abstract")
    dictionary_title = create_dict(wordlist_title, threshold_dict_ti, df.shape[0], blacklist, "title")
    dictionary_keywords = create_dict(wordlist_keywords, threshold_dict_kw, df.shape[0], blacklist, "keywords")

    # Step2.1 - extract first x-th percentile of words
    percentile_abstract = 0.05
    percentile_title = 0.05
    percentile_keywords = 0.05
    dictionary_abstract = order_and_select_words(dictionary=dictionary_abstract, percentile=percentile_abstract)
    dictionary_title = order_and_select_words(dictionary=dictionary_title, percentile=percentile_title)
    dictionary_keywords = order_and_select_words(dictionary=dictionary_keywords, percentile=percentile_keywords)

    # Step3 - scale the occurrences of the words in the dictionary in [0.06, 1]

    values_abs = dictionary_abstract.values()
    values_ti = dictionary_title.values()
    values_kw = dictionary_keywords.values()
    dict_weights_abstract = {key: (scaler(0.06, 1, values_abs, v)) for (key, v) in dictionary_abstract.items()}
    dict_weights_title = {key: (scaler(0.06, 1, values_ti, v)) for (key, v) in dictionary_title.items()}
    dict_weights_keywords = {key: (scaler(0.06, 1, values_kw, v)) for (key, v) in dictionary_keywords.items()}

    # Step4 - on each abstract compute the score and scale it in [0-1]

    score_abs = compute_score(wordlist_list_abs, dict_weights_abstract)
    score_ti = compute_score(wordlist_list_ti, dict_weights_title)
    score_kw = compute_score(wordlist_list_kw, dict_weights_keywords)

    score_final = list(map(lambda abstract, ti, kw: abstract + 5 * ti + 5 * kw, score_abs, score_ti, score_kw))

    # Step5 - scaled score > 0.09 --> classify as 1
    threshold = 0.09
    matching = matching_articles(score_final, threshold)
    if len(matching) != 0:
        df.loc[:, 'Match'] = matching

        print(df[['Article Title', 'Match']])
        return df


# TODO: confusion matrix

if __name__ == '__main__':
    classification_alg()
    print("hello")
