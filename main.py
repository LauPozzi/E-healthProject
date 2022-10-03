from easygui import enterbox
from query_parameters import query_param
import json
from dict2dataframe import *


def main():
    # user enters string
    string = enterbox("Please, enter a string for the research.", "Database Preparation")

    # returns dict with all articles information
    articles_dict = query_param(string)

    # save dict as json to see the structure . Once open data.json ctrl+alt+L too see structure
    # with open('data.json', 'w') as f:
    #    json.dump(articles_dict, f)

    print(articles_dict['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle'])

    # TODO: call to dict2dataframe.dict_2_dataframe()
    db=dict_2_dataframe(articles_dict) #function from dict2dataframe_Laura
    print(db)

    # TODO: create csv
    db.to_csv('export_dataframe.csv', sep='$', index=None)
if __name__ == '__main__':
    main()
