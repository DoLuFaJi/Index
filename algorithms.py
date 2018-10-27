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

class FaginsThreshold_Algorithm(Algorithm):

    def __init__(self, inverted_file):
        self.inverted_file = inverted_file

    def search(self,k,word_list):
        documents_score_dictionary = self.load_documents(word_list)
        pprint.pprint(documents_score_dictionary)
        return self.faginsThreshold_algorithm(k,word_list, documents_score_dictionary)
    def faginsThreshold_algorithm(self,k,word_list,documents_score_dictionary):

# slide dans le dossier note page 20
# 1
        C = {}
        pointers = {}
        tau = 2
        mu_min = 2.2
        doc_seen_for_each_qt = {}
        for word in word_list:
            pointers[word] = 0
        for word,documents_with_score in documents_score_dictionary.items() :
            documents_with_score.sort(key=lambda doc: doc.score, reverse=True)
# 2
        while ( len(C) < k and tau < mu_min) :
# 2.1
            max_score = -2
            scores = []
            d = ""
            for word,documents_with_score in documents_score_dictionary.items() :
                pt = pointers[word]
                if documents_with_score[pt].score > max_score :
                    max_score = documents_with_score[pt].score
                    d = documents_with_score[pt].name
# 2.1.1
            for word,documents_with_score in documents_score_dictionary.items() :
                for document_found in documents_with_score :
                    if document_found.name == d :
                        scores.append(document_found.score)
                        break
            mu = sum(scores) / float(len(scores))
# 2.1.2
            if len(C) < k :
                C[d] = mu
                if len(C) == 1 :
                    mu_min = mu
                else :
                    mu_min = min(mu,mu_min)
# 2.1.3
            elif mu_min < mu :
                for (name,score) in C.items():
                    if mu_min == score:
                        del C[name]
                C[d] = mu
                mu_min = mu
                for score in C.values():
                    if mu_min > score:
                        mu_min = score
# faire avancer les pointeurs
                for word,documents_with_score in documents_score_dictionary.items() :
                    pt = pointers[word]
                    while C.has_key(documents_with_score[pt].name) :
                        pt += 1
# 2.1.4
            doc_seen_for_each_qt[word] = 1
            taus = []
            if len(doc_seen_for_each_qt) == k :
                for word,documents_with_score in documents_score_dictionary.items() :
                    taus.append(documents_with_score[pt-1].score)
                tau = sum(taus) / float(len(taus))
# 3
        return C
