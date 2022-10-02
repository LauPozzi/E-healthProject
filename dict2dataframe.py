import collections.abc
import datetime
import sys
import time
import functools
import operator
import traceback

import pandas as pd
import requests
import xmltodict


def extract_authors(authors):
    authors_out = []
    for author in authors:
        authors_out.append([])
        if isinstance(author, list):
            authors_out[-1] = list(map(lambda d: d.get('LastName', 'n.a.') + ' ' + d.get('ForeName', 'n.a.'), author))
        elif isinstance(author, collections.abc.Mapping):
            authors_out[-1] = [author.get('LastName', 'n.a.') + ' ' + author.get('ForeName', 'n.a.')]
        else:
            authors_out[-1] = ['n.a.']

    return authors_out


def extract_abstracts(abstracts):
    abstracts_out = []
    for abstract in abstracts:
        if isinstance(abstract, str):
            abstracts_out.append(abstract)
        elif isinstance(abstract, list):
            abstracts_out.append(' '.join(list(map(lambda d: d.get('#text'), abstract))))
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
    dataframe = pd.DataFrame()
    column_names = ['Article Title', 'Date', 'Authors', 'Journal', 'Keywords', 'DOI', 'Abstract']
    data = []

    article_list = article_set['PubmedArticle']

    # TODO: set the default values, if it's not the last get() a dictionary should be provided to avoid errors (as in
    #  the years-months-days extractions)

    titles = list(map(lambda d: d.get('MedlineCitation').get('Article').get('ArticleTitle', "n.a."), article_list))

    years = list(map(int, map(lambda d: d.get('MedlineCitation', None).get('Article', None).get('ArticleDate', {
        'Year': datetime.MINYEAR}).get('Year', datetime.MINYEAR), article_list)))

    months = list(map(int, map(lambda d: d.get('MedlineCitation', None).get('Article', None).get('ArticleDate', {
        'Month': 1}).get('Month', 1), article_list)))

    days = list(map(int, map(lambda d: d.get('MedlineCitation', None).get('Article', None).get('ArticleDate', {
        'Day': 1}).get('Day', 1), article_list)))

    dates = [datetime.datetime(y, m, d) for y, m, d in zip(years, months, days)]

    authors = list(
        map(lambda d: d.get('MedlineCitation').get('Article').get('AuthorList', {'Author': []}).get('Author'),
            article_list))
    authors = extract_authors(authors)

    journals = list(map(lambda d: d.get('MedlineCitation').get('Article').get('Journal').get('Title'), article_list))

    keywords = list(
        map(lambda d: d.get('MedlineCitation').get('KeywordList', {'Keyword': [{'#text': 'n.a.'}]}).get('Keyword'),
            article_list))
    for i, keyword in enumerate(keywords):
        keywords[i] = list(map(lambda k: k.get('#text'), keyword))

    DOI_std = "https://doi.org/"
    dois = list(map(lambda d: list(
        filter(lambda k: k['@IdType'] == 'doi', d.get('PubmedData').get('ArticleIdList').get('ArticleId'))),
                    article_list))
    dois = list(map(lambda d: d[0], dois))  # To obtain the list of dictionaries
    dois = list(map(lambda d: DOI_std + d.get('#text'), dois))

    abstracts = list(
        map(lambda d: d.get('MedlineCitation').get('Article').get('Abstract').get('AbstractText'), article_list))
    abstracts = extract_abstracts(abstracts)

    data.append(titles)
    data.append(dates)
    data.append(authors)
    data.append(journals)
    data.append(keywords)
    data.append(dois)
    data.append(abstracts)

    try:
        for datum in data:
            assert len(datum) == len(data[0])
    except AssertionError:
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)  # Fixed format
        tb_info = traceback.extract_tb(tb)
        filename, line, func, text = tb_info[-1]

        print(
            'An error occurred on line {} in statement {}.\nThe data extracted are not of the same length'.format(line,
                                                                                                                  text))
        exit(1)

    for name in column_names:
        index = column_names.index(name)
        dataframe.insert(loc=index, column=name, value=data[index])

    return dataframe


if __name__ == '__main__':
    link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=serious+game+ADHD&retmode=json" \
            "&RetMax=100&WebEnv=%3Cwebenv%20string%3E&usehistory=y "
    f1 = requests.get(link1)
    dict1 = f1.json()
    dict2 = dict1['esearchresult']
    # If we want to use the fetch API we need webenv and querykey

    # FETCH API
    link2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key={}&WebEnv={}&retmode=xml".format(
        dict2['querykey'], dict2['webenv'])

    #
    f2 = requests.get(link2)
    f2_xml = f2.text
    dict3 = xmltodict.parse(f2_xml)
    ArticleSet = dict3['PubmedArticleSet']

    # TODO: study type not in xml... Get from abstract?
    database = dict_2_dataframe(ArticleSet)

    print(database['Article Title'])
