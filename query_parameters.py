import requests

def query_param(query):
    newString = query.replace(" ", "+")
    link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}&retmode=json&RetMax=100&WebEnv=%3Cwebenv%20string%3E&usehistory=y".format(newString)
    f1 = requests.get(link1)
    dict = f1.json()
    dict2 = dict['esearchresult']
    return dict2['webenv'], dict2['querykey']

