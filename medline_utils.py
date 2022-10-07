import re  # libreria regular expression
import collections
import pandas as pd


def text_edit(req):
    text = req.text.strip()  # strip delete space at the beginning and at the ending of the text
    articles = text.split("\n\n")  # single articles separated
    return articles


def article_division(article):
    # devo separare ogni riga: con regular expression individuo la stringa che separa
    # separo quando ho le seguenti cose:
    #    un a capo (\n) seguito da una o più lettere maiuscole([A-Z]+) ( il + è uno o più) ( le parentesi tonde servono a
    #       non eliminare il contenuto)
    #    zero o più spazi (\s)* (\s spazio, * zero o più)
    #    un trattino (-)
    #    zero o più spazi (\s)* (\s spazio, * zero o più)

    reg = re.compile(r"\n([A-Z]+)\s*-\s*")
    article_divided = reg.split("\n" + article) # \n added in order to select also the first header
    article_divided2 = article_divided[1:]  # consider from the second element since the first is empty
    article_tuple = (list(zip(article_divided2[::2], article_divided2[1::2]))) # creation of tuple with
    return article_tuple


def header_selection(list_tuple):
    # To select the tuples with the headers of interest
    wanted_field = ['TI', 'AB', 'AID', 'AU', 'JT', 'DP', 'OT', 'PT']
    article_filterd = [t for t in list_tuple if t[0] in wanted_field]
    return article_filterd


def tuple_manag(list_tuple) -> dict:
    # To handle the problem of equals header and \n in the strings
    list_tuple_nospace = [tuple(map(lambda i: str.replace(i, "\n      ", " "), tup)) for tup in list_tuple]

    # provare con c[a].append e non extend
    c = collections.defaultdict(list)
    for a,b in list_tuple_nospace:
        c[a].append(b)
    for key in c.keys():
        c[key] = ", ".join(c[key])
    dict_nodouble = dict(c.items()) # back to a normal dict since the problem of missing key will be handle in a following funct
    ## TODO: bisogna concatenare i risultati, magari separati da una virgola
    # dict_str = {k: str(v) for k,v in dict_nodouble.items()} # non viene
    return dict_nodouble


def extract_description(article_dict: dict, key: str):
    if article_dict.get(key) == None:
        return pd.NA
    else:
        return article_dict.get(key)


def extract_title(article_dict: dict, key: str):
    title = extract_description(article_dict, key)
    return title


def extract_date(article_dict: dict, key: str):
    date = extract_description(article_dict, key)
    return date


def extract_authors(article_dict: dict, key: str):
    author = extract_description(article_dict, key)
    return author


def extract_journal_name(article_dict: dict, key: str):
    journal = extract_description(article_dict, key)
    return journal


def extract_studytype(article_dict: dict, key: str):
    study_type = extract_description(article_dict, key)
    return study_type


def extract_keywords(article_dict: dict, key: str):
    author = extract_description(article_dict, key)
    return author


def extract_doi(article_dict: dict, key: str):
    DOI_std = "https://doi.org/"
    doi = extract_description(article_dict, key)
    reg = re.compile(r"([A-Za-z0-9\.\/]+)\s*\[doi]")

    try:
        return DOI_std + reg.findall(doi)[0]
    except:
        return doi


def extract_abstract(article_dict: dict, key: str):
    abstract = extract_description(article_dict, key)
    return abstract


def concat_articles(article: list, dic: dict):
    article_tuple = article_division(article)
    article_small = header_selection(article_tuple)
    article_dict = tuple_manag(article_small)
    dic = article_2_dict(article_dict, dic)
    return dic


def article_2_dict(article_dict: dict, data_dict: dict):
    """
    :param article_set:
    :type article_set:
    :return:
    :rtype:
    """
    data_dict['Article Title'].append(extract_title(article_dict, "TI")),
    data_dict['Date'].append(extract_date(article_dict, "DP")),
    data_dict['Authors'].append(extract_authors(article_dict, "AU")),
    data_dict['Journal'].append(extract_journal_name(article_dict, "JT")),
    data_dict['Study Type'].append(extract_studytype(article_dict, "PT")),
    data_dict['Keywords'].append(extract_keywords(article_dict, "OT")),
    data_dict['DOI'].append(extract_doi(article_dict, "AID")),
    data_dict['Abstract'].append(extract_abstract(article_dict, "AB"))

    return data_dict
