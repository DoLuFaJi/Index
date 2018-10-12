import pprint

from document import Document

class Algorithm:

    def __init__(self, inverted_file):
        self.inverted_file = inverted_file

    def search(self, word_list):
        pass

    def top_k_rank_search(self, word_list, k):
        pass

    def load_documents(self, word_list):
        # load document associated to word
        documents_score_dictionary = {}
        for word in word_list:
            #load Document with score
            documents_with_score = []
            for filename, score in self.inverted_file[word].items():
                documents_with_score.append(Document(filename, score))
            # add it to list
            documents_score_dictionary[word] = documents_with_score
        return documents_score_dictionary

    def score_sort(self, document):
        return document.rank

class NaiveAlgorithm(Algorithm):

    def search(self, word_list):
        documents_score_dictionary = self.load_documents(word_list)
        pprint.pprint(documents_score_dictionary)
        return self.naive_algorithm(word_list, documents_score_dictionary)

    def naive_algorithm(self, word_list, documents_score_dictionary):
        # first optimisation select word with shortest document size
        document_list = documents_score_dictionary[word_list[0]]
        document_to_display = []
        for document in document_list:
            can_be_added = True
            score = document.score
            for i in range(1, len(word_list)):
                found = False
                for document_found in documents_score_dictionary[word_list[i]]:
                    # todo change to document.name
                    if document is document_found:
                        found = True
                        score += document_found.score
                        break
                if not found:
                    can_be_added = False
                    break
            if can_be_added:
                document_to_display.append(Document(document.name, score/len(word_list)))
        document_to_display.sort(key=lambda doc: doc.score, reverse=True)
        return document_to_display
