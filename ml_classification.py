import pandas as pd

from main import main
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.stem import LancasterStemmer


def unsupervised_clustering():
    df = main()

    print(df[['Keywords', 'Abstract']])
    print(df.index)
    df['Keywords'].fillna("None", inplace=True)

    lancaster = LancasterStemmer()

    abstract_copy = df['Abstract'].copy(deep=True)

    for i in range(df.shape[0]):
        df.iloc[i]['Abstract'] = df.iloc[i]['Abstract'].split()

    #df.apply(map(lambda p: lancaster.stem(p), df['Abstract']))

    for i in range(df.shape[0]):
        df.iloc[i]['Abstract'] = list(map(lambda p: lancaster.stem(p), df.iloc[i]['Abstract']))

    for i in range(df.shape[0]):
        df.iloc[i]['Abstract'] = ' '.join(df.iloc[i]['Abstract'])

    tfidf = TfidfVectorizer(stop_words='english', norm=None, max_features=7)
    tfidf_matrix = tfidf.fit_transform(df['Abstract'])
    df_dtm = pd.DataFrame(tfidf_matrix.toarray(),
                          index=None,
                          columns=tfidf.get_feature_names_out())

    print(df_dtm)

    km = KMeans(n_clusters=2)
    km.fit(df_dtm)
    km.predict(df_dtm)
    print(km.labels_)

    df['Cluster'] = km.labels_

    df['Abstract'] = abstract_copy

    print(df[['Article Title', 'Cluster']])

    df.to_csv('export_dataframe_km.csv', index=False)


if __name__ == '__main__':
    unsupervised_clustering()
