import requests
import xmltodict

def webenv_2_dict(web_env, query_key):
    link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key={}&WebEnv={}&retmode=xml".format(query_key,web_env)
    f1 = requests.get(link)
    f1_xml = f1.text
    dict = xmltodict.parse(f1_xml)
    ArticleSet = dict['PubmedArticleSet']

    return (ArticleSet)

if __name__ == '__main__':
    # SEARCH API
    link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=serious+game+ADHD&retmode=json&RetMax=100&WebEnv=%3Cwebenv%20string%3E&usehistory=y"
    f1 = requests.get(link1)
    dict = f1.json()
    dict2 = dict['esearchresult']
    # If we want to use the fetch API we need webenv and querykey
    webenv=dict2['webenv']
    querykey=dict2['querykey']

    output=webenv_2_dict(webenv,querykey)
    print(type(output))
