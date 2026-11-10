#this service brings extraction,chunking and embedding together/
#coordinates the entire document processing process


import uuid

from app.services.text_extraction import extract_text
from app.services.chunking import chunk_documents
from app.services.embeddings import generate_embeddings
from app.services.chroma_db import collection

def ingest_document(file_path, filename):
    #Extract PDF text
    pages=extract_text(file_path)
    if not pages:
        raise ValueError("No readable text found in PDF.")

    

    #Split text into chunks
    chunks=chunk_documents(pages)

    if not chunks:
        raise ValueError("No chunks generated.")

    #Extract chunk text
    texts=[chunk['text']for chunk in chunks]

    #Geneerate embeddings
    embeddings=generate_embeddings(texts)

    #generate document ID
    document_id=str(uuid.uuid4())

    ids=[]
    metadatas=[]

    for index, chunk in enumerate(chunks):
        ids.append(f"{document_id}_{index}")

        metadatas.append({
              "document_id": document_id,
            "filename": filename,
            "page": chunk["page"],
            "chunk_index": index
        })
    #Store everything in ChromaDB
    collection.add(ids=ids,documents=texts,embeddings=embeddings,metadatas=metadatas)

    return {
        "document_id": document_id,
        "filename": filename,
        "total_chunks": len(chunks),
        "status": "success"
    }