import shutil
from fastapi import UploadFile
import os

UPLOAD_DIR = "uploads"

async def save_uploaded_file(uploaded_file: UploadFile):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    
    return file_path
