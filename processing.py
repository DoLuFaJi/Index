# This file countains the methods necessary for the data processing
from settings import DATAFOLDER
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
#nltk.download('stopwords')
import math
import os

class Tokenization:

    def tokenization (self, file_name, remove_tags=1, remove_stopwords=1):
        #This method takes the name of the file and return the list of word inside it
        file = open(DATAFOLDER+file_name, "r")
        text_from_file = file.read()

        if remove_tags:
            text = self.__remove_tags__(text_from_file)
        if remove_stopwords:
            text = self.__remove_stopwords__(text)

        #list of strings (only words no punctuation)
        tokenizer = RegexpTokenizer(r'\w+')
        tokenized_text = tokenizer.tokenize(text)

        file.close()
        return tokenized_text

    def __remove_tags__(self, text):
        #remove all tags
        cleanr = re.compile('<.*?>')
        text_clean = re.sub(cleanr, '', text)
        return text_clean

    def __remove_stopwords__(self, text):
        #remove stopwords
        pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
        text_clean = pattern.sub('', text)
        return text_clean

class Scoring:
    #Class to get score for term
    def __tf__ (self, tokens, term):
        #This method use the term frequency inside the file to give a score to a term
        #tokens = tokenization(file_name)
        tf = math.log10( 1+( tokens.count(term) / len(tokens) ) )
        return tf

    def __idf__ (self, nb_documents_term_appears, number_of_documents):
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
        idf = self.__idf__(nb_documents_term_appears, number_of_documents)
        score = tf * idf
        return score

#test
#lolo = Scoring()
#lala = Tokenization()
#for file in os.listdir(DATAFOLDER):
#    tokfile = lala.tokenization(file)
#    print(tokfile)
#    break
    #lili = lolo.compute_score(tokens=tokfile, term="alien", nb_documents_term_appears=359, number_of_documents=732)
