import glob, os
import string
from stemming.porter2 import stem
import math
from scipy import stats

#All 3 function implementations taken from CAB431 workshops 
def avg_doc_len(coll):
    tot_dl = 0
    for id, doc in coll.get_docs().items():
        tot_dl = tot_dl + doc.get_doc_len()
    return tot_dl/coll.get_num_docs()

#used in task1 Q3 
def bm25(coll, q, df):
    bm25s = {}
    avg_dl = avg_doc_len(coll)
    no_docs = coll.get_num_docs()
    for id, doc in coll.get_docs().items():
        query_terms = q.split()
        qfs = {}        
        for t in query_terms:
            term = stem(t.lower())
            try:
                qfs[term] += 1
            except KeyError:
                qfs[term] = 1
        #try:
        k = 1.2 * ((1 - 0.75) + 0.75 * (doc.get_doc_len() / float(avg_dl)))
        #except ZeroDivisionError:
            #k = 0
        
        bm25_ = 0.0
        for qt in qfs.keys():
            n = 0
            if qt in df.keys():
                n = df[qt]
                f = doc.get_term_count(qt)
                qf = qfs[qt]
                #try:
                bm = math.log(1.0 / ((n + 0.5) / (no_docs - n + 0.5)), 2) * (((1.2 + 1) * f) / (k + f)) * ( ((100 + 1) * qf) / float(100 + qf))
                #except ZeroDivisionError:
                    #bm = 0
                bm25_ += bm
        bm25s[doc.get_docid()] = bm25_
    return bm25s

#used in Task 2 
def w4(coll, ben, theta):
    T={}
    # select T from positive documents and r(tk)
    for id, doc in coll.get_docs().items():
        try:
            if ben[id] > 0:
                for term, freq in doc.terms.items():
                    try:
                        T[term] += 1
                    except KeyError:
                        T[term] = 1
        except KeyError:
            pass
    #calculate n(tk)
    ntk = {}
    for id, doc in coll.get_docs().items():
        for term in doc.get_term_list():
            try:
                ntk[term] += 1
            except KeyError:
                ntk[term] = 1
    
    #calculate N and R
                    
    No_docs = coll.get_num_docs()
    R = 0
    for id, fre in ben.items():
        if ben[id] > 0:
            R += 1
    
    for id, rtk in T.items():
        T[id] = ((rtk+0.5) / (R-rtk + 0.5)) / ((ntk[id]-rtk+0.5)/(No_docs-ntk[id]-R+rtk +0.5)) 

    #calculate the mean of w4 weights.
    meanW4= 0
    for id, rtk in T.items():
        meanW4 += rtk
    try:
        meanW4 = meanW4/len(T)
    except ZeroDivisionError:
        meanW4 = 0

    #Features selection
    Features = {t:r for t,r in T.items() if r > meanW4 + theta }
    return Features


def testRanking(coll, features):
    ranks={}
    for id, doc in coll.get_docs().items():
        Rank = 0
        for term in features.keys():
            if term in doc.get_term_list():
                try:
                    ranks[id] += features[term]
                except KeyError:
                    ranks[id] = features[term]
    return ranks



if __name__ == '__main__':

    #import helpful packages
    
    import sys
    import df
    from coll import BowColl, BowDoc
    from collections import defaultdict

    #PART 1

    #parse input queries
    topic_statements_f = open('topicstatements.txt', 'r')
    topicStatements = {}
    file_=topic_statements_f.readlines()
    numID = 0
    listOfIDs = []

    #storing relevant data
    for line in file_:
        line = line.strip()
        
        if line.startswith("<num>"):
            numID = line.replace("<num> Number: ", "")
            listOfIDs.append(numID)

        if line.startswith("<title>"):
            topicStatements[numID] = line.replace("<title>", "")


    stopwords_f = open('common-english-words.txt', 'r')
    stopWordsList = stopwords_f.read().split(',')
    stopwords_f.close()

    #masterDict[R104][coll][term]
    masterDict = defaultdict(lambda: defaultdict(dict))
    start_end = False

    #reading dataset files and adding 'clean' terms to coll
    for id in listOfIDs:
        coll = BowColl()
        print("reading "+ str(id))
        folderName = "Training" + id.replace("R", "")
        path = os.path.join('dataset101-150/' + folderName)
        for f in (os.listdir(path)):
            curr_doc = None
            curr_doc = BowDoc(f.replace(".xml", ""))
            word_count = 0
            myfile=open(path + "/" + f)
            file_ = myfile.readlines()

            for line in file_:

                line = line.strip()

                if(start_end == False):
                    if line.startswith("<text>"):
                        start_end = True
                elif line.startswith("</text>"):
                    break
                else:
                    line = line.replace("<p>", "").replace("</p>", "")
                    line = line.translate(str.maketrans('','', string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
                    line = line.replace("\\s+", " ")

                    for term in line.split():
                        word_count += 1
                        term = stem(term.lower())
                        if len(term) > 2 and term not in stopWordsList:
                                curr_doc.add_term(term)
            myfile.close()
            curr_doc.set_doc_len(word_count)
            coll.add_doc(curr_doc)
        masterDict[id] = coll
    

    #Q2

    baselineResults = defaultdict(dict)

    for x in topicStatements:
        wFile = open(os.path.join('baselineresults/', 'BaselineModel_' + str(x) + ".dat"), 'a')
        folderName = "Training" + x.replace("R", "")
        path = os.path.join('dataset101-150/' + folderName)
        scores = {}
        for f in (os.listdir(path)):
            docID = f.replace(".xml", "")
            termFound = False

            for q in topicStatements[x].split():
                q = q.replace("-", " ")
                q = q.replace(",", " ")
                q = q.replace("'", " ")
                q = stem(q.lower())
                if masterDict[x].get_doc(docID).check_term_exists(q) == 0:
                    pass
                else:
                    termFound = True
                    break
            if termFound:
                baselineResults[x][docID] = 1
            else:
                baselineResults[x][docID] = 0
    #Q3
        scores = bm25(masterDict[x], topicStatements[x], df.calc_df(masterDict[x]))
        for f in scores:
            wFile.write(f +' '+ str(scores[f]) +'\n') 
        wFile.close()

    #PART 2
    #Q5

    path = os.path.join('topicassignment101-150/')
    benchmark = defaultdict(dict)
    for f in (os.listdir(path)):
        myfile=open(path + "/" + f)
        file_ = myfile.readlines()
        for line in file_:
            line = line.strip()
            lineList = line.split()
            benchmark[f.replace("Training", "R").replace(".txt", "")][lineList[1]]=float(lineList[2])
        myfile.close()

    theta = 3.5
    trainingWeights = {}
    ranks = {}

    for x in topicStatements:
        trainingWeights[x] = w4(masterDict[x], benchmark[x], theta)
        ranks[x] = testRanking(masterDict[x], trainingWeights[x])

    for x in ranks:
        print("Ranking " + x)
        wFile = open(os.path.join('IFranks/', 'result_' + str(int(x.replace("R", "")) - 100) + ".dat"), 'a')
        for k, v in sorted(ranks[x].items(), key=lambda item: item[1], reverse=True):

        #for docScores in sorted(ranks[x]):
            wFile.write(k + " " + str(v) +'\n')
        wFile.close()

    #PART 3
    
    benchmarkResults = [None] * 50
    myResults = [None] * 50

    #calculate results using benchmarks (given data)
    for x in list(benchmark):
        R = 0
        for docID in benchmark[x]:
            if (benchmark[x][docID] == 1):
                R = R + 1

        R1 = 0
        for docID in ranks[x]:
            if(docID in ranks[x]):
                R1 = R1 + 1

        RR1 = 0
        for docID in benchmark[x]:
            try:
                if(benchmark[x][docID] == 1) and (docID in ranks[x]):
                    RR1 = RR1 + 1
            except KeyError:
                pass

        try:
            r = float(RR1)/float(R)
        except ZeroDivisionError:
            r = 0

        try:
            p = float(RR1)/float(R1)
        except ZeroDivisionError:
            p = 0

        try:
            F1 = 2*p*r/(p+r)
        except ZeroDivisionError:
            F1 = 0

        benchmarkResults[int(x.replace("R", "")) - 101] = [[r], [p], [F1]]


    #calculate results using baselineResults (my generated data)
    f = open('EvaluationResult.dat', 'w')
    f.write("Topic  Precision   Recall  F1\n")
    for x in list(baselineResults):
        R = 0
        for docID in baselineResults[x]:
            if (baselineResults[x][docID] == 1):
                R = R + 1

        R1 = 0
        for docID in ranks[x]:
            if(docID in ranks[x]):
                R1 = R1 + 1

        RR1 = 0
        for docID in baselineResults[x]:
            try:
                if(baselineResults[x][docID] == 1) and (docID in ranks[x]):
                    RR1 = RR1 + 1
            except KeyError:
                pass

         
        r = float(RR1)/float(R)
        try:
            p = float(RR1)/float(R1)
        except ZeroDivisionError:
            p = 0

        try:
            F1 = 2*p*r/(p+r)
        except ZeroDivisionError:
            F1 = 0

        myResults[int(x.replace("R", "")) - 101] = [[r], [p], [F1]]

        f.write(x + "   " + str(r) + "  " + str(p) + "    " + str(F1) + "\n")
    f.close()

    

    print(stats.ttest_ind(myResults, benchmarkResults))