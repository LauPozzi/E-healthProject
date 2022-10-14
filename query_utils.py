import requests
from medline_utils import text_edit

from itertools import permutations


def create_query(string):
    final_query = ''
    logics = ['or', 'and']

    lis = list(string.split())
    n_operators=len(lis)-1
    # Stores all possible permutations
    # of words in this list
    permute = permutations(lis)

    # Iterate over all permutations
    z=0
    for i in permute:
        permutelist = tuple(i)
        for j in range(2**n_operators):
            n_bin = f'{j:0{n_operators}b}'
            logic_position = list(n_bin)
            idx = 1
            sub_query = list(permutelist)
            for k in range(len(logic_position)):
                sub_query.insert(idx, logics[int(logic_position[k])])
                idx = idx + 2
            sub_query_str = ' '.join(sub_query)
            final_query = final_query + ') or (' + sub_query_str
            if z==0:
                z=1
                final_query = '(' + sub_query_str
    return final_query

def query_search(string):
    query = string
#    query = create_query(string)
    newString = query.replace(" ", "+")
    final_query = create_query(newString)
    # First search given the initial string
    link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}&retmode=json&RetMax=100&usehistory=y".format(
        newString)
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
    create_query("A B C")