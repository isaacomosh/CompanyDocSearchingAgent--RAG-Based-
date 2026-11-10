from flask import Blueprint, request, jsonify
from app.services.rag_service import ask_company_documents

chat_bp=Blueprint(
    "chat",__name__,url_prefix="/api/chat"
)

@chat_bp.route("/ask",methods=["POST"])
def ask_question():
    data=request.get_json(silent=True)or{}

    question=data.get("question")
    file_id=data.get("file_id")

    if not question:
        return jsonify({"Error":"Question is required"}),400
    
    try:

        result=ask_company_documents(
            question=question,document_id=file_id
        )
        return jsonify({
            "answer":result["answer"],"sources":result["sources"]
        }),200
    except Exception:
        return jsonify({ "error": "Unable to generate an answer"}),500