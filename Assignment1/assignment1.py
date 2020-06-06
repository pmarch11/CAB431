import glob, os
import string
from stemming.porter2 import stem
import math

class BowDocument:
    def __init__(self, path):
        self.id = self.getDocId(path)
        self.curr_doc = self.handleInput(path) # generating curr_doc from initial path passed in as an arg
        self.tf = self.computeTF(self.curr_doc)
        self.idf = {}
        self.docLength = self.computeDocLength() #Number of stemmed, non stop words in the document
        self.termLength = self.computeTermsLength() #Number of stemmed, unique, non stop words in the document
        self.avgDL = 0

    # ACCESSOR AND MUTATOR METHODS
    def set_docLength(self, val):
        self.docLength = val

    def get_docLength(self):
        return self.docLength

    def set_idf(self, val):
        self.idf = val
    
    def get_idf(self):
        return self.idf

    def set_avgDL(self, val):
        self.avgDL = val

    def computeDocLength(self):
        return sum(self.curr_doc.values())

    def computeTermsLength(self):
        return len(self.curr_doc.values())


    #Handling input and generating curr_doc variable
    def handleInput(self, doc_path):
        myfile=open(os.path.join('inputdata', doc_path))
        curr_doc = {}
        start_end = False

        file_=myfile.readlines()

        for line in file_:
            line = line.strip()

            #strip any tags
            if(start_end == False):
                if line.startswith("<text>"):
                    start_end = True
            elif line.startswith("</text>"):
                break
            else:
                line = line.replace("<p>", "").replace("</p>", "")
                line = line.translate(str.maketrans('','', string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
                line = line.replace("\\s+", " ")

                #for each term, preprocess and check it isnt a stop word
                for term in line.split():
                    term = stem(term.lower())
                    if len(term) > 2 and term not in stopWordsList:
                        try:
                            curr_doc[term] += 1
                        except KeyError:
                            curr_doc[term] = 1
        myfile.close()
        return curr_doc
        

    #Making sure key matches the documents ID
    def getDocId(self, path):
        myfile=open(os.path.join('inputdata', path))

        file_=myfile.readlines()
        for line in file_:
            line = line.strip()
            if line.startswith("<newsitem "):
                for part in line.split():
                    if part.startswith("itemid="):
                        docid = part.split("=")[1].split("\"")[1]
                        return docid

    #for adding new term to curr_doc
    def addTerm(self, term, freq):
        if len(term) > 2 and term not in stopWordsList:
            try:
                self.curr_doc[term] += freq
            except KeyError:
                self.curr_doc[term] = freq


    #for computing TF scores for given document
    def computeTF(self, curr_doc):

        tfDict = {}

        for k, v in curr_doc.items():
            tfDict[k] = v / sum(curr_doc.values())


        return tfDict

    #for displaying individual document information
    def displayDocInfo(self):
        print("Doc " + self.id + " contains " + str(len(self.curr_doc.keys()))
         + " terms (stems) and has total " + str(sum(self.curr_doc.values())) + " words")
        
        for word, count in sorted(self.curr_doc.items(), key=lambda item: item[1], reverse=True):
            print(word + ", " + str(count))

    def BM25(self, q=[], k1=1.5, b=0.75):
        scores = 0
        q = [stem(item.lower()) for item in q] #convert querys to lowercase and stemmed versions
        for query in q:
            tmp_score = []
            if query in self.tf:
                upper = (self.tf[query] * (k1+1))
                lower = ((self.tf[query]) + k1*(1 - b + b * self.termLength/self.avgDL))
                tmp_score.append(self.idf[query] * upper / lower)

            scores += (sum(tmp_score))
        return scores


if __name__ == '__main__':

    import sys
    import collections

    stopwords_f = open('common-english-words.txt', 'r')
    stopWordsList = stopwords_f.read().split(',')
    stopwords_f.close()


    fn1 = '741299newsML.xml'
    fn2 = '741309newsML.xml'
    fn3 = '780718newsML.xml'
    fn4 = '780723newsML.xml'
    fn5 = '783802newsML.xml'
    fn6 = '783803newsML.xml'
    fn7 = '807600newsML.xml'
    fn8 = '807606newsML.xml'
    fn9 = '809481newsML.xml'
    fn10 = '809495newsML.xml'

    xmlFNames = {fn1, fn2, fn3, fn4, fn5,
     fn6, fn7, fn8, fn9, fn10}

    bowDocuments = {}
    bowDocumentsOBJ = {}
    totalDocLength = 0
    avgDL = 0

    #Q1 START

    for fn in xmlFNames:
        p = BowDocument(fn)
        bowDocuments[p.id] = p.curr_doc
        bowDocumentsOBJ[p.id] = p
        p.displayDocInfo()
        print("\n")

    #Q2_s1 START

    super_dict = collections.defaultdict(set)

    for fileName in xmlFNames:
        strippedID = fileName.replace('newsML.xml', "")
        for k, v in bowDocuments[strippedID].items():
            super_dict[k]= v


    totalTerms = 0

    for x in super_dict:
        totalTerms += 1

    print("There are " + str(len(xmlFNames)) + " documents in this data set and contains " + str(totalTerms) + " terms.")

    for x in super_dict:
        print(x + ": " + str(super_dict[x]))
    print("\n")

    #Q2_s2 START

    for obj in bowDocumentsOBJ:
        bowDocumentsOBJ[obj]
        tfDict = bowDocumentsOBJ[obj].tf
        idfDict = {}
        tfidfDict = {}

        for x in super_dict:
            termDictCount = 0
            for fileName in xmlFNames:
                    strippedID = fileName.replace('newsML.xml', "")
                    if x in bowDocuments[strippedID]:
                        termDictCount += 1
            idfDict[x] = len(xmlFNames) / termDictCount

            try:
                tfidfDict[x] = tfDict[x] * idfDict[x]
            except KeyError:
                tfidfDict[x] = 0
        
        bowDocumentsOBJ[obj].set_idf(idfDict)

        twentyCounter = 0
        print("Document " + bowDocumentsOBJ[obj].id + " contains " + str(bowDocumentsOBJ[obj].termLength) + " terms")
        for k, v in sorted(tfidfDict.items(), key=lambda item: item[1], reverse=True):
            print(k + ": " + str(v))
            twentyCounter += 1
            if twentyCounter >= 20:
                break

        print("\n")

    #Q3 START
    for obj in bowDocumentsOBJ:
        totalDocLength += bowDocumentsOBJ[obj].get_docLength()
        print("Document: " + bowDocumentsOBJ[obj].id + ", Length: " + str(bowDocumentsOBJ[obj].get_docLength()))
    avgDL = totalDocLength / len(xmlFNames)

    query = ["British", "fashion"]

    print("\nAverage document length " + str(int(avgDL)) + " for query: " + ' '.join(query) + '\n')
    
    topDocs = {}
    #calculate all BM25 scores
    for obj in bowDocumentsOBJ:
        
        bowDocumentsOBJ[obj].set_avgDL(avgDL)
        print("Document: " + bowDocumentsOBJ[obj].id + ", Length: "+ str(bowDocumentsOBJ[obj].docLength) + " and BM25 Score: " + str(bowDocumentsOBJ[obj].BM25(query)))
        topDocs[bowDocumentsOBJ[obj].id] = bowDocumentsOBJ[obj].BM25(query)

    threeCounter = 0
    print('\nFor query "' + ' '.join(query) + '", three recommended relevant documents and their BM25 score:\n')
    for k, v in sorted(topDocs.items(), key=lambda item: item[1], reverse=True):
        print(k + ": " + str(v))
        threeCounter += 1
        if threeCounter >= 3:
            break






        

    





    
        





        
        
        
