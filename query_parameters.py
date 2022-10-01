import requests
import xmltodict


def query_param(query):
    newString = query.replace(" ", "+")
    # First search given the initial string
    link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}&retmode=json&RetMax=100&WebEnv=%3Cwebenv%20string%3E&usehistory=y".format(
        newString)
    f1 = requests.get(link1)
    dict = f1.json()
    # Secondo search given webevn and key
    link2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key={}&WebEnv={}&retmode=xml".format(
        dict['esearchresult']['querykey'], dict['esearchresult']['webenv'])
    f2 = requests.get(link2)
    f2_xml = f2.text
    dict2 = xmltodict.parse(f2_xml)
    ArticleSet = dict2['PubmedArticleSet']

    return ArticleSet  # dict
