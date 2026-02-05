def exact_search(query_tokens, index):
    """
    Returns:
    doc_id -> page_no -> {
        score: float,
        highlights: [ { word, x, y, width, height } ]
    }
    """

    results = {}

    for token in query_tokens:
        token = token.strip()
        if token not in index.index:
            continue

        idf = index.get_idf(token)

        for doc_id, pages in index.index[token].items():
            for page_no, boxes in pages.items():
                tf = len(boxes)
                score = tf * idf

                if doc_id not in results:
                    results[doc_id] = {}

                if page_no not in results[doc_id]:
                    results[doc_id][page_no] = {
                        "score": 0.0,
                        "highlights": []
                    }

                results[doc_id][page_no]["score"] += score

                for box in boxes:
                    results[doc_id][page_no]["highlights"].append({
                        "word": token,
                        "x": box["x"],
                        "y": box["y"],
                        "width": box["width"],
                        "height": box["height"]
                    })

    return results
