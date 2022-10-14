import pandas as pd
from main import main
import re


def count_words(text: str, blacklist_words: list, d: dict) -> dict:
    # code taken from: https://www.geeksforgeeks.org/python-count-occurrences-of-each-word-in-given-text-file/
    # Remove the leading spaces and newline character
    line = text.strip()
    # Convert the characters in line to lowercase to avoid case mismatch
    line = line.lower()
    # Remove the punctuation marks from the line
    line = re.sub(r'[.,"\'-?:!;]', ' ', line)
    line = re.sub(r'[\([{})\]]', ' ', line)
    # Split the line into words
    words = line.split()

    # Iterate over each word in line
    for word in words:
        if word in blacklist_words:
            continue
        else:
            # Check if the word is already in dictionary
            if word in d:
                # Increment count of word by 1
                d[word] = d[word] + 1
            else:
                # Add the word to dictionary with count 1
                d[word] = 1
    return d


def count_words_perarticle(text: str, blacklist_words: list) -> dict:
    # code taken from: https://www.geeksforgeeks.org/python-count-occurrences-of-each-word-in-given-text-file/
    d = dict()
    # Remove the leading spaces and newline character
    line = text.strip()
    # Convert the characters in line to lowercase to avoid case mismatch
    line = line.lower()
    # TODO: deal with plurals

    # Remove the punctuation marks from the line
    line = re.sub(r'[.,"\'-?:!;]', ' ', line)
    line = re.sub(r'[\([{})\]]', ' ', line)
    # Split the line into words
    words = line.split()

    # Iterate over each word in line
    for word in words:
        # Check if the word is already in dictionary
        if word in d:
            # Increment count of word by 1
            d[word] = d[word] + 1
        else:
            if word in blacklist_words:
                pass
            else:
                # Add the word to dictionary with count 1
                d[word] = 1
    return d


def create_dict(wordlist, threshold, size_df):
    dictionary = wordlist.copy()
    for value in wordlist.items():
        dictionary[value[0]] = value[1] / size_df
        if value[1] / size_df < threshold:
            del dictionary[value[0]]
        else:
            continue
    print(dictionary)
    return dictionary


def score_attribution(article_dict: dict, gold_std: dict) -> float:
    count = 0
    for k, v in article_dict.items():
        if k in gold_std:
            count = count + v * gold_std[k]
    return count


def scaler(NewMin: float, NewMax: float, values: list, x: float):
    min_ = min(values)
    max_ = max(values)
    return ((x - min_) * (NewMax - NewMin) / (max_ - min_) + NewMin)


def compute_score(wordlist_list, dict_weights):
    score = list()
    score_norm = list()
    for d in wordlist_list:
        score.append(score_attribution(d, dict_weights))

    for x in score:
        score_norm.append(scaler(0, 1, score, x))
    return score_norm


def matching_articles(score, threshold):
    matching = list()
    for x in score:
        if x >= threshold:
            matching.append(1)
        else:
            matching.append(0)
    return matching


def classification_alg():
    # Getting the dataframe of articles
    df = main()
    df.fillna("None", inplace=True)
    wordlist_list_abs = [dict() for x in range(df.shape[0])]
    wordlist_list_ti = [dict() for x in range(df.shape[0])]
    wordlist_list_kw = [dict() for x in range(df.shape[0])]

    # Step1 - count occurrences of all words (minus black list)
    blacklist_dict = pd.read_excel('blacklist_dict.xlsx', engine='openpyxl')
    # blacklist_dict.head(3)
    blacklist = list(blacklist_dict['WORD'])

    wordlist_abstract = dict()
    wordlist_title = dict()
    wordlist_keywords = dict()

    for i in range(df.shape[0]):
        wordlist_abstract = count_words(df.iloc[i]['Abstract'], blacklist, wordlist_abstract)
        wordlist_title = count_words(df.iloc[i]['Article Title'], blacklist, wordlist_title)
        wordlist_keywords = count_words(df.iloc[i]['Keywords'], blacklist, wordlist_keywords)
        wordlist_list_abs[i] = count_words_perarticle(df.iloc[i]['Abstract'], blacklist)
        wordlist_list_ti[i] = count_words_perarticle(df.iloc[i]['Article Title'], blacklist)
        wordlist_list_kw[i] = count_words_perarticle(df.iloc[i]['Keywords'], blacklist)

    # Step2 - create a dictionary based on a threshold
    threshold = 0.1
    dictionary_abstract = create_dict(wordlist_abstract, threshold, df.shape[0])
    dictionary_title = create_dict(wordlist_title, threshold, df.shape[0])
    dictionary_keywords = create_dict(wordlist_keywords, threshold, df.shape[0])

    # TODO: considerare anche le occurrences delle parole nel "generic dictionary"

    # Step3 - scale the occurrences of the words in the dictionary in [0.06, 1]

    values_abs = dictionary_abstract.values()
    values_ti = dictionary_title.values()
    values_kw = dictionary_keywords.values()
    dict_weights_abstract = {key: (scaler(0.06, 1, values_abs, v)) for (key, v) in dictionary_abstract.items()}
    dict_weights_title = {key: (scaler(0.06, 1, values_ti, v)) for (key, v) in dictionary_title.items()}
    dict_weights_keywords = {key: (scaler(0.06, 1, values_kw, v)) for (key, v) in dictionary_keywords.items()}
    # TODO: gestire errore dove min=max

    # Step4 - on each abstract compute the score and scale it in [0-1]

    score_abs = compute_score(wordlist_list_abs, dict_weights_abstract)
    score_ti = compute_score(wordlist_list_ti, dict_weights_title)
    score_kw = compute_score(wordlist_list_kw, dict_weights_keywords)

    score_final = list(map(lambda abstract, ti, kw: abstract + 5 * ti + 5 * kw, score_abs, score_ti, score_kw))

    # Step5 - scaled score > 0.09 --> classify as 1
    threshold = 0.09
    matching = matching_articles(score_final, threshold)

    df['Match'] = matching

    print(df[['Article Title', 'Match']])

    df.to_csv('export_dataframe_match.csv', index=False)


if __name__ == '__main__':
    classification_alg()
