import re
import pandas as pd


def word_counter(str):
    counts = dict()
    file = pd.read_excel('blacklist_dict.xlsx', engine='openpyxl')
    black_list = list(file['WORD'])
    str = re.sub(r'[.,"\'-?:!;]', '', str)  # remove punctuation from the string
    words = str.split()

    for word in words:
        if word in black_list:  # check if the word is in the black list
            continue
        else:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
    return counts
