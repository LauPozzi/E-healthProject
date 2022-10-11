import pandas as pd
from main import main
import re
import string


def count_words(text: str, blacklist_words: list, d: dict):
    # code taken from: https://www.geeksforgeeks.org/python-count-occurrences-of-each-word-in-given-text-file/
    # Remove the leading spaces and newline character
    line = text.strip()
    # Convert the characters in line to lowercase to avoid case mismatch
    line = line.lower()
    # Remove the punctuation marks from the line
    line = re.sub(r'[.,"\'-?:!;]', '', line)
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


# def count_relf(dict_list: list, dict_total: dict):
#   d = dict()
# First: I compute the number of abstracts where the words are present
#    for i in range(len(dict_list)):
#       for word in dict_list[i]:
#           if word in dict_total:
#               if word in d:
#                   d[word] = d[word] + 1
#               else:
#                   d[word] = 1
#           else:
#                pass


#    return d


def classification_alg():
    # Getting the dataframe of articles
    df = main()
    # wordlist_array = [dict() for x in range(df.shape[0])]

    # Step1 - count occurences of all words (minus black list)
    # blacklist_dict = pd.read_csv('export_dataframe.csv')
    blacklist_dict = pd.read_excel('blacklist_dict.xlsx', engine='openpyxl')
    # blacklist_dict.head(3)
    blacklist = list(blacklist_dict['WORD'])

    # Array of dictionaries for every article
    #    for i in range(df.shape[0]):
    #        wordlist_array[i] = count_words(df.iloc[i]['Abstract'], blacklist)

    wordlist = dict()
    # TODO: farlo anche per title e keywords
    for article in df['Abstract']:
        wordlist = count_words(article, blacklist, wordlist)

    # Count of words for the abstracts considered all at once
    # df2 = pd.DataFrame({'text': [', '.join(df['Abstract'].str.strip('"').tolist())]})
    # wordlist_total = count_words(df2.iloc[0]['text'], blacklist)

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

    # TODO: Step3 - scale the occurencies of the words in the dictionary in [0.06, 1]

    # TODO: Step4 - on each abstract compute the score and scale it in [0-1]

    # TODO: Step5 - scaled score > 0.09 --> classify as 1


if __name__ == '__main__':
    classification_alg()
