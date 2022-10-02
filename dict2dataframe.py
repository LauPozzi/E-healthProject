import collections.abc
import datetime
import time
import functools
import operator

import pandas as pd
import requests
import xmltodict


# def foo2(x):
#     print(list(map(operator.itemgetter('name'), x)))
#
#
# def foo(x):
#     return x.get('name') == 'pluto'
#
#
# a = [{'name': 'pippo', 'age': '5'}, {'name': 'pluto', 'age': '7'}]
# b = filter(foo, a)
# list(b)
# foo2(a)


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

def dict_2_dataframe(article_set: dict):
    dataframe = pd.DataFrame
    column_names = ['Article Title', 'Date', 'Authors', 'Journal', 'Study Type', 'Keywords', 'DOI', 'Abstract']
    data = []

    article_list = article_set['PubmedArticle']

    # TODO: choose best method among this and the for loop in dict_2_dataframe2()

    # titles = list(map(operator.itemgetter('ArticleTitle'),
    #                   map(operator.itemgetter('Article'),
    #                       map(operator.itemgetter('MedlineCitation'), article_list))))

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

    # TODO: authors is a list of dictionaries still -> I want a list of lists
    authors = list(
        map(lambda d: d.get('MedlineCitation').get('Article').get('AuthorList', {'Author': []}).get('Author'),
            article_list))

    authors = extract_authors(authors)

    journals = list(map(lambda d: d.get('MedlineCitation').get('Article').get('Journal').get('Title'), article_list))

    # TODO: study type not in xml... Get from abstract?

    # TODO: keywords is a list of dictionaries still -> I want a list of lists
    keywords = list(map(lambda d: d.get('MedlineCitation').get('KeywordList'), article_list))

    # TODO: there are dois that are values and dois that are lists
    DOI_std = "https://doi.org/"
    dois = list(map(lambda d: d.get('MedlineCitation').get('Article').get('ELocationID'), article_list)) #.get('#text')
    # dois = [DOI_std + doi for doi in dois]

    # TODO: there are abstracts that are values some are lists and some are dictionaries
    abstracts = list(map(lambda d: d.get('MedlineCitation').get('Article').get('Abstract').get('AbstractText'), article_list))

    data.append(titles)
    data.append(dates)
    data.append(authors)
    data.append(journals)
    data.append(keywords)
    # data.append(dois)
    data.append(abstracts)

    return data


# def dict_2_dataframe2(article_set: dict):
#     dataframe = pd.DataFrame()
#     column_names = ['Article Title', 'Date', 'Authors', 'Journal', 'Study Type', 'Keywords', 'DOI', 'Abstract']
#     data = []
#     for column in column_names:
#         data.append([])
#
#     for paper in article_set['PubmedArticle']:
#         data[column_names.index('Article Title')].append(paper['MedlineCitation']['Article']['ArticleTitle'])
#         year = paper['MedlineCitation']['Article']['ArticleDate']['Year']
#         month = paper['MedlineCitation']['Article']['ArticleDate']['Month']
#         day = paper['MedlineCitation']['Article']['ArticleDate']['Day']
#         date = datetime.datetime(int(year), int(month), int(day))
#         data[column_names.index('Date')].append(date)
#
#     dataframe.insert(loc=column_names.index('Article Title'), column='Article Title',
#                      value=data[column_names.index('Article Title')])
#     dataframe.insert(loc=column_names.index('Date'), column='Date',
#                      value=data[column_names.index('Date')])
#
#     print(dataframe)


if __name__ == '__main__':
    link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=serious+game+ADHD&retmode=json" \
            "&RetMax=100&WebEnv=%3Cwebenv%20string%3E&usehistory=y "
    f1 = requests.get(link1)
    dict = f1.json()
    print(type(dict))
    dict2 = dict['esearchresult']
    # If we want to use the fetch API we need webenv and querykey
    print(dict2['webenv'])
    print(dict2['querykey'])

    # FETCH API
    link2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key={}&WebEnv={}&retmode=xml".format(
        dict2['querykey'], dict2['webenv'])
    print(link2)

    #
    f2 = requests.get(link2)
    f2_xml = f2.text
    dict3 = xmltodict.parse(f2_xml)
    ArticleSet = dict3['PubmedArticleSet']

    # dict_2_dataframe2(ArticleSet)

    data = dict_2_dataframe(ArticleSet)
    for i in range(len(data[0])):
        print(data[0][i], '\n', data[2][i], end='\n\n')
    # print(data[0])
    # print(data[1])
    # print(data[2])
    # print(data[3])
    # print(data[5])

    # Extract title of first article
    # print(ArticleSet['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle'])
