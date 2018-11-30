Indexing quering text
=================================
Project was made with python3.7
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
> `python main.py -n name_of_saved`

To load it next time:
> `python main.py -n name_of_saved -m name_of_saved_mit`
## Run the tests
> `python test_sample.py -n name_of_saved -m name_of_saved_mit -t "akenb"`

After the -t the input string contains the tests you want to run
- to test the batch size when the inverted file is constructed: "b" but before create the directory ./if_test
- to test the algos: "a" and after append "k" to make the k of Fagin's vary, "e" to make epsilon of Fagin's threshold with epsilon vary, and "n" to make the number of terms vary
## Optional arguments details:

### main
  - d DATAFOLDER, --datafolder DATAFOLDER Choose datafolder
  - n NAME, --name NAME  Choose filename
  - m MAP, --map MAP     Map id term, set to load an index
  - s STEMMING, --stemming STEMMING
                        Do you want stemming ? (yes) -take a lit of time ==
  - b BATCHSIZE, --batchsize BATCHSIZE
                        Choose your batch size - default=1000
  - e EPSILON, --epsilon EPSILON
                        Epsilon for Fagins
### test
  - d DATAFOLDER, --datafolder DATAFOLDER
                        Choose datafolder
  - n NAME, --name NAME  Choose filename
  - m MAP, --map MAP     Map id term, set to load an index
  - s STEMMING, --stemming STEMMING
                        Do you want stemming ? (yes) -take a lit of time ==
  - b BATCHSIZE, --batchsize BATCHSIZE
                        Choose your batch size - default=1000
  - e EPSILON, --epsilon EPSILON
                        Epsilon for Fagins
  - c NUMBEROFTEST, --numberoftest NUMBEROFTEST
                        How many times tests must be run
  - t TESTS, --tests TESTS
                        Tests to run (a k e n b: algo, k, epsilon, nbterms,
                        batchsize)
  - r NBTERMS, --nbterms NBTERMS
                        nb terms in request
  - k K, --k K           k for fagins

## Report
[Report](Rapport Indexing and Querying Text.pdf)
