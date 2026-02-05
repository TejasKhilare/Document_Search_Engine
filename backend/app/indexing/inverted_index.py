from collections import defaultdict
import math

class InvertedIndex:
    def __init__(self):
        self.index=defaultdict(lambda:defaultdict(lambda: defaultdict(list)))
        self.doc_freq = defaultdict(int)
        self.seen_docs = defaultdict(set)
        self.total_docs = 0
    
    def add_token(self, token, doc_id, page_no, position):
        page_positions=self.index[token][doc_id][page_no]
        if doc_id not in self.seen_docs[token]:
            self.doc_freq[token] += 1
            self.seen_docs[token].add(doc_id)
        page_positions.append(position)

    def increment_doc_count(self):
        self.total_docs += 1
    
    def get_idf(self, token):
        df = self.doc_freq.get(token, 0)
        if df == 0:
            return 0
        return math.log((self.total_docs + 1) / (df + 1)) + 1

        
