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
    #Class to get score for term
    def __tf__ (self, tokens, term):
        #This method use the term frequency inside the file to give a score to a term
        #tokens = tokenization(file_name)
        tf = math.log10( 1+( tokens.count(term) / len(tokens) ) )
        return tf

    def __idf__ (self, term, nb_documents_term_appears, number_of_documents):
        #This method use the inverse document frequency to give a score to a term

        #number of documents where the term appears
        #nb_documents_term_appears = 0
        #for file in os.listdir(DATAFOLDER):
        #    if self.__tf__(file, term)>0:
        #        nb_documents_term_appears += 1

        idf = math.log10( number_of_documents / (1+nb_documents_term_appears) )
        return idf

    def compute_score (self, tokens, term, nb_documents_term_appears, number_of_documents):
        #compute the score of a term in a document
        tf = self.__tf__(tokens, term)
        idf = self.__idf__(term,nb_documents_term_appears, number_of_documents)
        score = tf * idf
        return score

#test
lolo = Scoring()
for file in os.listdir(DATAFOLDER):
    tokfile = tokenization(file)
    lili = lolo.compute_score(tokens=tokfile, term="alien", nb_documents_term_appears=359, number_of_documents=732)
