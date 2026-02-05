class DocumentStore:
    def __init__(self):
        self.docs = {}

    def add(self, doc_id, path):
        self.docs[doc_id] = path

    def get(self, doc_id):
        return self.docs.get(doc_id)
