import re  # libreria regular expression
import collections
import pandas as pd


def text_edit(req) -> list:
    """
    The function modify the medline text obtained by the fetch request separating the different articles
    :param req: text obtained by the fetch request
    :return: list of articles
    """
    text = req.text.strip()
    articles = text.split("\n\n")  # single articles separated
    return articles


def article_division(article: str) -> list:
    """
    The function transform the text of an article in a list of tuple: (header, description)
    :param article: string that contains all the information of an article
    :return: list of tuple: (header, description)
    """

    reg = re.compile(r"\n([A-Z]+)\s*-\s*")
    article_divided = reg.split("\n" + article)  # \n added in order to select also the first header
    article_divided2 = article_divided[1:]  # consider from the second element since the first is empty
    article_tuple = (list(zip(article_divided2[::2], article_divided2[1::2])))  # creation of tuple
    return article_tuple


def header_selection(list_tuple: list) -> list:
    """
    Function that selects the tuples with the header of interest
    :param list_tuple: list of tuple of all the headers
    :return: list of tuple with just the headers of interest
    """
    # To select the tuples with the headers of interest
    wanted_field = ['TI', 'AB', 'AID', 'AU', 'JT', 'DP', 'OT', 'PT']
    article_filterd = [t for t in list_tuple if t[0] in wanted_field]
    return article_filterd


def tuple_2_dict(list_tuple: list) -> dict:
    """
    The function delete redundant spaces in the descriptions and combine the tuple with the same header.
    It than transforms the list in a dictionary: key = header , value = description
    :param list_tuple: list of tuple (header,description)
    :return: dictionary key = header , value = description
    """
    # handle redundant spaces
    list_tuple_nospace = [tuple(map(lambda i: str.replace(i, "\n      ", " "), tup)) for tup in list_tuple]

    # handle multiple key
    c = collections.defaultdict(list) # def
    for a, b in list_tuple_nospace:
        c[a].append(b)
    for key in c.keys():
        c[key] = ", ".join(c[key])
    dict_nodouble = dict(
        c.items())
    return dict_nodouble


def extract_key(article_dict: dict, key: str):
    """
    The function, given the key of the dictionary, return the corresponding value (string description)
    :param article_dict: dictionary of a single article
    :param key: key of the dictionary
    :return: value of the corresponding key
    """
    if article_dict.get(key) is None:
        return pd.NA
    else:
        return article_dict.get(key)


def extract_general(article_dict: dict, key: str):
    """
    The function, given the dictionary of an article and a key, extracts the corresponding description
    :param article_dict: dictionary of an article
    :param key: key of interest
    :return: corresponding value
    """
    description = extract_key(article_dict, key)
    return description


def extract_doi(article_dict: dict, key: str):
    """
    The function, given the dictionary of an article and a key, extracts the corresponding DOI combining the description
    in the dict and the domain
    :param article_dict: dictionary of an article
    :param key: doi key
    :return: article doi
    """
    DOI_std = "https://doi.org/"
    doi = extract_key(article_dict, key)
    reg = re.compile(r"([A-Za-z0-9\.\/\-\(\)\_]+)\s*\[doi]")

    try:
        return DOI_std + reg.findall(doi)[0]
    except (TypeError, IndexError) as e:
        return doi

def article_2_dict(article_dict: dict, data_dict: dict, level_string: str) -> dict:
    """
    The function fill the pre-defined dictionary data_dict with the corresponding information of each article
    in article_dict

    :param article_dict:
    :param data_dict:
    :param level_string:
    :return:
    """
    data_dict['Article Title'].append(extract_general(article_dict, "TI")),
    data_dict['Date'].append(extract_general(article_dict, "DP")),
    data_dict['Authors'].append(extract_general(article_dict, "AU")),
    data_dict['Journal'].append(extract_general(article_dict, "JT")),
    data_dict['Study Type'].append(extract_general(article_dict, "PT")),
    data_dict['Keywords'].append(extract_general(article_dict, "OT")),
    data_dict['DOI'].append(extract_doi(article_dict, "AID")),
    data_dict['Abstract'].append(extract_general(article_dict, "AB"))
    data_dict['Topic of interest'].append(level_string)

    return data_dict
def concat_articles(article: list, dic: dict, level_string: str) -> dict:
    """
    The function modifies the dictionary dic in input adding the information form the article in input

    :param article: list of
    :param dic:
    :param level_string:
    :return:
    """
    article_tuple = article_division(article)
    article_small = header_selection(article_tuple)
    article_dict = tuple_2_dict(article_small)
    dic = article_2_dict(article_dict, dic, level_string)
    return dic



