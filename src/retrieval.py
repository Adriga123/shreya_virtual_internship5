
import re
import math
from collections import Counter


def tokenize(text):
    return re.findall(r"[a-zA-Z0-9_]+", str(text).lower())


def find_similar(query, records, top_k=3):

    # Accept a bug report dictionary or a normal text query
    if isinstance(query, dict):

        query = " ".join(
            str(query.get(key, ""))
            for key in (
                "title",
                "description",
                "stack_trace",
                "error_logs",
                "component",
                "content"
            )
        )

    else:
        query = str(query)

    query = query.strip()

    if not records or not query:
        return []

    documents = [
        " ".join(
            str(record.get(key, ""))
            for key in (
                "title",
                "content",
                "description",
                "component",
                "resolution"
            )
        )
        for record in records
    ]

    def get_terms(text):

        words = tokenize(text)

        bigrams = [
            words[i] + "_" + words[i + 1]
            for i in range(len(words) - 1)
        ]

        return words + bigrams

    all_terms = [get_terms(doc) for doc in documents]

    query_terms = get_terms(query)

    vocabulary = set(query_terms)

    for terms in all_terms:
        vocabulary.update(terms)

    total_docs = len(all_terms) + 1

    document_frequency = Counter()

    for terms in all_terms:
        document_frequency.update(set(terms))

    document_frequency.update(set(query_terms))

    def vectorize(terms):

        counts = Counter(terms)

        vector = {}

        for word, count in counts.items():

            tf = count / len(terms) if terms else 0

            idf = math.log(
                (total_docs + 1) /
                (document_frequency[word] + 1)
            ) + 1

            vector[word] = tf * idf

        return vector

    query_vector = vectorize(query_terms)

    def cosine_similarity(a, b):

        dot = sum(
            a.get(key, 0) * b.get(key, 0)
            for key in vocabulary
        )

        norm_a = math.sqrt(
            sum(value * value for value in a.values())
        )

        norm_b = math.sqrt(
            sum(value * value for value in b.values())
        )

        if not norm_a or not norm_b:
            return 0.0

        return dot / (norm_a * norm_b)

    ranked = []

    for index, terms in enumerate(all_terms):

        score = cosine_similarity(
            query_vector,
            vectorize(terms)
        )

        item = dict(records[index])

        item["similarity"] = round(score, 4)

        ranked.append(item)

    ranked.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return ranked[:top_k]
