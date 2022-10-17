from algorithm_classification import *
from easygui import multenterbox, msgbox
import math
from medline_utils import concat_articles
from query_utils import *

RETMAX = 10000


def main():
    # message to be displayed
    text = 'The string must contain synonyms separated by a comma \n\n' \
           'Use "" to force the search to look for combined terms \n\n' \
           'First search is mandatory '

    # window title
    title = "Research strings"

    # list of multiple inputs
    input_list = ["First search", "Second search", "Third search"]

    # list of default text
    default_list = ['serious game', 'children, kids', 'attention disorder, adhd']

    # creating a multiple enter box
    output = multenterbox(text, title, input_list, default_list)

    # retrieving user's outputs
    string_1 = output[0]
    string_2 = output[1]
    string_3 = output[2]

    # managing empty string case
    if not string_1:
        msgbox('No string inserted', 'Message', 'OK')
        exit()
    if not string_2:
        msgbox('No string inserted', 'Message', 'OK')
        exit()
    if not string_3:
        msgbox('No string inserted', 'Message', 'OK')
        exit()

    query_list = [string_1, string_2, string_3]

    # initializing dictionary with articles specifics
    dic = {'Article Title': [],
           'Date': [],
           'Authors': [],
           'Journal': [],
           'Study Type': [],
           'Keywords': [],
           'DOI': [],
           'Abstract': [],
           'Topic of interest': []
           }

    # initializing bullet points with different topics of interest
    bullet_points = ['treatment', 'cognitive enhancement', 'diagnosis support', 'screening tests']

    # doing a specific fetch for each topic
    for point in bullet_points:

        key, webenv, count = search(query_list, point)

        # defining how many chunks with 10000 articles each
        chunks = math.ceil(int(count) / RETMAX)

        # cycling the fetch on each chunk, done in case there are more than 10000 articles for a single search
        for i in range(chunks):

            # creating a list of strings with articles information
            articles = fetch(key, webenv, i, RETMAX)

            # for each element, extract information from the list and put it in a dictionary
            for article in articles:
                dic = concat_articles(article, dic, point)

    # creating dataframe from dictionary
    df = pd.DataFrame(dic)

    # initializing an empty dataframe
    df_classified = pd.DataFrame()

    # performing classification for each topic of interest separately
    for point in bullet_points:
        df_selected = df.loc[df['Topic of interest'] == point]
        df_classified = pd.concat([df_classified, classification_alg(df_selected.iloc[:, :])], ignore_index=True)

    # saving csv file
    df_classified.to_csv('export_dataframe_match.csv', index=False)


if __name__ == '__main__':
    main()
