import pandas as pd
import warnings
import csv
import json
import sys
import pickle
from timeit import default_timer as timer
from cleaned import clean
warnings.filterwarnings("ignore")
import math
import numpy as np
from multiprocessing import Pool, cpu_count


class find_similar:
    def __init__(self, corpus, tokenizer=None):
        self.corpus_size = len(corpus)
        self.avgdl = 0
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = []
        self.tokenizer = tokenizer

        if tokenizer:
            corpus = self._tokenize_corpus(corpus)

        nd = self._initialize(corpus)
        self._calc_idf(nd)

    def _initialize(self, corpus):
        nd = {}  # word -> number of documents with word
        num_doc = 0
        for document in corpus:
            self.doc_len.append(len(document))
            num_doc += len(document)

            frequencies = {}
            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            self.doc_freqs.append(frequencies)

            for word, freq in frequencies.items():
                try:
                    nd[word]+=1
                except KeyError:
                    nd[word] = 1

        self.avgdl = num_doc / self.corpus_size
        return nd

    def _tokenize_corpus(self, corpus):
        pool = Pool(cpu_count())
        tokenized_corpus = pool.map(self.tokenizer, corpus)
        return tokenized_corpus

    def get_top_n(self, query, documents, n=5):

        assert self.corpus_size == len(documents), "The documents given don't match the index corpus!"

        scores = self.get_scores(query)
        top_n = np.argsort(scores)[::-1][:n]
        return [documents[i] for i in top_n]

class find_similar_api(find_similar):
    def __init__(self, corpus, tokenizer=None, k1=1.5, b=0.75, epsilon=0.25):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        super().__init__(corpus, tokenizer)

    def _calc_idf(self, nd):
        """
        Calculates frequencies of terms in documents and in corpus.
        This algorithm sets a floor on the idf values to eps * average_idf
        """
        # collect idf sum to calculate an average idf for epsilon value
        idf_sum = 0
        # collect words with negative idf to set them a special epsilon value.
        # idf can be negative if word is contained in more than half of documents
        negative_idfs = []
        for word, freq in nd.items():
            idf = math.log(self.corpus_size - freq + 0.5) - math.log(freq + 0.5)
            self.idf[word] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(word)
        self.average_idf = idf_sum / len(self.idf)

        eps = self.epsilon * self.average_idf
        for word in negative_idfs:
            self.idf[word] = eps

    def get_scores(self, query):
   
        score = np.zeros(self.corpus_size)
        doc_len = np.array(self.doc_len)
        for q in query:
            q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
            score += (self.idf.get(q) or 0) * (q_freq * (self.k1 + 1) /
                                               (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))
        return score

    def get_batch_scores(self, query, doc_ids):
        """
        Calculate  scores between query and subset of all docs
        """
        assert all(di < len(self.doc_freqs) for di in doc_ids)
        score = np.zeros(len(doc_ids))
        doc_len = np.array(self.doc_len)[doc_ids]
        for q in query:
            q_freq = np.array([(self.doc_freqs[di].get(q) or 0) for di in doc_ids])
            score += (self.idf.get(q) or 0) * (q_freq * (self.k1 + 1) /
                                               (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))
        return score.tolist()


def main():
    inp = json.loads(sys.argv[1])
    #inp=input()

    #t0 = timer()
    df = pd.read_csv('//home//ec2-user//intern//intern-test//data//threads1.csv')
    incident= pd.read_csv('//home//ec2-user//intern//intern-test//data//Incident.csv')
    df=clean(df,incident)

    #read tokens from csv file
    with open('//home//ec2-user//intern//intern-test//final_full_length.csv', newline='',encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)
    #load object from file to increase speed of time
    with open('//home//ec2-user//intern//intern-test//object.obj', 'rb') as object_file:
    
        bmi=pickle.load(object_file)


    tokenized_query = inp.lower().split(" ")
    results=bmi.get_top_n(tokenized_query,df.Text.iloc[:len(data)].values)

    finaldata={"incident_id":1,"text":"test","thread_id":1}
    finaljson=[]
    for i in results:
        inc_id=int(df['Incident ID'][df['Text']==i])
        text=i
        thread_id=int(df['Incident Thread ID'][df['Text']==i])
        finaldata["incident_id"]=inc_id
        finaldata["text"]=text
        finaldata['thread_id']=thread_id
        finaljson.append(finaldata.copy())
    #t1 = timer()
    jsonstr = json.dumps(finaljson)
    #print("Time elapsed = ",t1-t0,"seconds")

    print(jsonstr)
    sys.stdout.flush()
if __name__=="__main__":
    main()

