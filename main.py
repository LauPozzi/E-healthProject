import math
import time
import pandas as pd
from easygui import enterbox, msgbox
from query_utils import *
from medline_utils import concat_articles
from algorithm_classification import *
from create_dictionary import word_counter



def main():
    # user enters string
    string_1 = enterbox("Please, enter a string for the research.", "Database Preparation")
    string_2 = enterbox("Please, enter a string for the research.", "Database Preparation")
    string_3 = enterbox("Please, enter a string for the research.", "Database Preparation")

    if not string_1 :
        msgbox('No string inserted', 'Message', 'OK')
        exit()
    if not string_2 :
        msgbox('No string inserted', 'Message', 'OK')
        exit()
    if not string_3:
        msgbox('No string inserted', 'Message', 'OK')
        exit()

    query_list = [string_1,string_2,string_3]



    dic = {'Article Title': [],
           'Date': [],
           'Authors': [],
           'Journal': [],
           'Study Type': [],
           'Keywords': [],
           'DOI': [],
           'Abstract': [],
           'Topic of interest': []
           }

    bullet_points = ['treatment', 'applications enhancement', 'diagnosis support', 'screening tests']

    for point in bullet_points:

        key, webenv, count = search(query_list, point)

        RETMAX = 10000
        chunks = math.ceil(int(count) / RETMAX)

        for i in range(chunks):

            articles = fetch(key, webenv, i, RETMAX)

            start = time.time()

            for article in articles:
                dic = concat_articles(article, dic, point)

            print(time.time()-start)

    df = pd.DataFrame(dic)

    df.to_csv('export_dataframe.csv', index=False)

    df_classified = pd.DataFrame()

    for point in bullet_points:
        df_selected = df.loc[df['Topic of interest'] == point]
        df_classified = pd.concat([df_classified, classification_alg(df_selected)], ignore_index=True)
        print(df_classified[['Article Title', 'Match']])

   #TODO: fix the 10 score that is suppose to be a 1

    df_classified.to_csv('export_dataframe_match.csv', index=False)
    return df


if __name__ == '__main__':
    main()
