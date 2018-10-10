# This file countains the methods necessary for the data processing
from settings import DATAFOLDER
import re
from nltk.tokenize import RegexpTokenizer
import math
import os


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
    def __tf__ (self, file_name, term):
        #This method use the term frequency inside the file to give a score to a term
        tokens = tokenization(file_name)
        tf = math.log10( 1+( tokens.count(term) / len(tokens) ) )
        print(tf)
        return tf

    def __idf__ (self, term):
        #This method use the inverse document frequency to give a score to a term

        #number of documents where the term appears
        nb_documents_term_appears = 0
        for file in os.listdir(DATAFOLDER):
            if self.__tf__(file, term)>0:
                nb_documents_term_appears += 1

        idf = math.log10( len(os.listdir(DATAFOLDER)) / (1+nb_documents_term_appears) )
        return idf

    def score (self, file_name, term):
        tf = self.__tf__(file_name, term)
        idf = self.__idf__(term)
        score = tf * idf
        return score

# #test
# lolo = Scoring()
# for file in os.listdir(DATAFOLDER):
#     lili = lolo.score(file_name=file,term="alien")
#     print(lili)
