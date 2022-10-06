import requests
import re  # libreria regular expression
import time
import collections

def text_edit(req):
    #
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


if __name__ == '__main__':

    link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key=1&WebEnv=MCID_633ef027b9dd030b563aebc4&rettype=medline"
    webpage = requests.get(link1)

    # search_entry = 'serious game'
    # search_entry = search_entry.split(' ')
    # search_entry = '+'.join(search_entry)
    # print(search_entry)
    #
    # link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}&retmode=json" \
    #         "&RetMax=1&WebEnv=%3Cwebenv%20string%3E&usehistory=y ".format(search_entry)
    #
    # f1 = requests.get(link1)
    # dict1 = f1.json()
    # dict2 = dict1['esearchresult']
    link2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key=1&WebEnv=MCID_633eefab4619a7137e059d23&retmode=xml"

    webpage = requests.get(link2)

    articles = text_edit(webpage)
    # Trying with just the first article
    article_tuple = article_division(articles[0])
    article_small = header_selection(article_tuple)
    article_dict = tuple_manag(article_small)
    print(article_dict)
#
#
#
#
#
