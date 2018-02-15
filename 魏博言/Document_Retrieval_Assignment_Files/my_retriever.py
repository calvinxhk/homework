import math
class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting

    # Method to apply query to index
    def forQuery(self,query):
        doc_id_max = max([max(self.index[i]) for i in self.index])
        result = []
        if self.termWeighting == 'binary':
            for doc_id in range(1, int(doc_id_max)+1):
                boolean = 0
                for term in query:
                    if term in self.index and doc_id in self.index[term]:
                        boolean +=1
                    else:
                        continue
                    result.append((boolean,doc_id))
        elif self.termWeighting == 'tf':
            for doc_id in range(1, int(doc_id_max)+1):
                a = []
                b = []
                for term in query:
                    qi = query[term]
                    if term in self.index and doc_id in self.index[term]:
                        di = self.index[term][doc_id]
                        a.append(qi*di)
                for term in self.index:
                    if doc_id in self.index[term]:
                        di = self.index[term][doc_id]
                        b.append(di**2)
                sim = sum(a)/(sum(b)**0.5)
                if sim:
                    result.append((sim,doc_id))
        elif self.termWeighting =='tfidf':
            for doc_id in range(1, int(doc_id_max) + 1):
                a = []
                b = []
                for term in query:
                    if term in self.index and doc_id in self.index[term]:
                        log = math.log(doc_id_max / len(self.index[term]))
                        xi = (self.index[term][doc_id]) * log
                        qi = (query[term]) * log
                    else:
                        xi = 0
                        qi = 0
                    a.append(xi*qi)
                for term in self.index:
                    if doc_id in self.index[term]:
                        log = math.log(doc_id_max / len(self.index[term]))
                        di = (self.index[term][doc_id]) * log
                        b.append(di**2)
                if sum(a)*sum(b) !=0:
                    sim = sum(a) / (sum(b) ** 0.5)
                    result.append((sim, doc_id))
        result.sort(reverse=True)
        result = [n for (m, n) in result[:10]]
        return result


