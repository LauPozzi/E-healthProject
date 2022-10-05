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

def tuple_manag(list_tuple):
    # To handle the problem of equals header and \n in the strings
    list_tuple_nospace = [tuple(map(lambda i: str.replace(i, "\n      ", " "), tup)) for tup in list_tuple]

    # I tried 2 methods to handle double header but they do not work

    # list_tuple_nodouble = []
    # i = {}
    # for k,s in list_tuple_nospace:
    #     if k not in i:
    #         list_tuple_nodouble.append((k, s))
    #         i[k] = len(i)
    #     else:
    #         list_tuple_nodouble[i[k]][1].extend(s)

    # c = collections.defaultdict(list)
    # for a,b in list_tuple_nospace:
    #     c[a].extend(b)
    # list_tuple_nodouble = list (c.items())

    return list_tuple_nospace


if __name__ == '__main__':
    link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key=1&WebEnv=MCID_633da339bb0361170641f64b&rettype=medline"
    webpage = requests.get(link1)
    articles = text_edit(webpage)
    # Trying with just the firt article
    article_tuple = article_division(articles[0])
    article_small = header_selection(article_tuple)
    article_final = tuple_manag(article_small)
    print(article_final)
#
#
#
#
#
