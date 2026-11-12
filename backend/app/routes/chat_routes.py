from flask import Blueprint, request, jsonify
from app.services.rag_service import ask_company_documents

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")


@chat_bp.route("/ask", methods=["POST"])
def ask_question():

    try:
        data = request.get_json()

        question = data.get("question")
        file_id = data.get("file_id")

        if not question:
            return jsonify({
                "error": "Question is required"
            }), 400

        result = ask_company_documents(
            question=question,
            document_id=file_id
        )

        return jsonify(result), 200

    except Exception as e:

        print("CHAT ERROR:", str(e))

        import traceback
        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500