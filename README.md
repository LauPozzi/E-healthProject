# E-healthProject - part 1 - Group09

## Setup
* Open a command prompt and execute:
    ```console
    conda create -n Group09_PartI_Env python=3.10
    conda activate Group09_PartI_Env
    ```

Now it is necessary to clone the repository and install all the dependencies listed in _requirements.txt_. To do so: 
* In the command prompt and execute:
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

### evaluation.py
If executed, this script provides an analysis of the classification algorithm.
The algorithm is applied both to a validation database (created with a relaxed version of the query of interest) and a test database (created with the actual query of interest).
Comparing the validation database to the manual classification (used as ground truth), it selects an optimal threshold which will be used for the binary classification of the test database.
It evaluates the classification on both databases based on AUC, accuracy, specificity, and sensitivity, reporting also many significant plots.


