import requests
from medline_utils import text_edit
from itertools import permutations
import re
from sympy.logic.boolalg import to_cnf


def compar_perm(str1: str, str2: str):
    #la funzione compara due espressioni e dice se sono equivalenti a livello logico booleano
    #TODO: usarla per controllare tutte le combinazioni create da create_query e per eliminare quelle ridondanti 
    str1 = str1.replace("AND", "&").replace("OR", "|")
    str2 = str2.replace("AND", "&").replace("OR", "|")

    return str(to_cnf(str1)) == str(to_cnf(str2))



def create_query(string):
    final_query = ''
    logics = ['OR', 'AND']

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
            final_query = final_query + ' or (' + sub_query_str + ')'
            if z==0:
                z=1
                final_query = '(' + sub_query_str + ')'
    return final_query

def query_search(main_string, level_string):
    query = main_string + ' ' + level_string
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
    print(create_query("A B C"))
    print(compar_perm('A AND B OR C', 'B AND A OR C'))