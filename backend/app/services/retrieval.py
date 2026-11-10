#now we implement semantic search
#Imagine an employee asks:
            #"How many annual leave days do employees receive?"====> We convert this question into an embedding and search ChromaDB for semantically similar document chunks

from app.services.embeddings import generate_embeddings
from app.services.chroma_db import collection

def retrieve_documents(query, document_id=None, top_k=10):
    #generate query embedding
    query_embedding=generate_embeddings([query])[0]
    #search ChromaDB
    results=collection.query(query_embeddings=[query_embedding],n_results=top_k,where={"document_id":document_id}if document_id else None)

    retrieved_documents=[]

    for index, text in enumerate(results["documents"][0]):
        retrieved_documents.append({
            "text":text,
            "metadata":results["metadatas"][0][index],
            "distance":results["distances"][0][index]
        })
    return retrieved_documents