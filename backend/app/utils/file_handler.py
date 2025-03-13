import os
import uuid
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}

async def save_temp_file(file: UploadFile) -> str:
    if not file.content_type in ALLOWED_MIME_TYPES:
        raise HTTPException(400, "Unsupported file type")
    
    ext = file.filename.split('.')[-1].lower()
    if ext not in ['pdf', 'docx']:
        raise HTTPException(400, "Invalid file extension")
    
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.{ext}")
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return file_path

def remove_temp_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error removing temp file: {e}")