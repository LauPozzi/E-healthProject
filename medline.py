import requests
import re  # libreria regular expression
import time

link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&query_key=1&WebEnv=MCID_633c6fbd40b53163211757ec&rettype=medline"
start = time.time()
f1 = requests.get(link1)
request_time = time.time()-start
print(request_time)
text = f1.text.strip()  # toglie spazio sopra e sotto
articles = text.split("\n\n")  # separo i singoli articoli che sono divisi da una riga vuota

# devo separare ogni riga: con regular expression individuo la stringa che separa
#    separo quando ho le seguenti cose:
#    un a capo (\n) seguito da una o più lettere maiuscole([A-Z]+) ( il + è uno o più) ( le parentesi tonde servono a
#       non eliminare il contenuto)
#    zero o più spazi (\s)* (\s spazio, * zero o più)
#    un trattino (-)
#    zero o più spazi (\s)* (\s spazio, * zero o più)
#
# concateno una riga vuota davanti all'articolo in modo tale che anche il primo header venga preso
reg=re.compile(r"\n([A-Z]+)\s*-\s*")

# PROVE CON I DIVERSI METODI PER CAPIRE QUELLO PIU' VELOCE. FANNO TUTTE LA STESSA COSA
start = time.time()
articles_divided = list()
for article in articles:
    articles_divided.append(reg.split("\n" + article))
regexpress_time = time.time()-start
print(regexpress_time)

start = time.time()
articles_divided = [reg.split("\n" + article) for article in articles]
regexpress_time = time.time()-start
print(regexpress_time)

start = time.time()
articles_divided = list(map(lambda article: reg.split("\n" + article), articles))
regexpress_time = time.time()-start
print(regexpress_time)

# TODO: DA LAVORARE SU TUTTI GLI ARTICOLI E NON SOLO UNO
# article_divided = article_divided[1:]  # considero dal primo elemento in poi perchè primo è vuoto
# # creo lista tuple: header(elementi pari), descrizione(elementi dispari)
# article = list(zip(article_divided[::2], article_divided[1::2]))

