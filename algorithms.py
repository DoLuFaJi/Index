import pprint
import copy
import operator
from bisect import bisect_left

from document import Document
from settings import EPSILON
MININT = -10000000

sort_pl = True

def binary_search(arr, value):
    """Given a sorted sequence arr, return the leftmost i such that
    arr[i] == value. Raise ValueError if no element in arr is equal
    to value.

    """
    left = 0
    right = len(arr)
    while left < right:
        mid = (left + right) // 2
        if value > arr[mid][0]:
            left = mid + 1
        else:
            right = mid
    if left != len(arr) and arr[left][0] == value:
        return left
    else:
        return -1


class Algorithm:
    def __init__(self, index):
        self.index = index

    def search(self, k, word_list):
        pass

    def top_k_rank_search(self, word_list, k):
        pass

    def load_documents(self, query_list):
        # load document associated to word
        posting_list = []
        for word in query_list:
            posting_list.append(self.index[word])
        return posting_list

    def score_sort(self, document):
        return document.rank


class NewNaiveAlgorithm(Algorithm):
    def search(self, k, query_list):
        posting_list = self.load_documents(query_list)
        return self.naive(query_list, posting_list)

    def naive(self, query_list, posting_list):
        for documents_with_score in posting_list :
            documents_with_score.sort(key=lambda doc: int(doc[1]), reverse=True)




class NaiveAlgorithm(Algorithm):
    def search(self,k, query_list):
        posting_list = self.load_documents(query_list)
        return self.naive_algorithm(query_list, posting_list)

    def naive_algorithm(self, query_list, posting_list):
        end_of_file = False
        maxDoc = 0
        seen = 0
        query_size = len(query_list)
        score = 0
        list_iterator = []
        document_to_display = []

        for documents_with_score in posting_list :
            documents_with_score.sort(key=lambda doc: int(doc[0]), reverse=False)
        # pprint.pprint(posting_list) #https://www.quora.com/What-does-n-do-in-python

        # set cursor for parallel scan
        for i in range(query_size):
            list_iterator.append(iter(posting_list[i]))
        # algorithm start here
        while not end_of_file:
            for i in range(query_size):
                value = next(list_iterator[i], None)
                # if (value[0] < maxDoc): change to while
                # move until doc >= maxDoc
                # print(value)
                if value is None:
                    end_of_file = True
                    break
                while( int(value[0]) < maxDoc ):
                    value = next(list_iterator[i], None)
                    # end of list not handled todo handle it!!!!! edit should be handled
                    # print(value)
                    if value is None:
                        end_of_file = True
                        break
                # need improvement
                if end_of_file:
                    break

                if int(value[0]) == maxDoc:
                    if seen == query_size-1:
                        document_to_display.append(Document(str(maxDoc), (score+value[1])/query_size))
                        # to do handle end of list edit done
                    else:
                        seen += 1
                        score += value[1]
                if int(value[0]) > maxDoc:
                    maxDoc = int(value[0])

                    if query_size == 1 :
                        document_to_display.append(Document(str(maxDoc), value[1]))
                        # to do handle end of list edit done

                    else :
                        score = value[1]
                        seen = 1
        document_to_display.sort(key=lambda doc: doc.score, reverse=True)
        # print('Naive ' + str(len(document_to_display)))
        return document_to_display

'''
        def naive_algorithm(self, query_list, posting_list):
        # first optimisation select word with shortest document size
        document_list = documents_score_dictionary[word_list[0]]
        document_to_display = []
        for document in document_list:
            can_be_added = True
            score = document[1]
            for i in range(1, len(word_list)):
                # refactored
                if document not in documents_score_dictionary[word_list[i]]:
                    can_be_added = False
                    break
                else:
                    score += document_found[1]
            if can_be_added:
                document_to_display.append(Document(document[0], score/len(word_list)))
        document_to_display.sort(key=lambda doc: doc.score, reverse=True)

        return document_to_display
'''

class FaginsThreshold_Algorithm(Algorithm):
    def search(self,k,word_list):
        posting_list = self.load_documents(word_list)
        return self.faginsThreshold_algorithm(k, word_list, posting_list)

    def faginsThreshold_algorithm(self,k,word_list,posting_list):
# slide dans le dossier note page 20
# 1
        C = {}
        tau = 100001
        mu_min = 100000
        doc_seen_for_each_qt = {}
        pointers = [0] * len(word_list)
        if sort_pl:
            for documents_with_score in posting_list :
                documents_with_score.sort(key=lambda doc: doc[1], reverse=True)
        # pprint.pprint(posting_list)
# 2
        flag_end = False
        while ((len(C) < k or tau > mu_min) and not flag_end ) :
# 2.1
            # print(tau,mu_min)
            max_score = -200000
            scores = []
            d = ""
            index_pl = -1
            word_index_pl = -1
            for documents_with_score in posting_list :
                index_pl += 1
                pt = pointers[index_pl]
                if pt >= len(documents_with_score) :
                    flag_end = True
                elif documents_with_score[pt][1] > max_score :
                    max_score = documents_with_score[pt][1]
                    d = documents_with_score[pt][0]
                    word_index_pl = index_pl

# 2.1.1
            is_found_eachdoc = True
            for documents_with_score in posting_list:
                found = False
                for document_found in documents_with_score :
                    if document_found[0] == d :
                        scores.append(document_found[1])
                        found = True
                        break
                if not found :
                    is_found_eachdoc = False
            if is_found_eachdoc:
                mu = sum(scores) / float(len(scores))
            else :
                mu = MININT

            # print (d,mu,pointers[0],pointers[1])
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
                        break
                C[d] = mu
                mu_min = mu
                for score in C.values():
                    if mu_min > score:
                        mu_min = score
# faire avancer les pointeurs
            index_pl = 0
            if word_index_pl != -1 :
                pointers[word_index_pl] += 1
            for documents_with_score in posting_list:
                pt = pointers[index_pl]
                while (pt < len(documents_with_score)) and (documents_with_score[pt][0] in C) :
                    pt += 1
                pointers[index_pl] = pt
                index_pl += 1
# 2.1.4
            doc_seen_for_each_qt[word_index_pl] = 1
            taus = []
            if len(doc_seen_for_each_qt) == len(word_list) :
                index_pl = 0
                for documents_with_score in posting_list :
                    taus.append(documents_with_score[pointers[index_pl]-1][1])
                    index_pl += 1
                tau = sum(taus) / float(len(taus))
# 3
        document_to_display = []
        for d, mu in C.items() :
            if mu > 0 :
                document_to_display.append(Document(d,mu))
        document_to_display.sort(key=lambda doc : (doc.score, -int(doc.name)), reverse=True)
        # print('FTA ' + str(len(document_to_display)))

        return document_to_display


class FaginsThreshold_WithEpsilon_Algorithm(Algorithm):

    def search(self,k,word_list):
        posting_list = self.load_documents(word_list)
        return self.faginsThreshold_algorithm(k, word_list, posting_list)

    def faginsThreshold_algorithm(self,k,word_list,posting_list):
# slide dans le dossier note page 20
# 1
        C = {}
        tau = 100001
        mu_min = 100000
        doc_seen_for_each_qt = {}
        pointers = [0] * len(word_list)
        if sort_pl:
            for documents_with_score in posting_list :
                documents_with_score.sort(key=lambda doc: doc[1], reverse=True)
        # pprint.pprint(posting_list)
# 2
        flag_end = False
        while ((len(C) < k or tau / ( 1 + EPSILON ) > mu_min) and not flag_end ) :
# 2.1
            # print(tau,mu_min)
            max_score = -200000
            scores = []
            d = ""
            index_pl = -1
            word_index_pl = -1
            for documents_with_score in posting_list :
                index_pl += 1
                pt = pointers[index_pl]
                if pt >= len(documents_with_score) :
                    flag_end = True
                elif documents_with_score[pt][1] > max_score :
                    max_score = documents_with_score[pt][1]
                    d = documents_with_score[pt][0]
                    word_index_pl = index_pl

# 2.1.1
            is_found_eachdoc = True
            for documents_with_score in posting_list:
                found = False
                for document_found in documents_with_score :
                    if document_found[0] == d :
                        scores.append(document_found[1])
                        found = True
                        break
                if not found :
                    is_found_eachdoc = False
            if is_found_eachdoc:
                mu = sum(scores) / float(len(scores))
            else :
                mu = MININT

            # print (d,mu,pointers[0],pointers[1])
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
                        break
                C[d] = mu
                mu_min = mu
                for score in C.values():
                    if mu_min > score:
                        mu_min = score
# faire avancer les pointeurs
            index_pl = 0
            if word_index_pl != -1 :
                pointers[word_index_pl] += 1
            for documents_with_score in posting_list:
                pt = pointers[index_pl]
                while (pt < len(documents_with_score)) and (documents_with_score[pt][0] in C) :
                    pt += 1
                pointers[index_pl] = pt
                index_pl += 1
# 2.1.4
            doc_seen_for_each_qt[word_index_pl] = 1
            taus = []
            if len(doc_seen_for_each_qt) == len(word_list) :
                index_pl = 0
                for documents_with_score in posting_list :
                    taus.append(documents_with_score[pointers[index_pl]-1][1])
                    index_pl += 1
                tau = sum(taus) / float(len(taus))
# 3
        document_to_display = []
        for d, mu in C.items() :
            if mu > 0 :
                document_to_display.append(Document(d,mu))
        document_to_display.sort(key=lambda doc : (doc.score, -int(doc.name)), reverse=True)
        # print('FTAE ' + str(len(document_to_display)))

        return document_to_display


class FaginAlgorithmW(Algorithm):
    def search(self, k, query_list):
        posting_list = self.load_documents(query_list)
        return self.fagin_algorithm(k, query_list, posting_list)

    def fagin_algorithm(self, k, query_list, posting_list):
        show_doc = []
        doc_seen = {}
        doc_unseen = {}
        random_pl = copy.deepcopy(posting_list)
        for documents_with_score in posting_list:
            documents_with_score.sort(key=lambda doc: doc[1], reverse=True)

        nb_qt = len(query_list)
        index_pl = 0
        exit_condition = False
        while len(show_doc) <= k and not exit_condition:
            for qt in range(nb_qt):
                pl_doc = posting_list[qt]
                if len(pl_doc) <= index_pl:
                    exit_condition = True
                    break
                doc, score = pl_doc[index_pl]

                if doc not in doc_seen:
                    doc_seen[doc] = []
                    doc_unseen[doc] = {i for i in range(nb_qt)}
                doc_unseen[doc].remove(qt)
                doc_seen[doc].append(score)
                if len(doc_seen[doc]) == nb_qt:
                    show_doc.append(Document(doc, sum(doc_seen[doc]) / len(doc_seen[doc])))
                    del doc_seen[doc]
                    del doc_unseen[doc]
            index_pl += 1

        for doc, unseen_qts in doc_unseen.items():
            for unseen_qt in unseen_qts:
                unseen_pl = random_pl[unseen_qt]
                index = binary_search(unseen_pl, doc)
                if index > -1:
                    unseen_doc, unseen_score = unseen_pl[index]
                    doc_seen[unseen_doc].append(unseen_score)
                    if len(doc_seen[unseen_doc]) == nb_qt:
                        show_doc.append(Document(unseen_doc, sum(doc_seen[unseen_doc]) / len(doc_seen[unseen_doc])))
                        break

        show_doc.sort(key=lambda doc: (doc.score, -int(doc.name)), reverse=True)
        # print('FA ' + str(len(show_doc)))

        return show_doc[:k]


class FaginAlgorithm(Algorithm):
    def search(self, k, query_list):
        posting_list = self.load_documents(query_list)
        posting_list_sorted_by_score = self.sort_posting_list(posting_list)
        posting_list_sorted = self.create_dictionary_from_posting_list(posting_list,len(query_list))
        return self.fagin_algorithm(query_list, posting_list_sorted, posting_list_sorted_by_score, k)

    def sort_posting_list(self, posting_list):
        posting_list_sorted = copy.deepcopy(posting_list) # check if it works or not
        for documents_with_score in posting_list_sorted :
            documents_with_score.sort(key=lambda doc: doc[1], reverse=True)
        return posting_list_sorted

    def create_dictionary_from_posting_list(self, posting_list, n): #needed for good access time or use a btree library
        posting_list_dictionary = [{}] * n # should works
        for i in range(0, n-1):
            for document in posting_list[i]:
                posting_list_dictionary[i][document[0]] = document # should work
        return posting_list_dictionary

    def fagin_algorithm(self, query_list, posting_list_sorted, posting_list, k):
        n = len(query_list) #todo get smallest document size
        list_iterator = []
        selected_document = {} # M : [avg, nbItem]
        document_to_display = [] # C: [avg]
        # set cursor for parallel scan
        for i in range(0, n):
            list_iterator.append(iter(posting_list[i]))

        exit_condition = False
        #Fagin start
        end_of_file = 0
        while not exit_condition: # |C|=k or end of file
            for i in range(0, n):
                # work here
                document = next(list_iterator[i], None)
                if document is None:
                    end_of_file = end_of_file + 1
                    if end_of_file == n:
                        exit_condition = True
                    break
                test = selected_document.get(document[0], None)
                if test is None:
                    selected_document[document[0]] = AgregateAvg(document[1], document[0], i, n)
                    test = selected_document.get(document[0], None)
                else:
                    selected_document[document[0]].updateAvg(document[1], i)
                if selected_document[document[0]].n == n: # also check when n = 1
                    document_to_display.append(Document(selected_document[document[0]].document, selected_document[document[0]].value))
                    del selected_document[document[0]]
                    if len(document_to_display) >= k:
                        exit_condition = True
                        break
        for key, document in selected_document.items():
            can_be_added = True
            query_term_to_see = document.unseen_query_term()
            for query_term in query_term_to_see:
                found_document = posting_list_sorted[i].get(document.document, None)
                if found_document is None: # if doc not found
                    can_be_added = False
                    break
                score = found_document[1]
                document.updateAvg(score, i)
            if can_be_added:
                document_to_display.append(Document(selected_document[key].document, selected_document[key].value))
            # no need to remove from selected document
        document_to_display.sort(key=lambda doc: (doc.score, -int(doc.name)), reverse=True)
        return document_to_display[:k]

class AgregateAvg:
    value = 0
    def __init__(self, first_value, document, i, size):
        self.sum_value = first_value
        self.n = 1
        self.document = document # useless ! edit finaly it's useful
        self.seen = [False] * size # initalize
        self.seen[i] = True # seen by the query term i
        self.value = self.sum_value / self.n

    def __repr__(self):
        return self.document

    def updateAvg(self, value_to_add, i):
        self.sum_value += value_to_add
        self.n = 1 + self.n
        self.value = self.sum_value / self.n
        self.seen[i] = True

    def unseen_query_term(self):
        unseen_list = []
        n = len(self.seen)
        for i in range(0, n):
            if not self.seen[i]:
                unseen_list.append(i)
        return unseen_list
