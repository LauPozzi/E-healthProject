from easygui import enterbox, msgbox
from query_utils import query_search, query_fetch
from medline_utils import concat_articles
from dict2dataframe import *


def main():
    # user enters string
    string = enterbox("Please, enter a string for the research.", "Database Preparation")
    if not string:
        msgbox('No string inserted', 'Message', 'OK')
        exit()
    # returns dict with all articles information

    key, webenv, count = query_search(string)

    dic = {'Article Title': [],
           'Date': [],
           'Authors': [],
           'Journal': [],
           'Study Type': [],
           'Keywords': [],
           'DOI': [],
           'Abstract': []
           }

    RETMAX = 10000
    chunks = math.ceil(int(count) / RETMAX)

    for i in range(chunks):

        articles = query_fetch(key, webenv, i, RETMAX)

        start = time.time()

        for article in articles:
            dic = concat_articles(article, dic)

        print(time.time()-start)

    df = pd.DataFrame(dic)

    df.to_csv('export_dataframe.csv', index=False)


if __name__ == '__main__':
    main()
