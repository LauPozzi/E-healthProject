import requests
from medline_utils import text_edit


def search(query_list: list, level_string: str) -> [str]:
    """
    The function creates a query and makes a request to PubMed for searching articles
    :param query_list: list with input words for the query
    :param level_string: string expressing the topic of interest
    :return: query key for fetching, web environment for fetching, and articles count
    """

    search_query = str()
    i = 0
    # inserting logical operators inside and outside each box
    for box in query_list:
        box = box.replace(",", " OR")
        search_query = search_query + ' AND (' + box + ')'

        if i == 0:
            i = 1
            search_query = '(' + box + ')'

    final_query = '(' + '(' + search_query + ')' + ' OR ' + '(' + '(' + query_list[0].replace(",", " OR") + ')' \
                  + ' AND ' + '(' + query_list[1].replace(",", " OR") + ')' + ')' + ' OR ' + '(' + '(' \
                  + query_list[0].replace(",", " OR") + ')' + ' AND ' + '(' + query_list[2].replace(",", " OR") \
                  + ')' + ')' + ') AND ' + level_string

    new_string = final_query.replace(" ", "+")

    # First search given the initial string
    link1 = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={new_string}&" \
            f"retmode=json&RetMax=100&usehistory=y"

    f1 = requests.get(link1)
    dictionary = f1.json()
    dictionary = dictionary['esearchresult']

    return dictionary['querykey'], dictionary['webenv'], dictionary['count']


def fetch(key: str, webenv: str, i: int, retmax: int) -> list:
    """
    The function fetches all articles information in medline format and saves them in a list
    :param key: query key for fetching
    :param webenv: web environment for fetching
    :param i: chunks counter
    :param retmax: constant for the search
    :return: list containing all fetched articles information
    """

    # FETCH API
    link2 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key={}&WebEnv={}&retstart={}&" \
            "retmax={}&rettype=medline".format(key, webenv, i * retmax, retmax)

    webpage = requests.get(link2)

    articles = text_edit(webpage)

    return articles


if __name__ == "__main__":
    query = ["serious game, game", "kids, children", "adhd, attention"]
    print(search(query, 'treatment'))
