# E-healthProject - part 1 - Group09

## Setup 
In requirements.txt there are all the python modules used, and all the 
environment settings (other than default) necessary to run the code. 
* Open a command prompt and execute:
    ```console
    git clone https://github.com/LauPozzi/E-healthProject.git
    cd E-healthProject
    pip install -r requirements.txt 
    ```

## Script Explanation 
### main.py:
If this script is executed, three boxes will subsequently appear. 
In each box it is required to write a set of synonyms useful for the research (e.g. children, kids).
The fetch is iterated for each bullet point (= different levels specified in slide 9 of Lab 4). 
The classification algorithm is applied to the dataframe considering each bullet point separately. 

### query_utils.py:
Provides all the functions required for the fetching and searching operations. 
It creates the following logical combination between the three search boxes and uses it as the query string:
(synonyms of box1 connected by "OR") AND (synonyms of box2 connected by "OR") AND (synonyms of box3 connected by "OR") AND bullet point

### medline_utils.py:
Contains all the function related to the construction of the database, given the result of the fetch. 
For each article, the functions define and fill-in the fields (title, abstract, doi etc...) that are inserted in the dataframe. 

### algorithm_classification.py: 
Provides all the functions useful for article classification (1-matching and 0-not matching).
(See description of the algorithm in the report file). 

### validation.py



