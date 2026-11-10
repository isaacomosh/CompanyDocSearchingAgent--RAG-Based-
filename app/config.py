import os
BASE_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
UPLOAD_FOLDER=os.path.join(BASE_DIR,"uploads")

MAX_CONTENT_LENGTH=20*1024*1024

ALLOWED_EXTENSIONS={"pdf,doc,md"}