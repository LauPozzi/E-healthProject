import pandas as pd
from main import main
import string

def count_words(text, blacklist_words):
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



def classification_alg():
    #Getting the dataframe of articles
    df = main()
    wordlist_array = [dict() for x in range(df.shape[0])]
    wordlist = {}

    #Step1 - count occurences of all words (minus black list)
    blacklist_dict = pd.read_csv('blacklist_dict.csv')
    blacklist_dict.head(3)
    blacklist = blacklist_dict['WORD'].tolist()

    for i in range(df.shape[0]):
        wordlist_array[i] = count_words(df.iloc[i]['Abstract'], blacklist)

    #TODO: merge the all the dictionaries into a unique dict in oder to count the total occurrences per word

    #TODO: Step2 - create a dictionary based on a treshold
        #TODO: considerare anche le occurrences delle parole nel "generic dictionary"

    #TODO: Step3 - scale the occurencies of the words in the dictionary in [0.06, 1]

    #TODO: Step4 - on each abstract compute the score and scale it in [0-1]

    #TODO: Step5 - scaled score > 0.09 --> classify as 1






if __name__ == '__main__':
    classification_alg()