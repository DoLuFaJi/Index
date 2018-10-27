# This file countains the methods necessary for the data processing
from settings import DATAFOLDER
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import *
from nltk.stem.porter import *
#from nltk.stem.snowball import SnowballStemmer

#nltk.python -m spacy download en_core_web_smdownload('stopwords')
import math
import os

class Tokenization:

    def tokenization(self, file_name, remove_tags=True, remove_stopwords=True, stemming=False):
        #This method takes the name of the file and return the list of word inside it
        file = open(DATAFOLDER+file_name, "r")

        #separate the document
        doc_in_file = file.read().split("<DOC>")
        del doc_in_file[0] #the first is empty

        #create the dictionary
        dict = {}

        #put thing inside the dictionary
        for doc in doc_in_file:
            try:
                docid = re.findall("<DOCID> (.*?) </DOCID>", doc)[0]
                # print(docid)
            except:
                 print("ERROR")
                 print(doc)
            if remove_tags:
                text = self.__remove_tags__(doc)
            if remove_stopwords:
                text = self.__remove_stopwords__(text)

            #list of strings (only words no punctuation)
            tokenizer = RegexpTokenizer(r'\w+')
            tokenized_text = tokenizer.tokenize(text)

            if stemming:
                tokenized_text = self.__stemming__(tokenized_text)

            dict[docid] = tokenized_text

        file.close()
        return dict

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

    def __stemming__(self, tokenized_text):
        #use snowball stemmer to stem text
        #stemmer = SnowballStemmer("english")
        #for word in tokenized_text:
        #word = stemmer.stem(word)
        porter = nltk.PorterStemmer()
        [porter.stem(t) for t in tokenized_text]
        return tokenized_text

class Scoring:
    #Class to get score for term
    def __tf__(self, tokens, term):
        #This method use the term frequency inside the file to give a score to a term
        #tokens = tokenization(file_name)
        tf = math.log10(1+(tokens.count(term) / len(tokens)))
        return tf

    def __idf__(self, nb_documents_term_appears, number_of_documents):
        #This method use the inverse document frequency to give a score to a term

        #number of documents where the term appears
        #nb_documents_term_appears = 0
        #for file in os.listdir(DATAFOLDER):
        #    if self.__tf__(file, term)>0:
        #        nb_documents_term_appears += 1

        idf = math.log10(number_of_documents / (1+nb_documents_term_appears))
        return idf

    def compute_score(self, tokens, term, nb_documents_term_appears, number_of_documents):
        #compute the score of a term in a document
        tf = self.__tf__(tokens, term)
        idf = self.__idf__(nb_documents_term_appears, number_of_documents)
        score = tf * idf
        return score

#test
#lolo = Scoring()
#lala = Tokenization()
#for file in os.listdir(DATAFOLDER):
#    print(file)
#    tokfile = lala.tokenization(file)
#     lili = lolo.compute_score(tokens=tokfile, term="alien", nb_documents_term_appears=359, number_of_documents=732)
