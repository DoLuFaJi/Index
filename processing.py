# This file countains the methods necessary for the data processing
from settings import DATAFOLDER
import re
from nltk.tokenize import RegexpTokenizer
import math


def tokenization (file_name):
    #This method takes the name of the file and return the list of word inside it
    file = open(DATAFOLDER+file_name, "r")
    text_from_file = file.read()

    #remove all tags
    cleanr = re.compile('<.*?>')
    text_clean = re.sub(cleanr, '', text_from_file)

    #list of strings (only words no punctuation)
    tokenizer = RegexpTokenizer(r'\w+')
    tokenized_text = tokenizer.tokenize(text_clean)

    file.close()
    return tokenized_text

class Scoring:
    #Mother class
    def __init__(self):
        #Constructor
        pass

class FrequencyScoring(Scoring):
    #Compute the score with the frequency method
    def __init__(self):
        #Constructor
        pass

    def score (self, file_name, term):
        #This method use the term frequency inside the file to give a score to a term
        tokens = tokenization(file_name)
        score = math.log10(1+(tokens.count(term) / len(tokens)))
        return score

#test
lala = tokenization("la012989")
print(lala)

lolo = FrequencyScoring()
print(lili)
lili = lolo.score("la012989", "the")
