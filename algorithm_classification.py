from collections import defaultdict, OrderedDict
import numpy as np
import pandas as pd
import re
from nltk.stem import LancasterStemmer

ARTICLE_BLACKLIST = 11000


def text_lemmatiser(text: str = '', dict_words=None) -> [list]:
    """
    Perform text lemmatization on a string or a dictionary of words
    :param text: a string containing the text
    :type text: str
    :param dict_words: a dictionary of words (strings)
    :type dict_words: dict
    :return: list of lemmatised words and dictionary of lemmatised words
    :rtype: list[str] and dict
    """
    if dict_words is None:
        dict_words = {}

    lemmatised_words = []
    lemmatised_dict = {}
    lancaster = LancasterStemmer()

    if text:
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


def count_words(text: str, d: dict = None) -> dict:
    """
    Count the occurrences of each word present in text
    :param text: string
    :param d: dictionary
    :return: dictionary with words and related occurrences
    """
    if d is None:
        d = {}
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



def filter_dict(wordlist: dict, size_df: int, general_dictionary: dict, string: str):
    """
    Filter the dictionary of relevant words based on a general dictionary
    :param wordlist: dictionary of all the words
    :param size_df: number of articles
    :param general_dictionary: dictionary of general word
    :return: dictionary of relevant words
    """
    # divide the count of each word by the number of articles
    wordlist = {k: v / size_df for k, v in wordlist.items()}
    dictionary = dict()

    _, general_dictionary = text_lemmatiser(dict_words=general_dictionary)

    for value in wordlist.items():
        if value[1] > 4 * general_dictionary.get(value[0], 0) / ARTICLE_BLACKLIST:
            dictionary[value[0]] = value[1]
    return dictionary



def score_attribution(article_dict: dict, gold_std: dict) -> float:
    """
    Count the number of word present in the gold standard and compute the related score
    :param article_dict: dictionary of words present in an article
    :param gold_std: dictionary of relevant words
    :return: Score
    """
    count = 0
    for k, v in article_dict.items():
        if k in gold_std:
            count = count + v * gold_std[k]
    return count


def scaler(newMin: float, newMax: float, values: list, x: float) -> float:
    """
    Scale values in the new range
    :param newMin: minimum value of the new range
    :param newMax: maximum value of the new range
    :param values: list of all values
    :param x: initial value
    :return: scaled value
    """
    min_ = min(values)
    max_ = max(values)
    result = 1
    if min_ != max_:
        result = ((x - min_) * (newMax - newMin) / (max_ - min_) + newMin)
    return result


def compute_score(wordlist_list: list, dict_weights: dict) -> list:
    """
    Compute the score for each article
    :param wordlist_list: list of dictionary of each article
    :param dict_weights: gold standard dictionary with related weights
    :return: list of normalized score
    """
    score = list()
    for d in wordlist_list:
        score.append(score_attribution(d, dict_weights))

    return score


def matching_articles(score: list, threshold: float) -> list:
    """
    Classify articles based on score and threshold
    :param score: list of score one per article
    :param threshold: number beyond which articles are classified as matching
    :return: classification list
    """
    matching = list((np.array(score) >= threshold) * 1)
    return matching


def order_and_select_words(dictionary, percentile):
    """
    Order the words in a python dictionary based on the value of the key-value pairs
    :param dictionary: dictionary of "string" : value
    :type dictionary: dict
    :param percentile: the first x-th percentile of words will be selected. Percentile in range [0 1]
    :type percentile: float
    :return: ordered dictionary with only the first percentile% of elements
    :rtype: dict
    """
    assert percentile <= 1.00
    assert percentile > 0.00

    # ordering dictionary by value
    dictionary = OrderedDict({k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)})

    # selecting the first (percentile)% elements -> if no elements is included the percentile increases of 0.01
    elements = 0
    while elements < 1 and percentile <= 1.00:
        elements = int(percentile * len(dictionary))
        percentile += 0.01

    while len(dictionary) > elements:
        dictionary.popitem(last=True)

    return dictionary


def classification_alg(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform articles classification based on a modified version of https://doi.org/10.1093/ehjci/ehaa946.3555
    :param df: original dataframe
    :return: pandas dataframe with matching column
    """

    df = df[df['Abstract'].notna()]
    df = df.reset_index()
    df = df.fillna("None")
    wordlist_list_abs = [dict() for x in range(df.shape[0])]
    wordlist_list_ti = [dict() for x in range(df.shape[0])]
    wordlist_list_kw = [dict() for x in range(df.shape[0])]

    # Step1 - count occurrences of all words (minus black list)

    general_dictionary = pd.read_excel('blacklist_dict.xlsx', engine='openpyxl')
    general_dictionary = dict(general_dictionary.values)

    # Step1 - count occurrences of all words
    wordlist_abstract = dict()
    wordlist_title = dict()
    wordlist_keywords = dict()

    for i in range(df.shape[0]):
        wordlist_abstract = count_words(df.iloc[i]['Abstract'], wordlist_abstract)
        wordlist_title = count_words(df.iloc[i]['Article Title'], wordlist_title)
        wordlist_keywords = count_words(df.iloc[i]['Keywords'], wordlist_keywords)
        wordlist_list_abs[i] = count_words(df.iloc[i]['Abstract'])
        wordlist_list_ti[i] = count_words(df.iloc[i]['Article Title'])
        wordlist_list_kw[i] = count_words(df.iloc[i]['Keywords'])

    # Step2 - create a dictionary based on generic dictionary
    dictionary_abstract = filter_dict(wordlist_abstract, df.shape[0], general_dictionary, "abstract")
    dictionary_title = filter_dict(wordlist_title, df.shape[0], general_dictionary, "title")
    dictionary_keywords = filter_dict(wordlist_keywords, df.shape[0], general_dictionary, "keywords")

    # Step2.1 - extract first x-th percentile of words
    percentile_abstract = 0.005
    percentile_title = 0.01
    percentile_keywords = 0.01

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

    # Step4 - compute the score and scale it in [0-1]

    score_abs = compute_score(wordlist_list_abs, dict_weights_abstract)
    score_ti = compute_score(wordlist_list_ti, dict_weights_title)
    score_kw = compute_score(wordlist_list_kw, dict_weights_keywords)

    score_final = list(map(lambda abstract, ti, kw: abstract + 5 * ti + 5 * kw, score_abs, score_ti, score_kw))
    score_final = list(map(lambda s: scaler(0, 1, score_final, s), score_final))

    # Step5 - scaled score > 0.09 --> classify as 1
    threshold = 0.17735435435435434
    matching = matching_articles(score_final, threshold)
    if len(matching) != 0:
        df.loc[:, 'Score'] = score_final
        df.loc[:, 'Match'] = matching

        print(df[['Article Title', 'Match']])
    return df
