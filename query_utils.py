import requests
from medline_utils import text_edit


def search(query_list: list, level_string):
    query = str()
    i = 0
    for box in query_list:
        box = box.replace(",", " OR")
        query = query + ' AND (' + box + ')'
        # TODO: try to use OR too between boxes and make different permutations between boxes

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
    print(search(query, 'treatment'))
