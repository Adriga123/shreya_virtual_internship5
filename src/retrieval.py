from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar(query, records, top_k=3):
    if not records or not query.strip():
        return []
    documents = [
        " ".join(str(record.get(k, "")) for k in ("title", "content", "component", "resolution"))
        for record in records
    ]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    matrix = vectorizer.fit_transform(documents + [query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    ranked = sorted(enumerate(scores), key=lambda pair: pair[1], reverse=True)
    output = []
    for index, score in ranked[:top_k]:
        item = dict(records[index])
        item["similarity"] = float(score)
        output.append(item)
    return output
