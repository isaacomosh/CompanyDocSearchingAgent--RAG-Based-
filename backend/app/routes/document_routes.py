import os
import uuid

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from backend.app.services.ingestion import ingest_document


document_bp = Blueprint(
    "documents",
    __name__,
    url_prefix="/api/documents"
)


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() == "pdf"
    )


@document_bp.route("/upload", methods=["POST"])
def upload_document():

    if "file" not in request.files:
        return jsonify({
            "error": "No file uploaded"
        }), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({
            "error": "No filename provided"
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Only PDF files are allowed"
        }), 400

    try:

        filename = secure_filename(file.filename)

        # Generate unique document ID
        file_id = str(uuid.uuid4())

        # Prevent filename collisions
        saved_filename = f"{file_id}_{filename}"

        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            saved_filename
        )

        file.save(file_path)

        # Send document to RAG ingestion pipeline
        result = ingest_document(
            file_path=file_path,
            filename=filename
        )

        return jsonify({
            "message": "Document successfully uploaded and indexed",
            "file_id": result["document_id"],
            "filename": filename,
            "total_chunks": result["total_chunks"],
            "status": "success"
        }), 201

    except Exception as e:

        current_app.logger.exception("Document ingestion failed")

        return jsonify({
            "error": "Document processing failed"
        }), 500