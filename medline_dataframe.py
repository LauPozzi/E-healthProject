import collections.abc
import datetime
import math
import time

import pandas as pd
import requests
import xmltodict
import collections
from medline_article import *

#TODO: magage, authors, keywords and abstracts extraction in case there are none

def extract_description(article_dict: dict, key: str, header: str):
    if article_dict.get(key)== None:
        return f"{header} not found"
    else:
        return article_dict.get(key)

def extract_title(article_dict: dict, key: str, header: str):
    title = extract_description(article_dict, key, header)
    return title

def extract_date(article_dict: dict, key: str, header: str):
    date = extract_description(article_dict, key, header)
    return date
#
def extract_authors(article_dict: dict, key: str, header: str):
    author = extract_description(article_dict, key, header)
    return author
#
# def extract_journal_names(article_dict):
#
#
def extract_studytype(article_dict: dict, key: str, header: str):
    study_type = extract_description(article_dict, key, header)
    return study_type


def extract_keywords(article_dict: dict, key: str, header: str):
    author = extract_description(article_dict, key, header)
    return author


#def extract_doi(article_dict):


def extract_abstract(article_dict: dict, key: str, header: str):
    abstract = extract_description(article_dict, key, header)
    return abstract
def dict_to_dataframe(article_dict: dict):
    """

    :param article_set:
    :type article_set:
    :return:
    :rtype:
    """

    data_dict = {'Article Title': [extract_title(article_dict,"TI","Title")],
                 'Date': [extract_date(article_dict,"DP","Date")],
                 'Authors': [extract_authors(article_dict,"AU","Author")],
                 # 'Journal': [extract_journal_name(article_dict,"JT","Journal")],
                 'Study Type': [extract_studytype(article_dict,"PT","Type")],
                 'Keywords': [extract_keywords(article_dict,"OT","keyword")],
                 # 'DOI': [extract_doi(article_dict,"AID","DOI")],
                 'Abstract': [extract_abstract(article_dict,"AB","Abstract")]

                 }
    print(data_dict)
    return pd.DataFrame(data_dict)

if __name__ == '__main__':

    search_entry = 'serious game'
    search_entry = search_entry.split(' ')
    search_entry = '+'.join(search_entry)
    print(search_entry)

    link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}&retmode=json" \
            "&RetMax=100&WebEnv=%3Cwebenv%20string%3E&usehistory=y ".format(search_entry)
    print(link1)
    f1 = requests.get(link1)
    dict1 = f1.json()
    dict2 = dict1['esearchresult']
    # If we want to use the fetch API we need webenv and querykey

    # FETCH API
    link2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key={}&WebEnv={}&rettype=medline".format(
        dict2['querykey'], dict2['webenv'])



    webpage = requests.get(link2)
    articles = text_edit(webpage)
    # Trying with just the first article
    article_tuple = article_division(articles[0])
    article_small = header_selection(article_tuple)
    article_dict = tuple_manag(article_small)
    df = dict_to_dataframe(article_dict)
    # df=pd.DataFrame(dic)

    print(df)
