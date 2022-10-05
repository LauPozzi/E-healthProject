import collections.abc
import datetime
import math
import time

import pandas as pd
import requests
import xmltodict
import collections

#TODO: magage, authors, keywords and abstracts extraction in case there are none
#La list con le lambda restituisce delle liste di dimensione minore del numero totale di articoli in caso manchino questi campi

def extract_titles(article_list):
    list_titles=list(map(lambda d: next(item for item in list(map(lambda x: x[1] if(x[0] == 'TI') else None, d))if item is not None), article_list))
    return list_titles


def extract_dates(article_list):
    return list(map(lambda d: next(item for item in list(map(lambda x: x[1] if (x[0] == 'DP') else None, d)) if item is not None), article_list))


def extract_authors(article_list):
    return list(map(lambda d: next(item for item in list(map(lambda x: x[1] if (x[0] == 'AU') else None, d)) if item is not None), article_list))


def extract_journal_names(article_list):
    return list(map(lambda d: next(item for item in list(map(lambda x: x[1] if (x[0] == 'JT') else None, d)) if item is not None), article_list))


def extract_studytypes(article_list):
    return list(map(lambda d: next(
        item for item in list(map(lambda x: x[1] if (x[0] == 'PT') else None, d)) if item is not None), article_list))


def extract_keywords(article_list):
    return list(map(lambda d: next(
        item for item in list(map(lambda x: x[1] if (x[0] == 'OT') else None, d)) if item is not None), article_list))



def extract_dois(article_list):
    return list(map(lambda d: next(
        item for item in list(map(lambda x: x[1] if (x[0] == 'AID') else None, d)) if item is not None), article_list))


def extract_abstracts(article_list):
    return list(map(lambda d: next(item for item in list(map(lambda x: x[1] if (x[0] == 'AB') else None, d)) if item is not None), article_list))


def list_2_dataframe(article_list: list):
    """

    :param article_set:
    :type article_set:
    :return:
    :rtype:
    """

    data_dict = {'Article Title': extract_titles(article_list),
                 'Date': extract_dates(article_list),
                 #'Authors': extract_authors(article_list),
                 'Journal': extract_journal_names(article_list),
                 'Study Type': extract_studytypes(article_list),
                 #'Keywords': extract_keywords(article_list),
                 'DOI': extract_dois(article_list),
                 #'Abstract': extract_abstracts(article_list)
                 }
    return pd.DataFrame(data_dict)


