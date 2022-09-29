import requests

link1 = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=serious+game+ADHD&retmode=json&RetMax=100&WebEnv=%3Cwebenv%20string%3E&usehistory=y"
f1 = requests.get(link1)
dict = f1.json()
print(type(dict))
dict2=dict['esearchresult']
#If we want to use the fetch API we need webenv and querykey
print(dict2['webenv'])
print(dict2['querykey'])
