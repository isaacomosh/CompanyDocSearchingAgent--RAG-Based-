from app.services.retrieval import retrieve_documents
from app.services.reranking import rerank_documents
from app.services.llm_services import generate_answer


def ask_company_documents(question, document_id=None):

    # Step 1: Retrieve relevant documents
    retrieved_documents = retrieve_documents(
        query=question,
        document_id=document_id,
        top_k=10
    )

    print("Retrieved documents:", len(retrieved_documents))

    # Step 2: Rerank retrieved documents
    reranked_documents = rerank_documents(
        query=question,
        documents=retrieved_documents,
        top_k=5
    )

    print("Reranked documents:", len(reranked_documents))

    # Step 3: Generate answer using Gemini
    answer = generate_answer(
        question=question,
        documents=reranked_documents
    )

    # Step 4: Extract source information
    sources = []

    for doc in reranked_documents:
        sources.append({
            "filename": doc["metadata"]["filename"],
            "page": doc["metadata"]["page"],
            "relevance_score": doc["rerank_score"]
        })

    return {
        "answer": answer,
        "sources": sources
    }