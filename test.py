
#JSOOOON
dict={"header":{"type":"esearch","version":"0.3"},"esearchresult":{"count":"23","retmax":"23","retstart":"0","querykey":"1","webenv":"MCID_63331c2760e8eb23450aab80","idlist":["35916694","35573357","35105418","34468332","34383674","33856585","33772095","33716812","33334505","32897233","32424511","32207697","31393252","31336804","31142022","29543891","28611610","28149281","27658428","26883052","26325247","26042366","18583430"],"translationset":[{"from":"ADHD","to":"\"attention deficit disorder with hyperactivity\"[MeSH Terms] OR (\"attention\"[All Fields] AND \"deficit\"[All Fields] AND \"disorder\"[All Fields] AND \"hyperactivity\"[All Fields]) OR \"attention deficit disorder with hyperactivity\"[All Fields] OR \"adhd\"[All Fields]"}],"translationstack":[{"term":"serious[All Fields]","field":"All Fields","count":"327631","explode":"N"},{"term":"game[All Fields]","field":"All Fields","count":"36186","explode":"N"},"AND",{"term":"\"attention deficit disorder with hyperactivity\"[MeSH Terms]","field":"MeSH Terms","count":"33436","explode":"Y"},{"term":"\"attention\"[All Fields]","field":"All Fields","count":"560218","explode":"N"},{"term":"\"deficit\"[All Fields]","field":"All Fields","count":"144319","explode":"N"},"AND",{"term":"\"disorder\"[All Fields]","field":"All Fields","count":"791551","explode":"N"},"AND",{"term":"\"hyperactivity\"[All Fields]","field":"All Fields","count":"63379","explode":"N"},"AND","GROUP","OR",{"term":"\"attention deficit disorder with hyperactivity\"[All Fields]","field":"All Fields","count":"33603","explode":"N"},"OR",{"term":"\"adhd\"[All Fields]","field":"All Fields","count":"30325","explode":"N"},"OR","GROUP","AND","GROUP"],"querytranslation":"serious[All Fields] AND game[All Fields] AND (\"attention deficit disorder with hyperactivity\"[MeSH Terms] OR (\"attention\"[All Fields] AND \"deficit\"[All Fields] AND \"disorder\"[All Fields] AND \"hyperactivity\"[All Fields]) OR \"attention deficit disorder with hyperactivity\"[All Fields] OR \"adhd\"[All Fields])"}}

dict2=dict['esearchresult']
#If we want to use the fetch API we need webenv and querykey
print(dict2['webenv'])
print(dict2['querykey'])
#print(dict2['idlist'])


