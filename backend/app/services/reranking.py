from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_documents(query, documents, top_k=5):

    if not documents:
        return []

    pairs = [
        [query, document["text"]]
        for document in documents
    ]

    scores = reranker.predict(pairs)

    for document, score in zip(documents, scores):
        document["rerank_score"] = float(score)

    ranked_documents = sorted(
        documents,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return ranked_documents[:top_k]