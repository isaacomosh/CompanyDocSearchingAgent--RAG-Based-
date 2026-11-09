from sentence_transformers import SentenceTranformer

model=SentenceTranformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def generate_embeddings(texts):

    embeddings=model.encode(
        texts,convert_to_numpy=True
,normalize_embeddings=True    )

    return embeddings.tolist()