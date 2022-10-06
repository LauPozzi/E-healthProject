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
def extract_journal_name(article_dict: dict, key: str, header: str):
    journal = extract_description(article_dict, key, header)
    return journal

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

def dict_to_dataframe(article_dict: dict, data_dict: dict):
    """
    :param article_set:
    :type article_set:
    :return:
    :rtype:
    """
    data_dict['Article Title'].append(extract_title(article_dict,"TI","Title")),
    data_dict['Date'].append(extract_date(article_dict,"DP","Date")),
    data_dict['Authors'].append(extract_authors(article_dict,"AU","Author")),
    data_dict['Journal'].append(extract_journal_name(article_dict,"JT","Journal")),
    data_dict['Study Type'].append(extract_studytype(article_dict,"PT","Type")),
    data_dict['Keywords'].append(extract_keywords(article_dict,"OT","keyword")),
                 # 'DOI': [extract_doi(article_dict,"AID","DOI")],
    data_dict['Abstract'].append(extract_abstract(article_dict,"AB","Abstract"))
    #print(data)

    return data_dict

if __name__ == '__main__':

    search_entry = 'serious game ADHD'
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
    dic = {'Article Title': [],
                 'Date': [],
                 'Authors': [],
                 'Journal': [],
                 'Study Type': [],
                 'Keywords': [],
                 # 'DOI': [],
                 'Abstract': []
                 }
    for article in articles:
        # Trying with just the first article
        article_tuple = article_division(article)
        article_small = header_selection(article_tuple)
        article_dict = tuple_manag(article_small)
        dic = dict_to_dataframe(article_dict, dic)

    df=pd.DataFrame(dic)

    print(df)
