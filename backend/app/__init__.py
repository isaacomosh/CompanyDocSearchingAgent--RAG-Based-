from flask import Flask
from app.config import UPLOAD_FOLDER,MAX_CONTENT_LENGTH
from flask_cors import CORS
import os
def create_app():
    app=Flask(__name__)
    CORS(app)
    app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"]=MAX_CONTENT_LENGTH

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    #register blueprints
    from app.routes.document_routes import document_bp
    from app.routes.chat_routes import chat_bp

    app.register_blueprint(document_bp)
    app.register_blueprint(chat_bp)

    return app