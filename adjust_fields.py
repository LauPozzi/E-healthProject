import collections


def adjust_fields(articles):
    # the function substitutes all the random '\n' with a blanck space and collects together the headers with the
    # same name (e.g. 'AU')

    stopword = '\n'
    result = []
    for article in articles:

        for item in article:
            # item=list(item)
            string = str(item[1])
            if stopword in string:
                item[1] = string.replace("\n", " ")

        c = collections.defaultdict(list)
        for a, b in article:
            c[a].append(b)
        article_list_nodouble = list(c.items())
        result.append(article_list_nodouble)

    return result
