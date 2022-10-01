from easygui import enterbox
from query_parameters import query_param


def main():

    # user enters string
    string = enterbox("Please, enter a string for the research.", "Database Preparation")

    # returns dict with all articles information
    articles_dict = query_param(string)
    print(articles_dict['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle'])

if __name__ == '__main__':
    main()
