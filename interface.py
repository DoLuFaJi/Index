def input_N_topN(algo_op):
    N = -1
    while (not algo_op == 0) and True:
        try :
            N = int(input('Top ?  (the X of the TopX results ) :'))
            if N > 0 :
                break
        except :
            print ("Enter an integer plz")
    return N

def input_terms():
    print("Enter terms one by one, line by line and end by 'E' : ")
    terms = []
    x = input('')
    while not x == "E" :
        terms.append(x)
        x = input('')
    return terms

def input_choose_algo():
    while True :
        try:
            algo_op = int(input("0 for Naive, 1 for Fagin, 2 for Fagins Threshold, 3 for Fagins Threshold With Epsilon\n"))
            if algo_op in [0,1,2,3] :
                break
            else :
                print ("0 or 1 or 2 or 3 plz")
        except :
            print ("0 or 1 or 2 or 3 plz")
    return algo_op
