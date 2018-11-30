Indexing quering text
=================================
Projet was made with python3.7
## Install
> `pip install -r requirements.txt`

>`python`

>`import nltk`

>`nltk.download('stopwords')`

Add the data (articles) in /data/latimes
## Run program
To run the program:
> `python main.py`

It will construct the invited file and then show an interactive interface in console line to make query

We advise to save the generated file on the first run:
> `python main.py -n name_of_saved

To load it next time:
> `python main.py -n name_of_saved -m name_of_saved_mit`
## Run the tests
> `python test_sample.py -n name_of_saved -m name_of_saved_mit -t "akenb"`

After the -t the input string contains the tests you want to run
- to test the batch size when the inverted file is constructed: "b" but before create the directory ./if_test
- to test the algos: "a" and after append "k" to make the k of Fagin's vary, "e" to make epsilon of Fagin's threshold with epsilon vary, and "n" to make the number of terms vary
## Optional arguments details:

### main

### test

## Report
[Report]()
