import pandas as pd
from main import main
import re
import string
import sklearn.preprocessing as sk


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
    #TODO: deal with plurals

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

def score_attribution(article_dict : dict, gold_std : dict) -> float:
    count = 0
    for k, v in article_dict.items():
        if k in gold_std:
            count = count+v*gold_std[k]
    return count

def scaler(NewMin:float, NewMax:float, values:list, x:float):
    min_ = min(values)
    max_ = max(values)
    return ((x - min_) * (NewMax - NewMin) / (max_ - min_) + NewMin)


def classification_alg():
    # Getting the dataframe of articles
    df = main()
    df.fillna("None", inplace=True)
    wordlist_list = [dict() for x in range(df.shape[0])]

    # Step1 - count occurences of all words (minus black list)
    blacklist_dict = pd.read_excel('blacklist_dict.xlsx', engine='openpyxl')
    # blacklist_dict.head(3)
    blacklist = list(blacklist_dict['WORD'])


    wordlist = dict()
    # TODO: farlo anche per title e keywords
    for i in range(df.shape[0]):
        wordlist = count_words(df.iloc[i]['Abstract'], blacklist, wordlist)
        wordlist_list[i] = count_words_perarticle(df.iloc[i]['Abstract'], blacklist)

    # Step2 - create a dictionary based on a treshold
    threshold = 0.2
    dictionary = wordlist.copy()
    for value in wordlist.items():
        dictionary[value[0]] = value[1] / df.shape[0]
        if value[1] / df.shape[0] < threshold:
            del dictionary[value[0]]
        else:
            continue
    print(dictionary)

    # TODO: considerare anche le occurrences delle parole nel "generic dictionary"

    #Step3 - scale the occurencies of the words in the dictionary in [0.06, 1]

    values = dictionary.values()
    dict_weights = {key: (scaler(0.06, 1, values, v)) for (key, v) in dictionary.items()}

    # Step4 - on each abstract compute the score and scale it in [0-1]
    score = list()
    score_norm=list()
    for d in wordlist_list:
        score.append(score_attribution(d, dict_weights))

    for x in score:
        score_norm.append(scaler(0, 1, score, x))

    #Step5 - scaled score > 0.09 --> classify as 1
    matching = list()
    treshold = 0.09

    for x in score_norm:
        if x >= treshold:
            matching.append(1)
        else:
            matching.append(0)

    df['Match'] = matching

    print(df[['Article Title', 'Match']])
    
    df.to_csv('export_dataframe_match.csv', index=False)


if __name__ == '__main__':
    classification_alg()
