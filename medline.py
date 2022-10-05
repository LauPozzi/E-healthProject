import requests
import re  # libreria regular expression
import time

# TODO: 1. creation of function that does all the following: input = text , output = articles_tuple
link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key=1&WebEnv=MCID_633d2ff062bb053a6d0921f9&rettype=medline"
start = time.time()
webpage = requests.get(link1)
request_time = time.time()-start
print(request_time)
text = webpage.text.strip()  # toglie spazio sopra e sotto
articles = text.split("\n\n")  # separo i singoli articoli che sono divisi da una riga vuota

# devo separare ogni riga: con regular expression individuo la stringa che separa
# separo quando ho le seguenti cose:
#    un a capo (\n) seguito da una o più lettere maiuscole([A-Z]+) ( il + è uno o più) ( le parentesi tonde servono a
#       non eliminare il contenuto)
#    zero o più spazi (\s)* (\s spazio, * zero o più)
#    un trattino (-)
#    zero o più spazi (\s)* (\s spazio, * zero o più)
#
reg=re.compile(r"\n([A-Z]+)\s*-\s*")

# PROVE CON I DIVERSI METODI PER CAPIRE QUELLO PIU' VELOCE. FANNO TUTTE LA STESSA COSA.
# bisogna seglierne uno
start = time.time()
articles_divided = list()
for article in articles:
    # concateno una riga vuota davanti all'articolo in modo tale che anche il primo header venga preso
    articles_divided.append(reg.split("\n" + article))
regexpress_time = time.time()-start
print(regexpress_time)

start = time.time()
# concateno una riga vuota davanti all'articolo in modo tale che anche il primo header venga preso
articles_divided = [reg.split("\n" + article) for article in articles]
regexpress_time = time.time()-start
print(regexpress_time)

start = time.time()
# concateno una riga vuota davanti all'articolo in modo tale che anche il primo header venga preso
articles_divided = list(map(lambda article: reg.split("\n" + article), articles))
regexpress_time = time.time()-start
print(regexpress_time)

# articles divided is now a list of list
# proceeding with one of the method: for now, FOR LOOP
articles_tuple = list()
for article in articles_divided:
    article = article[1:]  # considero dal primo elemento in poi perchè primo è vuoto
    # creo lista tuple: header(elementi pari), descrizione(elementi dispari)
    articles_tuple.append(list(zip(article[::2], article[1::2])))

# dictionary creation, for single article, with extraction of the important information
# since there could be more than 1 equal header, dict can't be directly created, since the key of dict must be unique

## TODO: 2. creation of a function that does the following. maybe do it directly with TODO 4.
wanted_field = ['TI', 'AB', 'AID', 'AU', 'JT', 'DP', 'OT', 'PT']
articles_filterd = list()
for article in articles_tuple:
    articles_filterd.append([t for t in article if t[0] in wanted_field]) # t[0] first element of tuple

articles_filterd
## TODO: 3.  function that adjust tuples: a) if more than one equal header : concatenate b) if contain \n, delete "\n   " (like in abstract)

## TODO: 4. functions for each header, like in dict2dataframe: creation of lists containing each a header from all the articles

## TODO: 5. dict creatin as in dict2dataframe




