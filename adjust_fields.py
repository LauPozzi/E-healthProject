
def adjust_fields(articles):
    stopword = '\n'
    for article in articles:
        for item in article:
            #item=list(item)
            string = str(item[1])
            if stopword in string:
                item[1]=string.replace("\n", " ")

    return articles