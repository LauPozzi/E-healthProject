import pandas as pd
from medline_article import *


# TODO: magage, authors, keywords and abstracts extraction in case there are none

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

    print(link2)

    webpage = requests.get(link2)

    articles = text_edit(webpage)

    dic = {'Article Title': [],
           'Date': [],
           'Authors': [],
           'Journal': [],
           'Study Type': [],
           'Keywords': [],
           'DOI': [],
           'Abstract': []
           }

    start = time.time()

    for article in articles:
        dic = concat_articles(article, dic)

    print(time.time()-start)

    df = pd.DataFrame(dic)
    df.to_csv('export_dataframe.csv', index=False)
