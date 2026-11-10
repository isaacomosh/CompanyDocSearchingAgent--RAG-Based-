from app.services.retrieval import retrieve_documents
from app.services.reranking import rerank_documents
from app.services.llm_services import generate_answer

def ask_company_documents(question,document_id=None):
    #step retrieve relevant chunks
    retrieved=retrieve_documents(question,document_id=document_id,top_k=10)
    #step 2 rerank retrieved chunks
    reranked=rerank_documents(query=question,documents=retrieved,top_k=5)
    #step 3 generate answer
    answer=generate_answer(
        question=question,documents=rerank_documents
    )
    #step 4: Return answer and sources
    sources=[
        {
            "filename":doc["metadata"]["filename"],
            "page":doc["metadata"]["page"],
            "relevance_score":doc["rerank_score"]
        }
        for doc in reranked
    ]
    return {"answer":answer,"sources":sources}