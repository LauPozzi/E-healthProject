import requests
from medline_utils import text_edit
from itertools import permutations
import re
#from sympy.logic.boolalg import to_cnf

# def create_query(string):
#     final_query = ''
#     logics = ['OR', 'AND']
#
#     lis = list(string.split())
#     n_operators=len(lis)-1
#     # Stores all possible permutations
#     # of words in this list
#     permute = permutations(lis)
#
#     # Iterate over all permutations
#     z=0
#     for i in permute:
#         permutelist = tuple(i)
#         for j in range(2**n_operators):
#             n_bin = f'{j:0{n_operators}b}'
#             logic_position = list(n_bin)
#             idx = 1
#             sub_query = list(permutelist)
#             for k in range(len(logic_position)):
#                 sub_query.insert(idx, logics[int(logic_position[k])])
#                 idx = idx + 2
#             sub_query_str = ' '.join(sub_query)
#             final_query = final_query + ' OR (' + sub_query_str + ')'
#             if z==0:
#                 z=1
#                 final_query = '(' + sub_query_str + ')'
#     return final_query

def search(query_list: list, level_string):
    query = str()
    i=0
    for box in query_list:
        box = box.replace(",", " OR")
        query = query + ' AND (' + box + ')'
        #TODO: try to use OR too between boxes and make different permutations between boxes

        if i == 0:
            i = 1
            query = '(' + box + ')'


    final_query = query + ' AND ' + level_string
    newString = final_query.replace(" ", "+")

    # First search given the initial string
    link1 = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={newString}&retmode=json&RetMax=100&usehistory=y"

    f1 = requests.get(link1)
    dictionary = f1.json()
    dictionary = dictionary['esearchresult']

    return dictionary['querykey'], dictionary['webenv'], dictionary['count']


def fetch(key, webenv, i, RETMAX):
    # FETCH API
    link2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key={}&WebEnv={}&retstart={}&retmax={}&rettype=medline".format(
        key, webenv, i * RETMAX, RETMAX)

    print(link2)

    webpage = requests.get(link2)

    articles = text_edit(webpage)

    return articles


if __name__ == "__main__":
    query = ["kids, children", "adhd, attention"]
    print(query_search(query,'treatment'))
