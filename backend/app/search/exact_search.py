from collections import defaultdict
from app.search.ranking import score_page

def exact_search(query_tokens,index):
    results=defaultdict(lambda:defaultdict(float))

    for token in query_tokens:
        postings=index.index.get(token,{})
        idf=index.get_idf(token)

        for doc_id,pages in postings.items():
            for page_no,positions in pages.items():
                tf=len(positions)
                results[doc_id][page_no] += score_page(tf, idf)
    return results