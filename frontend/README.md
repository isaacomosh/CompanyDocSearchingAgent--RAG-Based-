# CompanyDocs AI frontend

Responsive HTML/CSS/JavaScript frontend for the Flask RAG backend.

## Expected Flask endpoints

- `POST /api/documents/upload` — multipart form field `file`; response includes `file_id`, `filename`, `total_chunks`.
- `GET /api/documents/` — response includes `documents`, each with `document_id`, `filename`, `total_chunks`.
- `DELETE /api/documents/<document_id>` — removes indexed chunks.
- `POST /api/chat/ask` — JSON `{ "question": "...", "file_id": "optional-document-id" }`; response includes `answer` and optional `sources` with `filename` and `page`.

## Run it

1. Start Flask from your backend directory: `python run.py`
2. Open the frontend folder in VS Code.
3. Use the Live Server extension and open `index.html`.
4. The frontend expects the API at `http://127.0.0.1:5000`.

If needed, change `API_BASE` at the top of `js/app.js`.

## CORS

Install `flask-cors`:
```bash
pip install flask-cors
```
Inside `create_app()` in `app/__init__.py`, after creating the Flask app:
```python
from flask_cors import CORS
CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"])
```
Restart Flask after this change.

## Included features

PDF upload, indexed document list, document-specific search, all-document search, source filename/page display, document removal, responsive layout.

Security note: this frontend is not authentication. Add backend authentication and authorization before exposing company documents to real users. The current delete endpoint may remove Chroma chunks without deleting the original PDF file from `uploads`.
