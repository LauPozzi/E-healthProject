import collections.abc
import datetime
import math
import time

import pandas as pd
import requests
import xmltodict


# TODO: set the default values, if it's not the last get() a dictionary should be provided to avoid errors (as in
#  the years-months-days extractions)

RETMAX = 100

def extract_titles(article_list):
    return list(map(lambda d: d.get('MedlineCitation').get('Article').get('ArticleTitle', "n.a."), article_list))


def extract_dates(article_list):
    years = list(map(int, map(lambda d: d.get('MedlineCitation', None).get('Article', None).get('ArticleDate', {
        'Year': datetime.MINYEAR}).get('Year', datetime.MINYEAR), article_list)))

    months = list(map(int, map(lambda d: d.get('MedlineCitation', None).get('Article', None).get('ArticleDate', {
        'Month': 1}).get('Month', 1), article_list)))

    days = list(map(int, map(lambda d: d.get('MedlineCitation', None).get('Article', None).get('ArticleDate', {
        'Day': 1}).get('Day', 1), article_list)))

    return [datetime.datetime(y, m, d) for y, m, d in zip(years, months, days)]


def extract_authors(article_list):
    authors_out = []
    authors = list(
        map(lambda d: d.get('MedlineCitation').get('Article').get('AuthorList', {'Author': []}).get('Author'),
            article_list))
    for author in authors:
        if isinstance(author, list):
            authors_out.append(list(map(lambda d: d.get('LastName', 'n.a.') + ' ' + d.get('ForeName', 'n.a.'), author)))
        elif isinstance(author, collections.abc.Mapping):
            authors_out.append([author.get('LastName', 'n.a.') + ' ' + author.get('ForeName', 'n.a.')])
        else:
            authors_out.append(['n.a.'])
    return authors_out


def extract_journal_names(article_list):
    return list(map(lambda d: d.get('MedlineCitation').get('Article').get('Journal').get('Title'), article_list))


def extract_studytypes(article_list):
    study_types_out = []
    study_types = list(
        map(lambda d: d.get('MedlineCitation').get('Article').get('PublicationTypeList').get('PublicationType'),
            article_list))
    for type in study_types:
        if isinstance(type, list):
            study_types_out.append(list(map(lambda d: d.get('#text', 'n.a.'), type)))
        elif isinstance(type, collections.abc.Mapping):
            study_types_out.append([type.get('#text', 'n.a.')])
        else:
            study_types_out.append(['n.a.'])

    return study_types_out


def extract_keywords(article_list):
    keywords_dicts = list(
        map(lambda d: d.get('MedlineCitation').get('KeywordList', {'Keyword': [{'#text': 'n.a.'}]}).get('Keyword'),
            article_list))
    keywords = []

    for keyword in keywords_dicts:
        try:
            keywords.append(list(map(lambda k: k.get('#text'), keyword)))
        except AttributeError:
            keywords.append([keyword.get('#text')])

    return keywords


def doi_type_utility(k):
    try:
        return k['@IdType'] == 'doi'
    except TypeError:
        return k[0]


def doi_text_utility(d):
    try:
        return d[0]
    except IndexError:
        return {'#text': ''.join(d)}


def doi_concat_utility(d):
    DOI_std = "https://doi.org/"
    try:
        return DOI_std + d.get('#text')
    except AttributeError:
        return DOI_std + d


def extract_dois(article_list):
    dois = list(map(lambda d: list(
        filter(lambda k: doi_type_utility(k), d.get('PubmedData').get('ArticleIdList').get('ArticleId'))),
                    article_list))
    dois = list(map(lambda d: doi_text_utility(d), dois))  # To obtain the list of dictionaries
    dois = list(map(lambda d: doi_concat_utility(d), dois))
    return dois


def abstract_concat_utility(d):
    try:
        return d.get('#text')
    except AttributeError:
        d = 'n.a.' if d is None else d
        return d


def extract_abstracts(article_list):
    abstracts_out = []
    abstracts = list(
        map(lambda d: d.get('MedlineCitation').get('Article').get('Abstract', {'AbstractText': 'n.a.'}).get(
            'AbstractText'), article_list))
    for abstract in abstracts:
        if isinstance(abstract, str):
            abstracts_out.append(abstract)
        elif isinstance(abstract, collections.abc.Mapping):
            abstracts_out.append(abstract.get('#text'))
        elif isinstance(abstract, list):
            try:
                abstracts_out.append(' '.join(list(map(lambda d: abstract_concat_utility(d), abstract))))
            except TypeError:
                abstracts_out.append('n.a.')
        else:
            abstracts_out.append('n.a.')

    return abstracts_out


def dict_2_dataframe(article_set: dict):
    """

    :param article_set:
    :type article_set:
    :return:
    :rtype:
    """
    article_list = article_set['PubmedArticle']

    data_dict = {'Article Title': extract_titles(article_list),
                 'Date': extract_dates(article_list),
                 'Authors': extract_authors(article_list),
                 'Journal': extract_journal_names(article_list),
                 'Study Type': extract_studytypes(article_list),
                 'Keywords': extract_keywords(article_list),
                 'DOI': extract_dois(article_list),
                 'Abstract': extract_abstracts(article_list)
                 }
    return pd.DataFrame(data_dict)


if __name__ == '__main__':
    time1 = time.time()
    search_entry = 'serious game'
    search_entry = search_entry.split(' ')
    search_entry = '+'.join(search_entry)
    print(search_entry)

    link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}&retmode=json" \
            "&RetMax=1&WebEnv=%3Cwebenv%20string%3E&usehistory=y ".format(search_entry)

    f1 = requests.get(link1)

    time2 = time.time()

    print("Search in {:.4f} seconds".format(time2-time1))

    dict1 = f1.json()
    dict2 = dict1['esearchresult']

    total_results = int(dict2['count'])
    chunks = math.ceil(total_results/RETMAX)

    database = pd.DataFrame()

    for i in range(chunks):
        # FETCH API
        link2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key={}&WebEnv={}&retsart={}&retmax={}&retmode=xml".format(
            dict2['querykey'], dict2['webenv'], i*RETMAX, RETMAX)


        # TODO: manage this exception somewhere
        assert int(dict2['count']) > 0

        time3 = time.time()

        f2 = requests.get(link2)

        time4 = time.time()

        #print("Fetch in {:.4f} seconds".format(time4 - time3))

        f2_xml = f2.text
        dict3 = xmltodict.parse(f2_xml)
        ArticleSet = dict3['PubmedArticleSet']

        time5 = time.time()

        time_conv = time.time()
        database = pd.concat([database, dict_2_dataframe(ArticleSet)], ignore_index=True)

    end_conv = time.time()

    print("\nProcessed {} results in {:.4f} seconds.".format(database.shape[0], end_conv-time1))


