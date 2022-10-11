import pandas as pd
from main import main
import string

def count_words(text: str, blacklist_words: list):
    #code taken from: https://www.geeksforgeeks.org/python-count-occurrences-of-each-word-in-given-text-file/

    d = dict()
    # Remove the leading spaces and newline character
    line = text.strip()
    # Convert the characters in line to lowercase to avoid case mismatch
    line = line.lower()
    # Remove the punctuation marks from the line
    line = line.translate(line.maketrans("", "", string.punctuation))
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

def count_relf(dict_list: list, dict_total: dict):
    d = dict()
    #First: I compute the number of abstracts where the words are present
    for i in range(len(dict_list)):
        for word in dict_list[i]:
            if word in dict_total:
                if word in d:
                    d[word] = d[word] + 1
                else:
                    d[word] = 1
            else:
                pass

    #TODO: compute the relf index by: total n° of occurences in dict_total / n° of abstracts in d


    return d





def classification_alg():
    #Getting the dataframe of articles
    df = main()
    wordlist_array = [dict() for x in range(df.shape[0])]

    #Step1 - count occurences of all words (minus black list)
    blacklist_dict = pd.read_csv('blacklist_dict.csv')
    #blacklist_dict.head(3)
    blacklist = blacklist_dict['WORD'].tolist()

    #Array of dictionaries for every article
    for i in range(df.shape[0]):
        wordlist_array[i] = count_words(df.iloc[i]['Abstract'], blacklist)

    #Count of words for the abstracts considered all at once
    df2 = pd.DataFrame({'text': [', '.join(df['Abstract'].str.strip('"').tolist())]})
    wordlist_total = count_words(df2.iloc[0]['text'], blacklist)


    #TODO: Step2 - create a dictionary based on a treshold
    #use function count_relf

        #TODO: considerare anche le occurrences delle parole nel "generic dictionary"

    #TODO: Step3 - scale the occurencies of the words in the dictionary in [0.06, 1]

    #TODO: Step4 - on each abstract compute the score and scale it in [0-1]

    #TODO: Step5 - scaled score > 0.09 --> classify as 1






if __name__ == '__main__':
    classification_alg()