import requests
from medline_utils import text_edit

def query_search(query):
    newString = query.replace(" ", "+")
    # First search given the initial string
    link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}&retmode=json&RetMax=100&usehistory=y".format(
        newString)
    f1 = requests.get(link1)
    dictionary = f1.json()
    dictionary = dictionary['esearchresult']

    return dictionary['querykey'], dictionary['webenv'], dictionary['count']


def query_fetch(key, webenv, i, RETMAX):
    # FETCH API
    link2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key={}&WebEnv={}&retstart={}&retmax={}&rettype=medline".format(
        key, webenv, i * RETMAX, RETMAX)

    print(link2)

    webpage = requests.get(link2)

    articles = text_edit(webpage)

    return articles